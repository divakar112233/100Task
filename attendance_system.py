import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from pyzbar import pyzbar
import pandas as pd
from datetime import datetime
import os

class AttendanceSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📋 Attendance Management System")
        self.root.geometry("950x720")
        
        self.students_file = "students.csv"
        self.attendance_file = "attendance.csv"
        
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        if os.path.exists(self.students_file):
            self.students = pd.read_csv(self.students_file)
        else:
            self.students = pd.DataFrame(columns=['ID', 'Name', 'Class'])
            self.students.to_csv(self.students_file, index=False)
        
        if os.path.exists(self.attendance_file):
            self.attendance = pd.read_csv(self.attendance_file)
        else:
            self.attendance = pd.DataFrame(columns=['Date', 'ID', 'Name', 'Status', 'Time'])
            self.attendance.to_csv(self.attendance_file, index=False)
    
    def setup_ui(self):
        tk.Label(self.root, text="Attendance Management System", 
                font=("Arial", 22, "bold")).pack(pady=10)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mark Attendance Tab
        mark_tab = ttk.Frame(notebook)
        notebook.add(mark_tab, text="Mark Attendance")
        self.setup_mark_tab(mark_tab)
        
        # Students Tab
        student_tab = ttk.Frame(notebook)
        notebook.add(student_tab, text="Students")
        self.setup_student_tab(student_tab)
        
        # Reports Tab
        report_tab = ttk.Frame(notebook)
        notebook.add(report_tab, text="Reports")
        self.setup_report_tab(report_tab)
    
    def setup_mark_tab(self, parent):
        tk.Label(parent, text="Scan Barcode or Enter Student ID", font=("Arial", 14)).pack(pady=10)
        
        self.id_entry = tk.Entry(parent, font=("Arial", 14), width=30, justify="center")
        self.id_entry.pack(pady=5)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📷 Start Camera Scan", command=self.start_scanner,
                 bg="#27ae60", fg="white", font=("Arial", 12), width=18).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✅ Mark Present", command=self.mark_manual,
                 bg="#3498db", fg="white", font=("Arial", 12), width=18).pack(side="left", padx=5)
        
        self.scan_result = tk.Label(parent, text="Ready to scan...", 
                                  font=("Arial", 12), fg="blue", height=2)
        self.scan_result.pack(pady=15)
    
    def setup_student_tab(self, parent):
        add_frame = tk.LabelFrame(parent, text="Add New Student", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(add_frame, text="ID:").grid(row=0, column=0, padx=5)
        self.new_id = tk.Entry(add_frame, width=15)
        self.new_id.grid(row=0, column=1, padx=5)
        
        tk.Label(add_frame, text="Name:").grid(row=0, column=2, padx=5)
        self.new_name = tk.Entry(add_frame, width=20)
        self.new_name.grid(row=0, column=3, padx=5)
        
        tk.Label(add_frame, text="Class:").grid(row=0, column=4, padx=5)
        self.new_class = tk.Entry(add_frame, width=15)
        self.new_class.grid(row=0, column=5, padx=5)
        
        tk.Button(add_frame, text="Add Student", command=self.add_student, 
                 bg="#2ecc71", fg="white").grid(row=0, column=6, padx=10)
        
        tk.Label(parent, text="All Students", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.tree = ttk.Treeview(parent, columns=("ID", "Name", "Class"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Class", text="Class")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.refresh_students()
    
    def setup_report_tab(self, parent):
        tk.Button(parent, text="🔄 Refresh Reports", command=self.refresh_reports).pack(pady=5)
        
        self.report_tree = ttk.Treeview(parent, columns=("Date", "ID", "Name", "Status", "Time"), show="headings")
        for col in ("Date", "ID", "Name", "Status", "Time"):
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120)
        self.report_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Button(parent, text="💾 Export to CSV", command=self.export_csv,
                 bg="#8e44ad", fg="white").pack(pady=8)
        
        self.refresh_reports()
    
    def add_student(self):
        if not self.new_id.get() or not self.new_name.get():
            messagebox.showwarning("Error", "ID and Name are required!")
            return
        
        new_row = pd.DataFrame([{
            'ID': self.new_id.get().strip(),
            'Name': self.new_name.get().strip(),
            'Class': self.new_class.get().strip() or "N/A"
        }])
        
        self.students = pd.concat([self.students, new_row], ignore_index=True)
        self.students.to_csv(self.students_file, index=False)
        self.refresh_students()
        messagebox.showinfo("Success", "Student added successfully!")
    
    def refresh_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.students.iterrows():
            self.tree.insert("", "end", values=(row['ID'], row['Name'], row['Class']))
    
    def mark_manual(self):
        student_id = self.id_entry.get().strip()
        if student_id:
            self.mark_attendance(student_id)
        else:
            messagebox.showwarning("Input", "Please enter Student ID")
    
    def start_scanner(self):
        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Camera", "Camera started.\nPoint barcode/QR code to camera.\nPress 'q' to stop.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                data = barcode.data.decode("utf-8")
                self.mark_attendance(data)
                cv2.putText(frame, f"Marked: {data}", (30, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            
            cv2.imshow("Barcode Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def mark_attendance(self, student_id):
        student = self.students[self.students['ID'].astype(str) == str(student_id)]
        if student.empty:
            self.scan_result.config(text=f"❌ Student ID {student_id} not found!", fg="red")
            return
        
        name = student.iloc[0]['Name']
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        new_record = pd.DataFrame([{
            'Date': today,
            'ID': student_id,
            'Name': name,
            'Status': 'Present',
            'Time': current_time
        }])
        
        self.attendance = pd.concat([self.attendance, new_record], ignore_index=True)
        self.attendance.to_csv(self.attendance_file, index=False)
        
        self.scan_result.config(text=f"✅ {name} Marked Present at {current_time}", fg="green")
        self.refresh_reports()
    
    def refresh_reports(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        for _, row in self.attendance.iterrows():
            self.report_tree.insert("", "end", values=(
                row['Date'], row['ID'], row['Name'], row['Status'], row['Time']
            ))
    
    def export_csv(self):
        if self.attendance.empty:
            messagebox.showinfo("Empty", "No attendance records to export.")
            return
        filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        self.attendance.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Report exported as:\n{filename}")

if __name__ == "__main__":
    app = AttendanceSystem()
    app.root.mainloop()