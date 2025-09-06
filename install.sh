#!/usr/bin/env bash
set -e
echo "[+] Building and starting containers..."
docker compose up -d --build
echo "[+] Done!"
echo "Panel: http://localhost:8080"
echo "OLS Admin: https://localhost:7080 (user: admin, pass: set in docker-compose.yml)"
