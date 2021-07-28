import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# NUTRIONIX API CONSTANTS
NUTRIONIX_KEY = os.environ.get("NUTRIONIX_KEY")
NUTRIONIX_ID = os.environ.get("NUTRIONIX_ID")
SHEETY_PWD = os.environ.get("SHEETY_PWD")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")


# OTHER CONSTANTS

GENDER = "male"
WEIGHT_KG = 77
HEIGHT_CM = 175
AGE = 26

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/20cfd2f330ee5730404d7f3f98d65486/myWorkouts/workouts"
sheet_user_name = "msantamaria3"
exercise_text = input("Please tell me which exercises you did: ")

# Nutrionix API headers
headers = {
    "x-app-id": NUTRIONIX_ID,
    "x-app-key": NUTRIONIX_KEY,
 }

# Nutrionix exercise parameters
exercise_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
# print(exercise_params)
# POST request to get exercise data from Nutrionix based on entered string, convert to json format
response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()

# get current date and time formatted
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheet API headers
sheet_headers = {
    "Authorization": f"Basic {SHEETY_TOKEN}",
}

# get column data from result exercise data (dictionary format)
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

# use sheety to post response on google docs tracker!
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs,  headers=headers, auth=HTTPBasicAuth(sheet_user_name, SHEETY_PWD))

    print(sheet_response.text)
