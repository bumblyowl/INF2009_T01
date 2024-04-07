import streamlit as st


st.title("User Login")

# Input field for the user to enter their name
name = st.text_input("Enter your name")

# Button to submit the form
if st.button("Start Session"):
    if name:
        st.success(f"Welcome, {name}!")
    else:
        st.warning("Please enter your name.")
