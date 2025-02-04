import streamlit as st
import mysql.connector

from database import get_db_connection  

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
                
                st.switch_page("pages/attendance.py")
            else:
                st.error("Invalid password")
        else:
            st.error("User not found")

if __name__ == "__main__":
    login()
