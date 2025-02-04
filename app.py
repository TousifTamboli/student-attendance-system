import streamlit as st
import mysql.connector

# Database connection function
from database import get_db_connection  

# Streamlit session state to manage login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user from database
        cursor.execute("SELECT username, password FROM faculty WHERE username=%s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_username, stored_password = user
            if password == stored_password:  # ✅ No Hashing (Direct Comparison)
                st.success("Login Successful!")
                st.session_state["logged_in"] = True
                
                # ✅ Redirect to attendance page
                st.switch_page("pages/attendance.py")
            else:
                st.error("Invalid password")
        else:
            st.error("User not found")

# Call login function in the main script
if __name__ == "__main__":
    login()
