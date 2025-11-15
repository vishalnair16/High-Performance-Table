# 🚀 Quick Start Guide

## Single Command Setup

From the **root directory** of the project:

```bash
docker-compose up -d
```

That's it! All services will start automatically.

## First Time Setup

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Seed database:**
   ```bash
   docker exec -it high_perf_backend python seed.py
   ```

3. **Open your browser:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## Common Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after dependency changes
docker-compose up -d --build

# Check service status
docker-compose ps
```

## Troubleshooting

- **Port conflicts**: Change ports in `docker-compose.yml`
- **Database issues**: Check logs with `docker-compose logs mongodb`
- **Rebuild everything**: `docker-compose down -v && docker-compose up -d --build`

---

For detailed documentation, see the main README.md

