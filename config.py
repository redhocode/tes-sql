import pyodbc
import streamlit as st

def config():
    # SQL Server connection details
    SERVER = '127.0.0.1'
    DATABASE = 'tes'
    USERNAME = 'sa'
    PASSWORD = 'myPass123!'

    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=no;TrustServerCertificate=yes;'

    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        st.error(f"Kesalahan koneksi: {e}")
        return None
