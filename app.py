import streamlit as st
import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Fitness Trainer", page_icon="💪")

st.set_page_config(page_title="AI Fitness Trainer", page_icon="💪")

st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>AI Personal Fitness Trainer</h1>
<p style='text-align: center;'>Create personalized workout plans instantly</p>
""", unsafe_allow_html=True)

st.markdown("### 🧾 Enter Your Details")

name = st.text_input("Your Name")
goal = st.text_input("Fitness Goal")

level = st.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"]
)

equipment = st.text_input("Available Equipment")

time = st.slider("Workout Time (minutes)", 10, 120, 30)

days = st.slider("Days per week", 1, 7, 3)

focus = st.multiselect(
    "Focus Areas",
    ["Full Body", "Upper Body", "Lower Body", "Core", "Cardio"]
)


def generate_workout(goal, level, equipment, time, days, focus):

    
    fallback = f"""
Workout Plan

Goal: {goal}
Level: {level}
Equipment: {equipment}
Time: {time} minutes
Days per week: {days}
Focus: {", ".join(focus)}

Day 1 - Full Body
Push-ups - 3x12
Squats - 3x10
Plank - 3x30 sec

Day 2 - Cardio
Jump rope - 10 min
Running - 15 min

Day 3 - Strength
Dumbbell curls - 3x10
Lunges - 3x12
"""

  
    if not API_KEY:
        return fallback

    url = "https://api.openai.com/v1/chat/completions"

    prompt = f"""
    You are a professional personal trainer.

    Create a personalized weekly workout plan.

    User Info:
    Goal: {goal}
    Level: {level}
    Equipment: {equipment}
    Time: {time} minutes
    Days per week: {days}
    Focus areas: {", ".join(focus)}

    IMPORTANT:
    - Create EXACTLY {days} days (no more, no less)
    - Label each day clearly (Day 1, Day 2, etc.)
    - Each day should include 3–5 exercises
    - Include sets and reps

    FORMAT EXACTLY LIKE THIS:

    ### Day 1
    - Exercise - Sets x Reps

    ### Day 2
    - Exercise - Sets x Reps

    Repeat until Day {days}.

    Make it clean and easy to read.
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return fallback

    except:
        return fallback



generate = st.button("Generate Workout Plan")

st.markdown("---")

if generate:

    if goal == "":
        st.warning("Please enter your fitness goal!")
    else:
        plan = generate_workout(goal, level, equipment, time, days, focus)

        # --- SUMMARY CARD ---
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg, #E8F6F3, #D6EAF8);
        padding:20px;
        border-radius:12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
        <b>Goal:</b> {goal}<br>
        <b>Level:</b> {level}<br>
        <b>Equipment:</b> {equipment}<br>
        <b>Time:</b> {time} minutes<br>
        <b>Days:</b> {days}<br>
        <b>Focus:</b> {", ".join(focus)}
        </div>
        """, unsafe_allow_html=True)

     
        st.info(f"{name}, here is your personalized workout plan!")

     
        st.markdown("### 🏋️ Weekly Workout Plan")
        st.markdown(plan)

        st.success("Workout generated successfully!")


        import os
        os.makedirs("results", exist_ok=True)

        with open("results/workouts.txt", "a") as f:
            f.write(plan + "\n\n")