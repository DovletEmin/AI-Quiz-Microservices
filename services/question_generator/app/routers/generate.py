from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import httpx


router = APIRouter(prefix="/api", tags=["generate"])

class GenerateRequest(BaseModel):
    text: str

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


@router.post("/", response_model=GenerateResponse)
async def generate_questions(payload: GenerateRequest):
    text = payload.text

    topic = " ".join(text.split()[:3])

    questions = [
        Question(
            question = f"What does the word '{word}' mean in text?",
            options=None,
            answer=word
        ) for word in text.split()[:3]
    ]

    return GenerateResponse(topic=topic, questions=questions)

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
    
    topic = payload.topic
    questions = [
        Question(
            question = f"What does the word '{word}' mean?",
            options=None,
            answer=word
        ) for word in text.split()[:2]
    ]

    return GenerateResponse(topic=topic, questions=questions)