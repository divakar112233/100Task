import csv
import datetime
import os
import time

FILE_NAME = "expenses.csv"

# Create file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Description", "Amount"])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("="*60)
    print(f"          {title.center(50)}")
    print("="*60)

def add_expense():
    print_header("ADD NEW EXPENSE")
    date = datetime.date.today().strftime("%Y-%m-%d")
    category = input("   Category     : ").strip() or "Others"
    description = input("   Description  : ").strip()
    try:
        amount = float(input("   Amount (₹)   : "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            time.sleep(1.5)
            return
    except ValueError:
        print("❌ Please enter a valid number!")
        time.sleep(1.5)
        return
    
    with open(FILE_NAME, "a", newline="") as f:
        csv.writer(f).writerow([date, category, description, f"{amount:.2f}"])
    
    print("\n✅ Expense added successfully!")
    time.sleep(1.5)

def view_all_expenses():
    print_header("ALL EXPENSES HISTORY")
    try:
        with open(FILE_NAME, "r") as f:
            reader = csv.reader(f)
            print(f"{'Date':<12} | {'Category':<15} | {'Description':<30} | {'Amount':>8}")
            print("-"*70)
            for row in reader:
                if len(row) == 4:
                    print(f"{row[0]:<12} | {row[1]:<15} | {row[2]:<30} | ₹{row[3]:>7}")
    except:
        print("No expenses recorded yet.")
    input("\nPress Enter to continue...")

def today_summary():
    print_header("TODAY'S SUMMARY")
    today = datetime.date.today().strftime("%Y-%m-%d")
    total = 0.0
    count = 0
    
    try:
        with open(FILE_NAME, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            print(f"Date: {today}\n")
            print(f"{'Category':<15} | {'Description':<30} | {'Amount':>8}")
            print("-"*60)
            for row in reader:
                if row[0] == today:
                    print(f"{row[1]:<15} | {row[2]:<30} | ₹{float(row[3]):>7.2f}")
                    total += float(row[3])
                    count += 1
    except:
        pass
    
    if count == 0:
        print("   No expenses recorded today.")
    else:
        print("-"*60)
        print(f"Total Spent Today: ₹{total:.2f}   ({count} transactions)")

    input("\nPress Enter to continue...")

def main():
    while True:
        print_header("DAILY EXPENSE TRACKER")
        print("   1. ➕ Add New Expense")
        print("   2. 📋 View All Expenses")
        print("   3. 📊 Today's Summary")
        print("   4. 🚪 Exit")
        print("="*60)
        
        choice = input("\n   Enter your choice (1-4): ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            today_summary()
        elif choice == "4":
            print_header("GOODBYE!")
            print("   Thanks for using Expense Tracker!")
            print("   Stay smart with your money 💰")
            time.sleep(2)
            break
        else:
            print("   ❌ Invalid choice! Try again.")
            time.sleep(1.2)

if __name__ == "__main__":
    main()