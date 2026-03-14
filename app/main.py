from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import Base, engine
from app.routers import analytics, exercises, workouts
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="COMP3011 Fitness API",
    description="Fitness tracking API with authentication, exercise search, and workout analytics.",
    version="1.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(analytics.router)
app.include_router(exercises.router)


@app.get("/", tags=["UI"])
def dashboard(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Verify that the API is running."
)
def health_check():
    return {"status": "ok"}