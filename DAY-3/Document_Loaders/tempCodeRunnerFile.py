from langchain_community.document_loaders import TextLoader 
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()
data = TextLoader("./notes.txt", encoding="utf-8")
docs = data.load()

template = ChatPromptTemplate.from_messages(
    [("system", "You are an AI that summarises the text"),
    ("human", "{data}")]
)

model = ChatMistraAI(model = ['mistral-small-2506'])

prompt = template.format_messages(data=docs[0].page_content)

result = model.invoke(prompt)

print(result.content)
