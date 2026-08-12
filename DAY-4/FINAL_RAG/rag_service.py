"""The existing ingestion/retrieval logic, packaged for the web API."""

from __future__ import annotations

import uuid
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class RAGService:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._vectorstore = None
        self.document_name: str | None = None
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.llm = ChatMistralAI(model="mistral-small-2506")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use only the provided context to answer the question. If the answer is not present in the context, say: 'I could not find the answer in the document.'"),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ])

    @property
    def ready(self) -> bool:
        return self._vectorstore is not None

    def ingest(self, pdf_path: Path, original_name: str) -> tuple[int, int]:
        pages = PyPDFLoader(str(pdf_path)).load()
        chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(pages)
        # Keep every upload in a new collection.  On Windows, Chroma keeps the
        # active collection files open, so deleting the shared folder mid-session
        # raises WinError 32 and interrupts the next upload.
        self._vectorstore = Chroma.from_documents(
            chunks,
            self.embeddings,
            collection_name=f"document_{uuid.uuid4().hex}",
            persist_directory=str(self.db_path),
        )
        self.document_name = original_name
        return len(pages), len(chunks)

    def answer(self, question: str) -> tuple[str, list[int]]:
        docs = self._vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}).invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)
        response = self.llm.invoke(self.prompt.invoke({"context": context, "question": question}))
        source_pages = sorted({int(doc.metadata.get("page", 0)) + 1 for doc in docs})
        return response.content, source_pages
