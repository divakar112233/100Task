import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    assignee_id INTEGER,
    due_date TEXT,
    priority TEXT DEFAULT 'Medium',
    status TEXT DEFAULT 'Pending',
    created_date TEXT,
    FOREIGN KEY (assignee_id) REFERENCES team(id)
)''')

conn.commit()

def add_team_member():
    name = input("Team Member Name: ")
    role = input("Role: ")
    cursor.execute("INSERT INTO team (name, role) VALUES (?, ?)", (name, role))
    conn.commit()
    print("✅ Team member added successfully!")

def view_team():
    cursor.execute("SELECT * FROM team")
    members = cursor.fetchall()
    if not members:
        print("No team members yet.")
        return
    print("\n=== Team Members ===")
    for m in members:
        print(f"ID: {m[0]} | Name: {m[1]} | Role: {m[2]}")

def add_task():
    title = input("Task Title: ")
    description = input("Description: ")
    print("\nAvailable Team Members:")
    view_team()
    assignee_id = input("Assign to (Team ID, leave blank if unassigned): ")
    due_date = input("Due Date (YYYY-MM-DD): ")
    priority = input("Priority (Low/Medium/High): ") or "Medium"
    
    created_date = datetime.date.today().isoformat()
    assignee = int(assignee_id) if assignee_id.strip() else None
    
    cursor.execute("""INSERT INTO tasks 
        (title, description, assignee_id, due_date, priority, created_date) 
        VALUES (?, ?, ?, ?, ?, ?)""", 
        (title, description, assignee, due_date, priority, created_date))
    conn.commit()
    print("✅ Task added and assigned successfully!")

def view_tasks():
    cursor.execute("""SELECT t.id, t.title, t.description, tm.name as assignee, 
                      t.due_date, t.priority, t.status 
                      FROM tasks t 
                      LEFT JOIN team tm ON t.assignee_id = tm.id 
                      ORDER BY t.due_date""")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks found.")
        return
    print("\n=== All Tasks ===")
    for t in tasks:
        assignee = t[3] if t[3] else "Unassigned"
        print(f"ID: {t[0]} | Title: {t[1]} | Assignee: {assignee} | Due: {t[4]} | Priority: {t[5]} | Status: {t[6]}")

def update_task_status():
    view_tasks()
    task_id = input("\nEnter Task ID to update: ")
    new_status = input("New Status (Pending/In Progress/Completed): ")
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    print("✅ Task status updated!")

def main():
    while True:
        print("\n=== Task Assignment System ===")
        print("1. Add Team Member")
        print("2. View Team")
        print("3. Add New Task")
        print("4. View All Tasks")
        print("5. Update Task Status")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_team_member()
        elif choice == '2':
            view_team()
        elif choice == '3':
            add_task()
        elif choice == '4':
            view_tasks()
        elif choice == '5':
            update_task_status()
        elif choice == '6':
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    print("Welcome to Task Assignment System!")
    main()
    conn.close()
