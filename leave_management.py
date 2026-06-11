import sqlite3
from datetime import datetime, date

# Connect to database
conn = sqlite3.connect('leaves.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    leave_balance INTEGER DEFAULT 20
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    leave_type TEXT,
    start_date TEXT,
    end_date TEXT,
    days INTEGER,
    reason TEXT,
    status TEXT DEFAULT 'Pending',
    applied_date TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
)
''')

conn.commit()

def add_employee():
    name = input("Employee Name: ")
    dept = input("Department: ")
    cursor.execute("INSERT INTO employees (name, department) VALUES (?, ?)", (name, dept))
    conn.commit()
    print("✅ Employee added successfully!")

def view_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    if not employees:
        print("No employees found.")
        return
    print("\n--- Employees ---")
    for emp in employees:
        print(f"ID: {emp[0]} | Name: {emp[1]} | Dept: {emp[2]} | Balance: {emp[3]} days")

def apply_leave():
    view_employees()
    emp_id = int(input("\nEnter Employee ID: "))
    leave_type = input("Leave Type (Sick/Casual/Vacation): ")
    start_date = input("Start Date (YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")
    reason = input("Reason: ")
    
    try:
        s_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        e_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        days = (e_date - s_date).days + 1
        if days <= 0:
            print("❌ Invalid dates!")
            return
    except:
        print("❌ Invalid date format!")
        return
    
    cursor.execute("SELECT leave_balance FROM employees WHERE id = ?", (emp_id,))
    result = cursor.fetchone()
    if not result:
        print("❌ Employee not found!")
        return
    if result[0] < days:
        print(f"❌ Insufficient leave balance! Only {result[0]} days left.")
        return
    
    applied_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO leave_requests 
        (employee_id, leave_type, start_date, end_date, days, reason, applied_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (emp_id, leave_type, start_date, end_date, days, reason, applied_date))
    conn.commit()
    print("✅ Leave request submitted successfully!")

def view_leaves():
    cursor.execute("""
        SELECT lr.id, e.name, lr.leave_type, lr.start_date, lr.end_date, 
               lr.days, lr.reason, lr.status, lr.applied_date
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.id
        ORDER BY lr.applied_date DESC
    """)
    leaves = cursor.fetchall()
    if not leaves:
        print("No leave requests found.")
        return
    print("\n--- All Leave Requests ---")
    for l in leaves:
        print(f"ID:{l[0]} | Employee:{l[1]} | Type:{l[2]} | {l[3]} to {l[4]} ({l[5]} days) | Status: {l[7]}")

def update_leave_status():
    view_leaves()
    leave_id = int(input("\nEnter Leave Request ID to update: "))
    status = input("New Status (Approved/Rejected): ").capitalize()
    if status not in ['Approved', 'Rejected']:
        print("❌ Invalid status!")
        return
    
    cursor.execute("UPDATE leave_requests SET status = ? WHERE id = ?", (status, leave_id))
    
    if status == 'Approved':
        cursor.execute("SELECT employee_id, days FROM leave_requests WHERE id = ?", (leave_id,))
        req = cursor.fetchone()
        if req:
            cursor.execute("UPDATE employees SET leave_balance = leave_balance - ? WHERE id = ?", (req[1], req[0]))
    
    conn.commit()
    print(f"✅ Leave request {status} successfully!")

def main():
    while True:
        print("\n=== Leave Management System ===")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Apply for Leave")
        print("4. View All Leave Requests")
        print("5. Update Leave Status (Approve/Reject)")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_employee()
        elif choice == '2':
            view_employees()
        elif choice == '3':
            apply_leave()
        elif choice == '4':
            view_leaves()
        elif choice == '5':
            update_leave_status()
        elif choice == '6':
            print("Thank you for using Leave Management System!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    print("Welcome to Leave Management System!")
    main()
    conn.close()
