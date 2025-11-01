import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# --- App Header ---
st.title("🧮 Simple Calculator")
st.write("Perform basic arithmetic operations easily!")

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Enter first number:", value=0.0, step=1.0)

with col2:
    num2 = st.number_input("Enter second number:", value=0.0, step=1.0)

# --- Operation Selection ---
operation = st.radio(
    "Choose an operation:",
    ("Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)")
)

# --- Calculate Button ---
if st.button("Calculate"):
    try:
        if operation == "Addition (+)":
            result = num1 + num2
            st.success(f"✅ Result: {num1} + {num2} = {result}")
        elif operation == "Subtraction (-)":
            result = num1 - num2
            st.success(f"✅ Result: {num1} - {num2} = {result}")
        elif operation == "Multiplication (×)":
            result = num1 * num2
            st.success(f"✅ Result: {num1} × {num2} = {result}")
        elif operation == "Division (÷)":
            if num2 != 0:
                result = num1 / num2
                st.success(f"✅ Result: {num1} ÷ {num2} = {result}")
            else:
                st.error("❌ Division by zero is not allowed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io)")
