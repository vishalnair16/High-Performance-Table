from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.cache import connect_to_redis, close_redis_connection
from app.routes import product_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting application...")
    await connect_to_mongo()
    await connect_to_redis()
    yield
    # Shutdown
    logger.info("🛑 Shutting down application...")
    await close_mongo_connection()
    await close_redis_connection()

app = FastAPI(
    title="High Performance Data Table API",
    description="FastAPI backend for handling 100,000+ records with sub-100ms response times",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routes
app.include_router(product_routes.router)

@app.get("/")
def root():
    return {
        "message": "High Performance Data Table API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from app.core.database import db
        from app.core.cache import cache
        
        health_status = {
            "status": "healthy",
            "mongodb": "connected" if db.client else "disconnected",
            "redis": "connected" if cache.redis_client else "disconnected"
        }
        
        # Test MongoDB connection
        if db.client:
            await db.client.admin.command('ping')
        
        # Test Redis connection
        if cache.redis_client:
            await cache.redis_client.ping()
        
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
