@echo off
REM Quick start script for Windows

echo 🚀 Starting High Performance Data Table Backend...
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo ✅ Created .env file. Please update it with your MongoDB URI if needed.
    ) else (
        echo ❌ .env.example not found. Please create .env manually.
        exit /b 1
    )
)

REM Start Docker Compose
echo 🐳 Starting Docker Compose services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check health
echo 🏥 Checking service health...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Services are healthy!
) else (
    echo ⚠️  Services may still be starting...
)

echo.
echo ✅ Services started!
echo.
echo 📊 API Documentation: http://localhost:8000/docs
echo 🏥 Health Check: http://localhost:8000/health
echo.
echo 🌱 To seed the database, run:
echo    docker-compose exec backend python -m app.utils.seed_data
echo.
echo 📝 Or with reseed:
echo    docker-compose exec -e RESEED_DB=true backend python -m app.utils.seed_data
echo.

pause

