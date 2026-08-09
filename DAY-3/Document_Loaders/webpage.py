from langchain_community.document_loaders import WebBaseLoader

url = "https://denoise-x.vercel.app/"

data = WebBaseLoader(url)

docs = data.load()

print(len(docs))

print(docs[0].page_content)


