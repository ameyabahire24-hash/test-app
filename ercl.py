import streamlit as st
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Casio fx-991 Streamlit", page_icon="🧮", layout="centered")

# --- CUSTOM STYLES ---
st.markdown("""
<style>
body {
    background-color: #0f1116;
    color: #fff;
    font-family: 'Roboto Mono', monospace;
}
.calc {
    background: linear-gradient(145deg, #1a1d25, #20232b);
    border-radius: 25px;
    width: 360px;
    margin: auto;
    box-shadow: 0 0 30px rgba(0,255,255,0.3);
    padding: 20px;
}
.display {
    background-color: #0c0e12;
    color: #00ffc6;
    font-size: 1.6rem;
    border-radius: 10px;
    text-align: right;
    padding: 10px;
    margin-bottom: 12px;
    border: 1px solid #00ffff55;
    font-weight: bold;
}
button[kind="secondary"] {
    width: 70px !important;
}
.btn {
    width: 100%;
    height: 50px;
    border: none;
    border-radius: 8px;
    background: #30343f;
    color: white;
    font-size: 1.1rem;
    transition: 0.15s;
}
.btn:hover {
    background: #00ffff;
    color: #000;
}
.orange {
    background: #ffb347;
}
.orange:hover {
    background: #ffc369;
}
.blue {
    background: #00b3b3;
}
.blue:hover {
    background: #00ffff;
}
.title {
    text-align: center;
    color: #00ffff;
    font-size: 1.4rem;
    margin-bottom: 5px;
}
.mode {
    text-align: center;
    color: #ccc;
    margin-bottom: 10px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

# --- CALCULATOR LOGIC ---
def safe_eval(expr):
    try:
        expr = expr.replace("^", "**").replace("√", "math.sqrt")
        expr = expr.replace("π", str(math.pi)).replace("e", str(math.e))
        if st.session_state.mode == "DEG":
            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")
        else:
            expr = expr.replace("sin(", "math.sin(")
            expr = expr.replace("cos(", "math.cos(")
            expr = expr.replace("tan(", "math.tan(")
        return eval(expr, {"__builtins__": None}, math.__dict__)
    except:
        return "Error"

def press(key):
    if key == "C":
        st.session_state.expr = ""
    elif key == "=":
        res = safe_eval(st.session_state.expr)
        st.session_state.expr = str(res)
    elif key == "M+":
        try:
            st.session_state.memory += float(safe_eval(st.session_state.expr))
        except:
            pass
    elif key == "M-":
        try:
            st.session_state.memory -= float(safe_eval(st.session_state.expr))
        except:
            pass
    elif key == "MR":
        st.session_state.expr += str(st.session_state.memory)
    elif key == "MC":
        st.session_state.memory = 0.0
    elif key == "DEG/RAD":
        st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
    elif key == "!":
        try:
            val = int(safe_eval(st.session_state.expr))
            st.session_state.expr = str(math.factorial(val))
        except:
            st.session_state.expr = "Error"
    else:
        st.session_state.expr += key

# --- UI ---
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='title'>CASIO fx-991 (Streamlit Edition)</div>", unsafe_allow_html=True)
st.markdown(f"<div class='mode'>Mode: {st.session_state.mode} | Memory: {st.session_state.memory}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expr}</div>", unsafe_allow_html=True)

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
        if key != "":
            css = "btn"
            if key in ["=", "C"]: css += " orange"
            elif key in ["M+", "M-", "MR", "MC", "DEG/RAD"]: css += " blue"
            if cols[i].button(key, key=f"{key}-{i}"):
                press(key)
        else:
            cols[i].write("")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
