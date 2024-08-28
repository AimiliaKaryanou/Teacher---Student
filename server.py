from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from requests import Session
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
# uvicorn server:app --reload
# streamlit run app.py
# SQLite database setup
DATABASE_URL = "sqlite:///C:\\Projects\\Aimilia\\db.sqlite"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()

# CORS middleware for allowing requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Teacher(Base):
    __tablename__ = "Teachers"
    
    ID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    FirstName = Column(Text)
    LastName = Column(Text)
    
class Student(Base):
    __tablename__ = "Students"
    
    ID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    FirstName = Column(Text)
    LastName = Column(Text)
    
class Appointment(Base):
    __tablename__ = "Appointments"
    
    ID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    StudentID = Column(Integer)
    TeacherID = Column(Integer)
    Date = Column(Text)
    Time = Column(Text)

class TeacherCreate(BaseModel):
    FirstName: str
    LastName: str

class StudentsCreate(BaseModel):
    FirstName: str
    LastName: str

class Students(BaseModel):
    ID: int
    FirstName: str
    LastName: str

class Teachers(BaseModel):
    ID: int
    FirstName: str
    LastName: str

class AppointmentsCreate(BaseModel):
    StudentID: int
    TeacherID: int
    Date: str
    Time: str
    
Base.metadata.create_all(bind=engine)


# API endpoint to create a teacher
@app.post("/teachers/", response_model=TeacherCreate)
async def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(**teacher_data.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# API endpoint to view teachers
@app.get("/teachers/", response_model=list[TeacherCreate])
def get_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return teachers

# API endpoint to view teachers with id
@app.get("/teachersWithId/", response_model=list[Teachers])
def get_teachers_with_id(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return teachers


# API endpoint to create students
@app.post("/students/", response_model=StudentsCreate)
async def create_student(student_data: StudentsCreate, db: Session = Depends(get_db)):
    db_student = Student(**student_data.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# API endpoint to view students with ID
@app.get("/studentsWithId/", response_model=list[Students])
def get_students_with_id(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

# API endpoint to create appointment
@app.post("/appointments/", response_model=AppointmentsCreate)
async def create_appointment(appointment_data: AppointmentsCreate, db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment_data.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# New endpoint to get a single student by ID
@app.get("/students/{student_id}", response_model=StudentsCreate)
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.ID == student_id).first()
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")
