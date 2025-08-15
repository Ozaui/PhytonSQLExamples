import sqlite3
import os

def create_database():
    # Eğer database varsa sil. Risklidir dikkat et.
    if os.path.exists("students.db"):
        os.remove("students.db")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Foreign key desteğini aç
    cursor.execute("PRAGMA foreign_keys = ON;")

    return conn, cursor

def create_tables(cursor):
    # Öğrenci tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        StudentName VARCHAR(255) NOT NULL, 
        Surname VARCHAR(255) NOT NULL,
        age INTEGER NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        city VARCHAR(255) NOT NULL
    )
    ''')

    # Ders tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        CourseName VARCHAR(255) NOT NULL,
        instructor TEXT NOT NULL,
        credit INTEGER NOT NULL
    )
    ''')

    # Kayıt (öğrenci-ders ilişkisi) tablosu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
    )
    ''')

def insert_sample_data(cursor):
    students = [
        ("Alice", "Johnson", 20, "alice@gmail.com", "New York"),
        ("Bob", "Smith", 19, "bob@gmail.com", "İstanbul"),
        ("Carol", "White", 21, "carol@gmail.com", "Paris"),
        ("David", "Brown", 20, "david@gmail.com", "Ankara"),
        ("Emma", "Davis", 22, "emma@gmail.com", "İzmir"),
    ]
    cursor.executemany(
        "INSERT INTO Students (StudentName, Surname, age, email, city) VALUES (?,?,?,?,?)",
        students
    )

    courses = [
        ("Python", "Dr. Anderson", 3),
        ("Java", "Dr. Ecir", 4),
        ("C#", "Dr. Gökçe", 5)
    ]
    cursor.executemany(
        "INSERT INTO Courses (CourseName, instructor, credit) VALUES (?,?,?)",
        courses
    )

def basic_sql_query(cursor):
    # SELECT ALL
    cursor.execute("SELECT * FROM Students")
    records = cursor.fetchall()
    for row in records:
        print(row)

    # SELECT COLUMNS
    cursor.execute("SELECT StudentName FROM Students")
    records = cursor.fetchall()
    for row in records:
        print(row[0])

    # SELECT WHERE AGE
    print("--------------------------- age = 20 -----------------")
    cursor.execute("SELECT StudentName, Surname FROM Students WHERE age = 20")
    records = cursor.fetchall()
    for row in records:
        print(row[0], row[1])

    # ORDER BY
    print("--------------------------- ORDER BY age -----------------")
    cursor.execute("SELECT * FROM Students ORDER BY age")
    records = cursor.fetchall()
    for row in records:
        print(row[0], row[1])

def sql_update_delete_insert_operations(cursor):
    # Insert (id vermiyoruz)
    cursor.execute("""
        INSERT INTO Students (StudentName, Surname, age, email, city)
        VALUES ('Frank', 'Miller', 23, 'frank@gmail.com', 'Miami')
    """)


    # Update
    cursor.execute("UPDATE Students SET age = 24 WHERE id = 6")

    # DELETE
    cursor.execute("DELETE FROM Students WHERE id = 6")

def aggregate_functions(cursor):
    # 1) count
    print("--------------COUNT--------------")
    cursor.execute("SELECT count(*) FROM Students")
    result = cursor.fetchall()
    print(result[0][0])

    # 2) Avarage
    print("--------------AVARAGE--------------")
    cursor.execute("SELECT AVG(age) FROM Students")
    result = cursor.fetchall()
    print(result[0][0])


    # 2) MAX- MIN
    print("--------------MAX-MIN--------------")
    cursor.execute("SELECT MAX(age), MIN(age) FROM Students")
    result = cursor.fetchall()
    print(result[0][0], result[0][1])


    # 2) GROUP BY
    print("--------------GROUP BY--------------")
    cursor.execute("SELECT city, COUNT(*) FROM Students GROUP BY city")
    result = cursor.fetchall()
    print(result)

def main():
    print("SQL with Python")
    conn, cursor = create_database()
    try:
        create_tables(cursor)
        insert_sample_data(cursor)
        basic_sql_query(cursor)
        sql_update_delete_insert_operations(cursor)
        aggregate_functions(cursor)
        conn.commit()  # commit connection üzerinden yapılır
        print("Tablolar ve veriler başarıyla oluşturuldu.")
    except sqlite3.OperationalError as e:
        print("SQLite Hatası:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
