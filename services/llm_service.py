import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

if not os.getenv("GOOGLE_API_KEY"):
    print("variável de ambiente GOOGLE_API_KEY não encontrada.")
    exit(1)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def call_llm(question: str):
    response = llm.invoke([{"role": "user", "content": question}])
    return response.content

print(call_llm("Ola."))