"""
✨ CALCY ✨
A stunning, reliable glassmorphism-themed calculator built with Streamlit.
Run with: streamlit run app.py
"""

import streamlit as st
import math

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Calcy",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "display" not in st.session_state:
    st.session_state.display = "0"
if "history" not in st.session_state:
    st.session_state.history = []
if "just_evaluated" not in st.session_state:
    st.session_state.just_evaluated = False
if "pulse" not in st.session_state:
    st.session_state.pulse = 0
if "theme" not in st.session_state:
    st.session_state.theme = "Aurora"

THEMES = {
    "Aurora": {
        "bg1": "#0f0c29", "bg2": "#302b63", "bg3": "#24243e",
        "accent1": "#a770ef", "accent2": "#00d2ff", "accent3": "#f7797d",
        "glow": "rgba(167, 112, 239, 0.55)",
    },
    "Sunset": {
        "bg1": "#1a0f1f", "bg2": "#4a1942", "bg3": "#2b0f2f",
        "accent1": "#ff5e62", "accent2": "#ff9966", "accent3": "#ffd200",
        "glow": "rgba(255, 94, 98, 0.55)",
    },
    "Ocean": {
        "bg1": "#02111b", "bg2": "#0e3a53", "bg3": "#001e2b",
        "accent1": "#00c6ff", "accent2": "#0072ff", "accent3": "#7dfff0",
        "glow": "rgba(0, 198, 255, 0.55)",
    },
}

t = THEMES[st.session_state.theme]

# ----------------------------------------------------------------------------
# CSS — the magic
# ----------------------------------------------------------------------------
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Space Grotesk', sans-serif;
}}

.stApp {{
    background: linear-gradient(135deg, {t['bg1']} 0%, {t['bg2']} 50%, {t['bg3']} 100%);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
}}

@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* floating orbs behind everything */
.orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.45;
    z-index: 0;
    animation: floatOrb 12s ease-in-out infinite;
}}
.orb1 {{
    width: 300px; height: 300px;
    background: {t['accent1']};
    top: -80px; left: -80px;
    animation-delay: 0s;
}}
.orb2 {{
    width: 260px; height: 260px;
    background: {t['accent2']};
    bottom: -60px; right: -60px;
    animation-delay: 3s;
}}
.orb3 {{
    width: 200px; height: 200px;
    background: {t['accent3']};
    top: 40%; right: 10%;
    animation-delay: 6s;
}}
@keyframes floatOrb {{
    0%, 100% {{ transform: translate(0,0) scale(1); }}
    50% {{ transform: translate(30px,-30px) scale(1.1); }}
}}

/* header */
.calcy-title {{
    text-align: center;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, {t['accent1']}, {t['accent2']}, {t['accent3']});
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 4s linear infinite;
    margin-bottom: 0;
    letter-spacing: 1px;
}}
@keyframes shine {{
    to {{ background-position: 200% center; }}
}}
.calcy-subtitle {{
    text-align: center;
    color: rgba(255,255,255,0.45);
    font-size: 0.85rem;
    margin-top: -6px;
    margin-bottom: 22px;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

/* glass display panel */
.calc-glass {{
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 18px 22px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.37), inset 0 0 0.5px rgba(255,255,255,0.4);
    margin-bottom: 18px;
    position: relative;
    z-index: 1;
}}

.expr-line {{
    text-align: right;
    color: rgba(255,255,255,0.45);
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    min-height: 22px;
    overflow-x: auto;
    white-space: nowrap;
}}

.display-line {{
    text-align: right;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 3rem;
    letter-spacing: 1px;
    overflow-x: auto;
    white-space: nowrap;
    text-shadow: 0 0 20px {t['glow']};
    animation: fadeSlide 0.25s ease;
}}
@keyframes fadeSlide {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.pulse-glow {{
    animation: pulseGlow 0.6s ease;
}}
@keyframes pulseGlow {{
    0% {{ text-shadow: 0 0 4px {t['glow']}; }}
    50% {{ text-shadow: 0 0 40px {t['glow']}, 0 0 70px {t['glow']}; }}
    100% {{ text-shadow: 0 0 20px {t['glow']}; }}
}}

/* keypad grid spacing */
div[data-testid="column"] {{
    padding: 0 6px !important;
}}

/* buttons — big, reliable, rounded-square tap targets */
div.stButton {{
    width: 100% !important;
}}
div.stButton > button {{
    width: 100% !important;
    min-width: 100% !important;
    height: 78px !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.07) !important;
    color: #fff !important;
    font-size: 1.55rem !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    backdrop-filter: blur(10px);
    transition: all 0.15s cubic-bezier(.2,.8,.2,1);
    box-shadow: 0 3px 10px rgba(0,0,0,0.28);
    margin-bottom: 12px;
}}
div.stButton > button:hover {{
    transform: translateY(-3px) scale(1.04);
    background: rgba(255,255,255,0.17) !important;
    border-color: {t['accent2']} !important;
    box-shadow: 0 10px 24px {t['glow']};
}}
div.stButton > button:active {{
    transform: translateY(0px) scale(0.96);
}}
div.stButton > button:focus:not(:active) {{
    border-color: {t['accent2']} !important;
    box-shadow: 0 0 0 3px {t['glow']};
}}

/* operator / equal / clear variants */
.op-btn button {{
    background: linear-gradient(135deg, {t['accent1']}55, {t['accent2']}55) !important;
    border-color: {t['accent2']}99 !important;
    color: #fff !important;
    font-size: 1.4rem !important;
}}
.eq-btn button {{
    background: linear-gradient(135deg, {t['accent1']}, {t['accent2']}) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 800 !important;
    font-size: 1.7rem !important;
    box-shadow: 0 8px 22px {t['glow']} !important;
}}
.eq-btn button:hover {{
    box-shadow: 0 12px 32px {t['glow']} !important;
}}
.clear-btn button {{
    background: rgba(247, 121, 125, 0.16) !important;
    border-color: #f7797d77 !important;
    color: #ffb3b5 !important;
    font-size: 1.3rem !important;
}}

/* history */
.history-box {{
    backdrop-filter: blur(14px);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 12px 16px;
    max-height: 160px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.55);
    margin-top: 10px;
}}
.history-item {{
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    animation: fadeSlide 0.3s ease;
}}
.history-item:last-child {{ border-bottom: none; }}
.history-item span.result {{
    color: {t['accent2']};
    font-weight: 700;
}}

/* hide streamlit chrome */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

.block-container {{
    padding-top: 2.2rem;
    max-width: 560px;
}}
</style>

<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<div class="calcy-title">✨ Calcy</div>', unsafe_allow_html=True)
st.markdown('<div class="calcy-subtitle">a calculator, but make it glow</div>', unsafe_allow_html=True)

theme_choice = st.selectbox(
    "Theme", list(THEMES.keys()),
    index=list(THEMES.keys()).index(st.session_state.theme),
    label_visibility="collapsed",
)
if theme_choice != st.session_state.theme:
    st.session_state.theme = theme_choice
    st.rerun()

# ----------------------------------------------------------------------------
# CALC LOGIC
# ----------------------------------------------------------------------------
SAFE_CHARS = "0123456789.+-*/()% "

def evaluate_expression(expr: str) -> str:
    clean = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    if not clean or any(c not in SAFE_CHARS + "*" for c in clean):
        return "Error"
    try:
        result = eval(clean, {"__builtins__": {}}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(round(result, 10)) if isinstance(result, float) else str(result)
    except ZeroDivisionError:
        return "Can't ÷ by 0"
    except Exception:
        return "Error"

def press(key: str):
    if key == "AC":
        st.session_state.expression = ""
        st.session_state.display = "0"
    elif key == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
        st.session_state.display = st.session_state.expression or "0"
    elif key == "=":
        result = evaluate_expression(st.session_state.expression)
        if st.session_state.expression:
            st.session_state.history.insert(
                0, (st.session_state.expression, result)
            )
            st.session_state.history = st.session_state.history[:6]
        st.session_state.display = result
        st.session_state.expression = result if result not in ("Error", "Can't ÷ by 0") else ""
        st.session_state.just_evaluated = True
        st.session_state.pulse += 1
    elif key == "±":
        if st.session_state.expression.startswith("-"):
            st.session_state.expression = st.session_state.expression[1:]
        else:
            st.session_state.expression = "-" + st.session_state.expression
        st.session_state.display = st.session_state.expression or "0"
    elif key == "√":
        try:
            val = eval(st.session_state.expression or "0", {"__builtins__": {}}, {})
            res = math.sqrt(val)
            res = int(res) if res.is_integer() else round(res, 8)
            st.session_state.expression = str(res)
            st.session_state.display = str(res)
        except Exception:
            st.session_state.display = "Error"
    else:
        operators = ("+", "-", "*", "/", "%")
        if st.session_state.just_evaluated and key not in operators:
            st.session_state.expression = ""
        st.session_state.just_evaluated = False

        expr = st.session_state.expression

        # Prevent a leading operator (except minus, for negative numbers)
        if expr == "" and key in operators and key != "-":
            return

        # Collapse consecutive operators into the newest one
        if expr and expr[-1] in operators and key in operators:
            st.session_state.expression = expr[:-1] + key
            st.session_state.display = st.session_state.expression
            return

        # Prevent a second decimal point within the current number segment
        if key == ".":
            last_segment = expr
            for op in operators:
                last_segment = last_segment.split(op)[-1]
            if "." in last_segment:
                return
            if last_segment == "":
                key = "0."

        st.session_state.expression = expr + key
        st.session_state.display = st.session_state.expression

# ----------------------------------------------------------------------------
# DISPLAY
# ----------------------------------------------------------------------------
pulse_class = "display-line pulse-glow" if st.session_state.pulse else "display-line"
st.markdown(
    f"""
<div class="calc-glass">
    <div class="expr-line">{st.session_state.expression or "&nbsp;"}</div>
    <div class="{pulse_class}">{st.session_state.display}</div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# KEYPAD
# ----------------------------------------------------------------------------
rows = [
    [("AC", "clear"), ("⌫", "clear"), ("√", "op"), ("÷", "op")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("-", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
    [("±", "op"), ("0", "num"), (".", "num"), ("=", "eq")],
]

key_map = {"÷": "/", "×": "*"}

for r_idx, row in enumerate(rows):
    cols = st.columns(4, gap="small")
    for c_idx, (label, kind) in enumerate(row):
        with cols[c_idx]:
            css_class = {"op": "op-btn", "eq": "eq-btn", "clear": "clear-btn"}.get(kind, "")
            if css_class:
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(label, key=f"btn_{r_idx}_{c_idx}", use_container_width=True):
                press(key_map.get(label, label))
                st.rerun()
            if css_class:
                st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HISTORY
# ----------------------------------------------------------------------------
if st.session_state.history:
    items_html = "".join(
        f'<div class="history-item"><span>{expr}</span><span class="result">= {res}</span></div>'
        for expr, res in st.session_state.history
    )
    st.markdown(f'<div class="history-box">{items_html}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="history-box" style="text-align:center; opacity:0.4;">history will glow up here ✨</div>',
        unsafe_allow_html=True,
    )