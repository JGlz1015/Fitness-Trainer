import os
import requests
from dotenv import load_dotenv

print("Program started")

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def generate_workout(goal, level, equipment, time):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a certified personal trainer.

    Create a structured weekly workout plan.

    User Details:
    Goal: {goal}
    Experience Level: {level}
    Equipment: {equipment}
    Workout Time: {time} minutes

    Format the output clearly like this:

    Day 1 - [Muscle Group]
    Exercise - Sets x Reps

    Rules:
    - Include 3–5 workout days
    - Include exercise names
    - Include sets and reps
    - Balance muscle groups
    - Keep it realistic for the user level
    """

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()
    print(result) 

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"API Error: {result['error']['message']}"


# User input
goal = input("Enter your fitness goal: ")
level = input("Enter your experience level: ")
equipment = input("Available equipment: ")
time = input("Workout time (minutes): ")

plan = generate_workout(goal, level, equipment, time)

print("\n=== Your Workout Plan ===\n")
print(plan)

import os

os.makedirs("results", exist_ok=True)

with open("results/workouts.txt", "a") as f:
    f.write(plan + "\n\n")

