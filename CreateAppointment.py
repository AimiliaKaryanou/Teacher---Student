import streamlit as st
import requests


def app():
    # Streamlit form to create a teacher
    response = requests.get("http://localhost:8000/teachersWithId/")
    teachers = response.json()
    teachers_dict = {teacher['ID']: f"{teacher['FirstName']} {teacher['LastName']}" for teacher in teachers}
    selected_teacher_name = st.selectbox("Select a Teacher", list(teachers_dict.values()))
    teacher_id = next(key for key, value in teachers_dict.items() if value == selected_teacher_name)
    # Extract patient_id from the URL query parameters
    student_id = st.query_params['student_id']
    date = st.date_input("Select a Date")
    time = st.time_input("Select a Time")

    if st.button("Create Appointment"):
        date_str = date.strftime("%Y-%m-%d")
        time_str = str(time)
        appointment_data = {"TeacherID": teacher_id, "StudentID": student_id, "Date": date_str, "Time": time_str}
        response = requests.post("http://localhost:8000/appointments/", json=appointment_data)

        if response.status_code == 200:
            st.success("Appointment created successfully!")
        else:
            st.error(f"Error creating Appointment: {response.text}")