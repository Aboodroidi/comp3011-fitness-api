from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import ExerciseOut
from app.services.exercise_service import search_exercises

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
    sort_by: Optional[str] = Query(
        default="recommended",
        description="Sort results: recommended, rating_low_high, rating_high_low"
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of exercises to return"
    ),
    db: Session = Depends(get_db),
):
    return search_exercises(
        db=db,
        q=q,
        body_part=body_part,
        equipment=equipment,
        difficulty=difficulty,
        exercise_type=exercise_type,
        sort_by=sort_by,
        limit=limit,
    )