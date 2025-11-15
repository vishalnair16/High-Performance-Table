from datetime import datetime
from typing import Optional
from bson import ObjectId

class Product:
    """Product model for MongoDB"""
    
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        category: str,
        stock: int,
        sku: str,
        brand: Optional[str] = None,
        rating: Optional[float] = None,
        reviews_count: Optional[int] = None,
        tags: Optional[list] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.stock = stock
        self.sku = sku
        self.brand = brand
        self.rating = rating or 0.0
        self.reviews_count = reviews_count or 0
        self.tags = tags or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return {
            "_id": self._id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "stock": self.stock,
            "sku": self.sku,
            "brand": self.brand,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create product from dictionary"""
        return cls(
            _id=data.get("_id"),
            name=data["name"],
            description=data["description"],
            price=data["price"],
            category=data["category"],
            stock=data["stock"],
            sku=data["sku"],
            brand=data.get("brand"),
            rating=data.get("rating", 0.0),
            reviews_count=data.get("reviews_count", 0),
            tags=data.get("tags", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

