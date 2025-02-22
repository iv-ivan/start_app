from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class ItemResponse(BaseModel):
    item_id: int
    q: Optional[str]


app = FastAPI()

origins = [
    "http://localhost:5173/",
    "http://localhost:5173",
    "localhost:5173",
    "localhost:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def status():
    return {"status": "Ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return ItemResponse(item_id=item_id, q=q)