from collections import Counter
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import WorkoutLog
from app.schemas import WeeklySummaryOut, WorkoutStreakOut

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def parse_workout_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


@router.get(
    "/streak",
    response_model=WorkoutStreakOut,
    summary="Workout Streak",
    description="Returns the current workout streak, longest workout streak, and total number of distinct workout days."
)
def get_workout_streak(db: Session = Depends(get_db)):
    workouts = db.query(WorkoutLog).order_by(WorkoutLog.date.asc()).all()

    if not workouts:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_workout_days": 0,
        }

    unique_dates = sorted({parse_workout_date(w.date) for w in workouts})
    total_workout_days = len(unique_dates)

    longest_streak = 1
    current_run = 1

    for i in range(1, len(unique_dates)):
        prev_day = unique_dates[i - 1]
        curr_day = unique_dates[i]

        if curr_day == prev_day + timedelta(days=1):
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 1

    most_recent = unique_dates[-1]
    current_streak = 1

    for i in range(len(unique_dates) - 2, -1, -1):
        expected_day = most_recent - timedelta(days=1)
        if unique_dates[i] == expected_day:
            current_streak += 1
            most_recent = unique_dates[i]
        else:
            break

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_workout_days": total_workout_days,
    }


@router.get(
    "/weekly-summary",
    response_model=WeeklySummaryOut,
    summary="Weekly Summary",
    description="Returns the total number of workout sessions, total training minutes, and session counts by workout type for the selected week."
)
def get_weekly_summary(
    week_start: date = Query(..., description="Start date of the week in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    week_end = week_start + timedelta(days=6)

    workouts = db.query(WorkoutLog).all()

    filtered_workouts = []
    for workout in workouts:
        workout_date = parse_workout_date(workout.date)
        if week_start <= workout_date <= week_end:
            filtered_workouts.append(workout)

    total_sessions = len(filtered_workouts)
    total_minutes = sum(w.duration_min for w in filtered_workouts)
    sessions_by_type = dict(Counter(w.workout_type for w in filtered_workouts))

    return {
        "week_start": week_start,
        "week_end": week_end,
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "sessions_by_type": sessions_by_type,
    }