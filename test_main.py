
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_questions():
    response = client.get("/quiz/questions")
    assert response.status_code == 200

    questions = response.json()
    assert len(questions) == 3
    assert "answer" not in questions[0]


def test_correct_answer():
    response = client.post(
        "/quiz/check",
        json={"question_id": 1, "answer": "Islamabad"},
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True


def test_incorrect_answer():
    response = client.post(
        "/quiz/check",
        json={"question_id": 1, "answer": "Karachi"},
    )
    assert response.status_code == 200
    assert response.json()["correct"] is False


def test_unknown_question():
    response = client.post(
        "/quiz/check",
        json={"question_id": 999, "answer": "Unknown"},
    )
    assert response.status_code == 404
