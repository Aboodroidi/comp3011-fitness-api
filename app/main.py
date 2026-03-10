from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import Base, engine
from app.routers import workouts, analytics, exercises

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="COMP3011 Fitness API",
    version="1.0.0",
    description="A fitness tracking API with workout logging, analytics, and exercise search."
)

Base.metadata.create_all(bind=engine)

app.include_router(workouts.router)
app.include_router(analytics.router)
app.include_router(exercises.router)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})