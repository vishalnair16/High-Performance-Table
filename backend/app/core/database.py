from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(
            settings.MONGO_URI,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000,
        )
        db.database = db.client[settings.DB_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("✅ Connected to MongoDB!")
        
        # Create indexes for performance
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("✅ Disconnected from MongoDB")

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db.database

async def create_indexes():
    """Create database indexes for optimal query performance"""
    try:
        products_collection = db.database["products"]
        
        # Create indexes for common query patterns
        await products_collection.create_index("name", background=True)
        await products_collection.create_index("category", background=True)
        await products_collection.create_index("price", background=True)
        await products_collection.create_index("created_at", background=True)
        await products_collection.create_index([("name", "text"), ("description", "text")], background=True)
        
        # Compound indexes for common filter combinations
        await products_collection.create_index([("category", 1), ("price", 1)], background=True)
        await products_collection.create_index([("category", 1), ("created_at", -1)], background=True)
        
        logger.info("✅ Database indexes created successfully")
    except Exception as e:
        logger.warning(f"⚠️  Index creation warning: {e}")
