from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from urllib.parse import quote

router = APIRouter(prefix="/api", tags=["Fetch"])

_CACHE: dict[tuple[str, str], dict] = {}


class FetchRequest(BaseModel):
    topic: str
    lang: str | None = "en"


@router.post("/fetch")
async def fetch_content(payload: FetchRequest):
    lang = payload.lang or "en"
    topic = payload.topic.strip()
    key = (topic, lang)

    # Проверяем кэш
    if key in _CACHE:
        return {**_CACHE[key], "cached": True}

    async with httpx.AsyncClient(timeout=10.0) as client:
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(topic)}"
        r = await client.get(url)

        if r.status_code == 404:
            search_url = (
                f"https://{lang}.wikipedia.org/w/api.php"
                f"?action=query&list=search&srsearch={quote(topic)}&format=json"
            )
            search_resp = await client.get(search_url)
            search_resp.raise_for_status()

            results = search_resp.json().get("query", {}).get("search", [])
            if not results:
                raise HTTPException(status_code=404, detail="No text found for topic")

            first_title = results[0]["title"]
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(first_title)}"
            r = await client.get(url)

        r.raise_for_status()
        data = r.json()

    response = {
        "topic": topic,
        "lang": lang,
        "title": data.get("title", topic),
        "extract": data.get("extract", ""),
        "source_url": data.get("content_urls", {}).get("desktop", {}).get("page", url),
        "cached": False,
    }

    _CACHE[key] = response
    return response


@router.get("/content/{lang}/{topic}")
async def get_cached(lang: str, topic: str):
    key = (topic.strip(), lang)
    if key not in _CACHE:
        raise HTTPException(status_code=404, detail="Content not cached yet")
    return _CACHE[key]
