
import streamlit as st
st.set_page_config(page_title="RBI Financial Dashboard", layout="wide", page_icon="🏦")

# load css
with open("styles/global.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("assets/rbi_logo.png", width=140)
st.sidebar.title("🏦 RBI Dashboard")
st.sidebar.write("Navigation on the left — open pages from the Pages menu.")

st.title("🏦 RBI Financial Analytics Dashboard")
st.subheader("A unified platform for risk scoring, interest analysis, CPI trends, and global inflation forecasting.")

st.markdown("""
### 🔍 Modules Included:
- *RISCO Meter (Advanced)* – Risk scoring, gauge meter, profiling  
- *Interest Rate Calculator (Advanced)* – EMI chart & amortization  
- *USA CPI Dashboard (Advanced)* – Trends, graphs, inflation target comparison  
- *World Inflation Dashboard (Advanced)* – Multi-country trends + forecast  

*Designed with an RBI-style blue/gold theme for professional use.*
""")
