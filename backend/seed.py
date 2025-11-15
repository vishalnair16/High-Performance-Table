"""
Standalone script to seed the database.
Can be run directly: python seed.py
"""
import asyncio
import logging
from app.utils.seed_data import seed_database

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Seed 100,000 products
    asyncio.run(seed_database(100000))

