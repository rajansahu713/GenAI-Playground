from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uuid


app = FastAPI()

# Initialize the model once
model = OllamaLLM(
    model="llama3.1",
    base_url="http://localhost:11434"
)

# Store conversation history in memory (for production, use Redis or database)
conversation_history = {}


class QueryRequest(BaseModel):
    input: str
    session_id: Optional[str] = None  # Optional session ID for context retention


class QueryResponse(BaseModel):
    response: str
    session_id: str


@app.post("/ask", response_model=QueryResponse)
def ask_cricket(request: QueryRequest):
    """
    Ask a question to the cricket assistant with context retention
    """
    # Get or create session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Initialize conversation for new session
    if session_id not in conversation_history:
        conversation_history[session_id] = [
            SystemMessage(content="You are helpful assistant in cricket")
        ]

    # Get conversation history for this session
    messages = conversation_history[session_id]

    # Add user's new message
    messages.append(HumanMessage(content=request.input))

    # Invoke the model with full conversation history
    response = model.invoke(messages)

    # Add AI's response to history
    messages.append(AIMessage(content=response))

    # Update the history
    conversation_history[session_id] = messages

    return QueryResponse(
        response=response,
        session_id=session_id
    )


@app.post("/clear")
def clear_conversation(session_id: str):
    """
    Clear conversation history for a session
    """
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": "Conversation cleared", "session_id": session_id}
    return {"message": "Session not found", "session_id": session_id}


@app.get("/history/{session_id}")
def get_history(session_id: str):
    """
    Get conversation history for a session
    """
    if session_id in conversation_history:
        messages = conversation_history[session_id]
        return {
            "session_id": session_id,
            "messages": [
                {
                    "type": type(msg).__name__,
                    "content": msg.content
                }
                for msg in messages
            ]
        }
    return {"message": "Session not found", "session_id": session_id}


@app.get("/sessions")
def list_sessions():
    """
    List all active sessions
    """
    return {
        "sessions": list(conversation_history.keys()),
        "count": len(conversation_history)
    }
