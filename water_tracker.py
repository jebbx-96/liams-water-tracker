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

# 8 Plant growth stages (including Day 0 seed stage)
plant_images = [
    "images/stage0_seed.png", 
    "images/stage1_sprout.png", 
    "images/stage2_seedling.png", 
    "images/stage3_young_plant.png", 
    "images/stage4_flower_bush.png", 
    "images/stage5_small_tree.png", 
    "images/stage6_mini_forest.png", 
    "images/stage7_full_forest.png"
]

# Motivational message at halfway point
def get_motivation():
    if st.session_state.water_count == 4:
        return "Halfway there! You're doing great ❤️"
    elif st.session_state.water_count == WATER_GOAL:
        return "Good job, my love! 💖"
    return ""

def log_water():
    st.session_state.water_count += 1
    st.session_state.xp += XP_PER_CUP
    
    if st.session_state.water_count == WATER_GOAL:
        # Update plant growth dynamically per day
        st.session_state.plant_stage = min(st.session_state.day_count + 1, len(plant_images) - 1)
        st.session_state.day_count += 1
        
        if st.session_state.day_count == DAYS_TO_FOREST:
            st.session_state.message = "🌳 You've grown a full forest! Resetting..."
            reset_week()
        else:
            st.session_state.message = get_motivation()
    
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

# Streamlit UI - Enhanced Layout
st.set_page_config(page_title="Liam's Water Tracker", layout="wide")
st.title("🌊 Liam's Water Tracker 🌿")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Water Intake: {st.session_state.water_count}/{WATER_GOAL} cups")
    st.progress(st.session_state.water_count / WATER_GOAL)
    st.subheader(f"XP: {st.session_state.xp}")
    
    # Display motivation message
    motivation = get_motivation()
    if motivation:
        st.success(motivation)
    
    if st.button("💧 Log Water"):
        log_water()
    if st.button("🔄 New Day"):
        reset_day()

with col2:
    st.image(plant_images[st.session_state.plant_stage], caption="Your Growing Forest", use_container_width=True)
