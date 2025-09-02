# ITCS 6190/8190 – Docker Hands-On: Installing Docker & Building a Multi-Container Microservice

## 📌 Project Overview
This project demonstrates how to containerize a Python Flask application, connect it with a Redis cache, and orchestrate the services using Docker Compose. PostgreSQL was also deployed as part of the multi-container setup. The exercise helped in understanding container networking, service orchestration, and basic troubleshooting with Docker Desktop.

---

## 🚀 Execution Steps

### 1. Verify Docker Installation
``` 
docker -v
```
2. Pull PostgreSQL image
```
   docker pull postgress:14
```
3. Run PostgreSQL Container
```
   docker run -d -p 5432:5432 --name postgres1 -e POSTGRES_PASSWORD=pass12345 postgres:14
```

4. Create Project Folder
```
app.py
requirements.txt
Dockerfile
compose.yaml
```

5. Define Dependencies
```
requirements.txt
flask
redis
```

6. Define Flask Application

App.py

```
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f"Hello World! I have been seen {count} times.\n"
```

7. Create Dockerfile

Dockerfile

```
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

8. Define Multi-container setup

compose.yaml
```
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8000:5000"
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
```

9. Build and run application
```
docker compose up
```

10. Open application in browser
Go to:
http://localhost:8000

Each refresh will increase the counter.
