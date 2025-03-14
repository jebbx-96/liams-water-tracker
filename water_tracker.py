import streamlit as st
import time

# Initial stats
WATER_GOAL = 8
XP_PER_CUP = 5
DAYS_TO_FOREST = 7

if "water_count" not in st.session_state:
    st.session_state.water_count = 0
    st.session_state.xp = 0
    st.session_state.day_count = 0
    st.session_state.plant_stage = 0

# Plant growth stages
plant_images = ["🌱", "🌿", "🌳"]

def log_water():
    if st.session_state.water_count < WATER_GOAL:
        st.session_state.water_count += 1
        st.session_state.xp += XP_PER_CUP
        
        if st.session_state.water_count == WATER_GOAL:
            st.session_state.plant_stage = min(st.session_state.plant_stage + 1, 2)  # Progress plant stage
            st.session_state.day_count += 1
            st.session_state.message = "Good job, my love! 💖"
            
            if st.session_state.day_count == DAYS_TO_FOREST:
                st.session_state.message = "🌳 You've grown a full forest! Resetting..."
                reset_week()
    
        time.sleep(0.2)
        st.rerun()

def reset_day():
    st.session_state.water_count = 0
    st.session_state.message = ""
    st.rerun()

def reset_week():
    st.session_state.xp = 0
    st.session_state.day_count = 0
    st.session_state.plant_stage = 0
    reset_day()

# Streamlit UI
st.title("Liam's Water Tracker")

st.subheader(f"Water Intake: {st.session_state.water_count}/{WATER_GOAL} cups")
st.progress(st.session_state.water_count / WATER_GOAL)

st.subheader(f"XP: {st.session_state.xp}")

st.markdown(f"## {plant_images[st.session_state.plant_stage]}")

if "message" in st.session_state and st.session_state.message:
    st.success(st.session_state.message)

if st.button("💧 Log Water"):
    log_water()

if st.button("🔄 New Day"):
    reset_day()
