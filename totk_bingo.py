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

# Ensure the board stays consistent across interactions
if "bingo_card" not in st.session_state:
    random.shuffle(words)
    st.session_state.bingo_card = words[:25]

bingo_card = st.session_state.bingo_card

# Initialize session state for the bingo grid
if "bingo_grid" not in st.session_state:
    st.session_state.bingo_grid = [[False for _ in range(5)] for _ in range(5)]

def toggle_cell(i, j):
    st.session_state.bingo_grid[i][j] = not st.session_state.bingo_grid[i][j]

# Title
st.title("TotK Bingo")

# CSS to make buttons perfect squares
st.markdown("""
<style>
    .bingo-button {
        width: 100px !important;
        height: 100px !important;
        font-size: 16px;
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
        button_color = "yellow" if st.session_state.bingo_grid[i][j] else "white"
        
        with cols[j]:
            st.markdown(
                f'<button class="bingo-button" style="background-color: {button_color};">{word}</button>',
                unsafe_allow_html=True
            )
            if st.button(" ", key=key, on_click=toggle_cell, args=(i, j), use_container_width=False):
                pass

# Reset button
def reset_board():
    st.session_state.bingo_grid = [[False for _ in range(5)] for _ in range(5)]
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
