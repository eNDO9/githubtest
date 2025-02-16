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

def update_cell(i, j):
    if st.session_state.bingo_grid[i][j] == "":
        st.session_state.bingo_grid[i][j] = "X"
    elif st.session_state.bingo_grid[i][j] == "X":
        st.session_state.bingo_grid[i][j] = "O"
    else:
        st.session_state.bingo_grid[i][j] = ""

# Title
st.title("Interactive Bingo Game")

# CSS to make buttons perfect squares and remove gaps, also styling for colors
st.markdown("""
<style>
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
        padding: 0px !important;
        margin: 0px !important;
        flex-grow: 1;
    }
    .stButton>button {
        width: 100%;
        aspect-ratio: 1/1;
        font-size: 16px;
        margin: 0px !important;
        padding: 0px !important;
        border-radius: 0px;
        border: 1px solid black;
    }
    .x-mark {
        background-color: red !important;
        color: white !important;
    }
    .o-mark {
        background-color: blue !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

for i in range(5):
    cols = st.columns(5, gap="small")
    for j in range(5):
        word = bingo_card[i * 5 + j]
        key = f"cell_{i}_{j}"
        button_label = word  # Default label
        button_class = ""

        if st.session_state.bingo_grid[i][j] == "X":
            button_class = "x-mark"
        elif st.session_state.bingo_grid[i][j] == "O":
            button_class = "o-mark"

        with cols[j]:
            if st.button(button_label, key=key, on_click=update_cell, args=(i, j), help="Click to toggle X/O", use_container_width=True):
                pass
            st.markdown(f"<script>document.getElementById('{key}').classList.add('{button_class}');</script>", unsafe_allow_html=True)

# Reset button
def reset_board():
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
