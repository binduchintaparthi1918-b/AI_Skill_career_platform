import streamlit as st

st.title("CareerAI Test")

st.write("Hello! Streamlit is working.")

name = st.text_input("Enter your name")

if name:
    st.success(f"Welcome {name}!")