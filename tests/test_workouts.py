from app.models_exercises import Exercise


def seed_exercises_for_workout_tests(db_session):
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
    return exercises


def test_workouts_require_authentication(client):
    response = client.get("/workouts")
    assert response.status_code == 401


def test_create_workout(client, auth_headers):
    payload = {
        "date": "2026-03-07",
        "workout_type": "Push",
        "duration_min": 60,
        "notes": "Chest and shoulders",
        "exercises": []
    }

    response = client.post("/workouts", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["workout_type"] == "Push"
    assert data["duration_min"] == 60
    assert "id" in data
    assert data["exercises"] == []


def test_create_workout_with_exercises(client, db_session, auth_headers):
    exercises = seed_exercises_for_workout_tests(db_session)

    payload = {
        "date": "2026-03-07",
        "workout_type": "Push",
        "duration_min": 70,
        "notes": "Push session with tracked lifts",
        "exercises": [
            {
                "exercise_id": exercises[0].id,
                "sets": 4,
                "reps": 10,
                "weight_kg": 60
            },
            {
                "exercise_id": exercises[1].id,
                "sets": 3,
                "reps": 8,
                "weight_kg": 100
            }
        ]
    }

    response = client.post("/workouts", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert len(data["exercises"]) == 2
    assert data["exercises"][0]["sets"] == 4
    assert data["exercises"][0]["reps"] == 10


def test_list_workouts(client, auth_headers):
    payload = {
        "date": "2026-03-08",
        "workout_type": "Pull",
        "duration_min": 50,
        "notes": "Back session",
        "exercises": []
    }
    client.post("/workouts", json=payload, headers=auth_headers)

    response = client.get("/workouts", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_workout_by_id(client, auth_headers):
    payload = {
        "date": "2026-03-09",
        "workout_type": "Legs",
        "duration_min": 70,
        "notes": "Heavy leg day",
        "exercises": []
    }
    create_response = client.post("/workouts", json=payload, headers=auth_headers)
    workout_id = create_response.json()["id"]

    response = client.get(f"/workouts/{workout_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workout_id
    assert data["workout_type"] == "Legs"


def test_get_workout_invalid_id_returns_404(client, auth_headers):
    response = client.get("/workouts/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_update_workout(client, db_session, auth_headers):
    exercises = seed_exercises_for_workout_tests(db_session)

    payload = {
        "date": "2026-03-10",
        "workout_type": "Cardio",
        "duration_min": 30,
        "notes": "Treadmill",
        "exercises": []
    }
    create_response = client.post("/workouts", json=payload, headers=auth_headers)
    workout_id = create_response.json()["id"]

    update_payload = {
        "duration_min": 45,
        "notes": "Treadmill and bike",
        "exercises": [
            {
                "exercise_id": exercises[2].id,
                "sets": 3,
                "reps": 12,
                "weight_kg": 0
            }
        ]
    }

    response = client.put(f"/workouts/{workout_id}", json=update_payload, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["duration_min"] == 45
    assert data["notes"] == "Treadmill and bike"
    assert len(data["exercises"]) == 1
    assert data["exercises"][0]["exercise_id"] == exercises[2].id


def test_update_workout_invalid_id_returns_404(client, auth_headers):
    update_payload = {
        "duration_min": 45
    }

    response = client.put("/workouts/99999", json=update_payload, headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_delete_workout(client, auth_headers):
    payload = {
        "date": "2026-03-11",
        "workout_type": "Upper Body",
        "duration_min": 55,
        "notes": "Mixed session",
        "exercises": []
    }
    create_response = client.post("/workouts", json=payload, headers=auth_headers)
    workout_id = create_response.json()["id"]

    delete_response = client.delete(f"/workouts/{workout_id}", headers=auth_headers)

    assert delete_response.status_code == 204

    get_response = client.get(f"/workouts/{workout_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_workout_invalid_id_returns_404(client, auth_headers):
    response = client.delete("/workouts/99999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}


def test_create_workout_invalid_input_returns_422(client, auth_headers):
    payload = {
        "date": "not-a-date",
        "workout_type": "",
        "duration_min": -5,
        "notes": "Invalid workout",
        "exercises": []
    }

    response = client.post("/workouts", json=payload, headers=auth_headers)

    assert response.status_code == 422


def test_suggest_workout_plan(client, db_session):
    seed_exercises_for_workout_tests(db_session)

    response = client.get("/workouts/suggest-plan?goal=strength&days=3")

    assert response.status_code == 200
    data = response.json()

    assert data["goal"] == "strength"
    assert data["days"] == 3
    assert "plan" in data
    assert len(data["plan"]) == 3
    assert "focus" in data["plan"][0]
    assert "exercises" in data["plan"][0]


def test_user_only_sees_own_workouts(client):
    user1 = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "StrongPass123"
    }
    user2 = {
        "username": "user2",
        "email": "user2@example.com",
        "password": "StrongPass123"
    }

    client.post("/auth/register", json=user1)
    client.post("/auth/register", json=user2)

    login1 = client.post("/auth/login", json={"username": "user1", "password": "StrongPass123"})
    login2 = client.post("/auth/login", json={"username": "user2", "password": "StrongPass123"})

    headers1 = {"Authorization": f"Bearer {login1.json()['access_token']}"}
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    payload1 = {
        "date": "2026-03-12",
        "workout_type": "Push",
        "duration_min": 60,
        "notes": "User 1 workout",
        "exercises": []
    }
    payload2 = {
        "date": "2026-03-13",
        "workout_type": "Legs",
        "duration_min": 75,
        "notes": "User 2 workout",
        "exercises": []
    }

    client.post("/workouts", json=payload1, headers=headers1)
    client.post("/workouts", json=payload2, headers=headers2)

    response1 = client.get("/workouts", headers=headers1)
    response2 = client.get("/workouts", headers=headers2)

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    assert len(data1) == 1
    assert len(data2) == 1
    assert data1[0]["notes"] == "User 1 workout"
    assert data2[0]["notes"] == "User 2 workout"