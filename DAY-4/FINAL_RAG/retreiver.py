from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = Chroma(
    persist_directory = "./chroma_db",
    embedding_function = embedding_model

)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":4,
        "fetch_k":10 , #for MMR, fetch_k should be greater than k , 4/10 
        "lambda_mult": 0.5
    }
)

llm = ChatMistralAI(
    model="mistral-small-2506"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """You are a helpful assistant.
            Use only the provided context to answer the question .
            If the answer is not present in the context,
            say : "I could not find the answer in the document."
            """
        ),
        (
            "human",
            """Context:{context}

            Question : {question}
            """
        )
    ]
)

print("-----------Rag System Created-------------")

print("Press 0 to exit")

while True :
    query = input("You : ")
    if query=='0':
        print("Thankyou so much , You can call again for any other help")
        break 
    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )  

    final_prompt = prompt.invoke({
        "context":context,
        "question":query
    })

    response = llm.invoke(final_prompt)

    print(f"\n AI: {response.content}")


