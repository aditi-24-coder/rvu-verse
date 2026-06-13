# RVUverse Development Server Startup Script

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Green
python manage.py migrate

# Start development server
Write-Host "Starting development server..." -ForegroundColor Green
python manage.py runserver
