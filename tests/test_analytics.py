from app.models_exercises import Exercise


def test_workout_streak_empty_database(client):
    response = client.get("/analytics/streak")

    assert response.status_code == 200
    data = response.json()
    assert "current_streak" in data
    assert "longest_streak" in data
    assert "total_workout_days" in data


def test_workout_streak_with_data(client, auth_headers):
    workouts = [
        {
            "date": "2026-03-01",
            "workout_type": "Push",
            "duration_min": 60,
            "notes": "Day 1"
        },
        {
            "date": "2026-03-02",
            "workout_type": "Pull",
            "duration_min": 50,
            "notes": "Day 2"
        },
        {
            "date": "2026-03-03",
            "workout_type": "Legs",
            "duration_min": 70,
            "notes": "Day 3"
        }
    ]

    for workout in workouts:
        client.post("/workouts", json=workout, headers=auth_headers)

    response = client.get("/analytics/streak")

    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] >= 1
    assert data["longest_streak"] >= 1
    assert data["total_workout_days"] == 3


def test_weekly_summary_requires_week_start(client):
    response = client.get("/analytics/weekly-summary")

    assert response.status_code == 422


def test_weekly_summary_returns_expected_shape(client, auth_headers):
    workouts = [
        {
            "date": "2026-03-01",
            "workout_type": "Push",
            "duration_min": 60,
            "notes": "Session 1"
        },
        {
            "date": "2026-03-02",
            "workout_type": "Cardio",
            "duration_min": 40,
            "notes": "Session 2"
        }
    ]

    for workout in workouts:
        client.post("/workouts", json=workout, headers=auth_headers)

    response = client.get("/analytics/weekly-summary?week_start=2026-03-01")

    assert response.status_code == 200
    data = response.json()
    assert "week_start" in data
    assert "week_end" in data
    assert "total_sessions" in data
    assert "total_minutes" in data
    assert "sessions_by_type" in data


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def seed_exercise_distribution_data(db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Chest press",
            rating=8.5,
            rating_desc="Very good"
        ),
        Exercise(
            name="Incline Dumbbell Press",
            body_part="Chest",
            equipment="Dumbbell",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Upper chest press",
            rating=7.2,
            rating_desc="Good"
        ),
        Exercise(
            name="Plank",
            body_part="Abdominals",
            equipment="Body Only",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Core stability exercise",
            rating=9.1,
            rating_desc="Excellent"
        ),
    ]
    db_session.add_all(exercises)
    db_session.commit()


def test_exercise_distribution_by_body_part(client, db_session):
    seed_exercise_distribution_data(db_session)

    response = client.get("/analytics/exercise-distribution/body-part")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2

    categories = {item["category"]: item["count"] for item in data}
    assert categories["Chest"] == 2
    assert categories["Abdominals"] == 1


def test_exercise_distribution_by_equipment(client, db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Chest press",
            rating=8.5,
            rating_desc="Very good"
        ),
        Exercise(
            name="Back Squat",
            body_part="Quadriceps",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Leg exercise",
            rating=8.8,
            rating_desc="Excellent"
        ),
        Exercise(
            name="Plank",
            body_part="Abdominals",
            equipment="Body Only",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Core stability",
            rating=9.1,
            rating_desc="Excellent"
        ),
    ]
    db_session.add_all(exercises)
    db_session.commit()

    response = client.get("/analytics/exercise-distribution/equipment")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2

    categories = {item["category"]: item["count"] for item in data}
    assert categories["Barbell"] == 2
    assert categories["Body Only"] == 1


def test_top_rated_exercises_returns_highest_first(client, db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Chest press",
            rating=8.5,
            rating_desc="Very good"
        ),
        Exercise(
            name="Incline Dumbbell Press",
            body_part="Chest",
            equipment="Dumbbell",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Upper chest press",
            rating=7.2,
            rating_desc="Good"
        ),
        Exercise(
            name="Plank",
            body_part="Abdominals",
            equipment="Body Only",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Core stability",
            rating=9.1,
            rating_desc="Excellent"
        ),
    ]
    db_session.add_all(exercises)
    db_session.commit()

    response = client.get("/analytics/top-rated-exercises?limit=2")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Plank"
    assert data[1]["name"] == "Bench Press"


def test_top_rated_exercises_with_filter(client, db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Chest press",
            rating=8.5,
            rating_desc="Very good"
        ),
        Exercise(
            name="Incline Dumbbell Press",
            body_part="Chest",
            equipment="Dumbbell",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Upper chest press",
            rating=7.2,
            rating_desc="Good"
        ),
        Exercise(
            name="Plank",
            body_part="Abdominals",
            equipment="Body Only",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Core stability",
            rating=9.1,
            rating_desc="Excellent"
        ),
    ]
    db_session.add_all(exercises)
    db_session.commit()

    response = client.get("/analytics/top-rated-exercises?body_part=Chest&limit=5")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert all(item["body_part"] == "Chest" for item in data)
    assert data[0]["rating"] >= data[1]["rating"]