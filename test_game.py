import sys
import os
import json
from fastapi.testclient import TestClient

# Add parent directory to path to import api
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import app
from tools.user_database import UserDatabase

client = TestClient(app)
db = UserDatabase()

def test_game_flow():
    print("Testing Game Flow...")
    
    # 1. Register a test user
    import time
    unique_id = int(time.time())
    register_data = {
        "name": "Test User",
        "email": f"test{unique_id}@example.com",
        "password": "password123",
        "grade_level": "College Year 1"
    }
    # Try login first in case user exists
    login_response = client.post("/auth/login", json={"email": register_data["email"], "password": register_data["password"]})
    
    if login_response.status_code == 200:
        user_id = login_response.json()["user"]["id"]
        print(f"User logged in: {user_id}")
    else:
        reg_response = client.post("/auth/register", json=register_data)
        if reg_response.status_code == 200:
            user_id = reg_response.json()["user"]["user_id"]
            print(f"User registered: {user_id}")
        else:
            print(f"Registration failed: {reg_response.text}")
            return

    # 2. Get Current Game
    print("\nFetching current game...")
    game_response = client.get(f"/game/current?user_id={user_id}")
    if game_response.status_code != 200:
        print(f"Failed to get game: {game_response.text}")
        return
    
    game_data = game_response.json()
    print(f"Game Data: {json.dumps(game_data, indent=2)}")
    
    if game_data["played"]:
        print("User already played this window. Waiting for next window or testing replay prevention.")
    
    window_id = game_data["window_id"]
    
    # 3. Submit Answer (Correct)
    # We need to know the correct answer. In our mock service, we can cheat or just guess.
    # For testing, let's try to submit a wrong answer first
    print("\nSubmitting wrong answer...")
    submit_response = client.post("/game/submit", json={
        "user_id": user_id,
        "window_id": window_id,
        "answer": "Wrong Answer"
    })
    
    if submit_response.status_code == 200:
        result = submit_response.json()
        print(f"Submission Result: {json.dumps(result, indent=2)}")
    else:
        # It might fail if we already played
        print(f"Submission failed: {submit_response.text}")

    # 4. Verify Replay Prevention
    print("\nVerifying replay prevention...")
    replay_response = client.post("/game/submit", json={
        "user_id": user_id,
        "window_id": window_id,
        "answer": "Another Answer"
    })
    
    if replay_response.status_code == 400:
        print("Replay prevention working: " + replay_response.json()["detail"])
    else:
        print(f"Replay prevention failed or unexpected status: {replay_response.status_code}")

if __name__ == "__main__":
    test_game_flow()
