import asyncio
import logging
from app.core.database import get_database, connect_to_mongo, close_mongo_connection
from app.utils.faker_data import generate_products
from app.core.config import settings

logger = logging.getLogger(__name__)

async def seed_database(count: int = 100000):
    """Seed database with fake products"""
    try:
        # Connect to MongoDB first
        await connect_to_mongo()
        
        db = await get_database()
        if db is None:
            raise Exception("Failed to get database connection")
        
        collection = db["products"]
        
        # Check if data already exists
        existing_count = await collection.count_documents({})
        if existing_count > 0:
            logger.info(f"⚠️  Database already contains {existing_count} products")
            # For Docker/non-interactive environments, skip reseeding
            # Set RESEED_DB=true environment variable to force reseed
            import os
            if os.getenv("RESEED_DB", "false").lower() == "true":
                await collection.delete_many({})
                logger.info("✅ Cleared existing data (RESEED_DB=true)")
            else:
                logger.info("Skipping seed operation (set RESEED_DB=true to force reseed)")
                return
        
        logger.info(f"🌱 Starting to seed {count} products...")
        
        # Batch insert for performance
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, count, batch_size):
            batch_count = min(batch_size, count - i)
            products = generate_products(batch_count)
            
            result = await collection.insert_many(products)
            total_inserted += len(result.inserted_ids)
            
            if (i + batch_size) % 10000 == 0 or i + batch_size >= count:
                logger.info(f"✅ Inserted {total_inserted}/{count} products...")
        
        logger.info(f"✅ Successfully seeded {total_inserted} products!")
        
        # Verify count
        final_count = await collection.count_documents({})
        logger.info(f"✅ Database now contains {final_count} products")
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        # Close database connection
        await close_mongo_connection()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_database(100000))

