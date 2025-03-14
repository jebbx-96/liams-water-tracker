import streamlit as st
import time

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

demon_image = "images/dehydration_demon.png"
demon_sound = "https://www.myinstants.com/media/sounds/scary-sound.mp3"
celebration_sound = "https://www.myinstants.com/media/sounds/tada.mp3"

# Ordered silly messages for extra water intake
silly_messages = [
    "Oh, u so sexi 😘", 
    "Go piss girl! 💦", 
    "You didn't have to flex on the rest of us like this.", 
    "Is this what peak performance looks like?", 
    "Your pee is now clearer than my future.", 
    "Drink more and you'll unlock the secret ending.", 
    "If hydration was a crime, you'd be in jail.", 
    "Do you even have bones left or are you just liquid?", 
    "Your organs are clapping like my cheeks when you take me from behind lol. A standing ovation for hydration!", 
    "I bet rainbows appear when you pee at this point.", 
    "Fiji water is calling you daddy.", 
    "You’ve transcended mortal thirst. Welcome to the Liquid Realm.", 
    "The Pacific Ocean is quaking in its boots."
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
        extra_cups = st.session_state.water_count - WATER_GOAL
        if extra_cups <= len(silly_messages):
            st.success(silly_messages[extra_cups - 1])
    
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
    if st.session_state.water_count < WATER_GOAL:
        st.session_state.boss_battle = True
    else:
        st.session_state.boss_battle = False
    
    st.session_state.water_count = 0
    st.session_state.overflow = False
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
    if st.session_state.boss_battle:
        st.image(demon_image, caption="⚠️ The Dehydration Demon Strikes! Drink to defeat it! ⚠️", use_container_width=True)
        st.audio(demon_sound, start_time=0)
    else:
        st.image(plant_images[st.session_state.plant_stage], caption="🌳 Your Legendary Growth 🌳", use_container_width=True)
