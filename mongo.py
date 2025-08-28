from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB!")

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed!")
