from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


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


@router.post("/", response_model=GenerateResponse)
async def generate_questions(payload: GenerateRequest):
    text = payload.text

    topic = " ".join(text.split()[:3])

    questions = [
        Question(
            question = f"What does the word '{word}' mean in text",
            options=None,
            answer=word
        ) for word in text.split()[:3]
    ]

    return GenerateResponse(topic=topic, questions=questions)