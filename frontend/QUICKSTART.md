# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Docker Compose (Recommended)

1. **From the frontend directory, start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Seed the database (first time only):**
   ```bash
   docker exec -it high_perf_backend python seed.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend:**
   ```bash
   cd ../backend
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start MongoDB and Redis:**
   ```bash
   docker-compose up mongodb redis -d
   ```

4. **Seed database:**
   ```bash
   python seed.py
   ```

5. **Start backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create `.env.local`:**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start frontend:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   http://localhost:3000

## ✅ Verify Setup

1. Check backend health: http://localhost:8000/health
2. Check API docs: http://localhost:8000/docs
3. Check frontend: http://localhost:3000

## 🐛 Troubleshooting

- **Port already in use**: Stop other services using ports 3000, 8000, 27017, or 6379
- **Docker issues**: Make sure Docker is running
- **Database connection**: Verify MongoDB and Redis containers are healthy: `docker ps`

