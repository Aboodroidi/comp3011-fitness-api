from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_exercises import Exercise
from app.schemas import ExerciseOut

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)


@router.get(
    "",
    response_model=List[ExerciseOut],
    summary="List exercises",
    description="Search and filter exercises from the gym dataset."
)
def list_exercises(
    q: Optional[str] = Query(
        default=None,
        description="Search by exercise name or description"
    ),
    body_part: Optional[str] = Query(
        default=None,
        description="Filter by body part"
    ),
    equipment: Optional[str] = Query(
        default=None,
        description="Filter by equipment"
    ),
    difficulty: Optional[str] = Query(
        default=None,
        description="Filter by difficulty level"
    ),
    exercise_type: Optional[str] = Query(
        default=None,
        description="Filter by exercise type"
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of exercises to return"
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Exercise)

    if q:
        query = query.filter(
            or_(
                Exercise.name.ilike(f"%{q}%"),
                Exercise.description.ilike(f"%{q}%")
            )
        )

    if body_part:
        query = query.filter(Exercise.body_part == body_part)

    if equipment:
        query = query.filter(Exercise.equipment == equipment)

    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    if exercise_type:
        query = query.filter(Exercise.exercise_type == exercise_type)

    return query.order_by(Exercise.id.asc()).limit(limit).all()