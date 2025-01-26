requirements.txt
```
...
httpx>=0.23.0,<0.24.0
pytest>=8.3.4,<8.4.0
```
app/test_main.py
```
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/5?q=abc")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "abc"}
```
python3 -m pytest