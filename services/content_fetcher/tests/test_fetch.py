from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fetch_and_cache():
    # first request not from cache
    response = client.post("/api/fetch", json={"topic": "Ashgabat", "lang": "en"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Ashgabat"
    assert data["cached"] is False

    # seconds request (should be from cache)
    response2 = client.post("/api/fetch", json={"topic": "Ashgabat", "lang": "en"})
    data2 = response2.json()
    assert data2["cached"] is True

    # third request from cache
    response3 = client.get("/api/content/en/Ashgabat")
    assert response3.status_code == 200
    data3 = response3.json()
    assert data3["title"] == "Ashgabat"
