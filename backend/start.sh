#!/bin/bash

# Quick start script for the High Performance Data Table Backend

echo "🚀 Starting High Performance Data Table Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please update it with your MongoDB URI if needed."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Start Docker Compose
echo "🐳 Starting Docker Compose services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo "🏥 Checking service health..."
curl -s http://localhost:8000/health | python -m json.tool || echo "⚠️  Services may still be starting..."

echo ""
echo "✅ Services started!"
echo ""
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo ""
echo "🌱 To seed the database, run:"
echo "   docker-compose exec backend python -m app.utils.seed_data"
echo ""
echo "📝 Or with reseed:"
echo "   docker-compose exec -e RESEED_DB=true backend python -m app.utils.seed_data"
echo ""

