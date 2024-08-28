import streamlit as st
import requests


def app():
    # Streamlit form to create a student
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    if st.button("Create Student"):
        student_data = {"FirstName": first_name, "LastName": last_name}
        response = requests.post("http://localhost:8000/students/", json=student_data)

        if response.status_code == 200:
            st.success("Student created successfully!")
        else:
            st.error(f"Error creating doctor: {response.text}")