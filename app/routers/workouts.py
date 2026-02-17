from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/workouts", tags=["Workouts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    new_workout = models.WorkoutLog(
        date=workout.date,
        workout_type=workout.workout_type,
        duration_min=workout.duration_min,
        notes=workout.notes,
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout