# Setup script for RVUverse Google Auth
# Run this after installing requirements: pip install -r requirements.txt

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Green
python manage.py migrate

# Create superuser if needed
Write-Host ""
Write-Host "Create a superuser account for Django admin" -ForegroundColor Yellow
python manage.py createsuperuser

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Read GOOGLE_AUTH_SETUP.md for Google OAuth configuration"
Write-Host "2. Create a .env file with your Google OAuth credentials"
Write-Host "3. Run the development server: python manage.py runserver"
Write-Host "4. Go to http://localhost:8000/admin to configure Social Applications"
Write-Host ""
