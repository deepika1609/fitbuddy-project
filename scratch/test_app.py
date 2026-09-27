import sys
import os
from fastapi.testclient import TestClient

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import init_db, save_user, save_plan, get_user, get_original_plan, delete_user

def run_tests():
    print("--- 1. Testing Database Setup & Operations ---")
    init_db()
    
    # Clean up test user 999 if exists
    delete_user(999)
    
    save_user(
        user_id=999,
        name="Test User",
        age=30,
        weight=75.5,
        goal="muscle gain",
        intensity="High"
    )
    user = get_user(999)
    assert user is not None, "Failed to fetch saved user!"
    assert user.name == "Test User"
    print("[PASS] User creation and retrieval succeeded.")

    save_plan(999, "Day 1: Test Plan Content")
    plan = get_original_plan(999)
    assert plan == "Day 1: Test Plan Content", "Failed to fetch saved plan!"
    print("[PASS] Plan saving and retrieval succeeded.")

    print("\n--- 2. Testing FastAPI Routes via TestClient ---")
    client = TestClient(app)

    # Test GET /
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "FitBuddy" in res_home.text
    print("[PASS] Home page GET / status code 200 OK.")

    # Test POST /generate-workout
    res_gen = client.post("/generate-workout", data={
        "username": "Alex Doe",
        "user_id": "102",
        "age": "28",
        "weight": "68.0",
        "goal": "weight loss",
        "intensity": "Medium"
    })
    assert res_gen.status_code == 200
    assert "Your Personalized Workout Plan" in res_gen.text
    print("[PASS] POST /generate-workout status code 200 OK.")

    # Test POST /submit-feedback
    res_feed = client.post("/submit-feedback", data={
        "user_id": "102",
        "feedback": "Add more cardio on Friday"
    })
    assert res_feed.status_code == 200
    assert "updated based on your feedback" in res_feed.text.lower()
    print("[PASS] POST /submit-feedback status code 200 OK.")

    # Test GET /view-all-users
    res_admin = client.get("/view-all-users")
    assert res_admin.status_code == 200
    assert "Alex Doe" in res_admin.text
    print("[PASS] Admin view GET /view-all-users status code 200 OK.")

    # Test API JSON Endpoint /generate-workout/gemini
    res_api = client.post("/generate-workout/gemini", json={
        "goal": "flexibility",
        "intensity": "Low"
    })
    assert res_api.status_code == 200
    json_data = res_api.json()
    assert "workout_plan" in json_data
    print("[PASS] API /generate-workout/gemini status code 200 OK.")

    # Clean up test user
    delete_user(999)
    delete_user(102)

    print("\nALL UNIT & INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
