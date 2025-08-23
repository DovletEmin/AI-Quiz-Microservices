import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.fixture
def mock_fetch_response():
    return {
        "extract": "Python is a high-level programming language.",
        "topic": "Python"
    }

def test_generate_by_topic_sync(mock_fetch_response):
    payload = {
        "topic": "Python (programming language)",
        "lang": "en",
        "num_questions": 3
    }

    class MockResponse:
        def raise_for_status(self): 
            pass
        def json(self): 
            return mock_fetch_response

    # Мокаем httpx.AsyncClient.post, чтобы возвращался MockResponse
    async def mock_post(*args, **kwargs):
        return MockResponse()

    with patch("app.routers.generate.httpx.AsyncClient.post", new=mock_post):
        response = client.post("/api/by-topic", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert len(data["questions"]) == 3
        for q in data["questions"]:
            assert q["answer"] in q["options"]
            assert len(q["options"]) == 4
