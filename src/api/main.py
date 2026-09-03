from __future__ import annotations

import logging
import time
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from database import get_db_connection, initialize_db

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Contoso API", version="1.0.0")


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


@app.on_event("startup")
def on_startup() -> None:
    # Retry DB initialization briefly instead of crashing the container the
    # instant the database isn't reachable yet (e.g. cold start, DNS not
    # propagated, private endpoint still coming up).
    max_attempts = 5
    delay_seconds = 3
    for attempt in range(1, max_attempts + 1):
        try:
            initialize_db()
            logger.info("Database initialized successfully.")
            return
        except Exception:  # noqa: BLE001
            logger.exception(
                "Database initialization failed (attempt %s/%s).", attempt, max_attempts
            )
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Contoso API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=List[ItemResponse])
def list_items() -> List[ItemResponse]:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM items ORDER BY id")
            rows = cursor.fetchall()
    finally:
        connection.close()

    return [ItemResponse(id=row[0], name=row[1], description=row[2]) for row in rows]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> ItemResponse:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description FROM items WHERE id = %s",
                (item_id,),
            )
            row = cursor.fetchone()
    finally:
        connection.close()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return ItemResponse(id=row[0], name=row[1], description=row[2])


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> ItemResponse:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description",
                (payload.name, payload.description),
            )
            row = cursor.fetchone()
        connection.commit()
    except Exception as exc:  # pragma: no cover - defensive path
        connection.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    finally:
        connection.close()

    if row is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create item")

    return ItemResponse(id=row[0], name=row[1], description=row[2])
