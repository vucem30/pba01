
import pytest
from fastapi.testclient import TestClient
from main import app, load_questions

client = TestClient(app)

def mock_questions():
    return [
        {
            "id": 1,
            "question": "Pregunta 1",
            "options": [
                {"text": "A", "is_correct": True},
                {"text": "B", "is_correct": False}
            ],
            "type": "single"
        },
        {
            "id": 2,
            "question": "Pregunta 2",
            "options": [
                {"text": "C", "is_correct": True},
                {"text": "D", "is_correct": False}
            ],
            "type": "single"
        },
        {
            "id": 3,
            "question": "Pregunta 3",
            "options": [
                {"text": "E", "is_correct": True},
                {"text": "F", "is_correct": False}
            ],
            "type": "single"
        },
        {
            "id": 4,
            "question": "Pregunta 4",
            "options": [
                {"text": "G", "is_correct": True},
                {"text": "H", "is_correct": False}
            ],
            "type": "single"
        },
        {
            "id": 5,
            "question": "Pregunta 5",
            "options": [
                {"text": "I", "is_correct": True},
                {"text": "J", "is_correct": False}
            ],
            "type": "single"
        }
    ]

def test_get_assessment(monkeypatch):
    monkeypatch.setattr("main.load_questions", mock_questions)
    response = client.get("/assessment")
    assert response.status_code == 200
    for q in mock_questions():
        assert q["question"] in response.text
    assert response.text.count("form-check-input") == 10  # 2 opciones por pregunta, 5 preguntas

def test_submit_all_correct(monkeypatch):
    monkeypatch.setattr("main.load_questions", mock_questions)
    data = {str(q["id"]): q["options"][0]["text"] for q in mock_questions()}  # todas correctas
    response = client.post("/submit", data=data, follow_redirects=False)
    assert response.status_code == 303
    assert "/result?score=5" in response.headers["location"]

def test_result_page(monkeypatch):
    monkeypatch.setattr("main.load_questions", mock_questions)
    response = client.get("/result?score=5")
    assert response.status_code == 200
    assert "Tu puntuación es:" in response.text
    assert "5 / 5" in response.text
