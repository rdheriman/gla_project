from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.routes.reservation import router as reservation_router
from app.routes.salle import router as salle_router


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all,
        )

    yield

    await engine.dispose()


app = FastAPI(
    title="API de réservation de salles",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salle_router)
app.include_router(reservation_router)


@app.get("/")
async def root():
    return {"message": "API de réservation de salles"}


@app.get("/health")
async def health():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
