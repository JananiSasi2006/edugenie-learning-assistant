import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie", description="Google Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class LearningRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    level: str = Field(default="Beginner", max_length=40)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}

@app.post("/qa")
async def qa(data: LearningRequest):
    return {"result": await answer_question(data.text, data.level)}

@app.post("/explain")
async def explain(data: LearningRequest):
    return {"result": await explain_concept(data.text, data.level)}

@app.post("/quiz")
async def quiz(data: LearningRequest):
    return {"result": await generate_quiz(data.text, data.level)}

@app.post("/summarize")
async def summarize(data: LearningRequest):
    return {"result": await summarize_text(data.text, data.level)}

@app.post("/learn/recommendations")
async def recommendations(data: LearningRequest):
    return {"result": await get_learning_recommendations(data.text, data.level)}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Avoid exposing secrets or internal stack traces to users.
    return __import__("fastapi").responses.JSONResponse(
        status_code=500,
        content={"detail": "EduGenie encountered an unexpected error. Check the server terminal for details."}
    )
