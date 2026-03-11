from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import ExerciseFiltersOut, ExerciseOut
from app.services.exercise_service import (
    get_exercise_by_id,
    get_exercise_filter_metadata,
    recommend_exercises,
    search_exercises,
)

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)


@router.get(
    "/meta/filters",
    response_model=ExerciseFiltersOut,
    summary="Get available exercise filters",
    description="Returns available body parts, equipment types, difficulty levels, exercise types, and total exercise count."
)
def get_exercise_filters(
    db: Session = Depends(get_db),
):
    return get_exercise_filter_metadata(db)


@router.get(
    "/recommend",
    response_model=List[ExerciseOut],
    summary="Recommend exercises",
    description="Returns recommended exercises based on filters such as body part, equipment, difficulty, and exercise type."
)
def recommend_exercise_list(
    body_part: Optional[str] = Query(default=None, description="Filter by body part"),
    equipment: Optional[str] = Query(default=None, description="Filter by equipment"),
    difficulty: Optional[str] = Query(default=None, description="Filter by difficulty"),
    exercise_type: Optional[str] = Query(default=None, description="Filter by exercise type"),
    limit: int = Query(default=5, ge=1, le=20, description="Maximum number of recommended exercises"),
    db: Session = Depends(get_db),
):
    return recommend_exercises(
        db=db,
        body_part=body_part,
        equipment=equipment,
        difficulty=difficulty,
        exercise_type=exercise_type,
        limit=limit,
    )


@router.get(
    "/{exercise_id}",
    response_model=ExerciseOut,
    summary="Get exercise by ID",
    description="Retrieve a single exercise record by its unique identifier."
)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
):
    exercise = get_exercise_by_id(db, exercise_id)

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return exercise


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
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip"
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
        skip=skip,
        limit=limit,
    )