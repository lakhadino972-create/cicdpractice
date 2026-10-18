
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="General Knowledge Quiz API",
    description="A simple FastAPI project for practicing GitHub Actions CI/CD.",
    version="1.0.0",
)

QUESTIONS = [
    {
        "id": 1,
        "question": "What is the capital of Pakistan?",
        "options": ["Karachi", "Islamabad", "Lahore", "Quetta"],
        "answer": "Islamabad",
    },
    {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": "Mars",
    },
    {
        "id": 3,
        "question": "How many days are there in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": "366",
    },
]


class AnswerRequest(BaseModel):
    question_id: int
    answer: str


@app.get("/")
def home():
    return {
        "message": "Welcome to the General Knowledge Quiz API!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/quiz/questions")
def get_questions():
    # Never expose correct answers in the question list.
    return [
        {key: value for key, value in question.items() if key != "answer"}
        for question in QUESTIONS
    ]


@app.post("/quiz/check")
def check_answer(request: AnswerRequest):
    question = next(
        (q for q in QUESTIONS if q["id"] == request.question_id),
        None,
    )

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = request.answer.strip().casefold() == question["answer"].casefold()

    return {
        "question_id": request.question_id,
        "correct": correct,
        "message": "Correct answer!" if correct else "Incorrect answer.",
    }
