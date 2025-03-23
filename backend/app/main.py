from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from create_collections import MONGO_ADDRESS, DB_NAME
import pymongo


### Mongo
class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    print("Connect to Mongo...")
    db.client = AsyncIOMotorClient(MONGO_ADDRESS, timeoutMS=5000)
    collections = await db.client[DB_NAME].list_collection_names()
    print(f"Collections {collections}")


async def close_mongo_connection():
    print("Close Mongo connection...")
    if db.client:
        db.client.close()


### API
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

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.get("/")
async def status():
    return {"status": "Ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return ItemResponse(item_id=item_id, q=q)
