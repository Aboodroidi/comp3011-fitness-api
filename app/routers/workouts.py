from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/workouts", tags=["Workouts"])

not_found_response = {
    404: {
        "description": "Workout not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Workout not found"
                }
            }
        },
    }
}


@router.post(
    "",
    response_model=schemas.WorkoutOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Workout",
    description="Create a new workout record.",
)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
):
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


@router.get(
    "",
    response_model=list[schemas.WorkoutOut],
    summary="List Workouts",
    description="Retrieve a list of workout records with optional pagination.",
)
def list_workouts(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of records to return"),
):
    stmt = (
        select(models.WorkoutLog)
        .offset(skip)
        .limit(limit)
        .order_by(models.WorkoutLog.id.desc())
    )
    return db.execute(stmt).scalars().all()


@router.get(
    "/{workout_id}",
    response_model=schemas.WorkoutOut,
    summary="Get Workout",
    description="Retrieve a specific workout using its unique ID.",
    responses=not_found_response,
)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )
    return workout


@router.put(
    "/{workout_id}",
    response_model=schemas.WorkoutOut,
    summary="Update Workout",
    description="Update an existing workout entry using its unique ID.",
    responses=not_found_response,
)
def update_workout(
    workout_id: int,
    payload: schemas.WorkoutUpdate,
    db: Session = Depends(get_db),
):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(workout, key, value)

    db.commit()
    db.refresh(workout)
    return workout


@router.delete(
    "/{workout_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Workout",
    description="Delete a workout entry using its unique ID.",
    responses=not_found_response,
)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
):
    workout = db.get(models.WorkoutLog, workout_id)
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    db.delete(workout)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)