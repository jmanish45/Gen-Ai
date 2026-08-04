#Using langchain_core messages and langchain_mistralai to create a chatbot using Mistral AI model

from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = ChatMistralAI(model="mistral-small-2506", temperature=0.7)


messages = [
    SystemMessage(content="You are a funny agent that responds to user queries in a humorous way."),
]

print("Welcome to the Mistral AI Chatbot! Type '0' to quit.")
while True:
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == '0':
        print("Exiting the chatbot. Goodbye!")
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot : ", response.content)