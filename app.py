import streamlit as st
import random

# ==========================================
# TYPOLOGY PRIMER CODIFICATION ENGINE
# ==========================================
# Project Manager Notes: 
# This code has been fully annotated to demystify the logic.
# We strictly separate "Letter-Polarity" (which only changes the letter) 
# from "Influence-Polarity" (which only changes the underline/strikethrough).

# --- Page Configuration ---
st.set_page_config(layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
<style>
/* This makes the buttons large and sets their colors */
div.stButton > button { font-size: 20px !important; padding: 15px 30px !important; width: 100%; }
div.stButton:nth-of-type(1) > button { background-color: #FFD700 !important; color: #8B4513 !important; }
div.stButton:nth-of-type(2) > button { background-color: #C0C0C0 !important; color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# --- Math & Index Calculation ---
def calculate_index(inputs, dof_val):
    # Calculates the serial number based on dropdown positions
    col_totals = []
    for i in range(4):
        # We find the index (0, 1, 2, etc.) of the chosen dropdown value
        lp_idx = ["+", "-"].index(inputs["lp" + str(i)])
        mp_idx = [" ", "+", "-"].index(inputs["mp" + str(i)])
        mm_idx = ["1", "2", "3"].index(inputs["mm" + str(i)])
        sp_idx = [" ", "+", "-"].index(inputs["sp" + str(i)])
        sm_idx = ["1", "2", "3", "4", "5", "6"].index(inputs["sm" + str(i)])
        
        # Mathematical formula for the unique combination
        val = sm_idx + (6 * (sp_idx + (3 * (mm_idx + (3 * (mp_idx + (3 * lp_idx)))))))
        col_totals.append(val)
    
    total = col_totals[0] + (324 * col_totals[1]) + (324**2 * col_totals[2]) + (324**3 * col_totals[3])
    return (total * 5) + dof_val

# --- HTML Styling Engine ---
def apply_styles(letter, influence_pol, influence_mag, capacity_pol, capacity_mag, dof_val):
    # 1. Degree of Freedom controls the Font Family
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = ["font-family: " + fonts[dof_val] + ";"]
    
    # 2. Influence-Polarity controls Underline (+) or Strikethrough (-)
    if influence_pol == "+": 
        style.append("text-decoration: underline;")
    elif influence_pol == "-": 
        style.append("text-decoration: line-through;")
    # If it is " " (null), no text-decoration is appended!
    
    # 3. Influence-Magnitude controls Italic (1) or Bold (3)
    if influence_mag == "1": 
        style.append("font-style: italic;")
    elif influence_mag == "3": 
        style.append("font-weight: bold;")
    
    # 4. Capacity-Polarity controls Superscript (+) or Subscript (-)
    if capacity_pol == "+": 
        style.append("vertical-align: super; font-size: smaller;")
    elif capacity_pol == "-": 
        style.append("vertical-align: sub; font-size: smaller;")
    
    # 5. Capacity-Magnitude controls the Text Color
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append("color: " + colors[capacity_mag] + ";")
    
    # Combine all styles into a single HTML <span> tag
    return "<span style='" + " ".join(style) + "'>" + letter + "</span>"

# --- State Management & Randomization ---
# This stores our values in session_state so they don't reset when a button is clicked
if 'initialized' not in st.session_state:
    st.session_state.dof = "2"
    for i in range(4):
        st.session_state["lp" + str(i)] = "+"
        st.session_state["mp" + str(i)] = " "
        st.session_state["mm" + str(i)] = "1"
        st.session_state["sp" + str(i)] = " "
        st.session_state["sm" + str(i)] = "1"
    st.session_state.initialized = True

def randomize_data():
    st.session_state.dof = str(random.randint(0, 4))
    for i in range(4):
        st.session_state["lp" + str(i)] = random.choice(["+", "-"])
        st.session_state["mp" + str(i)] = random.choice([" ", "+", "-"])
        st.session_state["mm" + str(i)] = random.choice(["1", "2", "3"])
        st.session_state["sp" + str(i)] = random.choice([" ", "+", "-"])
        st.session_state["sm" + str(i)] = random.choice(["1", "2", "3", "4", "5", "6"])

# --- UI: Sidebar Controls ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>Input Controls</h2>", unsafe_allow_html=True)
    dof_val = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], key='dof')
    
    labels = ["PL", "PN", "PS", "PR"]
    inputs = {}
    
    # Loop to create the 4 columns of dropdowns
    for i in range(4):
        st.markdown("<h3 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>" + labels[i] + "</h3>", unsafe_allow_html=True)
        # lp = Letter-Polarity
        inputs["lp" + str(i)] = st.selectbox("Letter-Polarity", ["+", "-"], key="lp" + str(i))
        # mp = Influence-Polarity
        inputs["mp" + str(i)] = st.selectbox("Influence-Polarity", [" ", "+", "-"], key="mp" + str(i))
        # mm = Influence-Magnitude
        inputs["mm" + str(i)] = st.selectbox("Influence-Magnitude", ["1", "2", "3"], key="mm" + str(i))
        # sp = Capacity-Polarity
        inputs["sp" + str(i)] = st.selectbox("Capacity-Polarity", [" ", "+", "-"], key="sp" + str(i))
        # sm = Capacity-Magnitude
        inputs["sm" + str(i)] = st.selectbox("Capacity-Magnitude", ["1", "2", "3", "4", "5", "6"], key="sm" + str(i))

# --- UI: Main Page Header ---
current_index = calculate_index(inputs, int(dof_val))
idx_str = str(current_index) # Formatted to strictly avoid ASCII errors

st.markdown("<h3 style='font-size: 200%; margin-bottom: 0px;'><span style='color: #FF1493;'>" + idx_str + "</span> <span style='color: white;'>OF</span> <span style='color: #8A2BE2;'>55099802880 COMBINATIONS</span></h3>", unsafe_allow_html=True)
st.markdown("<h1 style='color: lightblue; font-size: 300%; margin-top: 10px;'>TYPOLOGY PRIMER CODIFICATION ENGINE</h1>", unsafe_allow_html=True)

# --- UI: Action Buttons ---
c1, c2 = st.columns([1, 4])
if c1.button("Randomize All"): 
    randomize_data()
    st.rerun()

# --- Core Generation Logic ---
if c2.button("Generate"):
    # Dictionary mapping the Letters based on the Letter-Polarity input
    mapping = {
        "PL": {"+":"E", "-":"I"}, 
        "PN": {"+":"S", "-":"N"}, 
        "PS": {"+":"T", "-":"F"}, 
        "PR": {"+":"J", "-":"P"}
    }
    
    html_out = ""
    # Loop through PL, PN, PS, PR
    for i in range(4):
        # 1. Get the raw Letter (e.g., "E" or "I") based on Letter-Polarity (lp)
        current_letter = mapping[labels[i]][inputs["lp" + str(i)]]
        
        # 2. Pass the Letter and the remaining formatting variables into the styling engine
        styled_letter = apply_styles(
            letter        = current_letter,
            influence_pol = inputs["mp" + str(i)], # Controls underline/strikethrough
            influence_mag = inputs["mm" + str(i)], # Controls bold/italic
            capacity_pol  = inputs["sp" + str(i)], # Controls super/subscript
            capacity_mag  = inputs["sm" + str(i)], # Controls color
            dof_val       = dof_val                # Controls font
        )
        
        # 3. Add the styled HTML span to the final output string
        html_out += styled_letter
        
    # 4. Render the massive text block on screen
    st.markdown("<div style='font-size: clamp(50px, 15vw, 300px); text-align: center;'>" + html_out + "</div>", unsafe_allow_html=True)

# --- UI: Glossary Section ---
st.markdown("---")
st.markdown("""
<div style="font-size: 150%; font-weight: bold; color: #FFEF00;">
<h3>Glossary of Typology Primers</h3>
<ul><li><b>PL (Practicality)</b>: The quality or state of being of relating to, or manifested in practice or action : not theoretical or ideal.<ul><li><b>+PL = (E)</b>: Extraversion: The use of practicality in decision making.</li><li><b>-PL = (I)</b>: Introversion: the lack of practicality and decision making.</li></ul></li>
<li><b>PN (Protocol)</b>: A system of rules that explain the correct conduct and procedures to be followed in formal situations.<ul><li><b>+PN = (S)</b>: Sensing: The use of protocol in decision making.</li><li><b>-PN = (N)</b>: Intuition: the lack of protocol in decision making.</li></ul></li>
<li><b>PS (Principal)</b>: A comprehensive and fundamental law, doctrine, or assumption.<ul><li><b>+PS = (T)</b>: Thinking: The use of principles in decision making.</li><li><b>-PS = (F)</b>: Feeling: the lack of principles in decision making.</li></ul></li>
<li><b>PR (Purpose)</b>: The aim or goal of a person.<ul><li><b>+PR = (J)</b>: Judging: the use of purpose and decision making.</li><li><b>-PR = (P)</b>: Perceiving: The lack of purpose in decision making.</li></ul></li></ul>
<h3>Additional Definitions</h3>
<ul><li><b>Letter-Polarity</b>: Either + or - before the letter code.</li><li><b>Influence-Polarity</b>: Either +, -, or null; visual representation is underline for +, strikethrough for -, and plain for null.</li><li><b>Influence-Magnitude</b>: 1 to 3 range; visual representation is italic (1), standard (2), and bold (3).</li><li><b>Capacity-Polarity</b>: Either +, -, or null; visual representation is superscript for +, subscript for -, and standard for null.</li><li><b>Capacity-Magnitude</b>: 1 to 6 range; visual representation is red(1), orange(2), yellow(3), green(4), blue(5), purple(6).</li></ul>
</div>
""", unsafe_allow_html=True)