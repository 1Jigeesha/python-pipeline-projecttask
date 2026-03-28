# Data Pipeline Project

A complete data pipeline with Flask mock server, FastAPI ingestion service, and PostgreSQL database using Docker Compose.

## Architecture

- **Flask Mock Server** (port 5000): Serves paginated customer data from JSON file.
- **FastAPI Pipeline Service** (port 8000): Ingests data from Flask into PostgreSQL using SQLAlchemy.
- **PostgreSQL** (port 5432): Stores customer data.

Flow: Flask (JSON) → FastAPI (Ingest) → PostgreSQL → API Response

## Prerequisites

- Docker Desktop (running)
- Python 3.10+
- Git

## Setup & Run

1. Clone the repository
2. From project root: `docker compose up --build -d`
3. Verify services: `docker compose ps`

## API Endpoints

### Flask Mock Server
- `GET /api/health` - Health check
- `GET /api/customers?page=1&limit=10` - Paginated customers
- `GET /api/customers/{id}` - Single customer (404 if not found)

### FastAPI Pipeline
- `POST /api/ingest` - Fetch all from Flask, upsert to DB
- `GET /api/customers?page=1&limit=10` - Paginated from DB
- `GET /api/customers/{id}` - Single from DB (404 if not found)

## Testing

Run these commands to verify:

```bash
# Health checks
curl http://localhost:5000/api/health
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Ingest data
curl -X POST http://localhost:8000/api/ingest

# Query database
curl "http://localhost:8000/api/customers?page=1&limit=5"
curl http://localhost:8000/api/customers/1
```

## Database

- **Credentials**: postgres / password
- **Database**: customer_db
- **Port**: 5432

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── .gitignore
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

## Technologies Used

- Flask, FastAPI, SQLAlchemy, PostgreSQL
- Docker, Docker Compose
- Python 3.11

## Submission Notes

- All services start with `docker compose up --build -d`
- Flask serves paginated data from JSON
- FastAPI ingests data successfully (20 records)
- All API endpoints work as specified
