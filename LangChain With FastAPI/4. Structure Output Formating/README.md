# Movie Review Structured Output API

A FastAPI application that uses LangChain with Ollama to extract structured movie review data and save it to PostgreSQL.

## Features

- **Structured Output**: Uses AI to extract title, review, and rating from unstructured text
- **Database Storage**: Saves structured data to PostgreSQL
- **REST API**: Simple endpoints for submitting and retrieving reviews
- **Real-time Analysis**: AI-powered review analysis with visual feedback

## Installation

```bash
pip install -r requirements.txt
```

## Database Setup

Create the table in the database:

```sql
CREATE TABLE movie_review (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    review TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

Edit `.env` file:

```bash
HOST=127.0.0.1
PORT=5432
PASSWORD=123456
USER=postgres
DATABASE=postgres
```

## Usage

### Start the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

### Access the Frontend

Open your browser and visit:
```
http://localhost:8000
```

This will show the beautiful web interface where you can:
- Submit movie reviews
- See AI analysis in real-time
- View all saved reviews
- Refresh the reviews list

### API Endpoints

#### 1. Submit a Movie Review

**POST /review**

Submit a movie review text, and the AI will extract structured data and save it to the database.

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "review_text": "Inception is a mind-bending thriller by Christopher Nolan. 9/10 amazing movie!"
  }'
```

Response:
```json
{
  "title": "Inception",
  "review": "A mind-bending thriller by Christopher Nolan.",
  "rating": 9
}
```

#### 2. Get All Reviews

**GET /reviews**

Retrieve all saved movie reviews from the database.

```bash
curl http://localhost:8000/reviews
```

Response:
```json
[
  {
    "title": "Inception",
    "review": "A mind-bending thriller by Christopher Nolan.",
    "rating": 9
  },
  {
    "title": "The Dark Knight",
    "review": "An epic superhero film.",
    "rating": 10
  }
]
```



## How It Works

1. **User submits review text** via web form or API
2. **AI extracts structured data** using PydanticOutputParser
   - Extracts movie title
   - Extracts review summary
   - Extracts rating as integer
3. **Saves to PostgreSQL** database
4. **Returns structured response** to user
5. **Frontend displays** the analyzed review with beautiful UI



