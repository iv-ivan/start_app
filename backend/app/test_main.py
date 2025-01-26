from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def  test_read_item():
    response = client.get("/items/5?q=abc")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "abc"}
