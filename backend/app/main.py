from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class ItemResponse(BaseModel):
    item_id: int
    q: Optional[str]


app = FastAPI()


@app.get("/")
async def status():
    return {"status": "Ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return ItemResponse(item_id=item_id, q=q)
