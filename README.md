# Student Attendance System

## Prerequisites
- Python 3.12+
- PostgreSQL
- Git

## Setup

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment.

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file using the project's required environment variables. Configure the PostgreSQL database connection.

5. Apply database migrations.

   ```powershell
   alembic upgrade head
   ```

## Run the Application

```powershell
uvicorn main:app --reload
```

- API documentation: `http://127.0.0.1:8000/docs`

## Project Conventions
- Follow the existing module structure and naming conventions.
- Keep routes, schemas, services, models, and validation logic separated.
- Use asynchronous database operations where applicable.
- Use Alembic migrations for database schema changes.
- Keep credentials and secrets in environment variables; never commit them.

## Development Notes
- Run the application from the project root.
- Ensure PostgreSQL is running and the database configuration is correct before starting.
- Create and test migrations before submitting database schema changes.
