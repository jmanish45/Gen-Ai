from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os


load_dotenv()


data = PyPDFLoader("./intro-to-ml.pdf")
docs = data.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

template = ChatPromptTemplate.from_messages(
    [("system", "You are an AI that summarises the text"),
    ("human", "{data}")]
)

model = ChatMistralAI(model = 'mistral-small-2506')

prompt = template.format_messages(data=docs[0].page_content)

result = model.invoke(prompt)

print(result.content)
