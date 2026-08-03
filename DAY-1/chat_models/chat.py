from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.5, max_tokens=50
)
print(model)
result = model.invoke("what is Lnagchain ?")
print(result.content)

from langchain_groq import ChatGroq

model1 = ChatGroq(model="llama3-8b-8192", max_tokens=50)
response = model1.invoke("what is LangGraph")
print(response.content)
