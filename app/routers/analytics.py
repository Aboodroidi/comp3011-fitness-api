from collections import Counter
from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WorkoutLog
from app.schemas import ExerciseDistributionItem, ExerciseOut
from app.services.analytics_service import (
    get_exercise_distribution_by_body_part,
    get_exercise_distribution_by_equipment,
    get_top_rated_exercises,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/streak",
    summary="Get workout streak statistics",
    description="Returns the current streak, longest streak, and total workout days."
)
def get_workout_streak(
    db: Session = Depends(get_db),
):
    workouts = db.query(WorkoutLog).order_by(WorkoutLog.date.asc()).all()

    if not workouts:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_workout_days": 0,
        }

    workout_dates = sorted(
        {
            workout.date if isinstance(workout.date, date)
            else date.fromisoformat(workout.date)
            for workout in workouts
        }
    )

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(workout_dates)):
        if workout_dates[i] == workout_dates[i - 1] + timedelta(days=1):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    latest_date = workout_dates[-1]
    running_streak = 1

    for i in range(len(workout_dates) - 2, -1, -1):
        if workout_dates[i] == latest_date - timedelta(days=1):
            running_streak += 1
            latest_date = workout_dates[i]
        else:
            break

    return {
        "current_streak": running_streak,
        "longest_streak": longest_streak,
        "total_workout_days": len(workout_dates),
    }


@router.get(
    "/weekly-summary",
    summary="Get weekly workout summary",
    description="Returns workout totals and distribution for a given week."
)
def get_weekly_summary(
    week_start: date = Query(..., description="Start date of the week in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    week_end = week_start + timedelta(days=6)

    workouts = (
        db.query(WorkoutLog)
        .filter(WorkoutLog.date >= week_start)
        .filter(WorkoutLog.date <= week_end)
        .all()
    )

    total_sessions = len(workouts)
    total_minutes = sum(workout.duration_min for workout in workouts)
    sessions_by_type = dict(Counter(workout.workout_type for workout in workouts))

    return {
        "week_start": str(week_start),
        "week_end": str(week_end),
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "sessions_by_type": sessions_by_type,
    }


@router.get(
    "/exercise-distribution/body-part",
    response_model=List[ExerciseDistributionItem],
    summary="Exercise distribution by body part",
    description="Returns the number of exercises available for each body part in the exercise dataset."
)
def exercise_distribution_by_body_part(
    db: Session = Depends(get_db),
):
    return get_exercise_distribution_by_body_part(db)


@router.get(
    "/exercise-distribution/equipment",
    response_model=List[ExerciseDistributionItem],
    summary="Exercise distribution by equipment",
    description="Returns the number of exercises available for each equipment type in the exercise dataset."
)
def exercise_distribution_by_equipment(
    db: Session = Depends(get_db),
):
    return get_exercise_distribution_by_equipment(db)


@router.get(
    "/top-rated-exercises",
    response_model=List[ExerciseOut],
    summary="Top rated exercises",
    description="Returns the highest-rated exercises from the dataset, with optional filtering."
)
def top_rated_exercises(
    body_part: Optional[str] = Query(default=None, description="Filter by body part"),
    equipment: Optional[str] = Query(default=None, description="Filter by equipment"),
    difficulty: Optional[str] = Query(default=None, description="Filter by difficulty"),
    exercise_type: Optional[str] = Query(default=None, description="Filter by exercise type"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of exercises to return"),
    db: Session = Depends(get_db),
):
    return get_top_rated_exercises(
        db=db,
        body_part=body_part,
        equipment=equipment,
        difficulty=difficulty,
        exercise_type=exercise_type,
        limit=limit,
    )