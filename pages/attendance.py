import streamlit as st
import pandas as pd
from database import get_db_connection

def fetch_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, roll_no, course, year FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def save_attendance(date, attendance_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    for student_id, status in attendance_data.items():
        cursor.execute("""
            INSERT INTO attendance (student_id, date, status) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (student_id, date, status))
    
    conn.commit()
    conn.close()

def attendance_page():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please login first.")
        st.stop()

    st.title("Student Attendance System")
    date = st.date_input("Select Date")
    
    students = fetch_students()

    df = pd.DataFrame(students, columns=["Student ID", "Name", "Roll No", "Course", "Year"])

    attendance_status = {}
    st.write("### Mark Attendance for Students")

    for index, row in df.iterrows():
        status = st.radio(f"Attendance for {row['Name']} ({row['Roll No']})", ['P', 'A'], index=0, key=row['Student ID'])
        attendance_status[row['Student ID']] = status

    df["Attendance"] = df['Student ID'].map(attendance_status)

    st.dataframe(df, height=600)

    if st.button("Save All Attendance"):
        save_attendance(date, attendance_status)
        st.success("Attendance for all students saved successfully!")

attendance_page()
