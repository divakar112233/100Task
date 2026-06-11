import sqlite3
import datetime

conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT
)''')

conn.commit()

def add_patient():
    name = input("Patient Name: ")
    age = int(input("Age: "))
    gender = input("Gender (M/F): ")
    phone = input("Phone: ")
    cursor.execute("INSERT INTO patients (name, age, gender, phone) VALUES (?, ?, ?, ?)",
                   (name, age, gender, phone))
    conn.commit()
    print("✅ Patient added!")

def view_patients():
    cursor.execute("SELECT * FROM patients")
    for p in cursor.fetchall():
        print(f"ID:{p[0]} | {p[1]} | Age:{p[2]} | {p[3]} | {p[4]}")

def add_doctor():
    name = input("Doctor Name: ")
    spec = input("Specialization: ")
    cursor.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)", (name, spec))
    conn.commit()
    print("✅ Doctor added!")

def view_doctors():
    cursor.execute("SELECT * FROM doctors")
    for d in cursor.fetchall():
        print(f"ID:{d[0]} | {d[1]} | {d[2]}")

def main():
    while True:
        print("\n=== Simple Hospital Management ===")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Exit")
        choice = input("Choose: ")
        
        if choice == '1': add_patient()
        elif choice == '2': view_patients()
        elif choice == '3': add_doctor()
        elif choice == '4': view_doctors()
        elif choice == '5': break
        else: print("Invalid option!")

if __name__ == "__main__":
    print("Welcome to Simple HMS!")
    main()
    conn.close()