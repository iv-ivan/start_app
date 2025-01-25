# HTTP API with Python
For our backend we are going to use Python with [FastAPI](https://fastapi.tiangolo.com/) framework.
You should have Python installed.

1) `mkdir backend && cd backend`
2) Create `requirements.txt` to specify what are the dependencies of our project:
```requirements
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
ruff>=0.9.3
```
3) Now we can install all these libs with: `pip3 install -r requirements.txt`
4) Let's write some code: `mkdir app && cd app`
5) I've created 2 files in `app` directory: `__init__.py` and `main.py`.
<br>They contain a very simple API:
   - GET /
   - GET /items/{item_id}?q={string}
6) Run Python linters: `python3 -m ruff check`
7) Run Python formatting: `python3 -m ruff format`
8) Let's test our API:
```shell
python3 -m fastapi dev main.py
curl -v http://127.0.0.1:8000/items/5?q=somequery
```
