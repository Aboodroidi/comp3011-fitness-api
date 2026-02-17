# COMP3011 Fitness API

A RESTful Fitness Habit & Workout Tracking API built with FastAPI and SQLite.
The API allows users to log workouts and query basic analytics such as streaks
and weekly summaries.

## Features
- CRUD operations for workout logs
- Analytics endpoints (streaks, summaries)
- Auto-generated API docs via Swagger UI

## Tech Stack
- Python (FastAPI)
- SQLite
- SQLAlchemy

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload