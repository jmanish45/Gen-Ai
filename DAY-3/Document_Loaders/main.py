from langchain_community.document_loaders import TextLoader 
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import os


load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "notes.txt")

data = TextLoader(file_path, encoding="utf-8")
docs = data.load()

template = ChatPromptTemplate.from_messages(
    [("system", "You are an AI that summarises the text"),
    ("human", "{data}")]
)

model = ChatMistralAI(model = 'mistral-small-2506')

prompt = template.format_messages(data=docs[0].page_content)

result = model.invoke(prompt)

print(result.content)
