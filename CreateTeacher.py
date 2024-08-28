import streamlit as st
import requests


def app():
    # Streamlit form to create a teacher
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    if st.button("Create Teacher"):
        teacher_data = {"FirstName": first_name, "LastName": last_name}
        response = requests.post("http://localhost:8000/teachers/", json=teacher_data)

        if response.status_code == 200:
            st.success("Teacher created successfully!")
        else:
            st.error(f"Error creating teacher: {response.text}")