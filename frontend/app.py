import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st
import requests
from datetime import date

from common.constants import DAYS_OF_WEEK


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Student Attendance System",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_data(endpoint):
    response = requests.get(f"{API_URL}{endpoint}")

    if response.status_code == 200:
        return response.json()

    return []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎓 Attendance System")

menu = st.sidebar.selectbox(
    "Select Page",
    [
        "Dashboard",
        "Students",
        "Teachers",
        "Timetable",
        "Attendance"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.title("📊 Attendance Dashboard")

    st.write(
        "Select a date and choose how you want to view the attendance."
    )

    # --------------------------------------------------------
    # GET DATA
    # --------------------------------------------------------

    students = get_data("/students/")
    teachers = get_data("/teachers/")
    timetables = get_data("/timetables/")
    attendance = get_data("/attendance/")

    # --------------------------------------------------------
    # FILTER OPTIONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_date = st.date_input(
            "📅 Select Date",
            value=date.today()
        )

    with col2:

        sort_by = st.selectbox(
            "🔽 View Attendance By",
            [
                "Student",
                "Teacher"
            ]
        )

    st.divider()

    # --------------------------------------------------------
    # CREATE LOOKUP DICTIONARIES
    # --------------------------------------------------------

    student_lookup = {
        student["id"]: student["name"]
        for student in students
    }

    teacher_lookup = {
        teacher["id"]: teacher["name"]
        for teacher in teachers
    }

    timetable_lookup = {
        timetable["id"]: timetable
        for timetable in timetables
    }

    # --------------------------------------------------------
    # FILTER ATTENDANCE BY DATE
    # --------------------------------------------------------

    selected_date_string = selected_date.isoformat()

    filtered_attendance = [
        record
        for record in attendance
        if record["date"] == selected_date_string
    ]

    # --------------------------------------------------------
    # NO RECORDS
    # --------------------------------------------------------

    if not filtered_attendance:

        st.info(
            f"No attendance records found for "
            f"{selected_date.strftime('%d %B %Y')}."
        )

    else:

        # ----------------------------------------------------
        # STUDENT VIEW
        # ----------------------------------------------------

        if sort_by == "Student":

            st.subheader(
                f"👨‍🎓 Attendance by Student — "
                f"{selected_date.strftime('%d %B %Y')}"
            )

            # Group attendance by student
            student_records = {}

            for record in filtered_attendance:

                student_id = record["student_id"]

                timetable_id = record["timetable_id"]

                timetable = timetable_lookup.get(
                    timetable_id
                )

                if timetable is None:
                    continue

                subject = timetable["subject"]

                if student_id not in student_records:

                    student_records[student_id] = {}

                student_records[student_id][subject] = (
                    record["status"]
                )

            # Find all subjects/classes for this date
            subjects = []

            for record in filtered_attendance:

                timetable = timetable_lookup.get(
                    record["timetable_id"]
                )

                if timetable:

                    subject = timetable["subject"]

                    if subject not in subjects:
                        subjects.append(subject)

            # Sort subjects alphabetically
            subjects.sort()

            # Build visual table
            table_data = []

            for student_id, records in student_records.items():

                row = {
                    "Student":
                        student_lookup.get(
                            student_id,
                            f"Student {student_id}"
                        )
                }

                for subject in subjects:

                    if subject in records:

                        if records[subject]:
                            row[subject] = "🟢 Present"
                        else:
                            row[subject] = "🔴 Absent"

                    else:

                        row[subject] = "—"

                table_data.append(row)

            if table_data:

                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )

        # ----------------------------------------------------
        # TEACHER VIEW
        # ----------------------------------------------------

        else:

            st.subheader(
                f"👨‍🏫 Attendance by Teacher — "
                f"{selected_date.strftime('%d %B %Y')}"
            )

            # Group attendance by teacher
            teacher_records = {}

            for record in filtered_attendance:

                timetable_id = record["timetable_id"]

                timetable = timetable_lookup.get(
                    timetable_id
                )

                if timetable is None:
                    continue

                teacher_id = timetable["teacher_id"]

                subject = timetable["subject"]

                if teacher_id not in teacher_records:

                    teacher_records[teacher_id] = {}

                if subject not in teacher_records[teacher_id]:

                    teacher_records[teacher_id][subject] = {
                        "present": 0,
                        "absent": 0
                    }

                if record["status"]:

                    teacher_records[teacher_id][subject]["present"] += 1

                else:

                    teacher_records[teacher_id][subject]["absent"] += 1

            # Get all subjects
            subjects = []

            for teacher_data in teacher_records.values():

                for subject in teacher_data:

                    if subject not in subjects:
                        subjects.append(subject)

            subjects.sort()

            # Build visual table
            table_data = []

            for teacher_id, records in teacher_records.items():

                row = {
                    "Teacher":
                        teacher_lookup.get(
                            teacher_id,
                            f"Teacher {teacher_id}"
                        )
                }

                for subject in subjects:

                    if subject in records:

                        present = records[subject]["present"]

                        absent = records[subject]["absent"]

                        total = present + absent

                        row[subject] = (
                            f"🟢 {present} Present / "
                            f"🔴 {absent} Absent"
                        )

                    else:

                        row[subject] = "—"

                table_data.append(row)

            if table_data:

                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.divider()

    st.subheader("📌 Daily Summary")

    present_count = sum(
        1
        for record in filtered_attendance
        if record["status"] is True
    )

    absent_count = sum(
        1
        for record in filtered_attendance
        if record["status"] is False
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Records",
            len(filtered_attendance)
        )

    with col2:

        st.metric(
            "🟢 Present",
            present_count
        )

    with col3:

        st.metric(
            "🔴 Absent",
            absent_count
        )


# ============================================================
# STUDENTS
# ============================================================

elif menu == "Students":

    st.title("👨‍🎓 Students")

    # --------------------------------------------------------
    # VIEW STUDENTS
    # --------------------------------------------------------

    st.subheader("All Students")

    students = get_data("/students/")

    if students:

        st.dataframe(
            students,
            use_container_width=True
        )

    else:

        st.info("No students found.")

    st.divider()

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    st.subheader("➕ Add Student")

    with st.form("add_student_form"):

        name = st.text_input("Student Name")

        email = st.text_input("Email")

        submitted = st.form_submit_button(
            "Add Student"
        )

        if submitted:

            response = requests.post(
                f"{API_URL}/students/",
                json={
                    "name": name,
                    "email": email
                }
            )

            if response.status_code == 200:

                st.success(
                    "Student added successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)

    st.divider()

    # --------------------------------------------------------
    # UPDATE STUDENT
    # --------------------------------------------------------

    st.subheader("✏️ Update Student")

    if students:

        student_options = {
            f'{student["id"]} - {student["name"]}':
            student
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys()),
            key="update_student_select"
        )

        student = student_options[selected_student]

        with st.form("update_student_form"):

            new_name = st.text_input(
                "Name",
                value=student["name"]
            )

            new_email = st.text_input(
                "Email",
                value=student["email"]
            )

            update_button = st.form_submit_button(
                "Update Student"
            )

            if update_button:

                response = requests.put(
                    f'{API_URL}/students/{student["id"]}',
                    json={
                        "name": new_name,
                        "email": new_email
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Student updated successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    st.divider()

    # --------------------------------------------------------
    # DELETE STUDENT
    # --------------------------------------------------------

    st.subheader("🗑️ Delete Student")

    if students:

        student_options = {
            f'{student["id"]} - {student["name"]}':
            student
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student to Delete",
            list(student_options.keys()),
            key="delete_student_select"
        )

        student = student_options[selected_student]

        if st.button("Delete Student"):

            response = requests.delete(
                f'{API_URL}/students/{student["id"]}'
            )

            if response.status_code == 200:

                st.success(
                    "Student deleted successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)


# ============================================================
# TEACHERS
# ============================================================

elif menu == "Teachers":

    st.title("👨‍🏫 Teachers")

    # --------------------------------------------------------
    # VIEW TEACHERS
    # --------------------------------------------------------

    st.subheader("All Teachers")

    teachers = get_data("/teachers/")

    if teachers:

        st.dataframe(
            teachers,
            use_container_width=True
        )

    else:

        st.info("No teachers found.")

    st.divider()

    # --------------------------------------------------------
    # ADD TEACHER
    # --------------------------------------------------------

    st.subheader("➕ Add Teacher")

    with st.form("add_teacher_form"):

        name = st.text_input("Teacher Name")

        email = st.text_input("Teacher Email")

        submitted = st.form_submit_button(
            "Add Teacher"
        )

        if submitted:

            response = requests.post(
                f"{API_URL}/teachers/",
                json={
                    "name": name,
                    "email": email
                }
            )

            if response.status_code == 200:

                st.success(
                    "Teacher added successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)

    st.divider()

    # --------------------------------------------------------
    # UPDATE TEACHER
    # --------------------------------------------------------

    st.subheader("✏️ Update Teacher")

    if teachers:

        teacher_options = {
            f'{teacher["id"]} - {teacher["name"]}':
            teacher
            for teacher in teachers
        }

        selected_teacher = st.selectbox(
            "Select Teacher",
            list(teacher_options.keys()),
            key="update_teacher_select"
        )

        teacher = teacher_options[selected_teacher]

        with st.form("update_teacher_form"):

            new_name = st.text_input(
                "Name",
                value=teacher["name"]
            )

            new_email = st.text_input(
                "Email",
                value=teacher["email"]
            )

            update_button = st.form_submit_button(
                "Update Teacher"
            )

            if update_button:

                response = requests.put(
                    f'{API_URL}/teachers/{teacher["id"]}',
                    json={
                        "name": new_name,
                        "email": new_email
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Teacher updated successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    st.divider()

    # --------------------------------------------------------
    # DELETE TEACHER
    # --------------------------------------------------------

    st.subheader("🗑️ Delete Teacher")

    if teachers:

        teacher_options = {
            f'{teacher["id"]} - {teacher["name"]}':
            teacher
            for teacher in teachers
        }

        selected_teacher = st.selectbox(
            "Select Teacher to Delete",
            list(teacher_options.keys()),
            key="delete_teacher_select"
        )

        teacher = teacher_options[selected_teacher]

        if st.button("Delete Teacher"):

            response = requests.delete(
                f'{API_URL}/teachers/{teacher["id"]}'
            )

            if response.status_code == 200:

                st.success(
                    "Teacher deleted successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)


# ============================================================
# TIMETABLE
# ============================================================

elif menu == "Timetable":

    st.title("📚 Timetable")

    teachers = get_data("/teachers/")
    timetables = get_data("/timetables/")

    # --------------------------------------------------------
    # VIEW TIMETABLE
    # --------------------------------------------------------

    st.subheader("All Classes")

    if timetables:

        st.dataframe(
            timetables,
            use_container_width=True
        )

    else:

        st.info("No timetable entries found.")

    st.divider()

    # --------------------------------------------------------
    # ADD TIMETABLE
    # --------------------------------------------------------

    st.subheader("➕ Add Class")

    if teachers:

        teacher_options = {
            f'{teacher["id"]} - {teacher["name"]}':
            teacher["id"]
            for teacher in teachers
        }

        with st.form("add_timetable_form"):

            selected_teacher = st.selectbox(
                "Teacher",
                list(teacher_options.keys())
            )

            subject = st.text_input(
                "Subject"
            )

            day = st.selectbox(
                "Day",
                DAYS_OF_WEEK
            )

            period = st.number_input(
                "Period",
                min_value=1,
                max_value=10,
                step=1
            )

            submitted = st.form_submit_button(
                "Add Class"
            )

            if submitted:

                response = requests.post(
                    f"{API_URL}/timetables/",
                    json={
                        "teacher_id":
                            teacher_options[selected_teacher],

                        "subject":
                            subject,

                        "day":
                            day,

                        "period":
                            period
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Class added successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    else:

        st.warning(
            "Add a teacher before creating a timetable."
        )

    st.divider()

    # --------------------------------------------------------
    # UPDATE TIMETABLE
    # --------------------------------------------------------

    st.subheader("✏️ Update Class")

    if timetables and teachers:

        teacher_options = {
            f'{teacher["id"]} - {teacher["name"]}':
            teacher["id"]
            for teacher in teachers
        }

        timetable_options = {
            f'{item["id"]} - {item["subject"]} - {item["day"]}':
            item
            for item in timetables
        }

        selected_class = st.selectbox(
            "Select Class",
            list(timetable_options.keys()),
            key="update_timetable_select"
        )

        timetable = timetable_options[selected_class]

        teacher_names = list(teacher_options.keys())

        current_teacher = next(
            (
                name
                for name, teacher_id
                in teacher_options.items()
                if teacher_id == timetable["teacher_id"]
            ),
            teacher_names[0]
        )

        with st.form("update_timetable_form"):

            selected_teacher = st.selectbox(
                "Teacher",
                teacher_names,
                index=teacher_names.index(current_teacher)
            )

            subject = st.text_input(
                "Subject",
                value=timetable["subject"]
            )

            days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ]

            current_day_index = (
                days.index(timetable["day"])
                if timetable["day"] in days
                else 0
            )

            day = st.selectbox(
                "Day",
                days,
                index=current_day_index
            )

            period = st.number_input(
                "Period",
                min_value=1,
                max_value=10,
                value=timetable["period"],
                step=1
            )

            update_button = st.form_submit_button(
                "Update Class"
            )

            if update_button:

                response = requests.put(
                    f'{API_URL}/timetables/{timetable["id"]}',
                    json={
                        "teacher_id":
                            teacher_options[selected_teacher],

                        "subject":
                            subject,

                        "day":
                            day,

                        "period":
                            period
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Class updated successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    st.divider()

    # --------------------------------------------------------
    # DELETE TIMETABLE
    # --------------------------------------------------------

    st.subheader("🗑️ Delete Class")

    if timetables:

        timetable_options = {
            f'{item["id"]} - {item["subject"]} - {item["day"]}':
            item
            for item in timetables
        }

        selected_class = st.selectbox(
            "Select Class to Delete",
            list(timetable_options.keys()),
            key="delete_timetable_select"
        )

        timetable = timetable_options[selected_class]

        if st.button("Delete Class"):

            response = requests.delete(
                f'{API_URL}/timetables/{timetable["id"]}'
            )

            if response.status_code == 200:

                st.success(
                    "Class deleted successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)


# ============================================================
# ATTENDANCE
# ============================================================

elif menu == "Attendance":

    st.title("📝 Attendance")

    students = get_data("/students/")
    timetables = get_data("/timetables/")
    attendance = get_data("/attendance/")

    # --------------------------------------------------------
    # VIEW ATTENDANCE
    # --------------------------------------------------------

    st.subheader("All Attendance Records")

    if attendance:

        st.dataframe(
            attendance,
            use_container_width=True
        )

    else:

        st.info("No attendance records found.")

    st.divider()

    # --------------------------------------------------------
    # MARK ATTENDANCE
    # --------------------------------------------------------

    st.subheader("➕ Mark Attendance")

    if students and timetables:

        student_options = {
            f'{student["id"]} - {student["name"]}':
            student["id"]
            for student in students
        }

        timetable_options = {
            f'{item["id"]} - {item["subject"]} - '
            f'{item["day"]} - Period {item["period"]}':
            item["id"]
            for item in timetables
        }

        with st.form("add_attendance_form"):

            selected_student = st.selectbox(
                "Student",
                list(student_options.keys())
            )

            selected_timetable = st.selectbox(
                "Class",
                list(timetable_options.keys())
            )

            attendance_date = st.date_input(
                "Date",
                value=date.today()
            )

            status = st.selectbox(
                "Status",
                [
                    "Present",
                    "Absent"
                ]
            )

            submitted = st.form_submit_button(
                "Mark Attendance"
            )

            if submitted:

                response = requests.post(
                    f"{API_URL}/attendance/",
                    json={
                        "student_id":
                            student_options[selected_student],

                        "timetable_id":
                            timetable_options[selected_timetable],

                        "date":
                            attendance_date.isoformat(),

                        "status":
                            status == "Present"
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Attendance marked successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    else:

        st.warning(
            "You need at least one student and one timetable class."
        )

    st.divider()

    # --------------------------------------------------------
    # UPDATE ATTENDANCE
    # --------------------------------------------------------

    st.subheader("✏️ Update Attendance")

    if attendance and students and timetables:

        attendance_options = {
            f'ID {record["id"]} - '
            f'Student {record["student_id"]} - '
            f'Date {record["date"]}':
            record
            for record in attendance
        }

        selected_record = st.selectbox(
            "Select Attendance Record",
            list(attendance_options.keys())
        )

        record = attendance_options[selected_record]

        student_options = {
            f'{student["id"]} - {student["name"]}':
            student["id"]
            for student in students
        }

        timetable_options = {
            f'{item["id"]} - {item["subject"]} - '
            f'{item["day"]} - Period {item["period"]}':
            item["id"]
            for item in timetables
        }

        current_student = next(
            (
                name
                for name, student_id
                in student_options.items()
                if student_id == record["student_id"]
            ),
            list(student_options.keys())[0]
        )

        current_timetable = next(
            (
                name
                for name, timetable_id
                in timetable_options.items()
                if timetable_id == record["timetable_id"]
            ),
            list(timetable_options.keys())[0]
        )

        with st.form("update_attendance_form"):

            selected_student = st.selectbox(
                "Student",
                list(student_options.keys()),
                index=list(student_options.keys()).index(
                    current_student
                )
            )

            selected_timetable = st.selectbox(
                "Class",
                list(timetable_options.keys()),
                index=list(timetable_options.keys()).index(
                    current_timetable
                )
            )

            current_date = date.fromisoformat(
                record["date"]
            )

            attendance_date = st.date_input(
                "Date",
                value=current_date
            )

            current_status = (
                "Present"
                if record["status"]
                else "Absent"
            )

            status = st.selectbox(
                "Status",
                [
                    "Present",
                    "Absent"
                ],
                index=(
                    0
                    if current_status == "Present"
                    else 1
                )
            )

            update_button = st.form_submit_button(
                "Update Attendance"
            )

            if update_button:

                response = requests.put(
                    f'{API_URL}/attendance/{record["id"]}',
                    json={
                        "student_id":
                            student_options[selected_student],

                        "timetable_id":
                            timetable_options[selected_timetable],

                        "date":
                            attendance_date.isoformat(),

                        "status":
                            status == "Present"
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Attendance updated successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    st.divider()

    # --------------------------------------------------------
    # DELETE ATTENDANCE
    # --------------------------------------------------------

    st.subheader("🗑️ Delete Attendance")

    if attendance:

        attendance_options = {
            f'ID {record["id"]} - '
            f'Student {record["student_id"]} - '
            f'Date {record["date"]}':
            record
            for record in attendance
        }

        selected_record = st.selectbox(
            "Select Attendance to Delete",
            list(attendance_options.keys()),
            key="delete_attendance_select"
        )

        record = attendance_options[selected_record]

        if st.button("Delete Attendance"):

            response = requests.delete(
                f'{API_URL}/attendance/{record["id"]}'
            )

            if response.status_code == 200:

                st.success(
                    "Attendance deleted successfully!"
                )

                st.rerun()

            else:

                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)