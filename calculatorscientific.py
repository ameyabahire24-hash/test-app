import streamlit as st
import math

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Casio fx-991 Scientific Calculator", page_icon="🧮", layout="centered")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: #f5f5f5;
}
.calc-container {
    background-color: #2c2c2c;
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 0 25px #00ffff33;
    width: 340px;
    margin: auto;
}
.display {
    background-color: #111;
    color: #00ffcc;
    font-size: 1.5rem;
    padding: 12px;
    border-radius: 10px;
    text-align: right;
    margin-bottom: 15px;
    font-family: 'Consolas', monospace;
}
button[kind="primary"] {
    background-color: #0ff !important;
}
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    background-color: #333;
    color: white;
    border: 1px solid #555;
    font-size: 1.1rem;
}
.stButton>button:hover {
    background-color: #00b3b3;
    color: black;
}
.row {
    display: flex;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DISPLAY ----------------
st.markdown("<h2 style='text-align:center;color:#00ffff;'>CASIO fx-991 Clone</h2>", unsafe_allow_html=True)

# Keep the input expression in session_state
if "expression" not in st.session_state:
    st.session_state.expression = ""

def press(key):
    """Handle button press."""
    if key == "C":
        st.session_state.expression = ""
    elif key == "=":
        try:
            result = eval(st.session_state.expression, {"__builtins__": None}, math.__dict__)
            st.session_state.expression = str(result)
        except Exception:
            st.session_state.expression = "Error"
    else:
        st.session_state.expression += key

# ---------------- DISPLAY FIELD ----------------
st.markdown(f"<div class='calc-container'><div class='display'>{st.session_state.expression}</div>", unsafe_allow_html=True)

# ---------------- BUTTON LAYOUT ----------------
buttons = [
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "^", "="],
    ["sin(", "cos(", "tan(", "log("],
    ["sqrt(", "pi", "e", "fact("],
]

for row in buttons:
    cols = st.columns(4)
    for i, key in enumerate(row):
        with cols[i]:
            if st.button(key):
                # Replace ^ with ** for Python evaluation
                if key == "^":
                    press("**")
                elif key == "fact(":
                    press("math.factorial(")
                elif key in ["sin(", "cos(", "tan(", "log(", "sqrt("]:
                    press(f"math.{key}")
                elif key == "pi":
                    press(str(math.pi))
                elif key == "e":
                    press(str(math.e))
                else:
                    press(key)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:gray;'>Made with ❤️ using Streamlit • Inspired by Casio fx-991</p>", unsafe_allow_html=True)
