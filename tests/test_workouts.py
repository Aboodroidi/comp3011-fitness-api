from app.models_exercises import Exercise


def test_create_workout(client):
    payload = {
        "date": "2026-03-07",
        "workout_type": "Push",
        "duration_min": 60,
        "notes": "Chest and shoulders"
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["workout_type"] == "Push"
    assert data["duration_min"] == 60
    assert "id" in data


def test_list_workouts(client):
    payload = {
        "date": "2026-03-08",
        "workout_type": "Pull",
        "duration_min": 50,
        "notes": "Back session"
    }
    client.post("/workouts", json=payload)

    response = client.get("/workouts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_workout_by_id(client):
    payload = {
        "date": "2026-03-09",
        "workout_type": "Legs",
        "duration_min": 70,
        "notes": "Heavy leg day"
    }
    create_response = client.post("/workouts", json=payload)
    workout_id = create_response.json()["id"]

    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_id
    assert data["workout_type"] == "Legs"


def test_get_workout_invalid_id_returns_404(client):
    response = client.get("/workouts/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_update_workout(client):
    payload = {
        "date": "2026-03-10",
        "workout_type": "Cardio",
        "duration_min": 30,
        "notes": "Treadmill"
    }
    create_response = client.post("/workouts", json=payload)
    workout_id = create_response.json()["id"]

    update_payload = {
        "duration_min": 45,
        "notes": "Treadmill and bike"
    }

    response = client.put(f"/workouts/{workout_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["duration_min"] == 45
    assert data["notes"] == "Treadmill and bike"


def test_update_workout_invalid_id_returns_404(client):
    update_payload = {
        "duration_min": 45
    }

    response = client.put("/workouts/99999", json=update_payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_delete_workout(client):
    payload = {
        "date": "2026-03-11",
        "workout_type": "Upper Body",
        "duration_min": 55,
        "notes": "Mixed session"
    }
    create_response = client.post("/workouts", json=payload)
    workout_id = create_response.json()["id"]

    delete_response = client.delete(f"/workouts/{workout_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/workouts/{workout_id}")
    assert get_response.status_code == 404


def test_delete_workout_invalid_id_returns_404(client):
    response = client.delete("/workouts/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_create_workout_invalid_input_returns_422(client):
    payload = {
        "date": "not-a-date",
        "workout_type": "",
        "duration_min": -5,
        "notes": "Invalid workout"
    }

    response = client.post("/workouts", json=payload)

    assert response.status_code == 422


def test_suggest_workout_plan(client, db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Chest exercise",
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
            name="Pull-Up",
            body_part="Lats",
            equipment="Body Only",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Back exercise",
            rating=9.0,
            rating_desc="Excellent"
        ),
    ]
    db_session.add_all(exercises)
    db_session.commit()

    response = client.get("/workouts/suggest-plan?goal=strength&days=3")

    assert response.status_code == 200
    data = response.json()

    assert data["goal"] == "strength"
    assert data["days"] == 3
    assert "plan" in data
    assert len(data["plan"]) == 3
    assert "focus" in data["plan"][0]
    assert "exercises" in data["plan"][0]