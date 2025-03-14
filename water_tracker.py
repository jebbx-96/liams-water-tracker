import streamlit as st
import time
import random

# Initial stats
WATER_GOAL = 8
STAMINA_PER_CUP = 5
DAYS_TO_FOREST = 8

if "water_count" not in st.session_state:
    st.session_state.water_count = 0
    st.session_state.stamina = 0
    st.session_state.day_count = 0
    st.session_state.plant_stage = 0
    st.session_state.overflow = False
    st.session_state.boss_battle = False

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

# Motivational messages for quest progression
def get_motivation():
    if st.session_state.water_count == 4:
        return "Halfway there, warrior! You're gaining strength ❤️"
    elif st.session_state.water_count == WATER_GOAL:
        return "Your stamina is at full power! ⚡💖"
    return ""

def log_water():
    st.session_state.water_count += 1
    st.session_state.stamina += STAMINA_PER_CUP
    
    if st.session_state.water_count > WATER_GOAL:
        st.session_state.overflow = True  # Trigger XP overflow event
    
    # Ensure final forest stage is always reached
    if st.session_state.day_count >= DAYS_TO_FOREST - 1:
        st.session_state.plant_stage = len(plant_images) - 1
    elif st.session_state.water_count == WATER_GOAL:
        # Update plant growth dynamically per day
        st.session_state.plant_stage = min(st.session_state.day_count + 1, len(plant_images) - 1)
        st.session_state.day_count += 1
        
        if st.session_state.day_count == DAYS_TO_FOREST:
            st.session_state.message = "🌳 Quest Complete! Your Vitality is unmatched! 🎉"
            reset_week()
        else:
            st.session_state.message = get_motivation()
    
    time.sleep(0.2)
    st.rerun()

def reset_day():
    st.session_state.water_count = 0
    st.session_state.overflow = False
    st.session_state.boss_battle = False
    st.session_state.message = ""
    st.rerun()

def reset_week():
    st.session_state.stamina = 0
    st.session_state.day_count = 0
    st.session_state.plant_stage = 0
    reset_day()

# Streamlit UI - Medieval Theme
st.set_page_config(page_title="🏺 The Flask of Vitality 🏺", layout="wide")
st.title("🏺 The Flask of Vitality 🏺 - A Hydration Quest! ⚔️")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"💧 Flask Refill: {st.session_state.water_count}/{WATER_GOAL} Cups")
    st.progress(min(st.session_state.water_count / WATER_GOAL, 1.0))
    st.subheader(f"⚡ Stamina Level: {st.session_state.stamina}")
    
    # Display quest motivation message
    motivation = get_motivation()
    if motivation:
        st.success(motivation)
    
    if st.button("🏺 Refill the Flask! 🏺"):
        log_water()
    if st.button("🛡️ New Battle Day 🛡️"):
        reset_day()

with col2:
    st.image(plant_images[st.session_state.plant_stage], caption="🌳 Your Legendary Growth 🌳", use_container_width=True)

# Overflow Stamina Celebration
if st.session_state.overflow:
    st.balloons()  # Fun visual effect when stamina overflows
    st.audio("https://www.myinstants.com/media/sounds/tada-fanfare-a.mp3")  # Celebration sound

# Boss Battle Mechanic - If hydration is missed
if st.session_state.water_count == 0 and st.session_state.day_count > 0:
    st.session_state.boss_battle = True
    st.error("⚔️ A Dehydration Demon has appeared! Defeat it by drinking water! ⚔️")
