from src.app import activities


def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_email_returns_400(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "someone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_same_email_is_idempotent_from_client_perspective(client):
    email = "repeat.student@mergington.edu"

    first = client.post("/activities/Art Studio/signup", params={"email": email})
    second = client.post("/activities/Art Studio/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert activities["Art Studio"]["participants"].count(email) == 1
