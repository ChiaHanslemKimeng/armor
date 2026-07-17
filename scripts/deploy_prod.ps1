# Armor Enterprise Platform - Windows Production Deployment Script
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      ARMOR ENTERPRISE HARDWARE PLATFORM - DEPLOY         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "[1/6] Checking Docker & Docker Compose installation..." -ForegroundColor Yellow
docker --version
docker compose version

Write-Host "[2/6] Building production Docker container images..." -ForegroundColor Yellow
docker compose -f docker-compose.yml build --pull

Write-Host "[3/6] Applying database migrations & syncing schemas..." -ForegroundColor Yellow
docker compose -f docker-compose.yml run --rm web python manage.py migrate --noinput

Write-Host "[4/6] Collecting static assets & optimizing bundles..." -ForegroundColor Yellow
docker compose -f docker-compose.yml run --rm web python manage.py collectstatic --noinput

Write-Host "[5/6] Launching production stack (Gunicorn + Daphne + Nginx + Redis + PostgreSQL)..." -ForegroundColor Yellow
docker compose -f docker-compose.yml up -d --remove-orphans

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Armor Enterprise Platform is LIVE!" -ForegroundColor Green
Write-Host "   - Web Storefront: http://localhost:80" -ForegroundColor White
Write-Host "   - HTTPS Endpoints: https://localhost:443" -ForegroundColor White
Write-Host "   - Admin Dashboard: http://localhost/dashboard/" -ForegroundColor White
Write-Host "   - Google Merchant Feed: http://localhost/dashboard/feed/google.xml" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
