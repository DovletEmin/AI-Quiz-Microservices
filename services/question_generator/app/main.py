from fastapi import FastAPI

from .routers.generate import router as generate_router 


app = FastAPI(title="Quiz Generator Service", version="0.1.0")


app.include_router(generate_router)

# @app.get("/")
# async def root():
#     return {"service": "question_generator", "status": "ok"}