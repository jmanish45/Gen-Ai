from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2506", temperature=0.7)


messages = []

print("Welcome to the Mistral AI Chatbot! Type '0' to quit.")
while True:
    prompt = input("You: ")
    messages.append({"role": "user", "content": prompt})
    if prompt == '0':
        print("Exiting the chatbot. Goodbye!")
        break
    response = model.invoke(messages)
    messages.append({'role':'assistant', 'content': response.content})
    print("Bot : ", response.content)