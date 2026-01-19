import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
import os

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide"
)

load_dotenv()
client = Groq(api_key=os.getenv("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"))

# -------------------- STYLES --------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.metric-card {
    background: linear-gradient(135deg, #111827, #1f2933);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
.section {
    background-color: #020617;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- PROMPT --------------------
def fitness_prompt(user):
    return f"""
You are a certified fitness trainer and nutritionist.

User Profile:
Age: {user['age']}
Gender: {user['gender']}
Height: {user['height']} cm
Weight: {user['weight']} kg
Goal: {user['goal']}
Activity Level: {user['activity']}

Tasks:
1. Create a 7-day workout plan with sets & reps
2. Create a daily diet plan (Indian friendly)
3. Mention approximate daily calories
4. Give 3 fitness tips
5. Keep advice safe and realistic

Use clear headings and bullet points.
Do NOT give medical advice.
"""

# -------------------- AI FUNCTION --------------------
def generate_fitness_plan(user_data):
    prompt = fitness_prompt(user_data)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1
    )

    return response.choices[0].message.content

# -------------------- SESSION INIT --------------------
if "progress" not in st.session_state:
    st.session_state.progress = pd.DataFrame(columns=["Week", "Weight"])

# -------------------- HEADER --------------------
st.title("💪 AI Fitness Coach")
st.caption("Modern AI-powered workout & diet planner with progress tracking")

# -------------------- SIDEBAR --------------------
st.sidebar.header("👤 Your Profile")

age = st.sidebar.number_input("Age", 18, 60, 22)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", 150, 200, 170)
weight = st.sidebar.number_input("Weight (kg)", 40, 150, 75)
goal = st.sidebar.selectbox("Goal", ["Fat Loss", "Muscle Gain"])
activity = st.sidebar.selectbox("Activity Level", ["Low", "Medium", "High"])

user_data = {
    "age": age,
    "gender": gender,
    "height": height,
    "weight": weight,
    "goal": goal,
    "activity": activity
}

# -------------------- METRICS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric-card'>🎯<br><b>Goal</b><br>{goal}</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric-card'>⚖️<br><b>Weight</b><br>{weight} kg</div>", unsafe_allow_html=True)

with col3:
    st.markdown(
        f"<div class='metric-card'>📅<br><b>Weeks Tracked</b><br>{len(st.session_state.progress)}</div>",
        unsafe_allow_html=True
    )

# -------------------- AI PLAN --------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🤖 AI-Generated Fitness Plan")

if st.button("🚀 Generate AI Plan"):
    with st.spinner("AI is creating your personalized fitness plan..."):
        st.session_state.plan = generate_fitness_plan(user_data)

if "plan" in st.session_state:
    st.markdown(st.session_state.plan)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- PROGRESS TRACKING --------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📈 Progress Tracking")

new_weight = st.number_input("Update Weekly Weight (kg)", value=weight)
week = len(st.session_state.progress) + 1

if st.button("➕ Add Progress"):
    new_row = {"Week": week, "Weight": new_weight}
    st.session_state.progress = pd.concat(
        [st.session_state.progress, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("Progress added successfully!")

if not st.session_state.progress.empty:
    st.dataframe(st.session_state.progress, use_container_width=True)

    fig = px.line(
        st.session_state.progress,
        x="Week",
        y="Weight",
        markers=True,
        title="Weight Progress Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.caption("🚀 Built with Streamlit + Groq AI | Final-Year / Resume-Ready Project")
