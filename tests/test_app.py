import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities before each test
    for activity in activities.values():
        if isinstance(activity["participants"], list):
            activity["participants"] = activity["participants"][:2]  # Reset to initial 2 participants

client = TestClient(app)

def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"].startswith("Signed up")

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
