🎓 Student Attendance System
A Student Attendance Management System built using FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic, and Streamlit.
🚀 Features
Student Management
- Create student
- View students
- Update student
- Delete student
- Filter students using query parameters
Teacher Management
- Create teacher
- View teachers
- Update teacher
- Delete teacher
- Filter teachers using query parameters
Classroom Management
- Create class
- View classes
- Update class
- Delete class
- Add students to a class
- View students in a class
- Remove students from a class
- Filter classes using query parameters
Timetable Management
- Create timetable entries
- View timetable
- View timetable entries by class
- Filter timetable entries using query parameters
- Update timetable
- Delete timetable
- Validate teacher/class relationships and scheduling conflicts
Attendance Management
- Mark attendance
- View attendance
- Filter attendance using query parameters
- Update attendance
- Delete attendance
- Validate student, timetable, and class relationships
- Prevent duplicate attendance for the same student, timetable, and date
Attendance Dashboard
- Select attendance date
- View attendance by student
- View attendance by teacher
- Present/Absent visual representation
- Daily attendance summary
🛠️ Technology Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic
- pydantic-settings
- asyncpg
- Alembic
- Streamlit
- Requests
📁 Project Structure
student_attsys/
│
├── common/
│   ├── constants.py
│   ├── routes.py
│   ├── validation.py
│   └── __init__.py
│
├── core/
│   └── settings.py
│
├── db/
│   ├── base.py
│   └── session.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
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
│   ├── classroom/
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
├── alembic.ini
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── .env
🗄️ Database
The application uses PostgreSQL with SQLAlchemy 2.0 and the asynchronous asyncpg driver.
Database configuration is loaded from the .env file through the application's settings configuration.
Example:
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/attendance_db
Do not commit the .env file to GitHub.
Database Migrations
Alembic is used to manage database schema migrations.
Check migration status:
alembic current
Check whether model changes require a migration:
alembic check
Apply migrations:
alembic upgrade head
Create a new migration after making model changes:
alembic revision --autogenerate -m "describe your change"
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
7. Apply database migrations
alembic upgrade head
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
   Validation
        ↓
    Services
        ↓
   SQLAlchemy
        ↓
   PostgreSQL
The Streamlit frontend communicates with the FastAPI backend through HTTP requests.
FastAPI routes handle HTTP requests and pass validation and business operations to the appropriate layers.
SQLAlchemy provides ORM-based asynchronous communication with PostgreSQL.
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
Classes
POST   /classes/
GET    /classes/
GET    /classes/{class_id}
PUT    /classes/{class_id}
DELETE /classes/{class_id}
POST   /classes/{class_id}/students/{student_id}
GET    /classes/{class_id}/students
DELETE /classes/{class_id}/students/{student_id}
Timetable
POST   /timetables/
GET    /timetables/
GET    /timetables/class/{class_id}
GET    /timetables/{timetable_id}
PUT    /timetables/{timetable_id}
DELETE /timetables/{timetable_id}
The timetable list endpoint supports dynamic query filters such as teacher_id, class_id, period, and other timetable fields.
Attendance
POST   /attendance/
GET    /attendance/
GET    /attendance/{attendance_id}
PUT    /attendance/{attendance_id}
DELETE /attendance/{attendance_id}
The attendance list endpoint supports dynamic filters including student, timetable, class, status, and date.
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
The application provides a working asynchronous FastAPI backend and Streamlit frontend with CRUD functionality for students, teachers, classes, timetable, and attendance.
Author
Pranav Mahoths Balija