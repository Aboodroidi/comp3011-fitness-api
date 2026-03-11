from typing import Optional

from sqlalchemy.orm import Session

from app.models_exercises import Exercise


GOAL_SPLITS = {
    "strength": {
        3: ["Chest", "Quadriceps", "Lats"],
        4: ["Chest", "Quadriceps", "Shoulders", "Hamstrings"],
        5: ["Chest", "Quadriceps", "Lats", "Shoulders", "Abdominals"],
    },
    "hypertrophy": {
        3: ["Chest", "Lats", "Quadriceps"],
        4: ["Chest", "Lats", "Shoulders", "Hamstrings"],
        5: ["Chest", "Lats", "Quadriceps", "Shoulders", "Biceps"],
    },
    "general_fitness": {
        3: ["Chest", "Quadriceps", "Abdominals"],
        4: ["Chest", "Lats", "Quadriceps", "Abdominals"],
        5: ["Chest", "Lats", "Quadriceps", "Shoulders", "Abdominals"],
    },
}


def _get_focuses(goal: str, days: int):
    goal = goal.lower()

    if goal not in GOAL_SPLITS:
        goal = "strength"

    if days < 3:
        days = 3
    if days > 5:
        days = 5

    return GOAL_SPLITS[goal][days], goal, days


def _query_exercises_for_focus(
    db: Session,
    focus: str,
    equipment: Optional[str],
    difficulty: Optional[str],
    limit: int = 4,
):
    query = db.query(Exercise).filter(Exercise.body_part == focus)

    if equipment:
        query = query.filter(Exercise.equipment == equipment)

    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    results = (
        query.order_by(Exercise.rating.desc().nullslast(), Exercise.name.asc())
        .limit(limit)
        .all()
    )

    if results:
        return results

    fallback_query = db.query(Exercise).filter(Exercise.body_part == focus)

    return (
        fallback_query.order_by(Exercise.rating.desc().nullslast(), Exercise.name.asc())
        .limit(limit)
        .all()
    )


def build_workout_plan(
    db: Session,
    goal: str = "strength",
    days: int = 3,
    equipment: Optional[str] = None,
    difficulty: Optional[str] = None,
):
    focuses, goal, days = _get_focuses(goal, days)

    plan = []

    for index, focus in enumerate(focuses, start=1):
        exercises = _query_exercises_for_focus(
            db=db,
            focus=focus,
            equipment=equipment,
            difficulty=difficulty,
            limit=4,
        )

        plan.append(
            {
                "day": index,
                "focus": focus,
                "exercises": [exercise.name for exercise in exercises],
            }
        )

    return {
        "goal": goal,
        "days": days,
        "equipment": equipment,
        "difficulty": difficulty,
        "plan": plan,
    }