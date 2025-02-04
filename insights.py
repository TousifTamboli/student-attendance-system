import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_db_connection

def fetch_attendance_data():
    conn = get_db_connection()
    query = "SELECT students.name, attendance.date, attendance.status FROM attendance JOIN students ON attendance.student_id = students.id"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def insights_page():
    if "logged_in" not in st.session_state:
        st.warning("Please login first.")
        return
    
    st.title("Student Attendance Insights")
    
    df = fetch_attendance_data()
    if df.empty:
        st.info("No attendance data available.")
        return
    
    st.write("### Attendance Data")
    st.dataframe(df)

    fig = px.histogram(df, x="name", color="status", title="Student Attendance Distribution", barmode="group")
    st.plotly_chart(fig)
