import streamlit as st
import random
import os

# Load challenges from challenges.txt
file_path = "challenges.txt"
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        all_challenges = [line.strip() for line in file.readlines()]
else:
    all_challenges = [
        "Conquer Yiga base", "Clear out Lurelin Village", "Complete Home on Arange", "Defeat a Molduga", "Get a matching outfit", "Fix a sign for Sign Guy", 
        "Complete 4 Shrines", "Complete 8 Shrines", "Complete 12 Shrines", "Find a hidden treasure map & item", "Cook with golden apple",
        "Take pictures of 10 different monsters", "Take pictures of 20 different monsters", "Clear monster camp naked", "Discover 2 hot springs",
        "Defeat an enemy using only Zonai tech", "Increase hearts", "Catch 5 different fish", "Catch 10 different fish", "Get weapon with 70 or more power",
        "Defeat an enemy while on horseback", "Defeat 5 enemies while on horseback", "Defeat 10 enemies while on horseback", 
        "Build a motorcycle", "Build a car", "Find a sages will", "Break five weapons", "Break 10 weapons",
        "Defeat a Boss Bokoblin parade", "Ride a dragon", "Clear an enemy camp naked", "Defeat a Lynel", "Defeat 3 Lynels", 
        "Complete a Colosseum", "Complete 3 Colosseums", "Cook a pizza", "Cook an omelette", "Get arrested in Gerudo town", 
        "Reunite a Korok with its friend", "Reunite 3 Koroks with their friends", "Register a horse", "Ride a non-horse", 
        "Increase stamina", "Upgrade 3 clothing items", "Find 4 lightroots", "Find 8 lightroots", "Discover 3 towers", "Discover 5 towers", 
        "Complete 4 sky shrines", "Collect an entire item set", "Give Beedle a beetle", "Bake a Bread", "Cook a Monster Meal", 
        "Defeat the hands", "Defeat a hinox", "Defeat 3 hinoxes", "Defeat a flux construct", "Defeat a Frox", "Experience low gravity", 
        "Fix 15 signs", "Defeat Kohga 2 Times", "Take a photo of a defeated lynel", "Send a korok to space", "Create 3 unique elixirs"
    ]

# Define categories for similar challenges to prevent duplicates based on numbers
categories = {
    "Shrines": ["Complete 4 Shrines", "Complete 8 Shrines", "Complete 12 Shrines"],
    "Pictures": ["Take pictures of 10 different monsters", "Take pictures of 20 different monsters"],
    "Horseback Defeats": ["Defeat an enemy while on horseback", "Defeat 5 enemies while on horseback", "Defeat 10 enemies while on horseback"],
    "Breaking Weapons": ["Break five weapons", "Break 10 weapons"],
    "Lightroots": ["Find 4 lightroots", "Find 8 lightroots"],
    "Towers": ["Discover 3 towers", "Discover 5 towers"],
    "Colosseums": ["Complete a Colosseum", "Complete 3 Colosseums"],
    "Reunite Koroks": ["Reunite a Korok with its friend", "Reunite 3 Koroks with their friends"],
    "Fish": ["Catch 5 different fish", "Catch 10 different fish"],
    "Lynels": ["Defeat a Lynel", "Defeat 3 Lynels"],
    "Hinoxes": ["Defeat a hinox", "Defeat 3 hinoxes"]
}

# Select one challenge per category
selected_challenges = []
for category in categories.values():
    selected_challenges.append(random.choice(category))

# Get remaining unique challenges
remaining_challenges = list(set(all_challenges) - set(sum(categories.values(), [])))
random.shuffle(remaining_challenges)

# Fill up to 25 slots
selected_challenges = list(set(selected_challenges))  # Ensure no duplicates
while len(selected_challenges) < 25:
    selected_challenges.append(remaining_challenges.pop())

# Shuffle the final board
random.shuffle(selected_challenges)

# Ensure the board stays consistent across interactions
if "bingo_card" not in st.session_state:
    st.session_state.bingo_card = selected_challenges

bingo_card = st.session_state.bingo_card

# Initialize session state for the bingo grid
if "bingo_grid" not in st.session_state:
    st.session_state.bingo_grid = [[0 for _ in range(5)] for _ in range(5)]

def toggle_cell(i, j):
    current_state = st.session_state.bingo_grid[i][j]
    new_state = (current_state + 1) % 4  # Cycle through 0, 1, 2, 3
    st.session_state.bingo_grid[i][j] = new_state

# Title
st.title("TotK Bingo")

# CSS to make buttons perfect squares
st.markdown("""
<style>
    .bingo-button {
        width: 100px !important;
        height: 100px !important;
        font-size: 15px;
        border-radius: 0px;
        border: 1px solid black;
        font-weight: bold;
    }
    .small-button {
        width: 50px !important;
        height: 20px !important;
        border-radius: 5px;
        border: 1px solid black;
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Create a 5x5 bingo board with correct state handling
for i in range(5):
    cols = st.columns(5)
    for j in range(5):
        word = bingo_card[i * 5 + j]
        key = f"cell_{i}_{j}"
        button_color_map = {0: "white", 1: "green", 2: "red", 3: "purple"}
        button_color = button_color_map[st.session_state.bingo_grid[i][j]]
        
        with cols[j]:
            st.markdown(
                f'<button class="bingo-button" style="background-color: {button_color};">{word}</button>',
                unsafe_allow_html=True
            )
            if st.button(" ", key=key, on_click=toggle_cell, args=(i, j), use_container_width=False):
                pass

# Reset button
def reset_board():
    random.shuffle(all_challenges)
    selected_challenges = []
    for category in categories.values():
        selected_challenges.append(random.choice(category))
    remaining_challenges = list(set(all_challenges) - set(sum(categories.values(), [])))
    random.shuffle(remaining_challenges)
    while len(selected_challenges) < 25:
        selected_challenges.append(remaining_challenges.pop())
    random.shuffle(selected_challenges)
    st.session_state.bingo_card = selected_challenges
    st.session_state.bingo_grid = [[False for _ in range(5)] for _ in range(5)]
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
