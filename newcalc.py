import streamlit as st
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Casio fx-991EX", page_icon="🧮", layout="centered")

# --- CSS FOR REALISTIC CASIO LOOK ---
st.markdown("""
<style>
body {
    background-color: #202124;
    color: white;
    font-family: 'Consolas', monospace;
}
.calc-body {
    background-color: #2b2d30;
    padding: 25px;
    border-radius: 25px;
    width: 380px;
    margin: auto;
    box-shadow: 0 0 40px #00e6e6;
}
.display {
    background-color: #0b0c0d;
    color: #00ffcc;
    font-size: 1.6rem;
    padding: 12px;
    border-radius: 10px;
    text-align: right;
    margin-bottom: 10px;
    border: 2px solid #00cccc;
    font-family: 'Consolas', monospace;
    height: 55px;
}
.key {
    background-color: #3c3f41;
    color: white;
    border-radius: 8px;
    height: 50px;
    width: 100%;
    border: none;
    font-size: 1.1rem;
    transition: 0.2s;
}
.key:hover {
    background-color: #00b3b3;
    color: black;
}
.orange {
    background-color: #ff9933;
}
.orange:hover {
    background-color: #ffaa4d;
}
.blue {
    background-color: #0099ff;
}
.blue:hover {
    background-color: #33adff;
}
.title {
    text-align: center;
    color: #00ffff;
    font-size: 1.4rem;
    margin-bottom: 10px;
}
.mode {
    text-align: center;
    color: #ccc;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

# --- UTILS ---
def press(key):
    """Handle button press."""
    if key == "C":
        st.session_state.expr = ""
    elif key == "=":
        try:
            expr = st.session_state.expr.replace("^", "**")
            expr = expr.replace("√", "math.sqrt")
            if st.session_state.mode == "DEG":
                expr = expr.replace("sin", "math.sin(math.radians")
                expr = expr.replace("cos", "math.cos(math.radians")
                expr = expr.replace("tan", "math.tan(math.radians")
                expr = expr.replace(")", "))")
            result = eval(expr, {"__builtins__": None}, math.__dict__)
            st.session_state.expr = str(result)
        except Exception:
            st.session_state.expr = "Error"
    elif key == "M+":
        try:
            st.session_state.memory += float(st.session_state.expr)
        except:
            pass
    elif key == "M-":
        try:
            st.session_state.memory -= float(st.session_state.expr)
        except:
            pass
    elif key == "MR":
        st.session_state.expr += str(st.session_state.memory)
    elif key == "MC":
        st.session_state.memory = 0.0
    elif key == "DEG/RAD":
        st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
    else:
        st.session_state.expr += key

# --- DISPLAY ---
st.markdown("<div class='calc-body'>", unsafe_allow_html=True)
st.markdown("<div class='title'>CASIO fx-991EX (Streamlit Edition)</div>", unsafe_allow_html=True)
st.markdown(f"<div class='mode'>Mode: {st.session_state.mode} | Memory: {st.session_state.memory}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expr}</div>", unsafe_allow_html=True)

# --- BUTTONS ---
rows = [
    ["MC", "MR", "M+", "M-"],
    ["sin(", "cos(", "tan(", "√("],
    ["log(", "ln(", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["π", "e", "!", "="],
    ["C", "DEG/RAD", "", ""]
]

for row in rows:
    cols = st.columns(4)
    for i, key in enumerate(row):
        if key == "":
            with cols[i]:
                st.write("")
        else:
            with cols[i]:
                btn_class = "key"
                if key in ["=", "C"]:
                    btn_class += " orange"
                elif key in ["M+", "M-", "MR", "MC", "DEG/RAD"]:
                    btn_class += " blue"
                if st.button(key, key=f"{key}-{i}"):
                    if key == "π":
                        press(str(math.pi))
                    elif key == "e":
                        press(str(math.e))
                    elif key == "!":
                        st.session_state.expr += "math.factorial("
                    else:
                        press(key)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:gray;'>Made with ❤️ using Streamlit • Inspired by Casio fx-991EX</p>", unsafe_allow_html=True)
