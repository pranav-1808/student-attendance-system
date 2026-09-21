# 🎓 Student Attendance System

A basic Student Attendance Management System built using FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic, and Streamlit.

## 🚀 Features

### Student Management
- Create student
- View students
- Update student
- Delete student

### Teacher Management
- Create teacher
- View teachers
- Update teacher
- Delete teacher

### Timetable Management
- Create timetable entries
- View timetable
- Update timetable
- Delete timetable

### Attendance Management
- Mark attendance
- View attendance
- Update attendance
- Delete attendance

### Attendance Dashboard
- Select attendance date
- View attendance by student
- View attendance by teacher
- Present/Absent visual representation
- Daily attendance summary

## 🛠️ Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic
- asyncpg
- Streamlit
- Requests

## 📁 Project Structure

```text
student_attsys/
│
├── common/
│   ├── constants.py
│   ├── validation.py
│   └── __init__.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── init_db.py
│
├── modules/
│   ├── student/
│   │   ├── routes.py
│   │   ├── validation.py
│   │   ├── services.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── teacher/
│   │   ├── routes.py
│   │   ├── validation.py
│   │   ├── services.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── timetable/
│   │   ├── routes.py
│   │   ├── validation.py
│   │   ├── services.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── attendance/
│       ├── routes.py
│       ├── validation.py
│       ├── services.py
│       ├── models.py
│       └── schemas.py
│
├── frontend/
│   └── app.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── .env
🗄️ Database

The application uses PostgreSQL as the database.

Database configuration is stored in the .env file.

Example:

DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/attendance_db

Note: Do not commit the .env file to GitHub.

⚙️ Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Enter the project directory
cd student_attsys
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Configure PostgreSQL

Create a PostgreSQL database named:

attendance_db

Create a .env file in the project root:

DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/attendance_db

Replace YOUR_PASSWORD with your PostgreSQL password.

▶️ Running the Application

The application requires two terminals.

Terminal 1 — FastAPI
uvicorn main:app --reload

The API will run at:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Terminal 2 — Streamlit
streamlit run frontend/app.py

The Streamlit frontend will open in the browser.

🔄 Application Flow
Streamlit Frontend
       ↓
     HTTP
       ↓
     FastAPI
       ↓
   SQLAlchemy
       ↓
   PostgreSQL

The Streamlit frontend communicates with the FastAPI backend through HTTP requests.

FastAPI handles validation, business logic, and database operations.

SQLAlchemy provides ORM-based communication with PostgreSQL.

📌 API Endpoints
Students
POST   /students/
GET    /students/
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}
Teachers
POST   /teachers/
GET    /teachers/
GET    /teachers/{teacher_id}
PUT    /teachers/{teacher_id}
DELETE /teachers/{teacher_id}
Timetable
POST   /timetables/
GET    /timetables/
GET    /timetables/{timetable_id}
PUT    /timetables/{timetable_id}
DELETE /timetables/{timetable_id}
Attendance
POST   /attendance/
GET    /attendance/
GET    /attendance/{attendance_id}
PUT    /attendance/{attendance_id}
DELETE /attendance/{attendance_id}
📝 Attendance Design

Attendance is associated with:

Student
   +
Timetable / Class
   +
Date
   +
Status

This allows a student to have attendance records for multiple classes on the same day.

The attendance table prevents duplicate attendance for the same:

student + timetable + date
🔐 Security

Sensitive configuration such as database credentials is stored in .env.

The .env file is excluded from Git using .gitignore.

👨‍💻 Project Status

The application currently provides a working backend API and Streamlit frontend with CRUD functionality for students, teachers, timetable, and attendance.

## Author

Pranav Mahoths Balija