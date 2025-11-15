# Quick Start Guide

## 🚀 Fastest Way to Get Started

### 1. Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Seed the database (100,000 products)
docker-compose exec backend python -m app.utils.seed_data

# Access API
# - API Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

### 2. Using Start Scripts

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

### 3. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (or use .env file)
export MONGO_URI="your_mongodb_uri"
export DB_NAME="high_performance_db"

# Start MongoDB and Redis (or use Docker)
# Then run:
uvicorn app.main:app --reload

# Seed database
python seed.py
```

## 📊 Test the API

```bash
# Get products (paginated)
curl "http://localhost:8000/api/v1/products?page=1&page_size=50"

# Search products
curl "http://localhost:8000/api/v1/products?search=laptop"

# Filter by category
curl "http://localhost:8000/api/v1/products?category=Electronics"

# Filter by price range
curl "http://localhost:8000/api/v1/products?min_price=100&max_price=1000"

# Sort by price
curl "http://localhost:8000/api/v1/products?sort_by=price&sort_order=desc"
```

## 🔧 Environment Variables

Create a `.env` file or set these variables:

```env
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=high_performance_db
REDIS_HOST=redis
REDIS_PORT=6379
ENABLE_CACHE=true
CACHE_TTL=300
```

## 📝 Common Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Reseed database (clears existing data)
docker-compose exec -e RESEED_DB=true backend python -m app.utils.seed_data
```

## 🐛 Troubleshooting

**Services won't start:**
- Check if ports 8000, 27017, 6379 are available
- Verify Docker is running
- Check logs: `docker-compose logs`

**Database connection fails:**
- Verify MongoDB URI is correct
- Check network connectivity
- Verify credentials

**Slow queries:**
- Ensure indexes are created (check logs on startup)
- Verify Redis is running for caching
- Check database size and connection pool

## 📚 Next Steps

1. Seed the database with 100,000+ products
2. Test API endpoints at `/docs`
3. Connect your NextJS frontend to `http://localhost:8000`
4. Monitor performance with health endpoint

For detailed documentation, see [README.md](README.md)

