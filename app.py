import pyodbc
import streamlit as st
import pandas as pd

# Fungsi untuk konfigurasi koneksi ke SQL Server
def config():
    # SQL Server connection details
    SERVER = '127.0.0.1'  # Ganti dengan alamat server Anda
    DATABASE = 'tes'      # Ganti dengan nama database Anda
    USERNAME = 'sa'       # Ganti dengan username Anda
    PASSWORD = 'myPass123!'  # Ganti dengan password Anda

    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=no;TrustServerCertificate=yes;'

    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        st.error(f"Kesalahan koneksi: {e}")
        return None

# Fungsi utama Streamlit untuk aplikasi
def app():
    st.title("Tes SQL - Karyawan Baru")

    # Membuat koneksi ke database SQL Server
    conn = config()
    if conn is None:
        return  # Jika koneksi gagal, berhenti eksekusi aplikasi

    cursor = conn.cursor()

    # Tampilkan tabel 'employees' dan 'departments' sebagai referensi
    st.subheader("Tabel 'employees'")
    query_employees = "SELECT * FROM employees;"
    employees_df = pd.read_sql(query_employees, conn)
    st.dataframe(employees_df)  # Menampilkan tabel 'employees'

    st.subheader("Tabel 'departments'")
    query_departments = "SELECT * FROM departments;"
    departments_df = pd.read_sql(query_departments, conn)
    st.dataframe(departments_df)  # Menampilkan tabel 'departments'

    # Fitur untuk menguji query SQL yang dimasukkan oleh pengguna
    st.subheader("Uji Query SQL Anda")

    # Input area untuk query SQL
    user_query = st.text_area("Masukkan query SQL untuk diuji", height=200)

    # Menjalankan query jika tombol ditekan
    if st.button("Jalankan Query"):
        try:
            # Mengeksekusi query
            result_df = pd.read_sql(user_query, conn)
            # Menampilkan hasil query
            st.write("Hasil dari query yang dijalankan:")
            st.dataframe(result_df)  # Menampilkan hasil query dalam bentuk dataframe
        except Exception as e:
            # Menampilkan error jika query tidak valid
            st.error(f"Terjadi kesalahan: {e}")

    # 10 soal SQL, termasuk soal JOIN
    questions = [
        ("Tampilkan semua kolom dan data dari tabel employees.", "SELECT * FROM employees;"),
        ("Tampilkan hanya kolom 'name' dan 'age'.", "SELECT name, age FROM employees;"),
        ("Tampilkan nama dan umur karyawan yang berusia lebih dari 30 tahun.", "SELECT name, age FROM employees WHERE age > 30;"),
        ("Tampilkan nama karyawan yang berusia di bawah 25 tahun.", "SELECT name FROM employees WHERE age < 25;"),
        ("Tampilkan nama karyawan yang diurutkan berdasarkan umur secara menurun.", "SELECT name, age FROM employees ORDER BY age DESC;"),
        ("Tampilkan jumlah karyawan di setiap departemen.", "SELECT department, COUNT(*) FROM employees GROUP BY department;"),
        ("Tampilkan nama karyawan yang namanya dimulai dengan huruf 'A'.", "SELECT name FROM employees WHERE name LIKE 'A%';"),
        ("Tampilkan nama karyawan yang berusia lebih dari 30 tahun dan bekerja di departemen 'IT'.", "SELECT name FROM employees WHERE age > 30 AND department = 'IT';"),
        ("Tampilkan nama karyawan yang bekerja di departemen 'HR' atau 'Finance'.", "SELECT name FROM employees WHERE department IN ('HR', 'Finance');"),
        ("Tampilkan nama karyawan dan lokasi departemen mereka dengan menggabungkan tabel employees dan departments berdasarkan nama departemen.", 
         "SELECT employees.name, departments.location FROM employees INNER JOIN departments ON employees.department = departments.department_name;")
    ]

    score = 0  # Menyimpan skor

    # Menampilkan soal-soal dan mengecek jawaban
    for i, (question, correct_answer) in enumerate(questions, 1):
        st.subheader(f"Soal {i}")
        st.write(question)
        user_answer = st.text_area(f"Jawaban untuk Soal {i}", height=100)

        if st.button(f"Periksa Jawaban Soal {i}", key=f"check_{i}"):
            if user_answer.strip().lower() == correct_answer.strip().lower():
                st.success("Jawaban benar!")
                score += 1
            else:
                st.error("Jawaban salah.")
    
    # Menampilkan hasil akhir
    st.write(f"Skor Anda: {score} / 10")

    # Menutup koneksi
    conn.close()

if __name__ == "__main__":
    app()
