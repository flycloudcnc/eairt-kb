"""FastAPI application entry point."""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import entries, tags
from app.schemas import HealthOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="eairt-kb",
    description="Enterprise Artificial Intelligence Runtime Knowledge Store",
    version="0.1.0",
)

app.include_router(entries.router)
app.include_router(tags.router)


@app.get("/health", response_model=HealthOut, tags=["health"])
def health():
    return HealthOut(status="ok")
