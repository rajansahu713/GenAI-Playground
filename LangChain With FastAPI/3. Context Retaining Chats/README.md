# Context Retaining Chat API

A FastAPI application with conversation context retention using LangChain and Ollama.

## Features

- **Context Retention**: Remembers conversation history across multiple requests
- **Session-based**: Each conversation is tracked with a unique session ID
- **Multiple Endpoints**: Ask questions, clear history, view history, list sessions

## Installation

```bash
pip install fastapi uvicorn langchain-ollama langchain-core
```

## Usage

### Start the Server

```bash
uvicorn main:app --reload
```

### API Endpoints

#### 1. Ask a Question (with context)

**POST /ask**

Ask a question with optional session ID for context retention.

```bash
# First message (new session)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"input": "Who is Rohit Sharma?"}'

# Response
{
  "response": "Rohit Sharma is an Indian cricketer...",
  "session_id": "abc-123-def-456"
}

# Follow-up message (with session_id for context)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What records does he hold?",
    "session_id": "abc-123-def-456"
  }'

# Response (AI remembers previous context)
{
  "response": "Rohit Sharma holds several records including...",
  "session_id": "abc-123-def-456"
}
```

#### 2. Clear Conversation

**POST /clear**

Clear conversation history for a session.

```bash
curl -X POST http://localhost:8000/clear?session_id=abc-123-def-456
```

#### 3. Get Conversation History

**GET /history/{session_id}**

View the full conversation history for a session.

```bash
curl http://localhost:8000/history/abc-123-def-456
```

Response:
```json
{
  "session_id": "abc-123-def-456",
  "messages": [
    {
      "type": "SystemMessage",
      "content": "You are helpful assistant in cricket"
    },
    {
      "type": "HumanMessage",
      "content": "Who is Rohit Sharma?"
    },
    {
      "type": "AIMessage",
      "content": "Rohit Sharma is an Indian cricketer..."
    }
  ]
}
```

#### 4. List All Sessions

**GET /sessions**

List all active conversation sessions.

```bash
curl http://localhost:8000/sessions
```

Response:
```json
{
  "sessions": ["abc-123-def-456", "xyz-789-uvw-012"],
  "count": 2
}
```

## How It Works

1. **Session Management**: Each conversation is tracked with a unique `session_id`
2. **Message History**: All messages (system, human, AI) are stored in memory
3. **Context Passing**: Full conversation history is sent to the model with each request
4. **AI Memory**: The AI can reference previous messages in the conversation
