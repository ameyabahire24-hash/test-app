# app.py
import streamlit as st
import ast
import operator
import math
import re

# ---------------- Page config ----------------
st.set_page_config(page_title="Casio-lite Fast Scientific", page_icon="🧮", layout="centered")

# ---------------- Minimal CSS (single injection) ----------------
st.markdown(
    """
<style>
:root{
  --bg:#071018; --panel:#0b1620; --accent:#00e6d6; --muted:#9fb0bd; --key:#0f1720; --key2:#14202a;
}
body { background: var(--bg); color: #e6eef0; font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
.container { background: linear-gradient(180deg,#07141b,#0b1620); padding:14px; border-radius:12px; width:420px; margin:auto; box-shadow: 0 8px 30px rgba(2,6,23,0.7); }
.header { text-align:center; margin-bottom:6px; }
.title { color: var(--accent); font-weight:700; font-size:18px; }
.sub { color: var(--muted); font-size:12px; margin-bottom:8px; }
.display { background:#031018; border:1px solid rgba(0,230,214,0.06); color:var(--accent); padding:10px 12px; border-radius:8px; text-align:right; font-family:'Roboto Mono', monospace; font-size:22px; min-height:56px; }
.row { display:flex; gap:8px; margin-top:8px; }
.col { flex:1; }
.btn { background:var(--key); color:#e6eef0; border-radius:8px; height:50px; width:100%; border:0; font-size:15px; box-shadow: 0 2px 0 rgba(0,0,0,0.5); }
.btn:active { transform: translateY(1px); }
.btn.alt { background:var(--key2); }
.btn.accent { background:var(--accent); color:#002825; font-weight:700; }
.btn.warn { background:#ffb347; color:#1b1200; font-weight:700; }
.footer { text-align:center; color:var(--muted); font-size:12px; margin-top:10px; }
@media (max-width:480px){ .container{ width:96% } .btn{ height:46px; font-size:14px } .display{ font-size:18px } }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- Session state ----------------
if "expr" not in st.session_state:
    st.session_state.expr = ""  # the visible input expression
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "mode" not in st.session_state:
    st.session_state.mode = "DEG"  # or "RAD"
if "last" not in st.session_state:
    st.session_state.last = None

# ---------------- Safe AST evaluator (runs only when '=' pressed) ----------------
# Allowed binary/unary operators
_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def make_names(mode: str):
    """Return allowed functions/constants based on DEG/RAD mode."""
    if mode == "DEG":
        return {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "sqrt": math.sqrt,
            "log": lambda x: math.log10(x),
            "ln": math.log,
            "factorial": math.factorial,
            "abs": abs,
            "pow": pow,
            "pi": math.pi,
            "e": math.e,
        }
    else:  # RAD
        return {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "log": lambda x: math.log10(x),
            "ln": math.log,
            "factorial": math.factorial,
            "abs": abs,
            "pow": pow,
            "pi": math.pi,
            "e": math.e,
        }

def _eval(node, names):
    """Recursively evaluate AST node using allowed operators and names."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, names)
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    if isinstance(node, ast.Num):  # older AST
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, names)
        right = _eval(node.right, names)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, names)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Call):
        # only allow direct function names, no attributes
        if isinstance(node.func, ast.Name):
            fname = node.func.id
            if fname not in names:
                raise NameError(f"Unknown function '{fname}'")
            func = names[fname]
            args = [_eval(a, names) for a in node.args]
            return func(*args)
        raise NameError("Only direct function calls allowed")
    if isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        raise NameError(f"Unknown identifier '{node.id}'")
    raise TypeError(f"Unsupported AST node: {type(node)}")

# Preprocessing: convert calculator-style tokens to Python-friendly AST input
FACTORIAL_RE = re.compile(r'(\d+|\))\s*!')  # e.g., 5! or (expr)!

def preprocess(expr: str) -> str:
    # normalize
    s = expr.strip()
    s = s.replace("−", "-")
    # ^ to **
    s = s.replace("^", "**")
    # pi/e unicode or typed:
    s = s.replace("π", "pi")
    # replace factorial postfix n! or (expr)! with factorial(n)
    # This is a simple transform sufficient for calculator inputs like 5!, (3+2)! etc.
    # Loop until no change so nested cases handled (e.g., (2+3)! )
    prev = None
    while prev != s:
        prev = s
        s = FACTORIAL_RE.sub(r'factorial(\1)', s)
    return s

def safe_eval(expr: str, mode: str):
    if not expr:
        raise ValueError("Empty expression")
    s = preprocess(expr)
    parsed = ast.parse(s, mode="eval")
    names = make_names(mode)
    return _eval(parsed, names)

# ---------------- Helpers to modify expression/state ----------------
def append_token(tok: str):
    st.session_state.expr += tok

def clear_expr():
    st.session_state.expr = ""

def do_equals():
    try:
        val = safe_eval(st.session_state.expr, st.session_state.mode)
        st.session_state.last = val
        # format result: integers as int, floats trimmed
        if isinstance(val, float):
            if val.is_integer():
                st.session_state.expr = str(int(val))
            else:
                # limit to 12 significant decimal digits to keep display sane
                s = f"{val:.12g}"
                st.session_state.expr = s
        else:
            st.session_state.expr = str(val)
    except Exception:
        st.session_state.expr = "Error"

# ---------------- UI (single container) ----------------
st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown("<div class='header'><div class='title'>Casio-lite — Fast Scientific</div><div class='sub'>Mode: <strong>{}</strong> · Memory: <strong>{}</strong></div></div>".format(st.session_state.mode, st.session_state.memory), unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expr or '0'}</div>", unsafe_allow_html=True)

# Button rows: keep simple tokens (no heavy processing on clicks)
rows = [
    ["MC", "MR", "M+", "M-"],
    ["sin(", "cos(", "tan(", "sqrt("],
    ["asin(", "acos(", "atan(", "ln("],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "π", "+"],
    ["^", "(", ")", "="],
    ["!", "log(", "DEG/RAD", "C"]
]

# Render rows
for r_i, row in enumerate(rows):
    cols = st.columns(4, gap="small")
    for c_i, label in enumerate(row):
        key = f"btn-{r_i}-{c_i}-{label}"
        with cols[c_i]:
            cls = "btn"
            if label in ("=",):
                cls += " btn accent"
            elif label in ("C",):
                cls += " btn warn"
            elif label in ("MC", "MR", "M+", "M-", "DEG/RAD"):
                cls += " btn alt"
            # render button; streamlit won't accept custom class param, so pass label only; class used in CSS for global styling
            if st.button(label, key=key):
                # handle special actions (minimal work per click)
                if label == "C":
                    clear_expr()
                elif label == "=":
                    do_equals()
                elif label == "MC":
                    st.session_state.memory = 0.0
                elif label == "MR":
                    append_token(str(st.session_state.memory))
                elif label == "M+":
                    try:
                        # evaluate quickly (use safe_eval)
                        v = safe_eval(st.session_state.expr or "0", st.session_state.mode)
                        st.session_state.memory += float(v)
                    except Exception:
                        pass
                elif label == "M-":
                    try:
                        v = safe_eval(st.session_state.expr or "0", st.session_state.mode)
                        st.session_state.memory -= float(v)
                    except Exception:
                        pass
                elif label == "DEG/RAD":
                    st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
                elif label == "π":
                    append_token("π")
                elif label == "!":
                    append_token("!")
                else:
                    append_token(label)

st.markdown("<div class='footer'>Made with ❤️ — fast, safe, and reliable</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
