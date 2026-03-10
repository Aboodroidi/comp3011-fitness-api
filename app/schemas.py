from datetime import date as dt_date
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from typing import Optional
from pydantic import BaseModel, ConfigDict


class WorkoutBase(BaseModel):
    date: dt_date
    workout_type: str = Field(..., min_length=1, max_length=100)
    duration_min: int = Field(..., ge=1, le=600)
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-09",
                "workout_type": "Push",
                "duration_min": 60,
                "notes": "Chest and shoulders session",
            }
        }
    )


class WorkoutUpdate(BaseModel):
    date: Optional[dt_date] = Field(
        default=None,
        json_schema_extra={"example": "2026-03-10"},
    )
    workout_type: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "Pull"},
    )
    duration_min: Optional[int] = Field(
        default=None,
        ge=1,
        le=600,
        json_schema_extra={"example": 45},
    )
    notes: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "Back and biceps session"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-10",
                "workout_type": "Pull",
                "duration_min": 45,
                "notes": "Back and biceps session",
            }
        }
    )


class WorkoutOut(WorkoutBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "date": "2026-03-09",
                "workout_type": "Push",
                "duration_min": 60,
                "notes": "Chest and shoulders session",
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
                    "Cardio": 1,
                },
            }
        }
    )