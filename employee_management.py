import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os

class EmployeeManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("👔 Employee Management System")
        self.root.geometry("1100x720")
        self.root.configure(bg="#f4f6f9")
        
        self.file = "employees.csv"
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        if os.path.exists(self.file):
            self.df = pd.read_csv(self.file)
        else:
            columns = ['ID', 'Name', 'Position', 'Department', 'Email', 
                      'Phone', 'Join_Date', 'Salary']
            self.df = pd.DataFrame(columns=columns)
            self.df.to_csv(self.file, index=False)
    
    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Employee Management System", 
                font=("Arial", 24, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(pady=15)
        
        # Notebook (Tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Tab 1: Dashboard
        dash_tab = ttk.Frame(notebook)
        notebook.add(dash_tab, text="📊 Dashboard")
        self.setup_dashboard(dash_tab)
        
        # Tab 2: All Employees
        emp_tab = ttk.Frame(notebook)
        notebook.add(emp_tab, text="👥 All Employees")
        self.setup_employees_tab(emp_tab)
        
        # Tab 3: Add / Edit Employee
        add_tab = ttk.Frame(notebook)
        notebook.add(add_tab, text="➕ Add / Edit Employee")
        self.setup_add_edit_tab(add_tab)
        
        self.refresh_all()
    
    def setup_dashboard(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        stats_frame = tk.Frame(frame, bg="white")
        stats_frame.pack(pady=20)
        
        self.total_emp = tk.Label(stats_frame, text="Total Employees: 0", 
                                font=("Arial", 16, "bold"), bg="white")
        self.total_emp.grid(row=0, column=0, padx=30)
        
        self.dept_count = tk.Label(stats_frame, text="Departments: 0", 
                                 font=("Arial", 16, "bold"), bg="white")
        self.dept_count.grid(row=0, column=1, padx=30)
        
        tk.Button(frame, text="🔄 Refresh Dashboard", command=self.refresh_dashboard,
                 bg="#3498db", fg="white", font=("Arial", 11)).pack(pady=10)
    
    def setup_employees_tab(self, parent):
        # Search
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_employees())
        
        tk.Button(search_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Name", "Position", "Department", "Email", "Phone", "Join_Date", "Salary")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=8)
        
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_employee,
                 bg="#e74c3c", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export to CSV", command=self.export_csv,
                 bg="#27ae60", fg="white").pack(side="left", padx=5)
    
    def setup_add_edit_tab(self, parent):
        frame = tk.LabelFrame(parent, text="Employee Details", padx=20, pady=20)
        frame.pack(pady=20, padx=20, fill="x")
        
        fields = [
            ("ID", "id"), ("Name", "name"), ("Position", "position"),
            ("Department", "dept"), ("Email", "email"), ("Phone", "phone"),
            ("Join Date (YYYY-MM-DD)", "join_date"), ("Salary", "salary")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=6)
            entry = tk.Entry(frame, width=40)
            entry.grid(row=i, column=1, pady=6, padx=10)
            self.entries[key] = entry
        
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Save Employee", command=self.save_employee,
                 bg="#2ecc71", fg="white", font=("Arial", 11)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form,
                 bg="#95a5a6").pack(side="left", padx=10)
    
    def save_employee(self):
        data = {key: self.entries[key].get().strip() for key in self.entries}
        
        if not data['id'] or not data['name']:
            messagebox.showwarning("Error", "ID and Name are required!")
            return
        
        if data['id'] in self.df['ID'].astype(str).values:
            # Update existing
            idx = self.df[self.df['ID'].astype(str) == data['id']].index[0]
            for key, value in data.items():
                self.df.at[idx, key.capitalize() if key != 'id' else 'ID'] = value
            messagebox.showinfo("Success", "Employee updated successfully!")
        else:
            # Add new
            new_row = pd.DataFrame([{
                'ID': data['id'],
                'Name': data['name'],
                'Position': data['position'],
                'Department': data['dept'],
                'Email': data['email'],
                'Phone': data['phone'],
                'Join_Date': data['join_date'] or datetime.now().strftime("%Y-%m-%d"),
                'Salary': data['salary']
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            messagebox.showinfo("Success", "New employee added successfully!")
        
        self.df.to_csv(self.file, index=False)
        self.refresh_all()
        self.clear_form()
    
    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected employee?"):
            item = self.tree.item(selected[0])
            emp_id = item['values'][0]
            
            self.df = self.df[self.df['ID'].astype(str) != str(emp_id)]
            self.df.to_csv(self.file, index=False)
            self.refresh_all()
            messagebox.showinfo("Deleted", "Employee deleted successfully")
    
    def filter_employees(self):
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = self.df.copy()
        if search_text:
            mask = filtered.apply(lambda row: row.astype(str).str.lower().str.contains(search_text).any(), axis=1)
            filtered = filtered[mask]
        
        for _, row in filtered.iterrows():
            self.tree.insert("", "end", values=list(row))
    
    def refresh_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))
    
    def refresh_dashboard(self):
        total = len(self.df)
        depts = self.df['Department'].nunique() if not self.df.empty else 0
        
        self.total_emp.config(text=f"Total Employees: {total}")
        self.dept_count.config(text=f"Departments: {depts}")
    
    def refresh_all(self):
        self.refresh_employees()
        self.refresh_dashboard()
    
    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def clear_search(self):
        self.search_var.set("")
        self.refresh_employees()
    
    def export_csv(self):
        if self.df.empty:
            messagebox.showinfo("Empty", "No data to export")
            return
        filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        self.df.to_csv(filename, index=False)
        messagebox.showinfo("Exported", f"Data saved as {filename}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmployeeManagementSystem()
    app.run()