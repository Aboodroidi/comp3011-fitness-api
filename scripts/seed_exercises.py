import csv
from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models_exercises import Exercise


DATA_FILE = Path("data/megaGymDataset.csv")


def clean_value(value):
    if value is None:
        return None

    value = str(value).strip()
    return value if value else None


def clean_float(value):
    value = clean_value(value)
    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def seed(db):
    inserted = 0

    # Clear existing exercise rows so the script can be rerun safely
    db.query(Exercise).delete()
    db.commit()

    with DATA_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = clean_value(row.get("Title"))
            if not name:
                continue

            exercise = Exercise(
                name=name,
                body_part=clean_value(row.get("BodyPart")),
                equipment=clean_value(row.get("Equipment")),
                difficulty=clean_value(row.get("Level")),
                exercise_type=clean_value(row.get("Type")),
                description=clean_value(row.get("Desc")),
                rating=clean_float(row.get("Rating")),
                rating_desc=clean_value(row.get("RatingDesc")),
            )

            db.add(exercise)
            inserted += 1

    db.commit()
    return inserted


def main():
    # Create tables first if they do not exist yet
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        inserted = seed(db)
        print(f"Inserted {inserted} exercises.")
    finally:
        db.close()


if __name__ == "__main__":
    main()