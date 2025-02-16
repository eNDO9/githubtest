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

# Apply light mode styling with full button color change
st.markdown("""
<style>
    body, .stApp {
        background-color: white;
        color: black;
    }
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
</style>
""", unsafe_allow_html=True)

for i in range(5):
    cols = st.columns(5, gap="small")
    for j in range(5):
        word = bingo_card[i * 5 + j]
        key = f"cell_{i}_{j}"
        button_color = "white"  # Default light mode button
        if st.session_state.bingo_grid[i][j] == "X":
            button_color = "red"
        elif st.session_state.bingo_grid[i][j] == "O":
            button_color = "blue"
        
        with cols[j]:
            btn = st.button(word, key=key, on_click=update_cell, args=(i, j), use_container_width=True)
            if btn:
                st.session_state.bingo_grid[i][j] = "X" if st.session_state.bingo_grid[i][j] == "" else ("O" if st.session_state.bingo_grid[i][j] == "X" else "")
            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"]:nth-of-type({i * 5 + j + 1}) button {{
                    background-color: {button_color} !important;
                    color: white !important;
                }}
                </style>
                """, unsafe_allow_html=True
            )

# Reset button
def reset_board():
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
