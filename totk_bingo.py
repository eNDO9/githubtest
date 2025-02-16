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

# Styling to make buttons square
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        aspect-ratio: 1/1;
        font-size: 16px;
        border: 1px solid black;
        margin: 0px;
        padding: 0px;
    }
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
        padding: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Create a bingo grid using st.container()
for i in range(5):
    with st.container():
        cols = st.columns(5)
        for j in range(5):
            word = bingo_card[i * 5 + j]
            key = f"cell_{i}_{j}"
            with cols[j]:
                if st.button(f"{word}\n({st.session_state.bingo_grid[i][j]})", key=key):
                    update_cell(i, j)
                    st.experimental_rerun()

# Reset button
def reset_board():
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]
    st.experimental_rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
