import requests

BASE_URL = "https://insurance-api-736907218290.us-central1.run.app"

def calculate_payout(claim_amount: float, deductible: float) -> float:
    """Calculates the final insurance payout after the deductible."""
    return max(0, claim_amount - deductible)

import requests

# Use the Cloud Run URL we just deployed
BASE_URL = "https://insurance-api-736907218290.us-central1.run.app"

def create_user(first_name: str, last_name: str, phone_number: int, current_plan: str):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "current_plan": current_plan
    }
    # Notice the '/user' prefix to match your FastAPI @app.post("/user/create")
    response = requests.post(url=f"{BASE_URL}/user/create", json=payload)
    
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create user. Status: {response.status_code}"}

def get_user_data(user_id: str):
    # Notice the '/user' prefix to match your FastAPI @app.get("/user/{user_id}")
    response = requests.get(url=f"{BASE_URL}/user/{user_id}")
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"error": "User not found. Please check the ID."}
    else:
        return {"error": "Connection error with the database."}