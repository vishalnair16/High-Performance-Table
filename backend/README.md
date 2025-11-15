# High Performance Data Table Backend

A high-performance FastAPI backend designed to handle 100,000+ records with sub-100ms response times through optimized queries, intelligent caching, and efficient database indexing.

## 🚀 Features

- **High Performance**: Sub-100ms API response times for 100,000+ records
- **Advanced Filtering**: Search, filter by category, price range, stock, and tags
- **Smart Caching**: Redis-based caching layer for frequently accessed data
- **Optimized Queries**: MongoDB indexes and query optimization
- **Pagination**: Efficient cursor-based pagination
- **RESTful API**: Clean, well-documented REST endpoints
- **Docker Ready**: Complete Docker Compose setup for easy deployment

## 📋 Tech Stack

- **Backend Framework**: FastAPI 0.104+
- **Database**: MongoDB 7.0
- **Cache**: Redis 7.2
- **Python**: 3.11+
- **ORM**: Motor (async MongoDB driver)
- **Validation**: Pydantic v2

## 🏗️ Architecture

### Performance Optimizations

1. **Database Indexing**
   - Single field indexes on frequently queried fields (name, category, price, created_at)
   - Text search index on name and description
   - Compound indexes for common filter combinations

2. **Redis Caching**
   - Query result caching with configurable TTL
   - Cache invalidation on data mutations
   - Pattern-based cache key generation

3. **Query Optimization**
   - Efficient MongoDB aggregation pipelines
   - Projection to limit returned fields
   - Batch operations for bulk inserts

4. **Connection Pooling**
   - MongoDB connection pooling (min: 10, max: 50)
   - Redis connection pooling (max: 50)

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── database.py         # MongoDB connection and indexes
│   │   └── cache.py            # Redis caching layer
│   ├── models/
│   │   └── product_models.py   # Product data models
│   ├── schemas/
│   │   └── product_schema.py   # Pydantic validation schemas
│   ├── routes/
│   │   └── product_routes.py   # API endpoints
│   └── utils/
│       ├── faker_data.py       # Fake data generation
│       └── seed_data.py        # Database seeding utility
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- MongoDB URI (or use local MongoDB via Docker)

> **📖 MongoDB Atlas Setup**: If you're using MongoDB Atlas, see [MONGODB_SETUP.md](MONGODB_SETUP.md) for detailed instructions on configuring your connection string and database name.

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create environment file** (optional, uses defaults if not provided)
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI if using external MongoDB
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Seed the database** (in a new terminal)
   ```bash
   docker-compose exec backend python -m app.utils.seed_data
   ```

5. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Option 2: Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export MONGO_URI="your_mongodb_uri"
   export DB_NAME="high_performance_db"
   export REDIS_HOST="localhost"
   export REDIS_PORT="6379"
   ```

3. **Start MongoDB and Redis** (if not using Docker)
   ```bash
   # MongoDB
   mongod
   
   # Redis
   redis-server
   ```

4. **Seed the database**
   ```bash
   python -m app.utils.seed_data
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📡 API Endpoints

### Products

- `GET /api/v1/products` - Get products with filtering, sorting, and pagination
- `GET /api/v1/products/{product_id}` - Get a single product
- `POST /api/v1/products` - Create a new product
- `PUT /api/v1/products/{product_id}` - Update a product
- `DELETE /api/v1/products/{product_id}` - Delete a product
- `GET /api/v1/products/stats/summary` - Get product statistics

### Query Parameters

**GET /api/v1/products** supports:
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 50, max: 1000)
- `search` (string): Search in name, description, SKU
- `category` (string): Filter by category
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `min_stock` (int): Minimum stock filter
- `sort_by` (string): Sort field (name, price, created_at, rating, stock)
- `sort_order` (string): Sort direction (asc, desc)
- `tags` (array): Filter by tags

### Example Requests

```bash
# Get products with pagination
curl "http://localhost:8000/api/v1/products?page=1&page_size=50"

# Search products
curl "http://localhost:8000/api/v1/products?search=laptop&page=1"

# Filter by category and price
curl "http://localhost:8000/api/v1/products?category=Electronics&min_price=100&max_price=1000"

# Sort by price descending
curl "http://localhost:8000/api/v1/products?sort_by=price&sort_order=desc"
```

## 🎯 Performance Optimization Techniques

### 1. Database Indexing
- **Single Field Indexes**: Created on `name`, `category`, `price`, `created_at`
- **Text Index**: Full-text search on `name` and `description`
- **Compound Indexes**: Optimized for common filter combinations
- **Background Indexing**: Indexes created in background to avoid blocking

### 2. Redis Caching Strategy
- **Query Result Caching**: Cache entire API responses with TTL
- **Cache Key Generation**: Pattern-based keys for efficient invalidation
- **Cache Invalidation**: Automatic invalidation on data mutations
- **Graceful Degradation**: System continues to work if Redis is unavailable

### 3. Query Optimization
- **Projection**: Limit returned fields to reduce network overhead
- **Efficient Pagination**: Skip/limit with proper indexing
- **Aggregation Pipelines**: Used for statistics and complex queries
- **Connection Pooling**: Reuse database connections

### 4. Code-Level Optimizations
- **Async/Await**: Non-blocking I/O operations
- **Batch Operations**: Bulk inserts for seeding
- **Response Serialization**: Efficient JSON serialization with orjson
- **Request Timing**: Middleware to track response times

## 📊 Performance Metrics

Target performance metrics:
- ✅ API response time: < 100ms (cached queries: < 10ms)
- ✅ Database query time: < 50ms (with indexes)
- ✅ Cache hit rate: > 80% (for frequently accessed data)
- ✅ Initial page load: < 2 seconds

## 🧪 Testing the Performance

```bash
# Test API response time
time curl "http://localhost:8000/api/v1/products?page=1&page_size=50"

# Test with cache (second request should be faster)
time curl "http://localhost:8000/api/v1/products?page=1&page_size=50"

# Test filtering performance
time curl "http://localhost:8000/api/v1/products?category=Electronics&min_price=100"
```

## 🔧 Configuration

Environment variables (see `.env.example`):

- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `REDIS_PASSWORD`: Redis password (optional)
- `ENABLE_CACHE`: Enable/disable caching (default: true)
- `CACHE_TTL`: Cache time-to-live in seconds (default: 300)

## 🐳 Docker Services

The `docker-compose.yml` includes:

1. **MongoDB**: Database service on port 27017
2. **Redis**: Cache service on port 6379
3. **Backend**: FastAPI application on port 8000

All services are connected via a Docker network and include health checks.

## 📝 Database Seeding

The seeding utility generates realistic product data:

- 100,000+ products by default
- 12 product categories
- Realistic pricing, ratings, and stock levels
- Batch insertion for performance

To seed:
```bash
# With Docker
docker-compose exec backend python -m app.utils.seed_data

# Locally
python -m app.utils.seed_data
```

## 🚨 Error Handling

- Comprehensive error handling with appropriate HTTP status codes
- Validation errors with detailed messages
- Global exception handler for unhandled errors
- Health check endpoint for monitoring

## 🔒 Security Considerations

- Input validation with Pydantic
- ObjectId validation for MongoDB queries
- SQL injection prevention (using parameterized queries)
- CORS configuration (update for production)

## 📈 Monitoring

- Health check endpoint: `/health`
- Request timing headers: `X-Process-Time`
- Structured logging for debugging
- Cache hit/miss logging

## 🎨 UI/UX Considerations (Frontend)

While this is the backend, the API is designed to support:

- **Virtual Scrolling**: Pagination supports large datasets
- **Instant Search**: Fast search with caching
- **Real-time Filtering**: Efficient filter queries
- **Smooth Sorting**: Indexed sort operations
- **Loading States**: Fast responses enable smooth UX

## 🔮 Future Improvements

With more time, I would implement:

1. **Advanced Caching**:
   - Cache warming strategies
   - Multi-level caching (in-memory + Redis)
   - Cache preloading for common queries

2. **Query Optimization**:
   - Query result compression
   - Response streaming for very large datasets
   - Materialized views for complex aggregations

3. **Monitoring & Observability**:
   - Prometheus metrics integration
   - Distributed tracing (OpenTelemetry)
   - Performance dashboards

4. **Scalability**:
   - Horizontal scaling with load balancing
   - Database sharding strategies
   - Read replicas for read-heavy workloads

5. **Advanced Features**:
   - Full-text search with Elasticsearch
   - GraphQL API alternative
   - WebSocket support for real-time updates
   - Rate limiting and throttling

6. **Testing**:
   - Comprehensive unit tests
   - Integration tests
   - Performance/load testing
   - API contract testing

## 📚 Documentation

- API documentation available at `/docs` (Swagger UI)
- Alternative docs at `/redoc` (ReDoc)
- Health check at `/health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of a technical assessment.

## 👤 Author

Built for high-performance data table demonstration.

---

**Note**: This backend is designed to work with a NextJS frontend. The frontend should be in a separate folder and can connect to this API at `http://localhost:8000`.

