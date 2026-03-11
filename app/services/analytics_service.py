from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models_exercises import Exercise


def get_exercise_distribution_by_body_part(db: Session):
    results = (
        db.query(
            Exercise.body_part.label("category"),
            func.count(Exercise.id).label("count")
        )
        .filter(Exercise.body_part.isnot(None))
        .group_by(Exercise.body_part)
        .order_by(func.count(Exercise.id).desc(), Exercise.body_part.asc())
        .all()
    )

    return [
        {
            "category": row.category,
            "count": row.count,
        }
        for row in results
    ]


def get_exercise_distribution_by_equipment(db: Session):
    results = (
        db.query(
            Exercise.equipment.label("category"),
            func.count(Exercise.id).label("count")
        )
        .filter(Exercise.equipment.isnot(None))
        .group_by(Exercise.equipment)
        .order_by(func.count(Exercise.id).desc(), Exercise.equipment.asc())
        .all()
    )

    return [
        {
            "category": row.category,
            "count": row.count,
        }
        for row in results
    ]


def get_top_rated_exercises(
    db: Session,
    body_part: Optional[str] = None,
    equipment: Optional[str] = None,
    difficulty: Optional[str] = None,
    exercise_type: Optional[str] = None,
    limit: int = 10,
):
    query = db.query(Exercise).filter(Exercise.rating.isnot(None))

    if body_part:
        query = query.filter(Exercise.body_part == body_part)

    if equipment:
        query = query.filter(Exercise.equipment == equipment)

    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    if exercise_type:
        query = query.filter(Exercise.exercise_type == exercise_type)

    return (
        query.order_by(Exercise.rating.desc(), Exercise.name.asc())
        .limit(limit)
        .all()
    )