import streamlit as st
from multiapp import MultiApp
import CreateTeacher, CreateStudent, ViewTeachers, ViewStudents, CreateAppointment


app = MultiApp()

# Initialize Page Config
st.set_page_config(
    page_title='Aimilia', 
    page_icon=':unamused:',
    layout='wide'
)

app.add_app("Create New Teacher", CreateTeacher.app)
app.add_app("Create New Student", CreateStudent.app)
app.add_app("View Teachers", ViewTeachers.app)
app.add_app("View Students", ViewStudents.app)
app.add_app("Create New Appointment", CreateAppointment.app)

app.run()