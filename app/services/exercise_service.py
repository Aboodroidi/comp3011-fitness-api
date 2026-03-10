from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Query, Session

from app.models_exercises import Exercise


def apply_exercise_search(
    query: Query,
    q: Optional[str],
) -> Query:
    if q:
        query = query.filter(
            or_(
                Exercise.name.ilike(f"%{q}%"),
                Exercise.description.ilike(f"%{q}%")
            )
        )
    return query


def apply_exercise_filters(
    query: Query,
    body_part: Optional[str],
    equipment: Optional[str],
    difficulty: Optional[str],
    exercise_type: Optional[str],
) -> Query:
    if body_part:
        query = query.filter(Exercise.body_part == body_part)

    if equipment:
        query = query.filter(Exercise.equipment == equipment)

    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    if exercise_type:
        query = query.filter(Exercise.exercise_type == exercise_type)

    return query


def apply_exercise_sorting(
    query: Query,
    sort_by: Optional[str],
) -> Query:
    if sort_by == "rating_low_high":
        query = query.order_by(
            Exercise.rating.asc().nullslast(),
            Exercise.id.asc()
        )
    elif sort_by == "rating_high_low":
        query = query.order_by(
            Exercise.rating.desc().nullslast(),
            Exercise.id.asc()
        )
    else:
        # recommended
        query = query.order_by(
            Exercise.rating.desc().nullslast(),
            Exercise.name.asc()
        )

    return query


def search_exercises(
    db: Session,
    q: Optional[str] = None,
    body_part: Optional[str] = None,
    equipment: Optional[str] = None,
    difficulty: Optional[str] = None,
    exercise_type: Optional[str] = None,
    sort_by: Optional[str] = "recommended",
    limit: int = 50,
):
    query = db.query(Exercise)

    query = apply_exercise_search(query, q)
    query = apply_exercise_filters(
        query,
        body_part=body_part,
        equipment=equipment,
        difficulty=difficulty,
        exercise_type=exercise_type,
    )
    query = apply_exercise_sorting(query, sort_by)

    return query.limit(limit).all()