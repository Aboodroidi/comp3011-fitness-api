from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

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


@router.get("", response_model=list[schemas.WorkoutOut])
def list_workouts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    stmt = select(models.WorkoutLog).offset(skip).limit(limit).order_by(models.WorkoutLog.id.desc())
    return db.execute(stmt).scalars().all()


@router.get("/{workout_id}", response_model=schemas.WorkoutOut)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.put("/{workout_id}", response_model=schemas.WorkoutOut)
def update_workout(workout_id: int, payload: schemas.WorkoutUpdate, db: Session = Depends(get_db)):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # Update only provided fields
    if payload.date is not None:
        workout.date = payload.date
    if payload.workout_type is not None:
        workout.workout_type = payload.workout_type
    if payload.duration_min is not None:
        workout.duration_min = payload.duration_min
    if payload.notes is not None:
        workout.notes = payload.notes

    db.commit()
    db.refresh(workout)
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(workout)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)