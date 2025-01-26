# Testing backend code
1) Let's use FastAPI [official tutorial](https://fastapi.tiangolo.com/tutorial/testing/#using-testclient)
2) First, patch requirements.txt:
```requirements
# requirements.txt
...
httpx>=0.23.0,<0.24.0
pytest>=8.3.4,<8.4.0
```
Then install libs `pip3 install -r requirements.txt`
2) Tests are added to `app/test_main.py`
3) Run tests `python3 -m pytest`