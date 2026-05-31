import sys

import streamlit as st

import re


# --- UI Configuration ---

st.title("Typology Codification Engine")

st.markdown("Enter your parameters to generate the typology render.")


# --- Logic Functions ---

def get_primer_letter(primer_type, state):

mapping = {

"PL": {"+": "E", "-": "I", "": "I"},

"PN": {"+": "S", "-": "N", "": "N"},

"PS": {"+": "T", "-": "F", "": "F"},

"PR": {"+": "J", "-": "P", "": "P"}

}

return mapping.get(primer_type, {}).get(state, "I")


def apply_styles(letter, influence, skill):

style = []

if "+" in influence: style.append("text-decoration: underline;")

elif "-" in influence: style.append("text-decoration: line-through;")

if "3" in influence: style.append("font-weight: bold;")

elif "1" in influence: style.append("font-style: italic;")

if "+" in skill: style.append("vertical-align: super; font-size: smaller;")

elif "-" in skill: style.append("vertical-align: sub; font-size: smaller;")


digit = re.sub(r'[\+\-]', '', skill)

colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}

if digit in colors: style.append(f"color: {colors[digit]};")

return f"<span style='{' '.join(style)}'>{letter}</span>"


# --- Input Fields ---

col1, col2, col3, col4 = st.columns(4)

primers = [get_primer_letter(p, st.sidebar.selectbox(f"State for {p}", ["+", "-", ""])) for p in ["PL", "PN", "PS", "PR"]]

influences = [st.sidebar.text_input(f"Influence {i+1}", "") for i in range(4)]

skills = [st.sidebar.text_input(f"Skill {i+1}", "1") for i in range(4)]

dof = st.sidebar.selectbox("Degree of Freedom", ["0", "1", "2", "3", "4"])


# --- Generation ---

if st.button("Generate Render"):

fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}

html_letters = "".join([apply_styles(primers[i], influences[i], skills[i]) for i in range(4)])

final_html = f"<div style='font-family: {fonts[dof]}; font-size: 100px; text-align: center;'>{html_letters}</div>"

st.components.v1.html(final_html, height=300)

