# Forum

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140-009688?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-8-47A248?logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?logo=jsonwebtokens&logoColor=white)

Forum is a FastAPI-based backend service for managing library events. It supports event creation and management, participant registration, statistics, audit logging, and basic system metrics.

## Features

- Event management: create, update, delete, and search events
- Participant registration and cancellation for events
- Event statistics: upcoming and popular events
- Audit logging for user actions and CSV export
- System metrics: CPU and memory usage

## Tech Stack

- Python 3.12
- FastAPI
- MongoDB
- Beanie (MongoDB ODM)
- JWT authentication
- Docker and Docker Compose

## Project Structure

- src/main.py — FastAPI entry point
- src/api — API routes
- src/services — business logic
- src/models — MongoDB models
- src/schemas — Pydantic schemas
- src/config — database connection configuration

## Requirements

For local development:

- Python 3.12+
- pip
- Docker and Docker Compose (for container-based setup)

## Environment Variables

Create a .env file in the project root with the following values:

```env
SECRET_KEY=change-me
ALGORITHM=HS256
DATABASE_URL=mongodb://app_user:app_password@localhost:27017/forum_db?authSource=admin
DATABASE_NAME=forum_db
```

Notes:

- When running with Docker Compose, the DATABASE_URL value will be overridden inside the container for internal MongoDB communication.
- For local runs, use localhost. For container-based runs, use the forum-db service hostname.

## Run with Docker Compose

1. Make sure Docker is installed and running.
2. If needed, create the external network:

```bash
docker network create backend-network
```

3. Start the app and database:

```bash
docker compose up --build -d
```

4. After startup, the application will be available at:

```text
http://localhost:8002
```

5. Swagger documentation will be available at:

```text
http://localhost:8002/docs
```

6. To stop the services:

```bash
docker compose down
```

## Local Run

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure MongoDB is available at the address specified in DATABASE_URL.

4. Start the server:

```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8002
```

5. Open Swagger UI:

```text
http://localhost:8002/docs
```

## API and Authentication

Most endpoints require a JWT token in the Authorization header:

```http
Authorization: Bearer <token>
```

To access administrative operations such as metrics and audit views, the token must include the admin role. For event creation and update operations, roles admin or librarian are accepted.

## Main Routes

- GET /docs — Swagger UI
- POST /events/create — create an event
- PUT /events/update/{event_id} — update an event
- DELETE /events/delete/{event_id} — delete an event
- GET /events/search — search events
- GET /events/{event_id} — get an event by ID
- POST /events/{event_id}/registrations — register a user
- DELETE /events/{event_id}/registrations — cancel registration
- GET /events/statistics/upcoming — upcoming events
- GET /events/statistics/popular — popular events
- GET /metrics/stats — system metrics
- GET /audit/logs — audit logs
- GET /audit/export — export audit logs as CSV

## Useful Commands

Check Docker Compose configuration:

```bash
docker compose config
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```
