# mycustomwebpanel
🔹 What this does

Fetches the repo with all the files I gave you (docker-compose.yml, FastAPI panel, OLS configs, scripts).

Runs docker compose up -d --build.

Starts OpenLiteSpeed, MariaDB, and the custom Panel.

🔹 After it runs

Panel UI → http://your-server-ip:8080

OLS Admin UI → https://your-server-ip:7080
 (login: admin / password from docker-compose.yml)
