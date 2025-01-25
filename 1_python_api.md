vim requirements.txt
```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
ruff>=0.9.3
```
pip3 install -r requirements.txt

mkdir app && cd app

touch __init__.py

vim main.py
```
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def status():
    return {"status": "Ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

python3 -m ruff check

python3 -m ruff format

python3 -m fastapi dev main.py

http://127.0.0.1:8000/items/5?q=somequery
