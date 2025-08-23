from fastapi import FastAPI


app = FastAPI(title="Quiz Generator Service", version="0.1.0")


@app.get("/")
async def root():
    return {"service": "question_generator", "status": "ok"}