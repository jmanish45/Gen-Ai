from langchain_community.vectorstores import Chroma

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document #for creating document object


docs = [
    Document(page_content="Python is widely used in data science and machine learning.", metadata={"source": "sample.txt"}
    ),
    Document(page_content="Pandas is a powerful data manipulation library.", metadata={"source": "sample2.txt"}),
    Document(page_content="Neural networks are a key component of deep learning.", metadata={"source": "sample3.txt"})
]

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

vector_store = Chroma.from_documents(
    documents = docs,
    embedding = embedding_model,
    persist_directory = "./chroma_db"
)

result = vector_store.similarity_search("What is Python used for?", k=2)
for r in result:
    print(r.page_content)
    print(r.metadata)
    print()

retriever = vector_store.as_retriever()    
