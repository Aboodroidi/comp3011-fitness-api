from app.models_exercises import Exercise


def seed_exercises_for_test(db_session):
    exercises = [
        Exercise(
            name="Bench Press",
            body_part="Chest",
            equipment="Barbell",
            difficulty="Intermediate",
            exercise_type="Strength",
            description="Compound chest exercise",
            rating=8.5,
            rating_desc="Very good"
        ),
        Exercise(
            name="Incline Dumbbell Press",
            body_part="Chest",
            equipment="Dumbbell",
            difficulty="Beginner",
            exercise_type="Strength",
            description="Upper chest pressing movement",
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


def test_list_exercises(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?limit=5")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_search_exercises_by_keyword(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?q=Bench")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Bench" in exercise["name"] for exercise in data)


def test_filter_exercises_by_body_part(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?body_part=Chest")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(exercise["body_part"] == "Chest" for exercise in data)


def test_filter_exercises_by_equipment(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?equipment=Dumbbell")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert all(exercise["equipment"] == "Dumbbell" for exercise in data)


def test_filter_exercises_by_difficulty(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?difficulty=Beginner")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(exercise["difficulty"] == "Beginner" for exercise in data)


def test_filter_exercises_by_exercise_type(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?exercise_type=Strength")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(exercise["exercise_type"] == "Strength" for exercise in data)


def test_sort_exercises_by_rating_high_to_low(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?sort_by=rating_high_low")

    assert response.status_code == 200
    data = response.json()
    ratings = [exercise["rating"] for exercise in data]
    assert ratings == sorted(ratings, reverse=True)


def test_sort_exercises_by_rating_low_to_high(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?sort_by=rating_low_high")

    assert response.status_code == 200
    data = response.json()
    ratings = [exercise["rating"] for exercise in data]
    assert ratings == sorted(ratings)


def test_recommended_sort_returns_highest_rated_first(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises?sort_by=recommended")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Plank"


def test_get_exercise_by_id(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises/1")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_get_exercise_filters(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises/meta/filters")

    assert response.status_code == 200
    data = response.json()
    assert "body_parts" in data
    assert "equipment" in data
    assert "difficulty" in data
    assert "exercise_types" in data
    assert "total_exercises" in data


def test_recommend_exercises(client, db_session):
    seed_exercises_for_test(db_session)

    response = client.get("/exercises/recommend?body_part=Chest&limit=2")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert all(item["body_part"] == "Chest" for item in data)
    assert data[0]["rating"] >= data[1]["rating"]