# NovaBank API

A simple FastAPI service backed by PostgreSQL.

## Run locally

1. Install dependencies:
   `pip install -r requirements.txt`
2. Create a PostgreSQL database and set environment variables (see `.env.example`).
3. Start the API:
   `uvicorn main:app --reload`

## Container build

```bash
docker build -t novabank-api:latest -f src/api/Dockerfile src/api
```

## Endpoints

- `GET /health`
- `GET /items`
- `GET /items/{item_id}`
- `POST /items`
