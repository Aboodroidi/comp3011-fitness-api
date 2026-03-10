from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.db import Base, engine
from app.routers import workouts
from app.routers import analytics
from app.routers import exercises


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="COMP3011 Fitness API",
    description="Fitness tracking API with exercise search and workout analytics.",
    version="1.0.0"
)


# Static files (CSS / JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Templates (UI)
templates = Jinja2Templates(directory="app/templates")


# Routers
app.include_router(workouts.router)
app.include_router(analytics.router)
app.include_router(exercises.router)


# UI Dashboard
@app.get("/", tags=["UI"])
def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Health check endpoint
@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Verify that the API is running."
)
def health_check():
    return {"status": "ok"}