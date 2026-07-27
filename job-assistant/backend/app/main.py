from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.api.routes import health, jobs
from app.core.database import Base, engine
from app.core.settings import settings


@asynccontextmanager
async def lifespan(
    _: FastAPI,
):
    """
    Cria as tabelas do MVP quando a API inicia.
    """

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


app.include_router(
    health.router,
    prefix="/api",
)

app.include_router(
    jobs.router,
    prefix="/api",
)


@app.get("/")
def root() -> dict:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }