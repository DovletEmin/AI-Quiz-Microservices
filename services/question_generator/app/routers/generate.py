import random
from app.utils import extract_keywords, generate_options
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import httpx

router = APIRouter(prefix="/api", tags=["Generate"])

class Question(BaseModel):
    question: str
    options: List[str] | None = None
    answer: str

class GenerateResponse(BaseModel):
    topic: str
    questions: List[Question]

class TopicRequest(BaseModel):
    topic: str
    lang: str = 'en'
    num_questions: int = 5

@router.post("/by-topic", response_model=GenerateResponse)
async def generate_by_topic(payload: TopicRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "http://127.0.0.1:8000/api/fetch",
                json={"topic": payload.topic, "lang": payload.lang},
                timeout=10
            )
            resp.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Fetch error: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    data = resp.json()
    text = data.get("extract", "")

    if not text:
        raise HTTPException(status_code=404, detail="No text found for topic")

    keywords = extract_keywords(text, n=payload.num_questions)
    words = [w for w in text.split() if w.isalpha()]

    questions = []
    for key in keywords:
        text_words = [w for w in words if w != key]
        options = generate_options(key, text_words, n=4)

        questions.append(
            Question(
                question=f"What does the word '{key}' mean?",
                options=options,
                answer=key
            )
        )

    return GenerateResponse(topic=payload.topic, questions=questions)
