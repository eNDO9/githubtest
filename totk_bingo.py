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

# Title
st.title("Interactive Bingo Game")

# Generate a 5x5 grid using HTML and JavaScript
html = """
<style>
    .bingo-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0px;
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
    }
</style>

<div class="bingo-grid">
"""

for i, word in enumerate(bingo_card):
    html += f"<div class='bingo-cell' id='cell{i}' onclick='toggleCell({i})'>{word}</div>"

html += """
</div>

<script>
    function toggleCell(index) {
        let cell = document.getElementById('cell' + index);
        if (cell.innerHTML.includes('(X)')) {
            cell.innerHTML = cell.innerHTML.replace('(X)', '(O)');
        } else if (cell.innerHTML.includes('(O)')) {
            cell.innerHTML = cell.innerHTML.replace('(O)', '');
        } else {
            cell.innerHTML += ' (X)';
        }
    }
</script>
"""

st.markdown(html, unsafe_allow_html=True)

# Reset button
if st.button("Reset Board"):
    st.rerun()
