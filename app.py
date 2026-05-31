import streamlit as st
import re

st.title("Typology Codification Engine")

def apply_styles(letter, influence, skill, dof_val):
    # Mapping DOF (0-4) to fonts
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = [f"font-family: {fonts[dof_val]};"]
    
    # Logic for Influence
    if "+" in influence: style.append("text-decoration: underline;")
    elif "-" in influence: style.append("text-decoration: line-through;")
    if "3" in influence: style.append("font-weight: bold;")
    elif "1" in influence: style.append("font-style: italic;")
    
    # Logic for Skill
    if "+" in skill: style.append("vertical-align: super; font-size: smaller;")
    elif "-" in skill: style.append("vertical-align: sub; font-size: smaller;")
    
    digit = re.sub(r'[\+\-]', '', skill)
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    if digit in colors: style.append(f"color: {colors[digit]};")
    
    return f"<span style='{' '.join(style)}'>{letter}</span>"

# Inputs
dof = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], index=2)
col1, col2, col3, col4 = st.columns(4)

with col1:
    p1 = st.selectbox("PL", ["+", "-"], index=0)
    inf1 = st.selectbox("Inf 1", ["", "+", "-", "+1", "+2", "+3", "-1", "-2", "-3"], index=0)
    sk1 = st.selectbox("Sk 1", ["1", "2", "3", "4", "5", "6", "+1", "+2", "-1", "-2"], index=0)
with col2:
    p2 = st.selectbox("PN", ["+", "-"], index=1)
    inf2 = st.selectbox("Inf 2", ["", "+", "-", "+1", "+2", "+3", "-1", "-2", "-3"], index=0)
    sk2 = st.selectbox("Sk 2", ["1", "2", "3", "4", "5", "6", "+1", "+2", "-1", "-2"], index=0)
with col3:
    p3 = st.selectbox("PS", ["+", "-"], index=1)
    inf3 = st.selectbox("Inf 3", ["", "+", "-", "+1", "+2", "+3", "-1", "-2", "-3"], index=0)
    sk3 = st.selectbox("Sk 3", ["1", "2", "3", "4", "5", "6", "+1", "+2", "-1", "-2"], index=0)
with col4:
    p4 = st.selectbox("PR", ["+", "-"], index=1)
    inf4 = st.selectbox("Inf 4", ["", "+", "-", "+1", "+2", "+3", "-1", "-2", "-3"], index=0)
    sk4 = st.selectbox("Sk 4", ["1", "2", "3", "4", "5", "6", "+1", "+2", "-1", "-2"], index=0)

if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    letters = [mapping["PL"][p1], mapping["PN"][p2], mapping["PS"][p3], mapping["PR"][p4]]
    influences = [inf1, inf2, inf3, inf4]
    skills = [sk1, sk2, sk3, sk4]
    
    html_output = "".join([apply_styles(letters[i], influences[i], skills[i], dof) for i in range(4)])
    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{html_output}</div>", unsafe_allow_html=True)