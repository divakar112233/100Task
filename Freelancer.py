import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('freelancer.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS freelancers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    skills TEXT,
    hourly_rate REAL,
    bio TEXT,
    experience INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    budget REAL,
    client_name TEXT,
    status TEXT DEFAULT 'Open',
    posted_date TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    freelancer_id INTEGER,
    proposed_rate REAL,
    message TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (freelancer_id) REFERENCES freelancers(id)
)''')

conn.commit()

def add_freelancer():
    name = input("Freelancer Name: ")
    skills = input("Skills (comma separated): ")
    rate = float(input("Hourly Rate ($): "))
    bio = input("Short Bio: ")
    exp = int(input("Years of Experience: "))
    cursor.execute("INSERT INTO freelancers (name, skills, hourly_rate, bio, experience) VALUES (?, ?, ?, ?, ?)",
                   (name, skills, rate, bio, exp))
    conn.commit()
    print("✅ Freelancer profile created!")

def view_freelancers():
    cursor.execute("SELECT * FROM freelancers")
    freelancers = cursor.fetchall()
    if not freelancers:
        print("No freelancers yet.")
        return
    for f in freelancers:
        print(f"ID:{f[0]} | {f[1]} | Skills: {f[2]} | Rate: ${f[3]}/hr | Exp: {f[4]} years")

def post_job():
    title = input("Job Title: ")
    desc = input("Description: ")
    budget = float(input("Budget ($): "))
    client = input("Client Name: ")
    date = datetime.date.today().isoformat()
    cursor.execute("INSERT INTO jobs (title, description, budget, client_name, posted_date) VALUES (?, ?, ?, ?, ?)",
                   (title, desc, budget, client, date))
    conn.commit()
    print("✅ Job posted successfully!")

def view_jobs():
    cursor.execute("SELECT * FROM jobs WHERE status = 'Open'")
    jobs = cursor.fetchall()
    if not jobs:
        print("No open jobs.")
        return
    for j in jobs:
        print(f"ID:{j[0]} | {j[1]} | Budget: ${j[3]} | Client: {j[4]} | Posted: {j[6]}")

def send_proposal():
    job_id = int(input("Enter Job ID: "))
    freelancer_id = int(input("Enter Your Freelancer ID: "))
    rate = float(input("Proposed Rate ($): "))
    message = input("Message/Cover Letter: ")
    cursor.execute("INSERT INTO proposals (job_id, freelancer_id, proposed_rate, message) VALUES (?, ?, ?, ?)",
                   (job_id, freelancer_id, rate, message))
    conn.commit()
    print("✅ Proposal sent!")

def view_proposals():
    cursor.execute('''SELECT p.id, j.title, f.name, p.proposed_rate, p.message, p.status 
                      FROM proposals p 
                      JOIN jobs j ON p.job_id = j.id 
                      JOIN freelancers f ON p.freelancer_id = f.id''')
    proposals = cursor.fetchall()
    if not proposals:
        print("No proposals yet.")
        return
    for p in proposals:
        print(f"Proposal ID:{p[0]} | Job: {p[1]} | Freelancer: {p[2]} | Rate: ${p[3]} | Status: {p[5]}")

def main():
    while True:
        print("\n=== Freelancer Marketplace ===")
        print("1. Add Freelancer Profile")
        print("2. View Freelancers")
        print("3. Post a Job")
        print("4. View Open Jobs")
        print("5. Send Proposal")
        print("6. View Proposals")
        print("7. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_freelancer()
        elif choice == '2':
            view_freelancers()
        elif choice == '3':
            post_job()
        elif choice == '4':
            view_jobs()
        elif choice == '5':
            send_proposal()
        elif choice == '6':
            view_proposals()
        elif choice == '7':
            print("Thank you for using Freelancer Marketplace!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    print("Welcome to Freelancer Marketplace!")
    main()
    conn.close()