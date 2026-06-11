import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os

class LibraryManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📚 Library Management System")
        self.root.geometry("1150x750")
        self.root.configure(bg="#f0f4f8")
        
        # Data files
        self.books_file = "books.csv"
        self.members_file = "members.csv"
        self.transactions_file = "transactions.csv"
        
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        # Books
        if os.path.exists(self.books_file):
            self.books = pd.read_csv(self.books_file)
        else:
            self.books = pd.DataFrame(columns=['Book_ID', 'Title', 'Author', 'ISBN', 
                                             'Category', 'Copies', 'Available'])
            self.books.to_csv(self.books_file, index=False)
        
        # Members
        if os.path.exists(self.members_file):
            self.members = pd.read_csv(self.members_file)
        else:
            self.members = pd.DataFrame(columns=['Member_ID', 'Name', 'Email', 
                                               'Phone', 'Membership_Type', 'Join_Date'])
            self.members.to_csv(self.members_file, index=False)
        
        # Transactions (Issued Books)
        if os.path.exists(self.transactions_file):
            self.transactions = pd.read_csv(self.transactions_file)
        else:
            self.transactions = pd.DataFrame(columns=['Transaction_ID', 'Book_ID', 'Title',
                                                    'Member_ID', 'Member_Name', 'Issue_Date',
                                                    'Due_Date', 'Return_Date', 'Status'])
            self.transactions.to_csv(self.transactions_file, index=False)
    
    def setup_ui(self):
        tk.Label(self.root, text="Library Management System", 
                font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=15)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Dashboard
        dash_tab = ttk.Frame(notebook)
        notebook.add(dash_tab, text="📊 Dashboard")
        self.setup_dashboard(dash_tab)
        
        # Books
        books_tab = ttk.Frame(notebook)
        notebook.add(books_tab, text="📖 Books")
        self.setup_books_tab(books_tab)
        
        # Members
        members_tab = ttk.Frame(notebook)
        notebook.add(members_tab, text="👤 Members")
        self.setup_members_tab(members_tab)
        
        # Issue / Return
        issue_tab = ttk.Frame(notebook)
        notebook.add(issue_tab, text="🔄 Issue / Return")
        self.setup_issue_tab(issue_tab)
        
        self.refresh_all()
    
    def setup_dashboard(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        stats = tk.Frame(frame, bg="white")
        stats.pack(pady=30)
        
        self.total_books = tk.Label(stats, text="Total Books: 0", font=("Arial", 16, "bold"), bg="white")
        self.total_books.grid(row=0, column=0, padx=40)
        
        self.available = tk.Label(stats, text="Available: 0", font=("Arial", 16, "bold"), bg="white", fg="green")
        self.available.grid(row=0, column=1, padx=40)
        
        self.issued = tk.Label(stats, text="Issued: 0", font=("Arial", 16, "bold"), bg="white", fg="orange")
        self.issued.grid(row=0, column=2, padx=40)
        
        tk.Button(frame, text="🔄 Refresh", command=self.refresh_dashboard, 
                 bg="#3498db", fg="white").pack(pady=20)
    
    def setup_books_tab(self, parent):
        # Add Book
        add_frame = tk.LabelFrame(parent, text="Add New Book", padx=15, pady=10)
        add_frame.pack(fill="x", padx=10, pady=8)
        
        fields = ["Book ID", "Title", "Author", "ISBN", "Category"]
        self.book_entries = {}
        for i, field in enumerate(fields):
            tk.Label(add_frame, text=field+":").grid(row=i//3, column=(i%3)*2, sticky="w", padx=5)
            entry = tk.Entry(add_frame, width=25)
            entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=4)
            self.book_entries[field.lower().replace(" ", "_")] = entry
        
        tk.Button(add_frame, text="Add Book", command=self.add_book, 
                 bg="#2ecc71", fg="white").grid(row=2, column=5, padx=10)
        
        # Books List
        tk.Label(parent, text="All Books", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        
        cols = ["Book_ID", "Title", "Author", "Category", "Available", "Copies"]
        self.books_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=120)
        self.books_tree.pack(fill="both", expand=True, padx=10, pady=5)
    
    def setup_members_tab(self, parent):
        add_frame = tk.LabelFrame(parent, text="Add New Member", padx=15, pady=10)
        add_frame.pack(fill="x", padx=10, pady=8)
        
        fields = ["Member ID", "Name", "Email", "Phone", "Membership Type"]
        self.member_entries = {}
        for i, field in enumerate(fields):
            tk.Label(add_frame, text=field+":").grid(row=i, column=0, sticky="w", padx=5)
            entry = tk.Entry(add_frame, width=35)
            entry.grid(row=i, column=1, padx=5, pady=4)
            self.member_entries[field.lower().replace(" ", "_")] = entry
        
        tk.Button(add_frame, text="Add Member", command=self.add_member, 
                 bg="#2ecc71", fg="white").grid(row=5, column=1, pady=8)
        
        tk.Label(parent, text="All Members", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
        
        cols = ["Member_ID", "Name", "Email", "Phone", "Membership_Type"]
        self.members_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=140)
        self.members_tree.pack(fill="both", expand=True, padx=10, pady=5)
    
    def setup_issue_tab(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Issue Book
        issue_frame = tk.LabelFrame(frame, text="Issue Book", padx=15, pady=10)
        issue_frame.pack(fill="x")
        
        tk.Label(issue_frame, text="Book ID:").grid(row=0, column=0)
        self.issue_book_id = tk.Entry(issue_frame, width=20)
        self.issue_book_id.grid(row=0, column=1, padx=5)
        
        tk.Label(issue_frame, text="Member ID:").grid(row=0, column=2, padx=10)
        self.issue_member_id = tk.Entry(issue_frame, width=20)
        self.issue_member_id.grid(row=0, column=3, padx=5)
        
        tk.Button(issue_frame, text="Issue Book", command=self.issue_book, 
                 bg="#e67e22", fg="white").grid(row=0, column=4, padx=15)
        
        # Return Book
        return_frame = tk.LabelFrame(frame, text="Return Book", padx=15, pady=10)
        return_frame.pack(fill="x", pady=15)
        
        tk.Label(return_frame, text="Book ID:").grid(row=0, column=0)
        self.return_book_id = tk.Entry(return_frame, width=30)
        self.return_book_id.grid(row=0, column=1, padx=5)
        
        tk.Button(return_frame, text="Return Book", command=self.return_book, 
                 bg="#27ae60", fg="white").grid(row=0, column=2, padx=15)
        
        # Issued Books
        tk.Label(frame, text="Currently Issued Books", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        cols = ["Transaction_ID", "Book_ID", "Title", "Member_Name", "Issue_Date", "Due_Date", "Status"]
        self.issued_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.issued_tree.heading(col, text=col)
            self.issued_tree.column(col, width=110)
        self.issued_tree.pack(fill="both", expand=True, pady=5)
    
    def add_book(self):
        try:
            new_book = {
                'Book_ID': self.book_entries['book_id'].get().strip(),
                'Title': self.book_entries['title'].get().strip(),
                'Author': self.book_entries['author'].get().strip(),
                'ISBN': self.book_entries['isbn'].get().strip(),
                'Category': self.book_entries['category'].get().strip(),
                'Copies': 1,
                'Available': 1
            }
            
            if not new_book['Book_ID'] or not new_book['Title']:
                messagebox.showwarning("Error", "Book ID and Title are required")
                return
            
            new_df = pd.DataFrame([new_book])
            self.books = pd.concat([self.books, new_df], ignore_index=True)
            self.books.to_csv(self.books_file, index=False)
            self.refresh_books()
            messagebox.showinfo("Success", "Book added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_member(self):
        try:
            new_member = {
                'Member_ID': self.member_entries['member_id'].get().strip(),
                'Name': self.member_entries['name'].get().strip(),
                'Email': self.member_entries['email'].get().strip(),
                'Phone': self.member_entries['phone'].get().strip(),
                'Membership_Type': self.member_entries['membership_type'].get().strip() or "Regular",
                'Join_Date': datetime.now().strftime("%Y-%m-%d")
            }
            
            if not new_member['Member_ID'] or not new_member['Name']:
                messagebox.showwarning("Error", "Member ID and Name are required")
                return
            
            new_df = pd.DataFrame([new_member])
            self.members = pd.concat([self.members, new_df], ignore_index=True)
            self.members.to_csv(self.members_file, index=False)
            self.refresh_members()
            messagebox.showinfo("Success", "Member added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def issue_book(self):
        book_id = self.issue_book_id.get().strip()
        member_id = self.issue_member_id.get().strip()
        
        if not book_id or not member_id:
            messagebox.showwarning("Error", "Both Book ID and Member ID are required")
            return
        
        book = self.books[self.books['Book_ID'] == book_id]
        member = self.members[self.members['Member_ID'] == member_id]
        
        if book.empty:
            messagebox.showerror("Error", "Book not found!")
            return
        if member.empty:
            messagebox.showerror("Error", "Member not found!")
            return
        if int(book.iloc[0]['Available']) <= 0:
            messagebox.showwarning("Unavailable", "No copies available!")
            return
        
        # Issue
        today = datetime.now().strftime("%Y-%m-%d")
        due = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        new_trans = pd.DataFrame([{
            'Transaction_ID': f"T{len(self.transactions)+1:04d}",
            'Book_ID': book_id,
            'Title': book.iloc[0]['Title'],
            'Member_ID': member_id,
            'Member_Name': member.iloc[0]['Name'],
            'Issue_Date': today,
            'Due_Date': due,
            'Return_Date': "",
            'Status': "Issued"
        }])
        
        self.transactions = pd.concat([self.transactions, new_trans], ignore_index=True)
        self.transactions.to_csv(self.transactions_file, index=False)
        
        # Update book availability
        idx = self.books[self.books['Book_ID'] == book_id].index[0]
        self.books.at[idx, 'Available'] = int(self.books.at[idx, 'Available']) - 1
        self.books.to_csv(self.books_file, index=False)
        
        messagebox.showinfo("Success", f"Book issued to {member.iloc[0]['Name']}\nDue: {due}")
        self.refresh_all()
    
    def return_book(self):
        book_id = self.return_book_id.get().strip()
        if not book_id:
            messagebox.showwarning("Error", "Enter Book ID")
            return
        
        pending = self.transactions[(self.transactions['Book_ID'] == book_id) & 
                                  (self.transactions['Status'] == "Issued")]
        
        if pending.empty:
            messagebox.showinfo("Info", "No active issue found for this book")
            return
        
        # Mark as returned
        idx = pending.index[0]
        self.transactions.at[idx, 'Return_Date'] = datetime.now().strftime("%Y-%m-%d")
        self.transactions.at[idx, 'Status'] = "Returned"
        self.transactions.to_csv(self.transactions_file, index=False)
        
        # Increase available copies
        book_idx = self.books[self.books['Book_ID'] == book_id].index[0]
        self.books.at[book_idx, 'Available'] = int(self.books.at[book_idx, 'Available']) + 1
        self.books.to_csv(self.books_file, index=False)
        
        messagebox.showinfo("Success", "Book returned successfully!")
        self.refresh_all()
    
    def refresh_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        for _, row in self.books.iterrows():
            self.books_tree.insert("", "end", values=list(row))
    
    def refresh_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        for _, row in self.members.iterrows():
            self.members_tree.insert("", "end", values=list(row))
    
    def refresh_issued(self):
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        issued = self.transactions[self.transactions['Status'] == "Issued"]
        for _, row in issued.iterrows():
            self.issued_tree.insert("", "end", values=list(row))
    
    def refresh_dashboard(self):
        total = len(self.books)
        available = self.books['Available'].sum() if not self.books.empty else 0
        issued = len(self.transactions[self.transactions['Status'] == "Issued"])
        
        self.total_books.config(text=f"Total Books: {total}")
        self.available.config(text=f"Available: {available}")
        self.issued.config(text=f"Issued: {issued}")
    
    def refresh_all(self):
        self.refresh_books()
        self.refresh_members()
        self.refresh_issued()
        self.refresh_dashboard()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()