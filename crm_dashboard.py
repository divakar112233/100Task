import sqlite3
import datetime
import os
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    company TEXT,
    status TEXT DEFAULT 'Active',
    created_at TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    source TEXT,
    status TEXT DEFAULT 'New',
    created_at TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    lead_id INTEGER,
    type TEXT,
    notes TEXT,
    date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (lead_id) REFERENCES leads(id)
)''')

conn.commit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + f"\n{'='*60}")
    print(f"  {title.center(56)}  ")
    print('='*60 + Style.RESET_ALL)

def add_customer():
    clear_screen()
    print_header("ADD NEW CUSTOMER")
    name = input(Fore.CYAN + "Name: " + Style.RESET_ALL)
    email = input(Fore.CYAN + "Email: " + Style.RESET_ALL)
    phone = input(Fore.CYAN + "Phone: " + Style.RESET_ALL)
    company = input(Fore.CYAN + "Company: " + Style.RESET_ALL)
    status = input(Fore.CYAN + "Status (Active/Inactive): " + Style.RESET_ALL) or "Active"
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO customers (name, email, phone, company, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, email, phone, company, status, date))
    conn.commit()
    print(Fore.GREEN + "\n✅ Customer added successfully!" + Style.RESET_ALL)

def add_lead():
    clear_screen()
    print_header("ADD NEW LEAD")
    name = input(Fore.CYAN + "Name: " + Style.RESET_ALL)
    email = input(Fore.CYAN + "Email: " + Style.RESET_ALL)
    phone = input(Fore.CYAN + "Phone: " + Style.RESET_ALL)
    source = input(Fore.CYAN + "Source (Website/Referral/etc): " + Style.RESET_ALL)
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO leads (name, email, phone, source, created_at) VALUES (?, ?, ?, ?, ?)",
                   (name, email, phone, source, date))
    conn.commit()
    print(Fore.GREEN + "\n✅ Lead added successfully!" + Style.RESET_ALL)

def record_interaction():
    clear_screen()
    print_header("RECORD INTERACTION")
    print(Fore.YELLOW + "1. With Customer")
    print("2. With Lead" + Style.RESET_ALL)
    choice = input(Fore.CYAN + "Choose: " + Style.RESET_ALL)
    
    if choice == '1':
        cid = input(Fore.CYAN + "Customer ID: " + Style.RESET_ALL)
        typ = input(Fore.CYAN + "Type (Call/Email/Meeting): " + Style.RESET_ALL)
        notes = input(Fore.CYAN + "Notes: " + Style.RESET_ALL)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO interactions (customer_id, type, notes, date) VALUES (?, ?, ?, ?)",
                       (cid, typ, notes, date))
    else:
        lid = input(Fore.CYAN + "Lead ID: " + Style.RESET_ALL)
        typ = input(Fore.CYAN + "Type (Call/Email/Meeting): " + Style.RESET_ALL)
        notes = input(Fore.CYAN + "Notes: " + Style.RESET_ALL)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO interactions (lead_id, type, notes, date) VALUES (?, ?, ?, ?)",
                       (lid, typ, notes, date))
    conn.commit()
    print(Fore.GREEN + "\n✅ Interaction recorded!" + Style.RESET_ALL)

def view_customers():
    clear_screen()
    print_header("ALL CUSTOMERS")
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    if not rows:
        print(Fore.YELLOW + "No customers found." + Style.RESET_ALL)
        return
    for row in rows:
        print(f"{Fore.WHITE}ID: {Fore.GREEN}{row[0]}{Style.RESET_ALL} | {row[1]} | {row[2]} | {row[4]} | Status: {Fore.CYAN}{row[5]}{Style.RESET_ALL}")

def view_leads():
    clear_screen()
    print_header("ALL LEADS")
    cursor.execute("SELECT * FROM leads")
    rows = cursor.fetchall()
    if not rows:
        print(Fore.YELLOW + "No leads found." + Style.RESET_ALL)
        return
    for row in rows:
        print(f"{Fore.WHITE}ID: {Fore.GREEN}{row[0]}{Style.RESET_ALL} | {row[1]} | Status: {Fore.YELLOW}{row[5]}{Style.RESET_ALL}")

def view_dashboard():
    clear_screen()
    print_header("CRM DASHBOARD")
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'New'")
    new_leads = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM interactions")
    total_interactions = cursor.fetchone()[0]
    
    print(Fore.GREEN + f"Total Customers     : {total_customers}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"New Leads           : {new_leads}" + Style.RESET_ALL)
    print(Fore.BLUE + f"Total Interactions  : {total_interactions}" + Style.RESET_ALL)
    
    print(Fore.MAGENTA + "\n--- Recent Interactions ---" + Style.RESET_ALL)
    cursor.execute("SELECT * FROM interactions ORDER BY date DESC LIMIT 5")
    for inter in cursor.fetchall():
        print(f"[{inter[5]}] {inter[2]} - {inter[3]}")

def main():
    while True:
        clear_screen()
        print_header("CRM DASHBOARD - MAIN MENU")
        print(Fore.CYAN + """
1. Add Customer
2. Add Lead
3. Record Interaction
4. View Customers
5. View Leads
6. View Dashboard
7. Exit
        """ + Style.RESET_ALL)
        
        choice = input(Fore.WHITE + "Enter your choice: " + Style.RESET_ALL)
        
        if choice == '1': add_customer()
        elif choice == '2': add_lead()
        elif choice == '3': record_interaction()
        elif choice == '4': view_customers()
        elif choice == '5': view_leads()
        elif choice == '6': view_dashboard()
        elif choice == '7':
            print(Fore.GREEN + "Thank you for using CRM Dashboard!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    print(Fore.GREEN + "🚀 Welcome to the Enhanced CRM Dashboard!" + Style.RESET_ALL)
    main()
    conn.close()
