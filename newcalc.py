import streamlit as st
import math
import ast
import operator
import re

# ---------------- Page config ----------------
st.set_page_config(page_title="Casio fx-991 (Streamlit)", page_icon="🧮", layout="centered")

# ---------------- CSS (visuals) ----------------
st.markdown(
    """
<style>
body { background-color: #202124; color: #e6f7f7; font-family: 'Consolas', monospace; }
.calc-container { background:#2b2d30; padding:20px; border-radius:16px; width:420px; margin:auto; box-shadow:0 0 30px #00e6e6; }
.title { text-align:center; color:#00f5ff; font-weight:700; margin-bottom:6px; }
.mode { text-align:center; color:#cfd8dc; margin-bottom:10px; }
.display { background:#0b0c0d; color:#aaffee; font-size:1.4rem; padding:10px; border-radius:8px; text-align:right; border:2px solid #00cccc; height:60px; overflow:auto; }
.row { display:flex; gap:8px; margin-top:8px; }
.col { flex:1; }
.key { background:#3c3f41; color:white; border-radius:8px; height:48px; width:100%; border:none; font-size:1.05rem; }
.key:hover { filter:brightness(1.08); cursor:pointer; }
.key.orange { background:#ff9933; color:#0a0a0a; }
.key.blue { background:#1e90ff; color:#0a0a0a; }
.footer { text-align:center; color: #9aa3a3; margin-top:10px; font-size:0.85rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- Session state ----------------
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

# ---------------- Safe evaluator ----------------
# Allowed operators map
_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.FloorDiv: operator.floordiv,
}

def make_functions_for_mode(mode):
    """Return a dictionary of allowed names (functions/constants) depending on DEG/RAD mode."""
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
    """Recursively evaluate AST node with allowed names/operators."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, names)
    if isinstance(node, ast.Constant):  # number e.g., 1, 3.14
        return node.value
    if isinstance(node, ast.Num):  # for older py AST
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, names)
        right = _eval(node.right, names)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](left, right)
        raise ValueError(f"Unsupported binary operator {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, names)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type}")
    if isinstance(node, ast.Call):
        # only simple function names allowed (no attributes)
        if isinstance(node.func, ast.Name):
            fname = node.func.id
            if fname not in names:
                raise NameError(f"Use of unknown function '{fname}'")
            func = names[fname]
            args = [_eval(a, names) for a in node.args]
            return func(*args)
        raise NameError("Only direct function calls allowed")
    if isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        raise NameError(f"Unknown identifier '{node.id}'")
    if isinstance(node, ast.Expr):
        return _eval(node.value, names)
    raise TypeError(f"Unsupported expression: {type(node)}")

def safe_eval(expr, mode="DEG"):
    """Preprocess and safely evaluate expression string using AST traversal."""
    if not expr:
        raise ValueError("Empty expression")
    # Basic preprocessing:
    # 1) Replace caret ^ with ** for power
    expr = expr.replace("^", "**")
    # 2) Replace unicode minus if any and weird spaces
    expr = expr.replace("−", "-").strip()
    # 3) Replace patterns like 5! or (expr)! with factorial(expr)
    #    We'll replace n! where n is a number or closing paren
    expr = re.sub(r'(\d+|\))\s*!', r'factorial(\1)', expr)
    # 4) For square-root button we used 'sqrt(' already when adding; no special symbol
    # Parse AST
    parsed = ast.parse(expr, mode="eval")
    names = make_functions_for_mode(mode)
    return _eval(parsed, names)

# ---------------- Button handling helpers ----------------
def append_token(tok: str):
    st.session_state.expr += tok

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

