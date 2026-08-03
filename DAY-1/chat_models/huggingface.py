import os
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# You might need to set the specific env var name Langchain expects
if (
    "HUGGINGFACE_HUB_ACCESS_TOKEN" in os.environ
    and "HUGGINGFACEHUB_API_TOKEN" not in os.environ
):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.environ["HUGGINGFACE_HUB_ACCESS_TOKEN"]

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1", task="text-generation", max_new_tokens=100
)
model = ChatHuggingFace(llm=llm)

response = model.invoke("What are transformers?")
print(response.content)
