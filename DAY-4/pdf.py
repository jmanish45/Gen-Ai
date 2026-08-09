from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

data = PyPDFLoader("./notes.pdf")

docs = data.load()

splitter = CharacterTextSplitter(
    separator="",
    chunk_size=109,
    chunk_overlap=10

)

chunks = splitter.split_documents(docs)

print(len(chunks))
for i in chunks :
    