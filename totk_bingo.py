import streamlit as st
import random
import os

# Load words from challenges.txt
file_path = "challenges.txt"
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        words = [line.strip() for line in file.readlines()]
else:
    words = [f"Word {i+1}" for i in range(50)]  # Fallback if file is missing

# Shuffle and select 25 words for the bingo card
random.shuffle(words)
bingo_card = words[:25]

# Initialize session state for the bingo grid
if "bingo_grid" not in st.session_state:
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]

# Title
st.title("Interactive Bingo Game")

# Bingo grid display
for i in range(5):
    cols = st.columns(5)
    for j in range(5):
        word = bingo_card[i * 5 + j]
        key = f"cell_{i}_{j}"
        
        # Button logic
        if key not in st.session_state:
            st.session_state[key] = ""  # Default empty
        
        if cols[j].button(f"{word}\n({st.session_state[key]})", key=key):
            if st.session_state[key] == "":
                st.session_state[key] = "X"
            elif st.session_state[key] == "X":
                st.session_state[key] = "O"
            else:
                st.session_state[key] = ""  # Reset

# Reset button
if st.button("Reset Board"):
    for i in range(5):
        for j in range(5):
            st.session_state[f"cell_{i}_{j}"] = ""
