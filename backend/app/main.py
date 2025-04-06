from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from create_collections import MONGO_ADDRESS, DB_NAME
import pymongo
import bcrypt
from models import User, UserInput, UserResponse, Session
import secrets
import datetime
from fastapi.responses import JSONResponse


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


@app.post("/api/login")
async def login(
    user_data: UserInput,
    response: Response,
    db_client: AsyncIOMotorClient = Depends(get_database),
):
    db = db_client[DB_NAME]
    user_doc = await db.users.find_one({"email": user_data.email})
    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such email registered"
        )
    user = User(**user_doc)

    stored_hash = user.passwordHash
    is_valid = bcrypt.checkpw(user_data.password.encode(), stored_hash)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    # Generate a unique session token
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=365)
    user_id = user_doc["_id"]

    # Create session document
    session_doc = Session(token=session_token, userId=user_id, expiresAt=expires_at)
    # Store session in database
    await db.sessions.insert_one(session_doc.model_dump())

    # Frontend will remmebr session in the cookies
    # Make it in a secure way, except samesite because our API is a subdomain: api.*
    response.set_cookie(
        key="session_id", httponly=True, secure=True, value=session_token, samesite=None
    )
    return UserResponse(email=user.email)


@app.post("/api/logout")
async def logout(
    session_id: Optional[str] = Cookie(default=None),
    db_client: AsyncIOMotorClient = Depends(get_database),
):
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Remove the session from database
    db = db_client[DB_NAME]
    doc = await db.sessions.find_one_and_delete({"token": session_id})

    if doc is None:
        # return 404 response
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Session is already expired"},
        )
    else:
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"status": "Ok"}
        )
    response.delete_cookie("session_id", httponly=True, secure=True, samesite=None)
    return response


@app.post("/api/auth")
async def check_auth(
    response: Response,
    session_id: Optional[str] = Cookie(default=None),
    db_client: AsyncIOMotorClient = Depends(get_database),
):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    db = db_client[DB_NAME]
    session_doc = await db.sessions.find_one({"token": session_id})
    if session_doc is None:
        response.delete_cookie("session_id", httponly=True, secure=True, samesite=None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
        )
    session = Session(**session_doc)

    # Possible improvement: check if session is near expiration (e.g., less than 1-7 days)
    # If so, extend the session expireAt

    user_doc = await db.users.find_one({"_id": session.userId})
    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user registered"
        )
    user = User(**user_doc)

    return UserResponse(email=user.email)


# To make protected endpoints that require auth,
# we can create a dependency Depends(get_current_user) similar to get_database()
# It will check current session and fetch current user from db, or raise 401 error
