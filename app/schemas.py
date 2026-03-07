from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ExerciseOut(BaseModel):
    id: int
    name: str
    body_part: Optional[str] = None
    equipment: Optional[str] = None
    target_muscle: Optional[str] = None
    difficulty: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class WorkoutBase(BaseModel):
    date: str = Field(..., examples=["2026-02-17"], description="YYYY-MM-DD")
    workout_type: str = Field(..., examples=["Push", "Pull", "Legs", "Cardio"])
    duration_min: int = Field(..., ge=1, le=600)
    notes: str | None = Field(default=None, max_length=300)

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(BaseModel):
    date: str | None = Field(default=None, examples=["2026-02-17"])
    workout_type: str | None = None
    duration_min: int | None = Field(default=None, ge=1, le=600)
    notes: str | None = Field(default=None, max_length=300)

class WorkoutOut(WorkoutBase):
    id: int

    class Config:
        from_attributes = True