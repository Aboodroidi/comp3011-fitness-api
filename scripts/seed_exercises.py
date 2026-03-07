import csv
from pathlib import Path

from app.db import SessionLocal
from app.models_exercises import Exercise


DATA_FILE = Path("data/gym_exercises.csv")


def seed(db):
    inserted = 0

    # avoid inserting duplicates if script runs more than once
    if db.query(Exercise).count() > 0:
        return 0

    with DATA_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get("Exercise_Name")
            if not name:
                continue

            exercise = Exercise(
                name=name.strip(),
                body_part=(row.get("muscle_gp") or "").strip() or None,
                equipment=(row.get("Equipment") or "").strip() or None,
                target_muscle=(row.get("muscle_gp_details") or "").strip() or None,
                difficulty=(row.get("Rating") or "").strip() or None,
                description=(row.get("Description") or "").strip() or None,
            )

            db.add(exercise)
            inserted += 1

    db.commit()
    return inserted


def main():
    db = SessionLocal()
    try:
        inserted = seed(db)
        print(f"Inserted {inserted} exercises.")
    finally:
        db.close()


if __name__ == "__main__":
    main()