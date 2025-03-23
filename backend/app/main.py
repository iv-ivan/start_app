from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from create_collections import MONGO_ADDRESS, DB_NAME
import pymongo
import bcrypt
from models import User, UserInput


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
async def status_endpoint():
    return {"status": "Ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return ItemResponse(item_id=item_id, q=q)


### Auth API


@app.post("/api/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserInput, db_client: AsyncIOMotorClient = Depends(get_database)
):
    # It's important to use POST and https to pass password securely
    db = db_client[DB_NAME]
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
        )

    # Generate salt randomly for every user, and hash password with it
    # - password_hash contains salt as prefix
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(user_data.password.encode(), salt)

    # Prepare user document
    user_doc = User(
        email=user_data.email,
        passwordHash=password_hash,
    )

    await db.users.insert_one(user_doc.model_dump())
    return {"status": "Ok"}
