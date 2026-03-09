from fastapi import FastAPI

from app.db import Base, engine
from app.schemas import HealthOut
from app.routers import analytics, exercises, workouts

import app.models
import app.models_exercises

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness API",
    description="A RESTful API for logging workouts, analysing training activity, and searching a preloaded exercise dataset.",
    version="0.1.0",
)

app.include_router(workouts.router)
app.include_router(analytics.router)
app.include_router(exercises.router)


@app.get(
    "/health",
    response_model=HealthOut,
    tags=["System"],
    summary="Health Check",
    description="Returns the current health status of the API service."
)
def health():
    return {"status": "ok"}