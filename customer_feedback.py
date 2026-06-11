import sqlite3
import datetime

conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comments TEXT,
    category TEXT,
    feedback_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)''')

conn.commit()

def clear_screen():
    print("\n" * 50)

def add_customer():
    clear_screen()
    print("=== Add New Customer ===")
    name = input("Customer Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()
    print("✅ Customer added successfully!")

def submit_feedback():
    clear_screen()
    print("=== Submit Feedback ===")
    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    if not customers:
        print("No customers found. Please add a customer first.")
        input("Press Enter to continue...")
        return
    
    print("Available Customers:")
    for c in customers:
        print(f"{c[0]}. {c[1]}")
    
    try:
        cust_id = int(input("\nEnter Customer ID: "))
    except:
        print("Invalid ID!")
        input("Press Enter...")
        return
    
    print("\nRating (1-5 stars):")
    for i in range(1,6):
        print(f"{i} - {'★' * i}")
    try:
        rating = int(input("Enter rating: "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5!")
            return
    except:
        print("Invalid rating!")
        return
    
    comments = input("Comments: ").strip()
    category = input("Category (Product/Service/Support/Other): ").strip()
    date = datetime.date.today().isoformat()
    
    cursor.execute("""INSERT INTO feedback 
        (customer_id, rating, comments, category, feedback_date) 
        VALUES (?, ?, ?, ?, ?)""", 
        (cust_id, rating, comments, category, date))
    conn.commit()
    print("✅ Feedback submitted successfully!")

def view_feedback():
    clear_screen()
    print("=== All Feedback ===")
    cursor.execute("""SELECT f.id, c.name, f.rating, f.comments, f.category, f.feedback_date 
                      FROM feedback f 
                      JOIN customers c ON f.customer_id = c.id 
                      ORDER BY f.feedback_date DESC""")
    feedbacks = cursor.fetchall()
    
    if not feedbacks:
        print("No feedback yet.")
    else:
        for fb in feedbacks:
            stars = '★' * fb[2]
            print(f"ID: {fb[0]} | Customer: {fb[1]} | Rating: {fb[2]} {stars}")
            print(f"Category: {fb[4]} | Date: {fb[5]}")
            print(f"Comments: {fb[3]}")
            print("-" * 60)
    
    input("\nPress Enter to continue...")

def dashboard():
    clear_screen()
    print("=== Customer Feedback Dashboard ===")
    
    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(rating) FROM feedback")
    avg = cursor.fetchone()[0]
    avg_str = f"{avg:.2f}" if avg else "N/A"
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]
    
    print(f"Total Feedback     : {total}")
    print(f"Average Rating     : {avg_str} ★")
    print(f"Total Customers    : {customers}")
    print("\nRecent Feedback:")
    
    cursor.execute("""SELECT c.name, f.rating, f.comments, f.feedback_date 
                      FROM feedback f 
                      JOIN customers c ON f.customer_id = c.id 
                      ORDER BY f.feedback_date DESC LIMIT 5""")
    recent = cursor.fetchall()
    for r in recent:
        print(f"• {r[0]} gave {r[1]}★ - {r[2][:60]}... ({r[3]})")
    
    input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        print("=== Customer Feedback System ===")
        print("1. Add New Customer")
        print("2. Submit Feedback")
        print("3. View All Feedback")
        print("4. Dashboard")
        print("5. Exit")
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            submit_feedback()
        elif choice == '3':
            view_feedback()
        elif choice == '4':
            dashboard()
        elif choice == '5':
            print("Thank you for using Customer Feedback System!")
            break
        else:
            print("Invalid choice! Please try again.")
        
        if choice != '5':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("Welcome to Customer Feedback System!")
    main()
    conn.close()
