import os
import subprocess
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader
import pymysql

APP_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def index():
    tpl = env.get_template('index.html')
    return tpl.render()

@app.post('/create-db')
async def create_db(db_name: str = Form(...), db_user: str = Form(...), db_pass: str = Form(...)):
    host = os.environ.get('DB_HOST', 'mariadb')
    port = int(os.environ.get('DB_PORT', 3306))
    root_user = os.environ.get('DB_ROOT_USER', 'root')
    root_pass = os.environ.get('DB_ROOT_PASS', '')

    try:
        conn = pymysql.connect(host=host, user=root_user, password=root_pass, port=port)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        cur.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY %s;", (db_pass,))
        cur.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%';")
        cur.execute("FLUSH PRIVILEGES;")
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse({"status": "ok", "message": f"Database {db_name} created."})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post('/create-vhost')
async def create_vhost(domain: str = Form(...)):
    docroot = f"/var/www/vhosts/{domain}/public_html"
    os.makedirs(docroot, exist_ok=True)
    with open(os.path.join(docroot, 'index.html'), 'w') as f:
        f.write(f"<h1>Site {domain} powered by OpenLiteSpeed</h1>")

    script = '/usr/local/lsws/admin/misc/create_vhost.sh'
    try:
        subprocess.check_output([script, domain, docroot], stderr=subprocess.STDOUT)
        return JSONResponse({"status": "ok", "message": f"VHost for {domain} created."})
    except subprocess.CalledProcessError as e:
        return JSONResponse({"status": "error", "message": e.output.decode()}, status_code=500)
