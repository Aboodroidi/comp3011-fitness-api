# COMP3011 Fitness API

A RESTful **Workout Logging and Fitness Analytics API** built with **FastAPI** and **SQLite**.

The API allows users to log workout sessions, manage workout history, and generate simple analytics such as workout streaks and weekly summaries.

This project was developed for the **COMP3011 – Web Services and Web Data** module at the **University of Leeds**.

---

# Live API

Deployed API  
https://aboodroid.pythonanywhere.com

Interactive Swagger Documentation  
https://aboodroid.pythonanywhere.com/docs

ReDoc Documentation  
https://aboodroid.pythonanywhere.com/redoc

---

# API Documentation

The full API documentation generated from the OpenAPI specification is included in this repository.

File:
API_Documentation.pdf

This documentation describes all endpoints, request schemas, and responses.

---

# Features

• Full CRUD operations for workout logs  
• Analytics endpoints including workout streaks and weekly summaries  
• Exercise dataset containing 471 gym exercises  
• SQLite database integration using SQLAlchemy  
• RESTful API design with correct HTTP status codes  
• Interactive API documentation via Swagger UI  
• Automated tests using pytest  
• Deployed API hosted on PythonAnywhere  

---

# Tech Stack

Python 3  
FastAPI  
SQLite  
SQLAlchemy  
Pydantic  
Pytest  
Uvicorn  

---

# Project Structure

comp3011-fitness-api  
│  
├── app  
│   ├── main.py  
│   ├── db.py  
│   ├── models.py  
│   ├── models_exercises.py  
│   ├── schemas.py  
│   │  
│   └── routers  
│       ├── workouts.py  
│       ├── analytics.py  
│       └── exercises.py  
│  
├── data  
│   └── gym_exercises.csv  
│  
├── scripts  
│   └── seed_exercises.py  
│  
├── tests  
│   ├── conftest.py  
│   ├── test_workouts.py  
│   ├── test_analytics.py  
│   └── test_exercises.py  
│  
├── API_Documentation.pdf  
├── openapi.json  
└── README.md  

---

# Setup Instructions

Clone the repository

git clone https://github.com/Aboodroidi/comp3011-fitness-api  
cd comp3011-fitness-api  

Create a virtual environment

python -m venv venv  
source venv/bin/activate  

Install dependencies

pip install -r requirements.txt  

---

# Initialize the Database

Create database tables

python -c "from app.db import Base, engine; import app.models; import app.models_exercises; Base.metadata.create_all(bind=engine)"

Seed the exercise dataset

python -m scripts.seed_exercises

This loads the **471 exercise records** used by the `/exercises` endpoint.

---

# Run the API

Start the server

uvicorn app.main:app --reload

The API will be available at

http://127.0.0.1:8000

Swagger documentation

http://127.0.0.1:8000/docs

---

# Example Endpoints

Create Workout

POST /workouts

Example request body

{
  "date": "2026-03-01",
  "workout_type": "Push",
  "duration_min": 60,
  "notes": "Chest workout"
}

---

Get Workout

GET /workouts/{workout_id}

---

Workout Streak

GET /analytics/streak

Example response

{
  "current_streak": 3,
  "longest_streak": 5,
  "total_workout_days": 12
}

---

Weekly Summary

GET /analytics/weekly-summary?week_start=2026-03-01

Returns total sessions, total minutes, and distribution of workout types.

---

# Testing

Run the automated test suite

pytest

The tests cover

• Workout CRUD endpoints  
• Error handling (404 and 422 responses)  
• Analytics endpoints  
• Exercise search functionality  

---

# Dataset

The exercise dataset contains **471 gym exercises** and is loaded from

data/gym_exercises.csv

The dataset includes

• exercise name  
• equipment type  
• muscle group  
• exercise images  
• description  

---

# Deployment

The API is deployed on **PythonAnywhere** using Uvicorn.

Live deployment

https://aboodroid.pythonanywhere.com

---

# Generative AI Usage

Generative AI tools were used during development to assist with debugging, exploring API design ideas, and improving documentation clarity. All generated suggestions were reviewed and modified before inclusion in the final system.

Examples of AI interaction logs are included in the coursework submission.

---

# License

This project was developed for academic coursework at the **University of Leeds**.