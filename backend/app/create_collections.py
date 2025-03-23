import asyncio
import motor.motor_asyncio
import os

DB_NAME = "my_app"
MONGO_ADDRESS = os.environ["MONGO_CONNECTION"]


async def setup_auth_collections(connection_string=MONGO_ADDRESS, drop_existing=False):
    # Create database connection
    client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
    db = client[DB_NAME]

    # Check if collections already exist and drop them if they do
    collections = await db.list_collection_names()
    if drop_existing:
        print("Dropping existing collections...")
        if "users" in collections:
            await db.users.drop()
        if "sessions" in collections:
            await db.sessions.drop()

    print("Creating collections...")
    await db.create_collection("users")
    await db.create_collection("sessions")

    print("Creating indexes...")
    # Create indexes
    await db.users.create_index("email", unique=True)

    # Sessions collection indexes
    await db.sessions.create_index("token", unique=True)
    await db.sessions.create_index("userId")

    # TTL index to automatically expire sessions
    await db.sessions.create_index("expiresAt", expireAfterSeconds=0)

    print("Collections created!")


if __name__ == "__main__":
    asyncio.run(setup_auth_collections())
