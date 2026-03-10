# COMP3011 Fitness API

A RESTful **Workout Logging and Fitness Analytics API** built using **FastAPI** and **SQLite**.

The system allows users to log workouts, track training history, explore a large dataset of gym exercises, and generate simple analytics such as workout streaks and weekly summaries.

This project demonstrates core web services concepts including:

- RESTful API design
- database integration
- automated testing
- OpenAPI documentation
- cloud deployment

The API exposes endpoints for managing workout logs and searching a dataset of gym exercises with filtering and sorting capabilities.

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

# Features

## Workout Logging

• Create workout sessions  
• Retrieve workout history  
• Update workout entries  
• Delete workout logs  

All operations follow RESTful conventions with appropriate HTTP status codes.

---

## Fitness Analytics

The API provides simple analytics derived from the workout history:

• **Workout streak tracking**  
• **Weekly workout summaries**  
• **Workout distribution by type**

These endpoints demonstrate how stored workout data can be used to generate useful insights.

---

## Exercise Dataset Search

The API integrates a gym exercise dataset allowing users to explore available exercises.

Supported capabilities include:

• Search exercises by keyword  
• Filter by body part  
• Filter by equipment  
• Filter by difficulty level  
• Filter by exercise type  
• Sort exercises by rating  
• Limit returned results  

Example queries:

Search exercises

GET /exercises?q=bench

Filter exercises by body part

GET /exercises?body_part=Chest

Sort exercises by rating (highest first)

GET /exercises?sort_by=rating_high_low

---

# Technology Stack

Backend

• Python 3  
• FastAPI  
• SQLAlchemy  
• SQLite  

Testing

• Pytest  

Deployment

• Uvicorn  
• PythonAnywhere  

---

# Project Structure

```
comp3011-fitness-api
│
├── app
│   ├── main.py                 # FastAPI application entry point
│   ├── db.py                   # Database configuration
│   ├── models.py               # Workout database models
│   ├── models_exercises.py     # Exercise dataset models
│   ├── schemas.py              # Pydantic validation schemas
│   │
│   └── routers
│       ├── workouts.py         # Workout CRUD endpoints
│       ├── analytics.py        # Analytics endpoints
│       └── exercises.py        # Exercise dataset search API
│
├── data
│   └── gym_exercises.csv       # Exercise dataset
│
├── scripts
│   └── seed_exercises.py       # Script to load exercise dataset
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
```

---

# Setup Instructions

Clone the repository

```
git clone https://github.com/Aboodroidi/comp3011-fitness-api
cd comp3011-fitness-api
```

Create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Initialize the Database

Create database tables

```
python -c "from app.db import Base, engine; import app.models; import app.models_exercises; Base.metadata.create_all(bind=engine)"
```

Seed the exercise dataset

```
python -m scripts.seed_exercises
```

This loads the gym exercise dataset used by the `/exercises` endpoint.

---

# Run the API

Start the server

```
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

# Example Endpoints

Create Workout

POST /workouts

Example request body

```
{
  "date": "2026-03-01",
  "workout_type": "Push",
  "duration_min": 60,
  "notes": "Chest workout"
}
```

---

Retrieve Workout

GET /workouts/{workout_id}

---

Workout Streak

GET /analytics/streak

Example response

```
{
  "current_streak": 3,
  "longest_streak": 5,
  "total_workout_days": 12
}
```

---

Weekly Summary

GET /analytics/weekly-summary?week_start=2026-03-01

Returns:

• total sessions  
• total minutes  
• distribution of workout types  

---

# Testing

Automated tests are implemented using **pytest**.

Run the full test suite

```
pytest
```

The tests cover:

• Workout CRUD endpoints  
• Error handling (404 and validation errors)  
• Analytics calculations  
• Exercise search and filtering  
• Sorting functionality  

Tests use a **separate test database** to ensure isolation from production data.

---

# Dataset

The exercise dataset used in this project was obtained from Kaggle:

https://www.kaggle.com/datasets/niharika41298/gym-exercise-data

The dataset includes information such as:

• exercise name  
• equipment used  
• target muscle group  
• difficulty level  
• exercise description  
• exercise images  

The dataset is stored locally as:

```
data/gym_exercises.csv
```

and is loaded into the SQLite database using the seeding script.

---

# Deployment

The API is deployed on **PythonAnywhere** using Uvicorn.

Live deployment

https://aboodroid.pythonanywhere.com

The deployed API includes:

• public REST endpoints  
• interactive Swagger documentation  
• ReDoc documentation  

---

# Generative AI Usage

Generative AI tools were used during development to assist with:

• debugging implementation issues  
• exploring improvements to API design  
• refining test structures  
• improving documentation clarity  

AI suggestions were treated as starting points and were carefully reviewed and modified before being integrated into the final system.

All generated code and ideas were manually verified and tested before inclusion.

Examples of AI interaction logs are included in the coursework submission as required by the module guidelines.

---

# License

This project was developed for academic coursework at the **University of Leeds**.