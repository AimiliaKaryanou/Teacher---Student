import streamlit as st
import requests

def app():
    # Streamlit app to view teachers
    st.title("Teacher Viewer")

    # Fetch teachers from the FastAPI endpoint
    response = requests.get("http://localhost:8000/teachers/")
    teachers = response.json()

    # Display the list of doctors in Streamlit
    if response.status_code == 200:
        st.subheader("List of Teachers")
        for teacher in teachers:
            st.write(f"First Name: {teacher['FirstName']}, Last Name: {teacher['LastName']}")
    else:
        st.error(f"Error fetching teachers: {response.text}")
