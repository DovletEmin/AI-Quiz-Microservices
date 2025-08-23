from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from urllib.parse import quote


router = APIRouter(prefix="/api", tags=["fetch"])


class FetchRequest(BaseModel):
    topic: str
    lang: str | None = "en"


@router.post("/fetch")
async def fetch_content(payload: FetchRequest):
    lang = payload.lang or "en"
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(payload.topic)}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url)

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Topic not found")
    r.raise_for_status()

    data = r.json()
    return {
        "topic": payload.topic,
        "lang": lang,
        "title": data.get("title", payload.topic),
        "extract": data.get("extract", ""),
        "source_url": data.get("content_urls", {}).get("desktop", {}).get("page", {}),
    }