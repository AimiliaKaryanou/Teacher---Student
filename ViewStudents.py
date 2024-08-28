import streamlit as st
import requests

def app():
    # Streamlit app to view student
    st.title("Select a Student")

    # Fetch patients from the FastAPI endpoint
    response = requests.get("http://localhost:8000/studentsWithId/")
    students = response.json()
    if response.status_code == 200:
        student_dict = {student['ID']: f"{student['FirstName']} {student['LastName']}" for student in students}
        # Display the list of patients in Streamlit
        st.subheader("List of students")
        selected_student_name = st.selectbox("Select a Student", list(student_dict.values()))
    else:
        st.error(f"Error fetching students: {response.text}")
    # Button to redirect to the appointment screen
    if st.button("Select Patient and Go to Appointments"):
        # Set the patient_id in the URL query parameters
        selected_student_id = next(key for key, value in student_dict.items() if value == selected_student_name)
        st.experimental_set_query_params(student_id=selected_student_id)
        # Rerun the app to reflect the changes in the URL
        st.experimental_rerun()
