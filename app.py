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

def fetch_attendance_by_date(date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.student_id, s.name, s.roll_no, s.course, s.year, a.status 
        FROM students s
        LEFT JOIN attendance a ON s.student_id = a.student_id AND a.date = %s
    """, (date,))
    
    attendance_records = cursor.fetchall()
    conn.close()
    return attendance_records

def mark_attendance_page():
    st.title("Student Attendance System")
    date = st.date_input("📅 Select Date for Attendance")

    students = fetch_students()
    attendance_status = {}

    st.write("### Mark Attendance")
    for student_id, name, roll_no, course, year in students:
        status = st.radio(f"Attendance for {name} ({roll_no})", ['P', 'A'], index=0, key=student_id)
        attendance_status[student_id] = status

    if st.button("Save Attendance"):
        save_attendance(date, attendance_status)
        st.success("✅ Attendance saved successfully!")

def check_attendance_page():
    st.title("Check Attendance Records")
    date = st.date_input("📅 Select Date to View Attendance")
    
    if st.button("Fetch Attendance"):
        attendance_data = fetch_attendance_by_date(date)
        
        if attendance_data:
            df = pd.DataFrame(attendance_data, columns=["Student ID", "Name", "Roll No", "Course", "Year", "Status"])
            st.dataframe(df, height=600)
        else:
            st.warning("⚠️ No attendance records found for this date.")

def main():
    st.sidebar.title("Navigation")  # Only show "Navigation"
    page = st.sidebar.radio("", ["Mark Attendance", "Check Attendance"])  # Remove extra sections
    
    if page == "Mark Attendance":
        mark_attendance_page()
    elif page == "Check Attendance":
        check_attendance_page()

if __name__ == "__main__":
    main()
