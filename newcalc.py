
   
def clear():
    st.session_state.expr = ""

def evaluate_expression():
    try:
        # safe evaluation
        val = safe_eval(st.session_state.expr, st.session_state.mode)
        # format result nicely: if integer-like, show as int
        if isinstance(val, float) and val.is_integer():
            st.session_state.expr = str(int(val))
        else:
            st.session_state.expr = str(val)
    except Exception as e:
        st.session_state.expr = "Error"

# ---------------- UI ----------------
st.markdown("<div class='calc-container'>", unsafe_allow_html=True)
st.markdown("<div class='title'>CASIO fx-991 (Streamlit Edition)</div>", unsafe_allow_html=True)
st.markdown(f"<div class='mode'>Mode: <strong>{st.session_state.mode}</strong>  &nbsp; | &nbsp; Memory: <strong>{st.session_state.memory}</strong></div>", unsafe_allow_html=True)
st.markdown(f"<div class='display' id='display'>{st.session_state.expr}</div>", unsafe_allow_html=True)

# Buttons layout - list of rows
buttons = [
    ["MC", "MR", "M+", "M-"],
    ["sin(", "cos(", "tan(", "sqrt("],
    ["asin(", "acos(", "atan(", "ln("],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "pi", "+"],
    ["^", "(", ")", "="],
    ["!", "log(", "DEG/RAD", "C"],
]

# render rows
for r_index, row in enumerate(buttons):
    cols = st.columns(4, gap="small")
    for c_index, label in enumerate(row):
        key = f"btn-{r_index}-{c_index}-{label}"
        btn_class = "key"
        if label in ("=", "C", "DEG/RAD"):
            btn_class += " orange"
        if label in ("MC", "MR", "M+", "M-", "DEG/RAD"):
            btn_class += " blue"
        with cols[c_index]:
            # use st.button but apply small inline style by wrapping html? simpler to use label only.
            if st.button(label, key=key):
                # handle special keys
                if label == "C":
                    clear()
                elif label == "=":
                    evaluate_expression()
                elif label == "MC":
                    st.session_state.memory = 0.0
                elif label == "MR":
                    # append memory value
                    append_token(str(st.session_state.memory))
                elif label == "M+":
                    # try to evaluate current expression into a number and add to memory
                    try:
                        res = safe_eval(st.session_state.expr, st.session_state.mode)
                        st.session_state.memory += float(res)
                    except Exception:
                        pass
                elif label == "M-":
                    try:
                        res = safe_eval(st.session_state.expr, st.session_state.mode)
                        st.session_state.memory -= float(res)
                    except Exception:
                        pass
                elif label == "DEG/RAD":
                    st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
                elif label == "pi":
                    append_token("pi")
                elif label == "!":
                    # append '!' and let safe_eval convert patterns like 5! to factorial(5)
                    append_token("!")
                else:
                    append_token(label)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Made with ❤️ using Streamlit — realistic scientific functions, safe evaluation</div>", unsafe_allow_html=True)

