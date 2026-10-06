import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date

import requests
import streamlit as st

from common.constants import DAYS_OF_WEEK

# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Student Attendance System", page_icon="🎓", layout="wide"
)


# ============================================================
# THEME (UI ONLY)
# ============================================================

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:wght@500;600;700&display=swap');

:root {
    --pine: #10302B;
    --pine-2: #17433C;
    --accent: #1B6B5A;
    --accent-dark: #145244;
    --paper: #F4F5F2;
    --surface: #FFFFFF;
    --line: #DDE2DC;
    --ink: #1C2A26;
    --muted: #62716B;
    --present: #1E7A4F;
    --absent: #B23A3A;
}

html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', -apple-system, 'Segoe UI', sans-serif;
    color: var(--ink);
}

.stApp { background: var(--paper); }

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1180px;
}

/* ---------- Headings ---------- */
h1, h2, h3 {
    font-family: 'Source Serif 4', Georgia, serif !important;
    color: var(--ink);
    letter-spacing: -0.01em;
}

h3 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-top: 0.4rem;
    padding-bottom: 0.35rem;
}

.page-head {
    padding: 0.2rem 0 1.1rem 0;
    margin-bottom: 1.4rem;
    border-bottom: 1px solid var(--line);
}
.page-head h1 {
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0;
    padding: 0;
    line-height: 1.15;
}
.page-head p {
    margin: 0.45rem 0 0 0;
    color: var(--muted);
    font-size: 0.98rem;
}

hr { border-color: var(--line) !important; margin: 1.6rem 0 !important; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--pine) 0%, var(--pine-2) 100%);
    border-right: none;
}
[data-testid="stSidebar"] * { color: #D5E2DD; }

.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.4rem 0.2rem 1.3rem 0.2rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}
.brand-mark {
    width: 40px; height: 40px;
    border-radius: 10px;
    background: #E9D9A6;
    color: var(--pine) !important;
    font-family: 'Source Serif 4', Georgia, serif;
    font-weight: 700;
    font-size: 1.25rem;
    display: flex; align-items: center; justify-content: center;
}
.brand-name {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #FFFFFF !important;
    line-height: 1.2;
}
.brand-sub { font-size: 0.78rem; color: #93ADA5 !important; }

[data-testid="stSidebar"] [role="radiogroup"] { gap: 0.2rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    width: 100%;
    padding: 0.6rem 0.85rem;
    border-radius: 8px;
    border-left: 3px solid transparent;
    cursor: pointer;
    transition: background 0.15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label p {
    font-size: 0.95rem;
    font-weight: 500;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: rgba(255,255,255,0.13);
    border-left-color: #E9D9A6;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 600;
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] p {
    color: var(--muted);
    font-size: 0.88rem;
    font-weight: 500;
}
[data-testid="stMetricValue"] {
    font-family: 'Source Serif 4', Georgia, serif;
    font-weight: 700;
    color: var(--ink);
}

/* ---------- Forms & inputs ---------- */
[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
}

[data-testid="stWidgetLabel"] p {
    font-size: 0.86rem;
    font-weight: 500;
    color: var(--muted);
}

[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="base-input"] {
    border-radius: 8px !important;
    background-color: var(--surface) !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="select"]:focus-within > div {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* ---------- Buttons ---------- */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: var(--accent);
    color: #FFFFFF;
    border: 1px solid var(--accent);
    border-radius: 8px;
    padding: 0.5rem 1.3rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    transition: background 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--accent-dark);
    border-color: var(--accent-dark);
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(16,48,43,0.22);
}
.stButton > button:focus-visible,
[data-testid="stFormSubmitButton"] > button:focus-visible {
    outline: 2px solid #E9D9A6;
    outline-offset: 2px;
    color: #FFFFFF;
}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
    background: var(--surface);
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--line);
}

/* ---------- Attendance radios (main area) ---------- */
.block-container [role="radiogroup"][aria-label] { gap: 1rem; }

/* ---------- Date input ---------- */
[data-testid="stDateInput"] input { font-weight: 500; }

/* ---------- Light rendering everywhere ---------- */
.stApp { color-scheme: light; }

/* ---------- Input text ---------- */
[data-baseweb="input"] input,
[data-baseweb="base-input"] input,
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    caret-color: var(--accent);
}
input::placeholder {
    color: #9AA6A1 !important;
    -webkit-text-fill-color: #9AA6A1 !important;
}

/* ---------- Selectbox (closed state) ---------- */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid var(--line) !important;
    border-radius: 8px !important;
    min-height: 42px;
}
[data-baseweb="select"] > div * {
    background-color: transparent !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
}
[data-baseweb="select"] input { caret-color: var(--accent); }
[data-baseweb="select"] svg { fill: var(--muted) !important; }

/* ---------- Dropdown menus (search + current option) ---------- */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul[role="listbox"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
}
[data-baseweb="popover"] ul[role="listbox"] {
    border: 1px solid var(--line);
    box-shadow: 0 8px 24px rgba(16,48,43,0.12);
}
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {
    background: #FFFFFF !important;
    color: var(--ink) !important;
}
[data-baseweb="popover"] li *,
[data-baseweb="popover"] [role="option"] * {
    background: transparent !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
}
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover {
    background: #EEF4F1 !important;
}
/* currently selected / highlighted option: light green, not black */
[data-baseweb="popover"] li[aria-selected="true"],
[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: #DCEBE6 !important;
    box-shadow: inset 3px 0 0 var(--accent);
    font-weight: 600;
}

/* ---------- Date picker ---------- */
[data-baseweb="calendar"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
[data-baseweb="calendar"] * {
    background-color: transparent !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    border-color: transparent !important;
}
/* month / year header and arrows */
[data-baseweb="calendar"] button,
[data-baseweb="calendar"] [role="button"] {
    border-radius: 8px !important;
}
[data-baseweb="calendar"] button:hover,
[data-baseweb="calendar"] [role="button"]:hover {
    background-color: #E6EFEC !important;
}
[data-baseweb="calendar"] svg { fill: var(--muted) !important; }

/* selected day */
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [aria-selected="true"]:hover {
    background-color: var(--accent) !important;
    border-radius: 8px !important;
}
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [aria-selected="true"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* disabled days */
[data-baseweb="calendar"] [aria-disabled="true"],
[data-baseweb="calendar"] [aria-disabled="true"] * {
    color: #B8C0BC !important;
    -webkit-text-fill-color: #B8C0BC !important;
}

/* month/year dropdown inside the calendar */
[data-baseweb="calendar"] [data-baseweb="select"] > div {
    border: none !important;
    background: transparent !important;
}

/* ---------- Calendar: day cells are painted by ::before / ::after ---------- */
/* clears the black blocks (empty cells before/after the month) and the black focus circle */
[data-baseweb="calendar"] *::before,
[data-baseweb="calendar"] *::after {
    background-color: transparent !important;
    border-color: transparent !important;
    box-shadow: none !important;
}
[data-baseweb="calendar"] [role="gridcell"],
[data-baseweb="calendar"] [role="gridcell"] > div,
[data-baseweb="calendar"] [role="row"],
[data-baseweb="calendar"] [role="grid"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* hovered / keyboard-focused day: soft green circle */
[data-baseweb="calendar"] [role="gridcell"]:hover::after,
[data-baseweb="calendar"] [role="gridcell"]:focus::after,
[data-baseweb="calendar"] [role="gridcell"]:focus-within::after {
    background-color: #E6EFEC !important;
    border-color: var(--accent) !important;
}

/* selected day: accent green circle instead of Streamlit's red */
[data-baseweb="calendar"] [aria-selected="true"]::after,
[data-baseweb="calendar"] [aria-selected="true"]:hover::after,
[data-baseweb="calendar"] [aria-selected="true"]:focus::after {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}
[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: transparent !important;
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


def page_header(title, subtitle=""):
    st.markdown(
        f'<div class="page-head"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
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

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-mark">A</div>
        <div>
            <div class="brand-name">Attendance</div>
            <div class="brand-sub">Student records</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Students", "Classes", "Teachers", "Timetable", "Attendance"],
    label_visibility="collapsed",
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":
    page_header(
        "Attendance dashboard",
        "Select a date and choose how you want to view the attendance.",
    )

    # --------------------------------------------------------
    # GET DATA
    # --------------------------------------------------------

    students = get_data("/students/")
    teachers = get_data("/teachers/")
    classes = get_data("/classes/")
    timetables = get_data("/timetables/")
    attendance = get_data("/attendance/")

    # --------------------------------------------------------
    # FILTER OPTIONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        selected_date = st.date_input(
            "Select date", value=date.today(), key="dashboard_date"
        )

    with col2:
        view_by = st.selectbox(
            "View attendance by", ["Student", "Teacher"], key="dashboard_view_by"
        )

    st.divider()

    selected_date_string = selected_date.isoformat()

    student_lookup = {student["id"]: student["name"] for student in students}

    teacher_lookup = {teacher["id"]: teacher["name"] for teacher in teachers}

    class_lookup = {classroom["id"]: classroom["name"] for classroom in classes}

    timetable_lookup = {timetable["id"]: timetable for timetable in timetables}

    filtered_attendance = [
        record for record in attendance if record["date"] == selected_date_string
    ]

    # Attendance lookup makes it easy to find a student's status
    # for a particular timetable on the selected date.
    attendance_lookup = {
        (record["student_id"], record["timetable_id"]): record["status"]
        for record in filtered_attendance
    }

    # --------------------------------------------------------
    # STUDENT VIEW
    # --------------------------------------------------------

    if view_by == "Student":
        st.subheader("Student attendance")

        class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom["id"]
            for classroom in classes
        }

        if not class_options:
            st.info("No classes found.")
        else:
            selected_class_label = st.selectbox(
                "Class", list(class_options.keys()), key="dashboard_student_class"
            )
            selected_class_id = class_options[selected_class_label]

            class_students = get_data(f"/classes/{selected_class_id}/students")

            class_timetables = [
                timetable
                for timetable in timetables
                if timetable.get("class_id") == selected_class_id
            ]

            class_timetables.sort(
                key=lambda item: (item.get("period", 0), item.get("subject", ""))
            )

            show_complete_table = st.checkbox(
                "Show complete table", key="dashboard_student_complete"
            )

            if not class_students:
                st.info("No students are currently assigned to this class.")
            elif not class_timetables:
                st.info("No timetable entries found for this class.")
            elif show_complete_table:
                # ------------------------------------------------
                # COMPLETE CLASS TABLE
                # One row = one student, one column = one period.
                # ------------------------------------------------
                table_data = []

                period_columns = []
                for timetable in class_timetables:
                    period = timetable["period"]
                    if period not in period_columns:
                        period_columns.append(period)

                period_columns.sort()

                for student in class_students:
                    row = {"Student": student["name"]}

                    for period in period_columns:
                        period_entries = [
                            timetable
                            for timetable in class_timetables
                            if timetable["period"] == period
                        ]

                        cell_values = []
                        for timetable in period_entries:
                            status = attendance_lookup.get(
                                (student["id"], timetable["id"])
                            )

                            status_text = (
                                "🟢 Present"
                                if status is True
                                else "🔴 Absent"
                                if status is False
                                else "—"
                            )

                            cell_values.append(f"{timetable['subject']}: {status_text}")

                        row[f"Period {period}"] = (
                            "\n".join(cell_values) if cell_values else "—"
                        )

                    table_data.append(row)

                st.dataframe(table_data, use_container_width=True, hide_index=True)

            else:
                # ------------------------------------------------
                # SEARCH FOR ONE STUDENT
                # ------------------------------------------------
                # Streamlit's selectbox is searchable, so the user
                # can type a name while still seeing all available
                # students in the dropdown.
                student_options = {
                    f"{student['name']} (ID {student['id']})": student
                    for student in class_students
                }

                selected_student_label = st.selectbox(
                    "Search student",
                    list(student_options.keys()),
                    index=None,
                    placeholder="Type a student name...",
                    key="dashboard_student_result",
                )

                if selected_student_label is not None:
                    selected_student = student_options[selected_student_label]

                    student_table = []

                    for timetable in class_timetables:
                        status = attendance_lookup.get(
                            (selected_student["id"], timetable["id"])
                        )

                        student_table.append(
                            {
                                "Period": timetable["period"],
                                "Subject": timetable["subject"],
                                "Day": timetable["day"],
                                "Status": (
                                    "🟢 Present"
                                    if status is True
                                    else "🔴 Absent"
                                    if status is False
                                    else "— No record"
                                ),
                            }
                        )

                    st.markdown(
                        f"**{selected_student['name']} — "
                        f"{selected_date.strftime('%d %B %Y')}**"
                    )
                    st.dataframe(
                        student_table, use_container_width=True, hide_index=True
                    )

    # --------------------------------------------------------
    # TEACHER VIEW
    # --------------------------------------------------------

    else:
        st.subheader("Teacher attendance")

        show_complete_table = st.checkbox(
            "Show complete table", key="dashboard_teacher_complete"
        )

        if not teachers:
            st.info("No teachers found.")
        else:
            if show_complete_table:
                teacher_table = []

                for teacher in teachers:
                    teacher_timetables = [
                        timetable
                        for timetable in timetables
                        if timetable["teacher_id"] == teacher["id"]
                    ]

                    for timetable in teacher_timetables:
                        records = [
                            record
                            for record in filtered_attendance
                            if record["timetable_id"] == timetable["id"]
                        ]

                        present = sum(
                            1 for record in records if record["status"] is True
                        )
                        absent = sum(
                            1 for record in records if record["status"] is False
                        )

                        teacher_table.append(
                            {
                                "Teacher": teacher["name"],
                                "Class": class_lookup.get(
                                    timetable.get("class_id"),
                                    f"Class {timetable.get('class_id', '—')}",
                                ),
                                "Period": timetable["period"],
                                "Subject": timetable["subject"],
                                "Present": present,
                                "Absent": absent,
                                "Total": present + absent,
                            }
                        )

                teacher_table.sort(
                    key=lambda row: (row["Teacher"], row["Period"], row["Subject"])
                )

                if teacher_table:
                    st.dataframe(
                        teacher_table, use_container_width=True, hide_index=True
                    )
                else:
                    st.info(
                        f"No teacher attendance records found for "
                        f"{selected_date.strftime('%d %B %Y')}."
                    )

            else:
                # ------------------------------------------------
                # SEARCH FOR ONE TEACHER
                # ------------------------------------------------
                # The selectbox is searchable and keeps all teachers
                # visible when the dropdown is opened.
                teacher_options = {
                    f"{teacher['name']} (ID {teacher['id']})": teacher
                    for teacher in teachers
                }

                selected_teacher_label = st.selectbox(
                    "Search teacher",
                    list(teacher_options.keys()),
                    index=None,
                    placeholder="Type a teacher name...",
                    key="dashboard_teacher_result",
                )

                if selected_teacher_label is not None:
                    selected_teacher = teacher_options[selected_teacher_label]

                    teacher_timetables = [
                        timetable
                        for timetable in timetables
                        if timetable["teacher_id"] == selected_teacher["id"]
                    ]

                    teacher_table = []

                    for timetable in teacher_timetables:
                        records = [
                            record
                            for record in filtered_attendance
                            if record["timetable_id"] == timetable["id"]
                        ]

                        present = sum(
                            1 for record in records if record["status"] is True
                        )
                        absent = sum(
                            1 for record in records if record["status"] is False
                        )

                        teacher_table.append(
                            {
                                "Period": timetable["period"],
                                "Class": class_lookup.get(
                                    timetable.get("class_id"),
                                    f"Class {timetable.get('class_id', '—')}",
                                ),
                                "Subject": timetable["subject"],
                                "Present": present,
                                "Absent": absent,
                                "Total": present + absent,
                            }
                        )

                    teacher_table.sort(
                        key=lambda row: (row["Period"], row["Class"], row["Subject"])
                    )

                    st.markdown(
                        f"**{selected_teacher['name']} — "
                        f"{selected_date.strftime('%d %B %Y')}**"
                    )

                    if teacher_table:
                        st.dataframe(
                            teacher_table, use_container_width=True, hide_index=True
                        )
                    else:
                        st.caption(
                            f"No timetable entries found for "
                            f"{selected_teacher['name']}."
                        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.divider()

    st.subheader("Daily summary")

    present_count = sum(1 for record in filtered_attendance if record["status"] is True)

    absent_count = sum(1 for record in filtered_attendance if record["status"] is False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total records", len(filtered_attendance))

    with col2:
        st.metric("Present", present_count)

    with col3:
        st.metric("Absent", absent_count)


# ============================================================
# STUDENTS
# ============================================================

elif menu == "Students":
    page_header("Students", "View, add, update and remove student records.")

    # --------------------------------------------------------
    # VIEW STUDENTS
    # --------------------------------------------------------

    st.subheader("All students")

    students = get_data("/students/")

    if students:
        st.dataframe(students, use_container_width=True)

    else:
        st.info("No students found.")

    st.divider()

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    st.subheader("Add student")

    with st.form("add_student_form"):
        name = st.text_input("Student Name")

        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            response = requests.post(
                f"{API_URL}/students/", json={"name": name, "email": email}
            )

            if response.status_code == 200:
                st.success("Student added successfully!")

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

    st.subheader("Update student")

    if students:
        student_options = {
            f"{student['id']} - {student['name']}": student for student in students
        }

        selected_student = st.selectbox(
            "Select Student", list(student_options.keys()), key="update_student_select"
        )

        student = student_options[selected_student]

        with st.form("update_student_form"):
            new_name = st.text_input("Name", value=student["name"])

            new_email = st.text_input("Email", value=student["email"])

            update_button = st.form_submit_button("Update Student")

            if update_button:
                response = requests.put(
                    f"{API_URL}/students/{student['id']}",
                    json={"name": new_name, "email": new_email},
                )

                if response.status_code == 200:
                    st.success("Student updated successfully!")

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

    st.subheader("Delete student")

    if students:
        student_options = {
            f"{student['id']} - {student['name']}": student for student in students
        }

        selected_student = st.selectbox(
            "Select Student to Delete",
            list(student_options.keys()),
            key="delete_student_select",
        )

        student = student_options[selected_student]

        if st.button("Delete Student"):
            response = requests.delete(f"{API_URL}/students/{student['id']}")

            if response.status_code == 200:
                st.success("Student deleted successfully!")

                st.rerun()

            else:
                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."

                st.error(error)


# ============================================================
# CLASSES
# ============================================================

elif menu == "Classes":
    page_header(
        "Classes", "Create classes and manage which students belong to each one."
    )

    classes = get_data("/classes/")
    students = get_data("/students/")

    # --------------------------------------------------------
    # VIEW CLASSES
    # --------------------------------------------------------

    st.subheader("All classes")

    if classes:
        st.dataframe(classes, use_container_width=True, hide_index=True)
    else:
        st.info("No classes found.")

    st.divider()

    # --------------------------------------------------------
    # ADD CLASS
    # --------------------------------------------------------

    st.subheader("Add class")

    with st.form("add_class_form"):
        class_name = st.text_input("Class Name")

        submitted = st.form_submit_button("Add Class")

        if submitted:
            response = requests.post(f"{API_URL}/classes/", json={"name": class_name})

            if response.status_code == 200:
                st.success("Class added successfully!")
                st.rerun()
            else:
                try:
                    error = response.json()["detail"]
                except Exception:
                    error = "Something went wrong."
                st.error(error)

    st.divider()

    # --------------------------------------------------------
    # MANAGE STUDENTS IN CLASS
    # --------------------------------------------------------

    st.subheader("Manage students in class")

    if classes:
        class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom
            for classroom in classes
        }

        selected_class_name = st.selectbox(
            "Select Class", list(class_options.keys()), key="manage_class_select"
        )

        selected_class = class_options[selected_class_name]
        class_id = selected_class["id"]

        class_students = get_data(f"/classes/{class_id}/students")

        current_student_ids = {student["id"] for student in class_students}

        st.write("**Students currently in this class:**")

        if class_students:
            st.dataframe(class_students, use_container_width=True, hide_index=True)
        else:
            st.info("No students have been added to this class yet.")

        available_students = [
            student for student in students if student["id"] not in current_student_ids
        ]

        st.markdown("### Add student")

        if available_students:
            student_options = {
                f"{student['id']} - {student['name']}": student["id"]
                for student in available_students
            }

            selected_student_name = st.selectbox(
                "Select Student",
                list(student_options.keys()),
                key="add_student_to_class_select",
            )

            if st.button("Add Student to Class", key="add_student_to_class_button"):
                response = requests.post(
                    f"{API_URL}/classes/{class_id}/students/{student_options[selected_student_name]}"
                )

                if response.status_code == 200:
                    st.success("Student added to class successfully!")
                    st.rerun()
                else:
                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."
                    st.error(error)

        else:
            if students:
                st.info("All students are already in this class.")
            else:
                st.warning("Add students before assigning them to a class.")

        st.markdown("### Remove student")

        if class_students:
            remove_options = {
                f"{student['id']} - {student['name']}": student["id"]
                for student in class_students
            }

            selected_remove_name = st.selectbox(
                "Select Student to Remove",
                list(remove_options.keys()),
                key="remove_student_from_class_select",
            )

            if st.button(
                "Remove Student from Class", key="remove_student_from_class_button"
            ):
                response = requests.delete(
                    f"{API_URL}/classes/{class_id}/students/{remove_options[selected_remove_name]}"
                )

                if response.status_code == 200:
                    st.success("Student removed from class successfully!")
                    st.rerun()
                else:
                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."
                    st.error(error)

    else:
        st.warning("Create a class before adding students to it.")

    st.divider()

    # --------------------------------------------------------
    # DELETE CLASS
    # --------------------------------------------------------

    st.subheader("Delete class")

    if classes:
        delete_class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom
            for classroom in classes
        }

        selected_delete_class = st.selectbox(
            "Select Class to Delete",
            list(delete_class_options.keys()),
            key="delete_class_select",
        )

        classroom = delete_class_options[selected_delete_class]

        if st.button("Delete Class", key="delete_class_button"):
            response = requests.delete(f"{API_URL}/classes/{classroom['id']}")

            if response.status_code == 200:
                st.success("Class deleted successfully!")
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
    page_header("Teachers", "View, add, update and remove teacher records.")

    # --------------------------------------------------------
    # VIEW TEACHERS
    # --------------------------------------------------------

    st.subheader("All teachers")

    teachers = get_data("/teachers/")

    if teachers:
        st.dataframe(teachers, use_container_width=True)

    else:
        st.info("No teachers found.")

    st.divider()

    # --------------------------------------------------------
    # ADD TEACHER
    # --------------------------------------------------------

    st.subheader("Add teacher")

    with st.form("add_teacher_form"):
        name = st.text_input("Teacher Name")

        email = st.text_input("Teacher Email")

        submitted = st.form_submit_button("Add Teacher")

        if submitted:
            response = requests.post(
                f"{API_URL}/teachers/", json={"name": name, "email": email}
            )

            if response.status_code == 200:
                st.success("Teacher added successfully!")

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

    st.subheader("Update teacher")

    if teachers:
        teacher_options = {
            f"{teacher['id']} - {teacher['name']}": teacher for teacher in teachers
        }

        selected_teacher = st.selectbox(
            "Select Teacher", list(teacher_options.keys()), key="update_teacher_select"
        )

        teacher = teacher_options[selected_teacher]

        with st.form("update_teacher_form"):
            new_name = st.text_input("Name", value=teacher["name"])

            new_email = st.text_input("Email", value=teacher["email"])

            update_button = st.form_submit_button("Update Teacher")

            if update_button:
                response = requests.put(
                    f"{API_URL}/teachers/{teacher['id']}",
                    json={"name": new_name, "email": new_email},
                )

                if response.status_code == 200:
                    st.success("Teacher updated successfully!")

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

    st.subheader("Delete teacher")

    if teachers:
        teacher_options = {
            f"{teacher['id']} - {teacher['name']}": teacher for teacher in teachers
        }

        selected_teacher = st.selectbox(
            "Select Teacher to Delete",
            list(teacher_options.keys()),
            key="delete_teacher_select",
        )

        teacher = teacher_options[selected_teacher]

        if st.button("Delete Teacher"):
            response = requests.delete(f"{API_URL}/teachers/{teacher['id']}")

            if response.status_code == 200:
                st.success("Teacher deleted successfully!")

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
    page_header("Timetable", "Schedule classes by teacher, subject, day and period.")

    teachers = get_data("/teachers/")
    classes = get_data("/classes/")
    timetables = get_data("/timetables/")

    # --------------------------------------------------------
    # VIEW TIMETABLE
    # --------------------------------------------------------

    st.subheader("All classes")

    if timetables:
        st.dataframe(timetables, use_container_width=True)

    else:
        st.info("No timetable entries found.")

    st.divider()

    # --------------------------------------------------------
    # ADD TIMETABLE
    # --------------------------------------------------------

    st.subheader("Add class")

    if teachers and classes:
        teacher_options = {
            f"{teacher['id']} - {teacher['name']}": teacher["id"]
            for teacher in teachers
        }

        class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom["id"]
            for classroom in classes
        }

        with st.form("add_timetable_form"):
            selected_teacher = st.selectbox("Teacher", list(teacher_options.keys()))

            selected_class = st.selectbox("Class", list(class_options.keys()))

            subject = st.text_input("Subject")

            day = st.selectbox("Day", DAYS_OF_WEEK)

            period = st.number_input("Period", min_value=1, max_value=10, step=1)

            submitted = st.form_submit_button("Add Class")

            if submitted:
                response = requests.post(
                    f"{API_URL}/timetables/",
                    json={
                        "teacher_id": teacher_options[selected_teacher],
                        "class_id": class_options[selected_class],
                        "subject": subject,
                        "day": day,
                        "period": period,
                    },
                )

                if response.status_code == 200:
                    st.success("Class added successfully!")

                    st.rerun()

                else:
                    try:
                        error = response.json()["detail"]
                    except Exception:
                        error = "Something went wrong."

                    st.error(error)

    else:
        st.warning(
            "Add at least one teacher and one class before creating a timetable."
        )

    st.divider()

    # --------------------------------------------------------
    # UPDATE TIMETABLE
    # --------------------------------------------------------

    st.subheader("Update class")

    if timetables and teachers and classes:
        teacher_options = {
            f"{teacher['id']} - {teacher['name']}": teacher["id"]
            for teacher in teachers
        }

        class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom["id"]
            for classroom in classes
        }

        timetable_options = {
            f"{item['id']} - {item['subject']} - {item['day']}": item
            for item in timetables
        }

        selected_timetable = st.selectbox(
            "Select Timetable",
            list(timetable_options.keys()),
            key="update_timetable_select",
        )

        timetable = timetable_options[selected_timetable]

        teacher_names = list(teacher_options.keys())
        class_names = list(class_options.keys())

        current_teacher = next(
            (
                name
                for name, teacher_id in teacher_options.items()
                if teacher_id == timetable["teacher_id"]
            ),
            teacher_names[0],
        )

        current_class = next(
            (
                name
                for name, class_id in class_options.items()
                if class_id == timetable["class_id"]
            ),
            class_names[0],
        )

        with st.form("update_timetable_form"):
            selected_teacher = st.selectbox(
                "Teacher", teacher_names, index=teacher_names.index(current_teacher)
            )

            selected_class = st.selectbox(
                "Class", class_names, index=class_names.index(current_class)
            )

            subject = st.text_input("Subject", value=timetable["subject"])

            current_day_index = (
                DAYS_OF_WEEK.index(timetable["day"])
                if timetable["day"] in DAYS_OF_WEEK
                else 0
            )

            day = st.selectbox("Day", DAYS_OF_WEEK, index=current_day_index)

            period = st.number_input(
                "Period", min_value=1, max_value=10, value=timetable["period"], step=1
            )

            update_button = st.form_submit_button("Update Class")

            if update_button:
                response = requests.put(
                    f"{API_URL}/timetables/{timetable['id']}",
                    json={
                        "teacher_id": teacher_options[selected_teacher],
                        "class_id": class_options[selected_class],
                        "subject": subject,
                        "day": day,
                        "period": period,
                    },
                )

                if response.status_code == 200:
                    st.success("Class updated successfully!")

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

    st.subheader("Delete class")

    if timetables:
        timetable_options = {
            f"{item['id']} - {item['subject']} - {item['day']}": item
            for item in timetables
        }

        selected_timetable = st.selectbox(
            "Select Timetable to Delete",
            list(timetable_options.keys()),
            key="delete_timetable_select",
        )

        timetable = timetable_options[selected_timetable]

        if st.button("Delete Class"):
            response = requests.delete(f"{API_URL}/timetables/{timetable['id']}")

            if response.status_code == 200:
                st.success("Class deleted successfully!")

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
    page_header(
        "Attendance", "Mark or correct attendance for a class, subject and date."
    )

    classes = get_data("/classes/")
    attendance = get_data("/attendance/")

    # --------------------------------------------------------
    # MARK ATTENDANCE
    # --------------------------------------------------------

    st.subheader("Mark attendance")

    if not classes:
        st.warning("No classes found.")

    else:
        class_options = {
            f"{classroom['id']} - {classroom['name']}": classroom["id"]
            for classroom in classes
        }

        selected_class = st.selectbox(
            "Class", list(class_options.keys()), key="attendance_class"
        )

        class_id = class_options[selected_class]

        # ----------------------------------------------------
        # GET TIMETABLES FOR SELECTED CLASS
        # ----------------------------------------------------

        timetables = get_data(f"/timetables/class/{class_id}")

        if not timetables:
            st.warning("No timetable entries found for this class.")

        else:
            timetable_options = {
                f"{item['subject']} - {item['day']} - Period {item['period']}": item
                for item in timetables
            }

            selected_timetable = st.selectbox(
                "Subject", list(timetable_options.keys()), key="attendance_timetable"
            )

            timetable = timetable_options[selected_timetable]

            timetable_id = timetable["id"]

            attendance_date = st.date_input(
                "Date", value=date.today(), key="attendance_date"
            )

            # ------------------------------------------------
            # GET STUDENTS IN SELECTED CLASS
            # ------------------------------------------------

            students = get_data(f"/classes/{class_id}/students")

            if not students:
                st.info("No students are currently assigned to this class.")

            else:
                st.divider()

                st.subheader(f"Students — {selected_class}")

                st.write(f"Subject: **{timetable['subject']}**")
                st.write(f"Day: **{timetable['day']}**")
                st.write(f"Period: **{timetable['period']}**")
                st.write(f"Date: **{attendance_date.strftime('%d %B %Y')}**")

                st.divider()

                # ------------------------------------------------
                # FIND EXISTING ATTENDANCE
                # ------------------------------------------------

                selected_date_string = attendance_date.isoformat()

                existing_attendance = {
                    record["student_id"]: record
                    for record in attendance
                    if (
                        record["timetable_id"] == timetable_id
                        and record["date"] == selected_date_string
                    )
                }

                attendance_status = {}

                # ------------------------------------------------
                # DISPLAY STUDENTS
                # ------------------------------------------------

                # Keep the selected status in Streamlit session state.
                # Each student gets two real buttons instead of radio buttons.
                #
                # The first button is always green (Present).
                # The second button is always red (Absent).
                # A check mark shows which status is currently selected.

                st.markdown(
                    """
                    <style>
                    /* Attendance action buttons */
                    [data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
                        background: #1E7A4F !important;
                        border-color: #1E7A4F !important;
                        color: #FFFFFF !important;
                    }

                    [data-testid="stButton"] button[data-testid="stBaseButton-secondary"] {
                        background: #B23A3A !important;
                        border-color: #B23A3A !important;
                        color: #FFFFFF !important;
                    }

                    [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
                        background: #17633F !important;
                        border-color: #17633F !important;
                    }

                    [data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover {
                        background: #922F2F !important;
                        border-color: #922F2F !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                # Table header
                header_col1, header_col2, header_col3 = st.columns([5, 1.5, 1.5])

                with header_col1:
                    st.markdown("**Student**")

                with header_col2:
                    st.markdown("**Present**")

                with header_col3:
                    st.markdown("**Absent**")

                st.divider()

                for student in students:
                    student_id = student["id"]
                    student_name = student["name"]

                    existing_record = existing_attendance.get(student_id)

                    # Create a unique state key for this student/date/class/subject.
                    state_key = (
                        f"attendance_status_{class_id}_"
                        f"{timetable_id}_"
                        f"{selected_date_string}_"
                        f"{student_id}"
                    )

                    # Load the database value the first time this row is shown.
                    if state_key not in st.session_state:
                        st.session_state[state_key] = (
                            existing_record["status"]
                            if existing_record is not None
                            else True
                        )

                    current_status = st.session_state[state_key]

                    row_col1, row_col2, row_col3 = st.columns([5, 1.5, 1.5])

                    with row_col1:
                        st.write(student_name)

                    with row_col2:
                        if st.button(
                            "✓ Present" if current_status else "Present",
                            key=f"present_{state_key}",
                            type="primary",
                            use_container_width=True,
                        ):
                            st.session_state[state_key] = True
                            st.rerun()

                    with row_col3:
                        if st.button(
                            "✓ Absent" if not current_status else "Absent",
                            key=f"absent_{state_key}",
                            type="secondary",
                            use_container_width=True,
                        ):
                            st.session_state[state_key] = False
                            st.rerun()

                    attendance_status[student_id] = st.session_state[state_key]

                st.divider()

                # ------------------------------------------------
                # SAVE ATTENDANCE
                # ------------------------------------------------

                if st.button("Save Attendance", use_container_width=True):
                    success_count = 0
                    error_found = False

                    for student in students:
                        student_id = student["id"]

                        payload = {
                            "student_id": student_id,
                            "timetable_id": timetable_id,
                            "class_id": class_id,
                            "date": selected_date_string,
                            "status": attendance_status[student_id],
                        }

                        existing_record = existing_attendance.get(student_id)

                        if existing_record is None:
                            response = requests.post(
                                f"{API_URL}/attendance/", json=payload
                            )

                        else:
                            response = requests.put(
                                f"{API_URL}/attendance/{existing_record['id']}",
                                json=payload,
                            )

                        if response.status_code == 200:
                            success_count += 1

                        else:
                            error_found = True

                            try:
                                error = response.json()["detail"]
                            except Exception:
                                error = "Something went wrong."

                            st.error(f"{student['name']}: {error}")

                    if not error_found:
                        st.success(
                            f"Attendance saved successfully "
                            f"for {success_count} students!"
                        )

                        st.rerun()

                # ------------------------------------------------
                # CURRENT ATTENDANCE SUMMARY
                # ------------------------------------------------

                st.divider()

                st.subheader("Attendance summary")

                present_count = sum(
                    1 for status in attendance_status.values() if status
                )

                absent_count = sum(
                    1 for status in attendance_status.values() if not status
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total students", len(students))

                with col2:
                    st.metric("Present", present_count)

                with col3:
                    st.metric("Absent", absent_count)
