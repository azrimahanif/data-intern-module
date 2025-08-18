@echo off
echo 🚀 Week 4: Docker ^& CI/CD Quick Start
echo ======================================

echo.
echo 📋 Prerequisites Check:
echo ----------------------

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Docker is installed
) else (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Download from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM Check Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Docker Compose is installed
) else (
    echo ❌ Docker Compose is not installed.
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python is installed
) else (
    echo ❌ Python is not installed.
    pause
    exit /b 1
)

echo.
echo 🔧 Setup Instructions:
echo --------------------
echo 1. Copy all starter files to your Week 3 submission folder
echo 2. Install dependencies: pip install -r requirements.txt
echo 3. Test local app: uvicorn main:app --reload
echo 4. Build Docker image: docker build -t employee-api .
echo 5. Test Docker: docker run -p 8000:8000 employee-api
echo 6. Use Docker Compose: docker-compose up -d
echo 7. Deploy to Render using the provided configuration

echo.
echo 📚 Next Steps:
echo -------------
echo • Read WEEK4_GUIDE.md for detailed instructions
echo • Follow the 4 phases step by step
echo • Test each phase before moving to the next
echo • Use Postman to test your API endpoints

echo.
echo 🎯 Goal: Deploy your Week 3 FastAPI app to Render with CI/CD!
echo.
echo Good luck! 🚀
pause
