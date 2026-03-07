from fastapi import FastAPI

from app.routers import workouts, analytics, exercises  

from app.db import Base, engine
import app.models
import app.models_exercises

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness API")

app.include_router(workouts.router)
app.include_router(analytics.router)
app.include_router(exercises.router)


@app.get("/health")
def health():
    return {"status": "ok"}