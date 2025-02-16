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

# CSS to make buttons perfect squares and change colors
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
    .red-button {
        background-color: red !important;
        color: white !important;
    }
    .blue-button {
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
        button_color_class = ""
        if st.session_state.bingo_grid[i][j] == "X":
            button_color_class = "red-button"
        elif st.session_state.bingo_grid[i][j] == "O":
            button_color_class = "blue-button"
        
        with cols[j]:
            st.markdown(f'<style>div[data-testid="stButton-{key}"] button {{background-color: {"red" if button_color_class == "red-button" else ("blue" if button_color_class == "blue-button" else "white")} !important;}}</style>', unsafe_allow_html=True)
            if st.button(word, key=key, on_click=update_cell, args=(i, j)):
                pass

# Reset button
def reset_board():
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
