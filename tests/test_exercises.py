from app.models_exercises import Exercise


def seed_exercises_for_test(db_session):
    if db_session.query(Exercise).count() == 0:
        exercises = [
            Exercise(
                name="Bench Press",
                body_part="Chest",
                equipment="Barbell",
                target_muscle="Pectorals",
                difficulty="Intermediate",
                description="Compound chest exercise"
            ),
            Exercise(
                name="Shoulder Press",
                body_part="Shoulders",
                equipment="Dumbbell",
                target_muscle="Deltoids",
                difficulty="Intermediate",
                description="Overhead pressing movement"
            ),
            Exercise(
                name="Lat Pulldown",
                body_part="Back",
                equipment="Cable",
                target_muscle="Lats",
                difficulty="Beginner",
                description="Vertical pulling exercise"
            ),
        ]
        db_session.add_all(exercises)
        db_session.commit()


def test_list_exercises(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?limit=5")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_filter_exercises_by_name(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?q=Bench")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Bench" in exercise["name"] for exercise in data)


def test_filter_exercises_by_equipment(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?equipment=Dumbbell")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(exercise["equipment"] == "Dumbbell" for exercise in data)