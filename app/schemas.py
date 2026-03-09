from datetime import date
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkoutBase(BaseModel):
    date: date
    workout_type: str = Field(..., min_length=1, max_length=100)
    duration_min: int = Field(..., ge=1, le=600)
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(BaseModel):
    date: Optional[date] = None
    workout_type: Optional[str] = Field(None, min_length=1, max_length=100)
    duration_min: Optional[int] = Field(None, ge=1, le=600)
    notes: Optional[str] = None


class WorkoutOut(WorkoutBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ExerciseOut(BaseModel):
    id: int
    name: str
    body_part: Optional[str] = None
    equipment: Optional[str] = None
    target_muscle: Optional[str] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class HealthOut(BaseModel):
    status: str


class WorkoutStreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    total_workout_days: int


class WeeklySummaryOut(BaseModel):
    week_start: date
    week_end: date
    total_sessions: int
    total_minutes: int
    sessions_by_type: Dict[str, int]