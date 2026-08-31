from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine


app = FastAPI(
    title="API de réservation de salles",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "API de réservation de salles"
    }


@app.get("/health")
async def health():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }