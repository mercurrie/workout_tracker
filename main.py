import requests
import os
from datetime import datetime


APP_ID = os.environ.get("NE_APP_ID")
API_KEY = os.environ.get("NE_API_KEY")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
QUESTION = "Tell me what exercises you did: "
AGE = 28
GENDER = "male"
WEIGHT_KG = 120
HEIGHT_CM = 200
SHEET_ENDPOINT = os.environ.get("SHEET_API_ENDPOINT")
DATE = "%d/%m/%Y"
TIME = "%X"


def workout_data(user_workout: str):

    header = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY
    }

    params = {
        "query": user_workout,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    response = requests.post(url=EXERCISE_ENDPOINT, json=params, headers=header)
    response.raise_for_status()
    return response.json()


def post_to_spreadsheet(data):

    today_date = datetime.now().strftime(DATE)
    now_time = datetime.now().strftime(TIME)

    for exercise in data["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs)
        sheet_response.raise_for_status()


def workout_tracker():
    answer = input(QUESTION)

    result = workout_data(user_workout=answer)

    post_to_spreadsheet(data=result)


if __name__ == "__main__":
    workout_tracker()
