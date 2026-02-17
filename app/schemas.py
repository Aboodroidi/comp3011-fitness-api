from pydantic import BaseModel, Field

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