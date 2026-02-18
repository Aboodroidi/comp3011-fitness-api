from fastapi import FastAPI

from .db import engine
from .models import WorkoutLog
from .routers import workouts, analytics

app = FastAPI(
    title="COMP3011 Fitness API",
    version="0.3.0",
    description="Fitness workout logging + analytics API (CRUD + insights).",
)

# Create tables on startup (simple + suitable for coursework)
WorkoutLog.metadata.create_all(bind=engine)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

# Routers
app.include_router(workouts.router)
app.include_router(analytics.router)