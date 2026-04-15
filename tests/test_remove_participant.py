from src.app import activities


def test_remove_participant_success(client):
    email = "remove.me@mergington.edu"
    activities["Programming Class"]["participants"].append(email)

    response = client.delete(
        "/activities/Programming Class/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Programming Class"
    assert email not in activities["Programming Class"]["participants"]


def test_remove_participant_not_found_returns_404(client):
    response = client.delete(
        "/activities/Programming Class/participants",
        params={"email": "absent@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_remove_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": "anyone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_is_reflected_in_final_state(client):
    email = activities["Tennis Club"]["participants"][0]

    response = client.delete(
        "/activities/Tennis Club/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities["Tennis Club"]["participants"]
