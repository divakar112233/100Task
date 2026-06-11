import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('job_portal.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    description TEXT,
    posted_date TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    applicant_name TEXT,
    email TEXT,
    resume TEXT,
    applied_date TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
)''')

conn.commit()

def add_job():
    title = input("Job Title: ")
    company = input("Company: ")
    location = input("Location: ")
    salary = input("Salary: ")
    description = input("Description: ")
    posted_date = datetime.date.today().isoformat()
    cursor.execute("""INSERT INTO jobs (title, company, location, salary, description, posted_date)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (title, company, location, salary, description, posted_date))
    conn.commit()
    print("✅ Job posted successfully!")

def view_jobs():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    if not jobs:
        print("No jobs available.")
        return
    print("\n=== Available Jobs ===")
    for job in jobs:
        print(f"ID: {job[0]} | {job[1]} at {job[2]} | {job[3]} | Salary: {job[4]}")
        print(f"   Posted: {job[6]}\n")

def apply_job():
    view_jobs()
    job_id = int(input("Enter Job ID to apply: "))
    name = input("Your Name: ")
    email = input("Your Email: ")
    resume = input("Resume link or details: ")
    applied_date = datetime.date.today().isoformat()
    cursor.execute("""INSERT INTO applications (job_id, applicant_name, email, resume, applied_date)
                      VALUES (?, ?, ?, ?, ?)""",
                   (job_id, name, email, resume, applied_date))
    conn.commit()
    print("✅ Application submitted successfully!")

def view_applications():
    cursor.execute("""SELECT a.id, j.title, a.applicant_name, a.email, a.applied_date 
                      FROM applications a JOIN jobs j ON a.job_id = j.id""")
    apps = cursor.fetchall()
    if not apps:
        print("No applications yet.")
        return
    print("\n=== Applications ===")
    for app in apps:
        print(f"App ID: {app[0]} | Job: {app[1]} | Applicant: {app[2]} | Email: {app[3]} | Date: {app[4]}")

def main():
    while True:
        print("\n=== Job Portal ===")
        print("1. Post a New Job")
        print("2. View All Jobs")
        print("3. Apply for a Job")
        print("4. View Applications")
        print("5. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_job()
        elif choice == '2':
            view_jobs()
        elif choice == '3':
            apply_job()
        elif choice == '4':
            view_applications()
        elif choice == '5':
            print("Thank you for using the Job Portal!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    print("Welcome to the Python Job Portal!")
    main()
    conn.close()