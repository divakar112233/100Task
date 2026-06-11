import sqlite3
import datetime
import os

# Database setup
conn = sqlite3.connect('freelance.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    invoice_number TEXT,
    date TEXT,
    freelancer_name TEXT,
    freelancer_email TEXT,
    client_name TEXT,
    client_email TEXT,
    total_amount REAL,
    status TEXT DEFAULT 'Pending'
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    description TEXT,
    hours REAL,
    rate REAL,
    amount REAL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
)''')

conn.commit()

def generate_invoice_number():
    today = datetime.date.today().strftime("%Y%m%d")
    cursor.execute("SELECT COUNT(*) FROM invoices WHERE date LIKE ?", (f"{today}%",))
    count = cursor.fetchone()[0] + 1
    return f"INV-{today}-{count:03d}"

def create_invoice():
    print("\n=== Create New Invoice ===")
    
    freelancer_name = input("Your Name: ")
    freelancer_email = input("Your Email: ")
    client_name = input("Client Name: ")
    client_email = input("Client Email: ")
    
    invoice_number = generate_invoice_number()
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    items = []
    print("\nAdd Line Items (type 'done' when finished):")
    while True:
        desc = input("Description (or 'done'): ")
        if desc.lower() == 'done':
            break
        try:
            hours = float(input("Hours: "))
            rate = float(input("Rate per hour: "))
            amount = hours * rate
            items.append((desc, hours, rate, amount))
            print(f"Added: {desc} - ${amount:.2f}")
        except ValueError:
            print("Invalid input. Try again.")
    
    if not items:
        print("No items added. Invoice cancelled.")
        return
    
    subtotal = sum(item[3] for item in items)
    tax_rate = float(input("Tax rate (%) [default 0]: ") or 0)
    tax = subtotal * (tax_rate / 100)
    total = subtotal + tax
    
    # Save to database
    cursor.execute('''INSERT INTO invoices 
        (invoice_number, date, freelancer_name, freelancer_email, client_name, client_email, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (invoice_number, today, freelancer_name, freelancer_email, client_name, client_email, total))
    invoice_id = cursor.lastrowid
    
    for item in items:
        cursor.execute('''INSERT INTO invoice_items 
            (invoice_id, description, hours, rate, amount)
            VALUES (?, ?, ?, ?, ?)''', (invoice_id, *item))
    
    conn.commit()
    print(f"\n✅ Invoice {invoice_number} created successfully!")
    print(f"Total Amount: ${total:.2f}")
    
    # Generate text file
    generate_invoice_file(invoice_id, invoice_number, today, freelancer_name, freelancer_email, 
                         client_name, client_email, items, subtotal, tax, total)

def generate_invoice_file(invoice_id, invoice_number, date, f_name, f_email, c_name, c_email, items, subtotal, tax, total):
    filename = f"{invoice_number}.txt"
    with open(filename, 'w') as f:
        f.write("="*60 + "\n")
        f.write(" " * 20 + "FREELANCE INVOICE\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Invoice Number: {invoice_number}\n")
        f.write(f"Date: {date}\n\n")
        
        f.write("FROM:\n")
        f.write(f"{f_name}\n")
        f.write(f"{f_email}\n\n")
        
        f.write("BILL TO:\n")
        f.write(f"{c_name}\n")
        f.write(f"{c_email}\n\n")
        
        f.write("-" * 60 + "\n")
        f.write(f"{'Description':<40} {'Hours':<10} {'Rate':<10} {'Amount':<10}\n")
        f.write("-" * 60 + "\n")
        
        for item in items:
            f.write(f"{item[0]:<40} {item[1]:<10.1f} ${item[2]:<9.2f} ${item[3]:<9.2f}\n")
        
        f.write("-" * 60 + "\n")
        f.write(f"{'Subtotal':<60} ${subtotal:.2f}\n")
        if tax > 0:
            f.write(f"{'Tax ({tax/(subtotal)*100:.1f}%)':<60} ${tax:.2f}\n")
        f.write(f"{'TOTAL':<60} ${total:.2f}\n")
        f.write("="*60 + "\n")
        f.write("Thank you for your business!\n")
    
    print(f"📄 Invoice saved as: {filename}")

def view_invoices():
    print("\n=== All Invoices ===")
    cursor.execute('''SELECT id, invoice_number, date, client_name, total_amount, status 
                      FROM invoices ORDER BY date DESC''')
    invoices = cursor.fetchall()
    if not invoices:
        print("No invoices yet.")
        return
    for inv in invoices:
        print(f"ID: {inv[0]} | {inv[1]} | {inv[2]} | {inv[3]} | ${inv[4]:.2f} | {inv[5]}")

def main():
    while True:
        print("\n=== Freelance Invoice Generator ===")
        print("1. Create New Invoice")
        print("2. View All Invoices")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            create_invoice()
        elif choice == '2':
            view_invoices()
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    print("Welcome to Freelance Invoice Generator!")
    main()
    conn.close()