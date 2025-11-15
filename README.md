# High Performance Data Table - Full Stack

A complete full-stack application designed to handle 100,000+ records with sub-100ms API response times and smooth, responsive UI interactions.

## 🚀 Quick Start (Single Command)

From the **root directory** of the project:

```bash
docker-compose up -d
```

This single command will start:
- ✅ MongoDB (port 27017)
- ✅ Redis (port 6379)
- ✅ FastAPI Backend (port 8000)
- ✅ Next.js Frontend (port 3000)

### First Time Setup

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Seed the database:**
   ```bash
   docker exec -it high_perf_backend python seed.py
   ```

3. **Access the application:**
   - 🌐 Frontend: http://localhost:3000
   - 🔌 Backend API: http://localhost:8000
   - 📚 API Docs: http://localhost:8000/docs

### Stop All Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
```

## 📁 Project Structure

```
Project/
├── docker-compose.yml      # Single compose file for all services
├── backend/                # FastAPI backend
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/               # Next.js frontend
    ├── app/
    ├── components/
    ├── Dockerfile
    └── package.json
```

## 🛠️ Development

### Backend Development

The backend code is mounted as a volume, so changes are hot-reloaded automatically.

### Frontend Development

The frontend code is mounted as a volume, so changes are hot-reloaded automatically.

### Rebuild After Dependency Changes

If you change `package.json` or `requirements.txt`:

```bash
docker-compose up -d --build
```

## 🔧 Configuration

### Environment Variables

You can override environment variables by creating a `.env` file in the root directory:

```env
# Backend
MONGO_URI=mongodb://admin:admin123@mongodb:27017/?authSource=admin
DB_NAME=high_performance_db
REDIS_HOST=redis
REDIS_PORT=6379
ENABLE_CACHE=true
CACHE_TTL=300

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Services

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js application |
| Backend | 8000 | FastAPI REST API |
| MongoDB | 27017 | Database |
| Redis | 6379 | Cache layer |

## 🐛 Troubleshooting

### Port Already in Use

If ports are already in use, you can change them in `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8001:8000"  # Change backend port
```

### Database Connection Issues

Check if MongoDB is healthy:
```bash
docker-compose ps
docker-compose logs mongodb
```

### Rebuild Everything

```bash
docker-compose down -v  # Remove volumes too
docker-compose up -d --build
```

## 📚 More Information

- **Backend Details**: See `backend/README.md`
- **Frontend Details**: See `frontend/README.md`

## 🎯 Features

- ✅ Single command setup (`docker-compose up`)
- ✅ Hot reload for development
- ✅ Health checks for all services
- ✅ Persistent data volumes
- ✅ Optimized for 100,000+ records
- ✅ Sub-100ms API responses
- ✅ Virtual scrolling UI

---

Built with ❤️ using FastAPI and Next.js

