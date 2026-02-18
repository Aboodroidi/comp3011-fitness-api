from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import SessionLocal
from .. import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _dates_sorted_unique(workouts: list[models.WorkoutLog]) -> list[str]:
    # Dates are stored as YYYY-MM-DD strings, so lexical sort works.
    return sorted({w.date for w in workouts})


@router.get("/streak")
def workout_streak(db: Session = Depends(get_db)):
    """
    Calculates:
    - current_streak: consecutive days up to the most recent workout date
    - longest_streak: max consecutive-day run in the dataset
    """
    workouts = db.execute(select(models.WorkoutLog)).scalars().all()
    dates = _dates_sorted_unique(workouts)

    if not dates:
        return {"current_streak": 0, "longest_streak": 0, "total_workout_days": 0}

    # Convert to day numbers via simple parsing (no timezone concerns)
    def to_ordinal(d: str) -> int:
        y, m, day = d.split("-")
        import datetime as dt
        return dt.date(int(y), int(m), int(day)).toordinal()

    ords = [to_ordinal(d) for d in dates]

    longest = 1
    current_run = 1
    best = 1

    for i in range(1, len(ords)):
        if ords[i] == ords[i - 1] + 1:
            current_run += 1
        else:
            best = max(best, current_run)
            current_run = 1
    best = max(best, current_run)
    longest = best

    # Current streak = run ending at last date
    current = 1
    for i in range(len(ords) - 1, 0, -1):
        if ords[i] == ords[i - 1] + 1:
            current += 1
        else:
            break

    return {
        "current_streak": current,
        "longest_streak": longest,
        "total_workout_days": len(dates),
        "most_recent_workout_date": dates[-1],
    }


@router.get("/weekly-summary")
def weekly_summary(
    week_start: str = Query(..., description="Week start date (YYYY-MM-DD). Monday recommended."),
    db: Session = Depends(get_db),
):
    """
    Returns totals for workouts whose date is in [week_start, week_start+6].
    """
    import datetime as dt

    y, m, d = week_start.split("-")
    start = dt.date(int(y), int(m), int(d))
    end = start + dt.timedelta(days=6)

    workouts = db.execute(select(models.WorkoutLog)).scalars().all()

    def parse_date(s: str) -> dt.date:
        yy, mm, dd = s.split("-")
        return dt.date(int(yy), int(mm), int(dd))

    week_workouts = []
    for w in workouts:
        wd = parse_date(w.date)
        if start <= wd <= end:
            week_workouts.append(w)

    total_sessions = len(week_workouts)
    total_minutes = sum(w.duration_min for w in week_workouts)

    by_type: dict[str, int] = {}
    for w in week_workouts:
        by_type[w.workout_type] = by_type.get(w.workout_type, 0) + 1

    return {
        "week_start": str(start),
        "week_end": str(end),
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "sessions_by_type": by_type,
    }