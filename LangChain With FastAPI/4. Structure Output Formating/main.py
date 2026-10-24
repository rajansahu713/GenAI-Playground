from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()



# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        password=os.getenv("PASSWORD"),
        user='postgres',
        database=os.getenv("DATABASE")
    )



app = FastAPI(title="Movie Review Structured Output API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the model
model = OllamaLLM(
    model="llama3.1",
    base_url="http://localhost:11434"
)


# Pydantic model for structured output
class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie")
    review: str = Field(description="A brief review of the movie")
    rating: int = Field(description="The rating of the movie")


# Pydantic model for API request
class ReviewRequest(BaseModel):
    review_text: str


# Pydantic model for API response
class ReviewResponse(BaseModel):
    title: str
    review: str
    rating: int




@app.post("/review", response_model=ReviewResponse)
def save_review(request: ReviewRequest):
    """
    Submit a movie review, extract structured data using AI, and save to database
    """
    try:
        # Setup parser
        parser = PydanticOutputParser(pydantic_object=MovieReview)

        # Create prompt with format instructions
        prompt = ChatPromptTemplate.from_template(
            "Extract movie information from the following review.\n"
            "Review: {review}\n\n"
            "{format_instructions}"
        ).partial(format_instructions=parser.get_format_instructions())

        # Create chain and invoke
        chain = prompt | model | parser
        result = chain.invoke({"review": request.review_text})

        # Save to database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO movie_review (title, review, rating) VALUES (%s, %s, %s)",
            (result.title, result.review, result.rating)
        )
        conn.commit()
        cur.close()
        conn.close()

        return ReviewResponse(
            title=result.title,
            review=result.review,
            rating=result.rating
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews", response_model=List[ReviewResponse])
def get_reviews():
    """
    Get all saved movie reviews from the database
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT title, review, rating FROM movie_review ORDER BY created_at DESC")
        reviews = cur.fetchall()
        cur.close()
        conn.close()

        return [
            ReviewResponse(
                title=review["title"],
                review=review["review"],
                rating=review["rating"]
            )
            for review in reviews
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    """Serve the HTML frontend"""
    with open("index.html", "r") as f:
        return f.read()


@app.get("/api")
def root():
    return {
        "message": "Movie Review Structured Output API",
        "endpoints": {
            "POST /review": "Submit a movie review",
            "GET /reviews": "Get all saved reviews"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
