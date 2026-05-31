import streamlit as st
import re

st.title("Typology Codification Engine")

def apply_styles(letter, influence, skill, dof_font):
    style = [f"font-family: {dof_font};"]
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

# Inputs
dof = st.selectbox("Select Degree of Freedom (Font Style)", ["serif", "sans-serif", "fantasy", "cursive", "monospace"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    p1 = st.selectbox("PL", ["+", "-"])
    inf1 = st.text_input("Inf 1", "")
    sk1 = st.text_input("Sk 1", "1")
with col2:
    p2 = st.selectbox("PN", ["+", "-"])
    inf2 = st.text_input("Inf 2", "")
    sk2 = st.text_input("Sk 2", "1")
with col3:
    p3 = st.selectbox("PS", ["+", "-"])
    inf3 = st.text_input("Inf 3", "")
    sk3 = st.text_input("Sk 3", "1")
with col4:
    p4 = st.selectbox("PR", ["+", "-"])
    inf4 = st.text_input("Inf 4", "")
    sk4 = st.text_input("Sk 4", "1")

if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    letters = [mapping["PL"][p1], mapping["PN"][p2], mapping["PS"][p3], mapping["PR"][p4]]
    influences = [inf1, inf2, inf3, inf4]
    skills = [sk1, sk2, sk3, sk4]
    
    html_output = "".join([apply_styles(letters[i], influences[i], skills[i], dof) for i in range(4)])
    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{html_output}</div>", unsafe_allow_html=True)