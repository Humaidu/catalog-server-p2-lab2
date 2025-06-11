# Catalog Server

A simple, lightweight Catalog API built with Flask and PostgreSQL, deployed on an EC2 instance and served with Nginx as a reverse proxy.

---

## Features

- REST API to retrieve product listings.
- Backend powered by Flask and SQLAlchemy ORM.
- PostgreSQL as the relational database.
- Nginx configured as a reverse proxy for performance and security.
- Systemd unit file for managing the Flask app as a background service.
- Environment variable-based configuration for security and portability.

---

## Project Structure
catalog-server/
    ├── app.py # Main Flask application
    ├── .env # Environment variables
    ├── requirements.txt # Python dependencies
    └── venv/ # Python virtual environment

---


---

## Prerequisites

- Python 3.12+
- PostgreSQL
- Nginx
- Git
- EC2 instance or any Linux environment

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Humaidu/catalog-server.git
cd catalog-server
```

### 2. Set Up Python Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 3. Configure Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://db_user:db_password@localhost/db_name

```

### 4. Update `app.py` to Use `.env`

```
from dotenv import load_dotenv
load_dotenv()

```

### 5. Set Up PostgreSQL

```
sudo -u postgres psql
CREATE DATABASE catalog_db;
CREATE USER catalog_user WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE catalog_db TO catalog_user;

CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	description TEXT,
	price DECIMAL NOT NULL
);"

\q

```

## Run the App

```
python app.py

```

---

## Live App 

**http://3.249.117.153/products**

---

## Configure Nginx as Reverse Proxy

**Create Nginx config file:**

```
sudo nano /etc/nginx/sites-available/catalog

```

**Paste the following config:**

```
# /etc/nginx/sites-available/catalog
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```

**Enable Configuration and reload:**

```
sudo ln -s /etc/nginx/sites-available/catalog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

```

---

## Run Flask as a Background Service

**Create a systemd service file:**

```
sudo nano /etc/systemd/system/catalog.service

```

**Paste the following configuration (replace placeholders)**

```
[Unit]
Description=Catalog API Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/catalog-server
ExecStart=/home/ubuntu/catalog-server/venv/bin/python app.py
Restart=always
Environment="FLASK_ENV=production"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target

```

**Update paths and user if different:**
- `User=ubuntu` (use your actual Linux username)
- `WorkingDirectory` and `ExecStart` should point to your project directory and Python binary inside the virtual environment.

**Start, Reload and Enable the catalog servive:**
```
sudo systemctl daemon-reload
sudo systemctl start catalog
sudo systemctl enable catalog

```

---

## API Endpoints

| Method | Endpoint    | Description            |
| ------ | ----------- | ---------------------- |
| GET    | `/products` | Get all product items  |
| GET    | `/`         | Health check / welcome |

---

## Test the API

curl http://<your-ec2-ip>/products

**Example:**
curl http://3.249.117.153/products

**Output:**

```
[
  {
    "description": "Powerful laptop",
    "id": 1,
    "name": "Laptop",
    "price": 1200.0
  },
  {
    "description": "Android phone",
    "id": 2,
    "name": "Smartphone",
    "price": 800.0
  },
  {
    "description": "10-inch screen",
    "id": 3,
    "name": "Tablet",
    "price": 400.0
  }
]

```

