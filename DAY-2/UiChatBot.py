# Using langchain_core messages and langchain_mistralai to create a chatbot using Mistral AI model
# Streamlit UI version — same functionality and roles as the original CLI script

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="Mistral AI Chatbot", page_icon="🤖")
st.title("Welcome to the Mistral AI Chatbot!")

# Initialize the model once
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.7)

# Initialize message history with the same system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a funny agent that responds to user queries in a humorous way."),
    ]

# Display existing conversation (skip the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# Chat input
prompt = st.chat_input("You: ")

if prompt:
    if prompt == "0":
        st.info("Exiting the chatbot. Goodbye!")
    else:
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)

        response = st.session_state.model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

        with st.chat_message("assistant"):
            st.write(response.content)