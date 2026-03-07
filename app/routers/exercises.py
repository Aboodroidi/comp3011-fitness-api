from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.schemas import ExerciseOut
from app.models_exercises import Exercise

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("", response_model=List[ExerciseOut])
def list_exercises(
    q: Optional[str] = Query(default=None, description="Search in exercise name"),
    body_part: Optional[str] = Query(default=None),
    equipment: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Exercise)
    if q:
        query = query.filter(Exercise.name.ilike(f"%{q}%"))
    if body_part:
        query = query.filter(Exercise.body_part == body_part)
    if equipment:
        query = query.filter(Exercise.equipment == equipment)

    return query.order_by(Exercise.id.asc()).limit(limit).all()