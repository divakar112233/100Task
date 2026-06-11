import sqlite3
import datetime

# Connect to database
conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complainant TEXT NOT NULL,
    contact TEXT,
    category TEXT,
    description TEXT NOT NULL,
    date TEXT,
    status TEXT DEFAULT 'Pending',
    resolution TEXT
)''')
conn.commit()

def add_complaint():
    print("\n--- Register New Complaint ---")
    complainant = input("Complainant Name: ")
    contact = input("Contact (Phone/Email): ")
    category = input("Category (e.g., Service, Product, Billing): ")
    description = input("Description: ")
    date = datetime.date.today().isoformat()
    
    cursor.execute("""INSERT INTO complaints 
                     (complainant, contact, category, description, date) 
                     VALUES (?, ?, ?, ?, ?)""", 
                     (complainant, contact, category, description, date))
    conn.commit()
    print(f"✅ Complaint registered successfully! ID: {cursor.lastrowid}")

def view_complaints():
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    complaints = cursor.fetchall()
    if not complaints:
        print("No complaints found.")
        return
    print("\n--- All Complaints ---")
    for c in complaints:
        print(f"ID: {c[0]} | {c[1]} | {c[3]} | Status: {c[6]} | Date: {c[5]}")

def update_status():
    view_complaints()
    cid = input("\nEnter Complaint ID to update: ")
    print("1. Pending")
    print("2. In Progress")
    print("3. Resolved")
    print("4. Closed")
    status_choice = input("Choose status: ")
    status_map = {'1':'Pending', '2':'In Progress', '3':'Resolved', '4':'Closed'}
    status = status_map.get(status_choice, 'Pending')
    
    resolution = input("Resolution Notes (optional): ")
    
    cursor.execute("UPDATE complaints SET status=?, resolution=? WHERE id=?", 
                   (status, resolution, cid))
    conn.commit()
    print("✅ Status updated!")

def search_complaint():
    keyword = input("\nSearch by name, category or description: ")
    cursor.execute("""SELECT * FROM complaints 
                      WHERE complainant LIKE ? OR category LIKE ? OR description LIKE ?""", 
                      (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if not results:
        print("No matching complaints.")
        return
    print("\n--- Search Results ---")
    for c in results:
        print(f"ID: {c[0]} | {c[1]} | {c[3]} | Status: {c[6]}")

def main():
    while True:
        print("\n" + "="*40)
        print("   COMPLAINT MANAGEMENT PORTAL")
        print("="*40)
        print("1. Register New Complaint")
        print("2. View All Complaints")
        print("3. Update Complaint Status")
        print("4. Search Complaints")
        print("5. Exit")
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_complaint()
        elif choice == '2':
            view_complaints()
        elif choice == '3':
            update_status()
        elif choice == '4':
            search_complaint()
        elif choice == '5':
            print("Thank you for using Complaint Management Portal!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    print("Welcome to Complaint Management Portal!")
    main()
    conn.close()
