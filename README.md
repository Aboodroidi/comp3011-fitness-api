# COMP3011 Fitness API

A RESTful **Workout Logging and Fitness Intelligence API** built using **FastAPI** and **SQLite**.

The system allows users to register and authenticate, log workouts, track training history, explore a large dataset of gym exercises, generate workout plans, and derive training analytics such as workout streaks and weekly summaries.

This project demonstrates key **Web Services and Web Data concepts**, including:

- RESTful API design
- database integration with SQLAlchemy
- automated API testing
- OpenAPI documentation
- dataset-driven APIs
- authentication and authorization
- cloud deployment
- interactive frontend dashboard

The API supports **workout tracking with exercise-level logging**, meaning users can record the **sets, reps, and weight for each exercise performed in a workout session**.

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

## User Authentication

The API supports **user authentication and authorization**, allowing multiple users to securely manage their own workout data.

Supported capabilities include:

• user registration  
• user login  
• token-based authentication  
• protected workout endpoints  
• user-specific workout access  

Example registration request

```json
POST /auth/register

{
  "username": "john",
  "email": "john@example.com",
  "password": "StrongPass123"
}

Example Login request 

POST /auth/login

{
  "username": "john",
  "password": "StrongPass123"
}

Example login response

POST /auth/login

{
  "username": "john",
  "password": "StrongPass123"
}

Authenticated requests to protected endpoints must include:

Authorization: Bearer <token>

## Workout Logging

The API provides full authenticated CRUD functionality for workout sessions.

Supported operations:

• Create workout sessions  
• Retrieve workout history  
• Update workout entries  
• Delete workout logs  

Each workout can include **multiple exercises**, allowing detailed tracking of:

• exercise used  
• number of sets  
• repetitions  
• weight lifted (kg)

Example workout structure:

```
{
  "date": "2026-03-01",
  "workout_type": "Push",
  "duration_min": 60,
  "notes": "Chest session",
  "exercises": [
    {
      "exercise_id": 1,
      "sets": 4,
      "reps": 10,
      "weight_kg": 60
    }
  ]
}
```

All operations follow **RESTful conventions** with appropriate HTTP status codes.

---

## Fitness Analytics

The API provides several analytics endpoints derived from the workout history.

Available analytics include:

• **Workout streak tracking**  
• **Weekly workout summaries**  
• **Workout distribution by type**  
• **Top rated exercises from the dataset**

These endpoints demonstrate how stored workout data can be transformed into meaningful insights.

Example:

```
GET /analytics/streak
```

Response:

```
{
  "current_streak": 3,
  "longest_streak": 5,
  "total_workout_days": 12
}
```

---

## Exercise Dataset Search

The API integrates a large **gym exercise dataset** allowing users to explore available exercises.

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

```
GET /exercises?q=bench
```

Filter exercises by body part

```
GET /exercises?body_part=Chest
```

Sort exercises by rating

```
GET /exercises?sort_by=rating_high_low
```

---

## Exercise Recommendations

The API includes a **recommendation endpoint** that returns exercises based on selected filters such as:

• body part  
• equipment  
• difficulty  
• exercise type  

Example:

```
GET /exercises/recommend?body_part=Chest&difficulty=Beginner
```

---

## Workout Plan Generator

The API can generate a **simple multi-day workout plan** using the exercise dataset.

Plans can be customized based on:

• training goal  
• number of training days  
• equipment availability  
• difficulty level

Example:

```
GET /workouts/suggest-plan?goal=hypertrophy&days=4
```

---

# Interactive Dashboard

The project also includes a **frontend dashboard** which interacts with the API.

The dashboard allows users to:

• register and log in through the interface  
• log workouts through a form interface  
• select exercises from the dataset  
• record sets, reps, and weights  
• browse exercises  
• view recommendations  
• generate workout plans  
• view workout analytics and summaries  

The UI communicates directly with the REST API endpoints.

---

# Technology Stack

Backend

• Python 3  
• FastAPI  
• SQLAlchemy  
• SQLite  
• token-based authentication  
• password hashing  

Testing

• Pytest (38 automated tests)

Deployment

• Uvicorn  
• PythonAnywhere  

Frontend

• HTML  
• CSS  
• JavaScript (Fetch API)

---

# Project Structure

```
comp3011-fitness-api
│
├── app
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── models_exercises.py
│   ├── schemas.py
│   ├── security.py
│   │
│   └── routers
│       ├── auth.py
│       ├── workouts.py
│       ├── analytics.py
│       └── exercises.py
├── data
│   └── gym_exercises.csv
│
├── scripts
│   └── seed_exercises.py
│
├── static
│   ├── styles.css
│   └── app.js
│
├── templates
│   └── index.html
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

---

# Run the API

Start the server

```
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# Testing

Automated tests are implemented using **pytest**.

Run the full test suite:

```
pytest
```

The tests cover:

• user registration and login  
• protected workout CRUD endpoints  
• nested exercise logging  
• user-specific data access control  
• error handling and validation  
• analytics calculations  
• exercise search and filtering  
• sorting and recommendation logic  

The tests use a **separate test database** to ensure isolation from production data.

---

# Security

The API now includes **token-based authentication** for protected workout operations.

Security-related features include:

• user registration and login  
• password hashing before storage  
• protected workout endpoints  
• user-specific authorization checks  

This ensures that each authenticated user can only access and modify their own workout records.


# Dataset

The exercise dataset used in this project was obtained from Kaggle:

https://www.kaggle.com/datasets/niharika41298/gym-exercise-data

The dataset contains information including:

• exercise name  
• equipment used  
• target muscle group  
• difficulty level  
• exercise description  

The dataset is stored locally as:

```
data/gym_exercises.csv
```

and loaded into the SQLite database using the provided seeding script.

---

# Deployment

The API is deployed on **PythonAnywhere** using Uvicorn.

Live deployment:

https://aboodroid.pythonanywhere.com

The deployed API includes:

• public and protected REST endpoints  
• interactive Swagger documentation  
• ReDoc documentation  
• interactive dashboard UI  
• authenticated multi-user workout access   

---

# Generative AI Usage

Generative AI tools were used during development to assist with:

• debugging implementation issues  
• exploring improvements to API design  
• refining test structures  
• improving documentation clarity  

AI suggestions were treated as **starting points only** and were carefully reviewed, modified, and tested before inclusion in the final system.

All generated outputs were manually validated to ensure correctness and compliance with coursework requirements.

Examples of AI interaction logs are included in the coursework submission as supplementary material, in accordance with the module guidelines.

---

# License

This project was developed for academic coursework at the **University of Leeds**.