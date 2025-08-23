from fastapi import FastAPI

from .routers import generate


app = FastAPI(title="Quiz Generator Service", version="0.1.0")


app.include_router(generate.router)

# @app.get("/")
# async def root():
#     return {"service": "question_generator", "status": "ok"}