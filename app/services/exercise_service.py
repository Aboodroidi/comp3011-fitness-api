from typing import Optional

from sqlalchemy.orm import Query, Session
from sqlalchemy import or_

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
    skip: int = 0,
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

    return query.offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_exercise_filter_metadata(db: Session):
    body_parts = [
        row[0]
        for row in db.query(Exercise.body_part)
        .filter(Exercise.body_part.isnot(None))
        .distinct()
        .order_by(Exercise.body_part.asc())
        .all()
    ]

    equipment = [
        row[0]
        for row in db.query(Exercise.equipment)
        .filter(Exercise.equipment.isnot(None))
        .distinct()
        .order_by(Exercise.equipment.asc())
        .all()
    ]

    difficulty = [
        row[0]
        for row in db.query(Exercise.difficulty)
        .filter(Exercise.difficulty.isnot(None))
        .distinct()
        .order_by(Exercise.difficulty.asc())
        .all()
    ]

    exercise_types = [
        row[0]
        for row in db.query(Exercise.exercise_type)
        .filter(Exercise.exercise_type.isnot(None))
        .distinct()
        .order_by(Exercise.exercise_type.asc())
        .all()
    ]

    total_exercises = db.query(Exercise).count()

    return {
        "body_parts": body_parts,
        "equipment": equipment,
        "difficulty": difficulty,
        "exercise_types": exercise_types,
        "total_exercises": total_exercises,
    }


def recommend_exercises(
    db: Session,
    body_part: Optional[str] = None,
    equipment: Optional[str] = None,
    difficulty: Optional[str] = None,
    exercise_type: Optional[str] = None,
    limit: int = 5,
):
    query = db.query(Exercise).filter(Exercise.rating.isnot(None))

    query = apply_exercise_filters(
        query,
        body_part=body_part,
        equipment=equipment,
        difficulty=difficulty,
        exercise_type=exercise_type,
    )

    query = query.order_by(
        Exercise.rating.desc(),
        Exercise.name.asc()
    )

    results = query.limit(limit).all()

    if results:
        return results

    fallback_query = db.query(Exercise)

    if body_part:
        fallback_query = fallback_query.filter(Exercise.body_part == body_part)

    fallback_query = fallback_query.order_by(
        Exercise.rating.desc().nullslast(),
        Exercise.name.asc()
    )

    return fallback_query.limit(limit).all()