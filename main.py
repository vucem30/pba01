
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)


@app.get("/assessment")
async def get_assessment(request: Request):
    questions = load_questions()
    return templates.TemplateResponse("assessment.html", {"request": request, "questions": questions})


@app.post("/submit")
async def post_submit(request: Request):
    form = await request.form()
    questions = load_questions()
    score = 0
    for q in questions:
        qid = str(q["id"])
        if q["type"] == "single":
            answer = form.get(qid)
            for opt in q["options"]:
                if opt["text"] == answer and opt["is_correct"]:
                    score += 1
        elif q["type"] == "multi":
            answers = form.getlist(qid)
            correct_opts = [opt["text"] for opt in q["options"] if opt["is_correct"]]
            # Solo cuenta si todas las correctas y solo las correctas fueron seleccionadas
            if set(answers) == set(correct_opts):
                score += 1
    return RedirectResponse(f"/result?score={score}", status_code=303)


@app.get("/result")
async def get_result(request: Request, score: int = 0):
    questions = load_questions()
    total = len(questions)
    return templates.TemplateResponse("result.html", {"request": request, "score": score, "total": total})
