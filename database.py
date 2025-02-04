import mysql.connector
import streamlit as st

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tousiftamboli3",
        database="attendance_db"
    )

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS faculty (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE,
                        password_hash VARCHAR(255))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        date DATE,
                        status ENUM('P', 'A'),
                        FOREIGN KEY(student_id) REFERENCES students(id))''')
    
    conn.commit()
    conn.close()