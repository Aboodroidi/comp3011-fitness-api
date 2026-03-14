from datetime import date as dt_date
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "abdullah",
                "email": "abdullah@example.com",
                "password": "StrongPass123"
            }
        }
    )


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "abdullah",
                "password": "StrongPass123"
            }
        }
    )


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "abdullah",
                "email": "abdullah@example.com"
            }
        }
    )


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ1c2VyX2lkIjoxLCJleHAiOjE3MDAwMDAwMDB9.signature",
                "token_type": "bearer"
            }
        }
    )


class WorkoutExerciseBase(BaseModel):
    exercise_id: int = Field(..., ge=1)
    sets: int = Field(..., ge=1, le=20)
    reps: int = Field(..., ge=1, le=100)
    weight_kg: Optional[int] = Field(default=None, ge=0, le=1000)


class WorkoutExerciseCreate(WorkoutExerciseBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "exercise_id": 1,
                "sets": 4,
                "reps": 10,
                "weight_kg": 60
            }
        }
    )


class WorkoutExerciseOut(WorkoutExerciseBase):
    id: int
    exercise_name: Optional[str] = None
    body_part: Optional[str] = None
    equipment: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "exercise_id": 1,
                "exercise_name": "Bench Press",
                "body_part": "Chest",
                "equipment": "Barbell",
                "sets": 4,
                "reps": 10,
                "weight_kg": 60
            }
        }
    )


class WorkoutBase(BaseModel):
    date: dt_date
    workout_type: str = Field(..., min_length=1, max_length=100)
    duration_min: int = Field(..., ge=1, le=600)
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-09",
                "workout_type": "Push",
                "duration_min": 60,
                "notes": "Chest and shoulders session",
                "exercises": [
                    {
                        "exercise_id": 1,
                        "sets": 4,
                        "reps": 10,
                        "weight_kg": 60
                    }
                ]
            }
        }
    )


class WorkoutUpdate(BaseModel):
    date: Optional[dt_date] = Field(default=None)
    workout_type: Optional[str] = Field(default=None, min_length=1, max_length=100)
    duration_min: Optional[int] = Field(default=None, ge=1, le=600)
    notes: Optional[str] = Field(default=None)
    exercises: Optional[List[WorkoutExerciseCreate]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-10",
                "workout_type": "Pull",
                "duration_min": 45,
                "notes": "Back and biceps session",
                "exercises": [
                    {
                        "exercise_id": 2,
                        "sets": 3,
                        "reps": 12,
                        "weight_kg": 25
                    }
                ]
            }
        }
    )


class WorkoutOut(WorkoutBase):
    id: int
    exercises: List[WorkoutExerciseOut] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "date": "2026-03-09",
                "workout_type": "Push",
                "duration_min": 60,
                "notes": "Chest and shoulders session",
                "exercises": [
                    {
                        "id": 1,
                        "exercise_id": 1,
                        "exercise_name": "Bench Press",
                        "body_part": "Chest",
                        "equipment": "Barbell",
                        "sets": 4,
                        "reps": 10,
                        "weight_kg": 60
                    }
                ]
            }
        },
    )


class ExerciseOut(BaseModel):
    id: int
    name: str
    body_part: Optional[str] = None
    equipment: Optional[str] = None
    difficulty: Optional[str] = None
    exercise_type: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    rating_desc: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Crunch",
                "body_part": "Abdominals",
                "equipment": "Body Only",
                "difficulty": "Beginner",
                "exercise_type": "Strength",
                "description": "A core exercise targeting the abdominal muscles.",
                "rating": 8.9,
                "rating_desc": "Highly effective for core activation."
            }
        },
    )


class HealthOut(BaseModel):
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
            }
        }
    )


class WorkoutStreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    total_workout_days: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_streak": 3,
                "longest_streak": 5,
                "total_workout_days": 12,
            }
        }
    )


class WeeklySummaryOut(BaseModel):
    week_start: dt_date
    week_end: dt_date
    total_sessions: int
    total_minutes: int
    sessions_by_type: Dict[str, int]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "week_start": "2026-03-01",
                "week_end": "2026-03-07",
                "total_sessions": 4,
                "total_minutes": 215,
                "sessions_by_type": {
                    "Push": 1,
                    "Pull": 1,
                    "Legs": 1,
                    "Cardio": 1
                }
            }
        }
    )


class ExerciseFiltersOut(BaseModel):
    body_parts: List[str]
    equipment: List[str]
    difficulty: List[str]
    exercise_types: List[str]
    total_exercises: int


class ExerciseDistributionItem(BaseModel):
    category: str
    count: int