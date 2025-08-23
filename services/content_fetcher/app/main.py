from fastapi import FastAPI

from routers import fetch


app = FastAPI(title="Content Fetcher Service", version="0.1.0")


app.include_router(fetch.router)

@app.get("/")
async def root():
    return {"service": "content_fetcher", "status": "ok"}

@app.get("/health")
async def health():
    return {"ok": True}