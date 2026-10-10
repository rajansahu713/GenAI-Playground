from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()


def create_chain():
    model = OllamaLLM(
        model="llama3.1",
        base_url="http://localhost:11434"
    )
    prompt = ChatPromptTemplate.from_template("Please tell the story for: {input}")
    parser = StrOutputParser()
    chain = prompt | model | parser
    return chain


class QueryRequest(BaseModel):
    input: str


@app.post("/stream")
async def stream_story(request: QueryRequest):
    chain = create_chain()

    async def generate():
        response = chain.stream({"input": request.input})
        for chunk in response:
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")