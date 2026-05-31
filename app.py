import streamlit as st
import re

st.title("Typology Codification Engine")

def apply_styles(letter, pol, mag, skill_pol, skill_mag, dof_val):
    # Mapping DOF (0-4) to fonts
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = [f"font-family: {fonts[dof_val]};"]
    
    # Logic for Polarity/Magnitude
    if pol == "+": style.append("text-decoration: underline;")
    elif pol == "-": style.append("text-decoration: line-through;")
    if mag == "3": style.append("font-weight: bold;")
    elif mag == "1": style.append("font-style: italic;")
    
    # Logic for Skill
    if skill_pol == "+": style.append("vertical-align: super; font-size: smaller;")
    elif skill_pol == "-": style.append("vertical-align: sub; font-size: smaller;")
    
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append(f"color: {colors[skill_mag]};")
    
    return f"<span style='{' '.join(style)}'>{letter}</span>"

# DOF Selection
dof = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], index=2)

# Grid Input
cols = st.columns(4)
data = []
labels = ["PL", "PN", "PS", "PR"]

for i, col in enumerate(cols):
    with col:
        st.subheader(labels[i])
        pol = st.selectbox(f"Pol {i+1}", [" ", "+", "-"], index=0)
        mag = st.selectbox(f"Mag {i+1}", ["1", "2", "3"], index=0)
        spol = st.selectbox(f"S-Pol {i+1}", [" ", "+", "-"], index=0)
        smag = st.selectbox(f"S-Mag {i+1}", ["1", "2", "3", "4", "5", "6"], index=0)
        data.append((pol, mag, spol, smag))

if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I", " ":"I"}, "PN": {"+":"S", "-":"N", " ":"N"}, 
               "PS": {"+":"T", "-":"F", " ":"F"}, "PR": {"+":"J", "-":"P", " ":"P"}}
    
    html_output = ""
    for i, label in enumerate(labels):
        pol, mag, spol, smag = data[i]
        letter = mapping[label][pol]
        html_output += apply_styles(letter, pol, mag, spol, smag, dof)
    
    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{html_output}</div>", unsafe_allow_html=True)