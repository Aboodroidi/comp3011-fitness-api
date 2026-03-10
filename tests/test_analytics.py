def test_workout_streak_empty_database(client):
    response = client.get("/analytics/streak")

    assert response.status_code == 200
    data = response.json()
    assert "current_streak" in data
    assert "longest_streak" in data
    assert "total_workout_days" in data


def test_workout_streak_with_data(client):
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
        client.post("/workouts", json=workout)

    response = client.get("/analytics/streak")

    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] >= 1
    assert data["longest_streak"] >= 1
    assert data["total_workout_days"] == 3


def test_weekly_summary_requires_week_start(client):
    response = client.get("/analytics/weekly-summary")

    assert response.status_code == 422


def test_weekly_summary_returns_expected_shape(client):
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
        client.post("/workouts", json=workout)

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