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

# Title
st.title("Interactive Bingo Game")

# CSS + JavaScript for a dynamic, non-resetting grid
html_code = """
<style>
    .bingo-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 5px;
        width: 100%;
        max-width: 500px;
        margin: auto;
    }
    .bingo-cell {
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: bold;
        border: 1px solid black;
        cursor: pointer;
        user-select: none;
        background-color: white;
        color: black;
    }
    .bingo-cell.x-mark {
        background-color: red;
        color: white;
    }
    .bingo-cell.o-mark {
        background-color: blue;
        color: white;
    }
</style>

<div class="bingo-grid">
"""

for i in range(5):
    for j in range(5):
        word = bingo_card[i * 5 + j]
        cell_id = f"cell-{i}-{j}"
        mark_class = ""
        if st.session_state.bingo_grid[i][j] == "X":
            mark_class = "x-mark"
        elif st.session_state.bingo_grid[i][j] == "O":
            mark_class = "o-mark"
        
        html_code += f'<div id="{cell_id}" class="bingo-cell {mark_class}" onclick="toggleMark(\"{cell_id}\")">{word}</div>'

html_code += """
</div>

<script>
    function toggleMark(cellId) {
        let cell = document.getElementById(cellId);
        if (cell.classList.contains("x-mark")) {
            cell.classList.remove("x-mark");
            cell.classList.add("o-mark");
        } else if (cell.classList.contains("o-mark")) {
            cell.classList.remove("o-mark");
        } else {
            cell.classList.add("x-mark");
        }
    }
</script>
"""

st.markdown(html_code, unsafe_allow_html=True)

# Reset button
def reset_board():
    st.session_state.bingo_grid = [["" for _ in range(5)] for _ in range(5)]
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Reset Board"):
    reset_board()
