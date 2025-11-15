from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
from datetime import datetime
import time
import logging
from bson import ObjectId
from bson.errors import InvalidId

from app.core.database import get_database
from app.core.cache import get_cache, set_cache, generate_cache_key, delete_cache_pattern
from app.schemas.product_schema import (
    ProductResponse, 
    ProductListResponse, 
    ProductCreate, 
    ProductUpdate,
    ProductQueryParams
)
from app.core.config import settings

router = APIRouter(prefix="/api/v1/products", tags=["products"])
logger = logging.getLogger(__name__)

def build_query_filters(
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_stock: Optional[int] = None,
    tags: Optional[List[str]] = None
) -> dict:
    """Build MongoDB query filters"""
    filters = {}
    
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"sku": {"$regex": search, "$options": "i"}}
        ]
    
    if category:
        filters["category"] = category
    
    if min_price is not None or max_price is not None:
        filters["price"] = {}
        if min_price is not None:
            filters["price"]["$gte"] = min_price
        if max_price is not None:
            filters["price"]["$lte"] = max_price
    
    if min_stock is not None:
        filters["stock"] = {"$gte": min_stock}
    
    if tags:
        filters["tags"] = {"$in": tags}
    
    return filters

def build_sort(sort_by: str = "created_at", sort_order: str = "desc") -> list:
    """Build MongoDB sort specification"""
    order = -1 if sort_order == "desc" else 1
    return [(sort_by, order)]

@router.get("", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_stock: Optional[int] = Query(None, ge=0),
    sort_by: str = Query("created_at", pattern="^(name|price|created_at|rating|stock)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    tags: Optional[List[str]] = Query(None)
):
    """
    Get products with filtering, sorting, and pagination.
    Optimized for high performance with caching.
    """
    start_time = time.time()
    
    try:
        # Generate cache key
        cache_key = generate_cache_key(
            "products_list",
            page=page,
            page_size=page_size,
            search=search,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            sort_by=sort_by,
            sort_order=sort_order,
            tags=",".join(tags) if tags else None
        )
        
        # Try to get from cache
        cached_result = await get_cache(cache_key)
        if cached_result:
            logger.info(f"Cache hit for {cache_key}")
            return ProductListResponse(**cached_result)
        
        # Build query
        filters = build_query_filters(
            search=search,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_stock=min_stock,
            tags=tags
        )
        
        sort_spec = build_sort(sort_by, sort_order)
        
        # Get database
        db = await get_database()
        collection = db["products"]
        
        # Get total count (optimized with hint)
        total = await collection.count_documents(filters)
        
        # Calculate pagination
        skip = (page - 1) * page_size
        total_pages = (total + page_size - 1) // page_size
        
        # Fetch products with projection for performance
        cursor = collection.find(filters).sort(sort_spec).skip(skip).limit(page_size)
        products = await cursor.to_list(length=page_size)
        
        # Convert ObjectId to string and format response
        product_list = []
        for product in products:
            product["_id"] = str(product["_id"])
            product["created_at"] = product.get("created_at", datetime.utcnow())
            product["updated_at"] = product.get("updated_at", datetime.utcnow())
            product_list.append(ProductResponse(**product))
        
        response_data = {
            "products": [p.dict(by_alias=True) for p in product_list],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
        
        # Cache the result
        await set_cache(cache_key, response_data, ttl=settings.CACHE_TTL)
        
        elapsed_time = (time.time() - start_time) * 1000
        logger.info(f"Query completed in {elapsed_time:.2f}ms")
        
        return ProductListResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get a single product by ID.
    """
    start_time = time.time()
    
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        # Check cache
        cache_key = generate_cache_key("product_detail", product_id=product_id)
        cached_result = await get_cache(cache_key)
        if cached_result:
            return ProductResponse(**cached_result)
        
        # Get database
        db = await get_database()
        collection = db["products"]
        
        # Find product
        product = await collection.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Format response
        product["_id"] = str(product["_id"])
        product["created_at"] = product.get("created_at", datetime.utcnow())
        product["updated_at"] = product.get("updated_at", datetime.utcnow())
        
        response_data = ProductResponse(**product).dict(by_alias=True)
        
        # Cache the result
        await set_cache(cache_key, response_data, ttl=settings.CACHE_TTL * 2)
        
        elapsed_time = (time.time() - start_time) * 1000
        logger.info(f"Query completed in {elapsed_time:.2f}ms")
        
        return ProductResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    Create a new product.
    """
    try:
        db = await get_database()
        collection = db["products"]
        
        # Check if SKU already exists
        existing = await collection.find_one({"sku": product.sku})
        if existing:
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")
        
        # Create product document
        product_dict = product.dict()
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        
        # Insert product
        result = await collection.insert_one(product_dict)
        
        # Fetch created product
        created_product = await collection.find_one({"_id": result.inserted_id})
        created_product["_id"] = str(created_product["_id"])
        
        # Invalidate cache
        await delete_cache_pattern("cache:products_list:*")
        
        return ProductResponse(**created_product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    """
    Update a product.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        db = await get_database()
        collection = db["products"]
        
        # Check if product exists
        existing = await collection.find_one({"_id": ObjectId(product_id)})
        if not existing:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Prepare update data
        update_data = product_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update product
        await collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        # Fetch updated product
        updated_product = await collection.find_one({"_id": ObjectId(product_id)})
        updated_product["_id"] = str(updated_product["_id"])
        
        # Invalidate cache
        await delete_cache_pattern("cache:products_list:*")
        await delete_cache_pattern(f"cache:product_detail:product_id_{product_id}")
        
        return ProductResponse(**updated_product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
    """
    Delete a product.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        db = await get_database()
        collection = db["products"]
        
        # Delete product
        result = await collection.delete_one({"_id": ObjectId(product_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Invalidate cache
        await delete_cache_pattern("cache:products_list:*")
        await delete_cache_pattern(f"cache:product_detail:product_id_{product_id}")
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats():
    """
    Get product statistics.
    """
    try:
        cache_key = generate_cache_key("products_stats")
        cached_result = await get_cache(cache_key)
        if cached_result:
            return cached_result
        
        db = await get_database()
        collection = db["products"]
        
        # Use aggregation pipeline for efficient stats
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_products": {"$sum": 1},
                    "total_stock": {"$sum": "$stock"},
                    "avg_price": {"$avg": "$price"},
                    "min_price": {"$min": "$price"},
                    "max_price": {"$max": "$price"},
                    "avg_rating": {"$avg": "$rating"}
                }
            }
        ]
        
        result = await collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            stats = result[0]
            stats.pop("_id", None)
        else:
            stats = {
                "total_products": 0,
                "total_stock": 0,
                "avg_price": 0,
                "min_price": 0,
                "max_price": 0,
                "avg_rating": 0
            }
        
        # Cache stats
        await set_cache(cache_key, stats, ttl=settings.CACHE_TTL)
        
        return stats
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

