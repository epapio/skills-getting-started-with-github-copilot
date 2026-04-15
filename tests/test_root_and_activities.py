from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == set(activities.keys())

    sample_activity = data["Chess Club"]
    assert "description" in sample_activity
    assert "schedule" in sample_activity
    assert "max_participants" in sample_activity
    assert "participants" in sample_activity
    assert isinstance(sample_activity["participants"], list)
