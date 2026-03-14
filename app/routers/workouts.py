from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.security import get_current_user
from ..db import get_db
from .. import models, schemas
from app.services.workout_plan_service import build_workout_plan

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


def _attach_workout_exercises(
    workout: models.WorkoutLog,
    exercise_entries: list[schemas.WorkoutExerciseCreate],
):
    for entry in exercise_entries:
        workout.exercises.append(
            models.WorkoutExercise(
                exercise_id=entry.exercise_id,
                sets=entry.sets,
                reps=entry.reps,
                weight_kg=entry.weight_kg,
            )
        )


def _get_workout_with_exercises(
    db: Session,
    workout_id: int,
    owner_id: int,
):
    stmt = (
        select(models.WorkoutLog)
        .options(
            selectinload(models.WorkoutLog.exercises).selectinload(models.WorkoutExercise.exercise)
        )
        .where(
            models.WorkoutLog.id == workout_id,
            models.WorkoutLog.owner_id == owner_id,
        )
    )
    return db.execute(stmt).scalars().first()


@router.post(
    "",
    response_model=schemas.WorkoutOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Workout",
    description="Create a new workout record for the authenticated user.",
)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_workout = models.WorkoutLog(
        owner_id=current_user.id,
        date=workout.date.isoformat(),
        workout_type=workout.workout_type,
        duration_min=workout.duration_min,
        notes=workout.notes,
    )

    db.add(new_workout)
    db.flush()

    _attach_workout_exercises(new_workout, workout.exercises)

    db.commit()

    created_workout = _get_workout_with_exercises(db, new_workout.id, current_user.id)
    return created_workout


@router.get(
    "",
    response_model=list[schemas.WorkoutOut],
    summary="List Workouts",
    description="Retrieve workout records belonging to the authenticated user.",
)
def list_workouts(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of records to return"),
    current_user: models.User = Depends(get_current_user),
):
    stmt = (
        select(models.WorkoutLog)
        .options(
            selectinload(models.WorkoutLog.exercises).selectinload(models.WorkoutExercise.exercise)
        )
        .where(models.WorkoutLog.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(models.WorkoutLog.id.desc())
    )
    return db.execute(stmt).scalars().all()


@router.get(
    "/suggest-plan",
    summary="Suggest a workout plan",
    description="Returns a simple workout plan using the exercise dataset based on goal, number of training days, equipment, and difficulty."
)
def suggest_workout_plan(
    goal: str = Query(
        default="strength",
        description="Training goal: strength, hypertrophy, or general_fitness"
    ),
    days: int = Query(
        default=3,
        ge=3,
        le=5,
        description="Number of training days per week"
    ),
    equipment: Optional[str] = Query(
        default=None,
        description="Preferred equipment"
    ),
    difficulty: Optional[str] = Query(
        default=None,
        description="Preferred difficulty level"
    ),
    db: Session = Depends(get_db),
):
    return build_workout_plan(
        db=db,
        goal=goal,
        days=days,
        equipment=equipment,
        difficulty=difficulty,
    )


@router.get(
    "/{workout_id}",
    response_model=schemas.WorkoutOut,
    summary="Get Workout",
    description="Retrieve a specific workout owned by the authenticated user.",
    responses=not_found_response,
)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    workout = _get_workout_with_exercises(db, workout_id, current_user.id)

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
    description="Update an existing workout entry owned by the authenticated user.",
    responses=not_found_response,
)
def update_workout(
    workout_id: int,
    payload: schemas.WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    workout = _get_workout_with_exercises(db, workout_id, current_user.id)

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    if payload.date is not None:
        workout.date = payload.date.isoformat()

    if payload.workout_type is not None:
        workout.workout_type = payload.workout_type

    if payload.duration_min is not None:
        workout.duration_min = payload.duration_min

    if payload.notes is not None:
        workout.notes = payload.notes

    if payload.exercises is not None:
        workout.exercises.clear()
        db.flush()
        _attach_workout_exercises(workout, payload.exercises)

    db.commit()

    updated_workout = _get_workout_with_exercises(db, workout_id, current_user.id)
    return updated_workout


@router.delete(
    "/{workout_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Workout",
    description="Delete a workout entry owned by the authenticated user.",
    responses=not_found_response,
)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    workout = db.execute(
        select(models.WorkoutLog).where(
            models.WorkoutLog.id == workout_id,
            models.WorkoutLog.owner_id == current_user.id,
        )
    ).scalars().first()

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found",
        )

    db.delete(workout)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)