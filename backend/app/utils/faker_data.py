from faker import Faker
import random
from typing import List
from app.models.product_models import Product

fake = Faker()

# Product categories
CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden", "Sports & Outdoors",
    "Books", "Toys & Games", "Health & Beauty", "Automotive",
    "Food & Beverages", "Pet Supplies", "Office Supplies", "Jewelry"
]

# Product brands
BRANDS = [
    "TechCorp", "StyleBrand", "HomeEssentials", "SportMax", "BookWorld",
    "GameZone", "BeautyPlus", "AutoPro", "FreshFoods", "PetCare",
    "OfficePro", "JewelryLux", "Generic", "Premium", "Budget"
]

# Product tags
TAGS_POOL = [
    "new", "sale", "popular", "featured", "bestseller", "limited",
    "eco-friendly", "premium", "budget", "trending", "vintage",
    "modern", "classic", "innovative", "durable", "lightweight"
]

def generate_product() -> Product:
    """Generate a single fake product"""
    category = random.choice(CATEGORIES)
    price = round(random.uniform(5.99, 9999.99), 2)
    
    # Generate realistic product name based on category
    if category == "Electronics":
        name = f"{fake.word().title()} {random.choice(['Smart', 'Pro', 'Ultra', 'Max', 'Mini'])} {random.choice(['Device', 'Gadget', 'Tool', 'System'])}"
    elif category == "Clothing":
        name = f"{fake.word().title()} {random.choice(['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'])}"
    elif category == "Books":
        name = f"{fake.catch_phrase()} - {fake.name()}"
    else:
        name = fake.catch_phrase()
    
    # Generate SKU
    sku = f"{category[:3].upper()}-{fake.bothify(text='####-???').upper()}"
    
    # Generate description
    description = fake.text(max_nb_chars=200)
    
    # Generate tags (2-5 random tags)
    num_tags = random.randint(2, 5)
    tags = random.sample(TAGS_POOL, num_tags)
    
    # Generate rating (weighted towards higher ratings)
    rating = round(random.choices(
        [1.0, 2.0, 3.0, 4.0, 4.5, 5.0],
        weights=[1, 2, 5, 15, 25, 52]
    )[0], 1)
    
    # Reviews count (correlated with rating)
    reviews_count = int(random.uniform(0, 10000) * (rating / 5))
    
    return Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock=random.randint(0, 1000),
        sku=sku,
        brand=random.choice(BRANDS),
        rating=rating,
        reviews_count=reviews_count,
        tags=tags
    )

def generate_products(count: int) -> List[dict]:
    """Generate multiple fake products"""
    products = []
    for _ in range(count):
        product = generate_product()
        products.append(product.to_dict())
    return products

