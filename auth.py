import streamlit as st
import mysql.connector
from database import get_db_connection

def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO faculty (username, password_hash) VALUES (%s, %s)",
                           (username, password))  # Store password directly (not recommended for security)
            conn.commit()
            st.success("Registered Successfully! Please Login.")
        except mysql.connector.errors.IntegrityError:
            st.error("Username already exists!")
        cursor.close()
        conn.close()

def login():
    st.title("Faculty Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = mysql.connector.connect(
            host="localhost", user="root", password="tousiftamboli3", database="attendance_db"
        )
        cursor = conn.cursor()

        # Fetch user data
        cursor.execute("SELECT username, password FROM faculty WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[1]  # Stored password (directly in DB)
            if password == stored_password:  # Direct password comparison
                st.success("Login successful")

                # Redirect to attendance.py (Ensure it's in the pages/ directory)
                st.switch_page("pages/attendance.py")
            else:
                st.error("Invalid password")
        else:
            st.error("User not found")

        cursor.close()
        conn.close()

# Run the login function
login()
