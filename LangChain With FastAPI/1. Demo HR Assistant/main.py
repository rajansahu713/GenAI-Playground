from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

def langChainExperienceLanguage():
    model = OllamaLLM(
        model="llama3.1",
        base_url="http://localhost:11434"
    )


    prompt = ChatPromptTemplate.from_template("""
    You are a helpful HR assistant.
    Question: {input}
    """)

    chain = prompt | model | StrOutputParser()
    return chain


class QueryRequest(BaseModel):
    input: str


@app.post("/hr/ask")
def ask_hr(request: QueryRequest):
    chain = langChainExperienceLanguage()
    response = chain.invoke({"input": request.input})
    return {"response": response}