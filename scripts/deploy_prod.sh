#!/usr/bin/env bash
# Armor Enterprise Platform - Zero-Downtime Production Deployment Script
set -e

echo "=========================================================="
echo "      ARMOR ENTERPRISE HARDWARE PLATFORM - DEPLOY         "
echo "=========================================================="

echo "[1/6] Checking Docker & Docker Compose installation..."
docker --version
docker compose version

echo "[2/6] Building production Docker container images..."
docker compose -f docker-compose.yml build --pull

echo "[3/6] Applying database migrations & syncing schemas..."
docker compose -f docker-compose.yml run --rm web python manage.py migrate --noinput

echo "[4/6] Collecting static assets & optimizing bundles..."
docker compose -f docker-compose.yml run --rm web python manage.py collectstatic --noinput

echo "[5/6] Seeding default enterprise catalog & warehouse telemetry..."
docker compose -f docker-compose.yml run --rm web python manage.py loaddata initial_data.json || echo "No initial fixture found or already seeded."

echo "[6/6] Launching production stack (Gunicorn + Daphne + Nginx + Redis + PostgreSQL)..."
docker compose -f docker-compose.yml up -d --remove-orphans

echo "=========================================================="
echo " ✔ SUCCESS: Armor Enterprise Platform is LIVE!"
echo "   - Web Storefront: http://localhost:80"
echo "   - HTTPS Endpoints: https://localhost:443"
echo "   - Admin Dashboard: http://localhost/dashboard/"
echo "   - Google Merchant Feed: http://localhost/dashboard/feed/google.xml"
echo "=========================================================="
