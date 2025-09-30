#!/usr/bin/env python3
"""
Student Account Management System
================================
Professional student account and class management for school deployment.
Integrates with existing gradebook and standards systems.
"""

import sqlite3
import json
import csv
import hashlib
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class StudentAccountManager:
    """Comprehensive student account and class management system."""
    
    def __init__(self):
        """Initialize the student account management system."""
        self.db_path = Path("student_accounts.db")
        self.setup_database()
        
    def setup_database(self):
        """Create and configure the student accounts database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            grade_level INTEGER,
            email TEXT,
            guardian_email TEXT,
            enrollment_date DATE,
            active_status BOOLEAN DEFAULT 1,
            notes TEXT
        )
        ''')
        
        # Classes table  
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id TEXT PRIMARY KEY,
            class_name TEXT NOT NULL,
            teacher_name TEXT,
            grade_level INTEGER,
            semester TEXT,
            year INTEGER,
            active_status BOOLEAN DEFAULT 1
        )
        ''')
        
        # Student-Class enrollment table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            class_id TEXT,
            enrollment_date DATE,
            status TEXT DEFAULT 'enrolled',
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (class_id) REFERENCES classes (class_id)
        )
        ''')
        
        # Student activity tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_activity (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            class_id TEXT,
            activity_type TEXT,
            activity_name TEXT,
            completion_date DATE,
            score REAL,
            time_spent INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (class_id) REFERENCES classes (class_id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_student(self, student_data: Dict[str, Any]) -> bool:
        """Add a new student to the system."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate student ID if not provided
            if not student_data.get('student_id'):
                student_data['student_id'] = self.generate_student_id(
                    student_data['first_name'], 
                    student_data['last_name']
                )
            
            cursor.execute('''
            INSERT INTO students 
            (student_id, first_name, last_name, grade_level, email, 
             guardian_email, enrollment_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_data['student_id'],
                student_data['first_name'],
                student_data['last_name'], 
                student_data.get('grade_level'),
                student_data.get('email', ''),
                student_data.get('guardian_email', ''),
                student_data.get('enrollment_date', date.today()),
                student_data.get('notes', '')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            return False  # Student ID already exists
        except Exception as e:
            print(f"Error adding student: {e}")
            return False
    
    def generate_student_id(self, first_name: str, last_name: str) -> str:
        """Generate a unique student ID."""
        base_id = f"{first_name[:2]}{last_name[:2]}{datetime.now().year}"
        
        # Check for uniqueness and add suffix if needed
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        counter = 1
        student_id = base_id
        
        while True:
            cursor.execute('SELECT student_id FROM students WHERE student_id = ?', (student_id,))
            if not cursor.fetchone():
                break
            student_id = f"{base_id}_{counter:02d}"
            counter += 1
            
        conn.close()
        return student_id
        
    def create_class(self, class_data: Dict[str, Any]) -> bool:
        """Create a new class."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO classes 
            (class_id, class_name, teacher_name, grade_level, semester, year)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                class_data['class_id'],
                class_data['class_name'],
                class_data['teacher_name'],
                class_data.get('grade_level'),
                class_data.get('semester', 'Fall'),
                class_data.get('year', datetime.now().year)
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            return False  # Class ID already exists
        except Exception as e:
            print(f"Error creating class: {e}")
            return False
    
    def enroll_student(self, student_id: str, class_id: str) -> bool:
        """Enroll a student in a class."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO enrollments (student_id, class_id, enrollment_date)
            VALUES (?, ?, ?)
            ''', (student_id, class_id, date.today()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error enrolling student: {e}")
            return False
    
    def get_class_roster(self, class_id: str) -> List[Dict[str, Any]]:
        """Get the roster for a specific class."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT s.student_id, s.first_name, s.last_name, s.grade_level, 
               s.email, e.enrollment_date
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id  
        WHERE e.class_id = ? AND e.status = 'enrolled'
        ORDER BY s.last_name, s.first_name
        ''', (class_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'student_id': row[0],
                'first_name': row[1], 
                'last_name': row[2],
                'grade_level': row[3],
                'email': row[4],
                'enrollment_date': row[5]
            }
            for row in rows
        ]
    
    def import_from_csv(self, csv_file: Path, import_type: str = 'students') -> Dict[str, int]:
        """Import students or classes from CSV file."""
        results = {'success': 0, 'errors': 0}
        
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    if import_type == 'students':
                        success = self.add_student(row)
                    elif import_type == 'classes':
                        success = self.create_class(row)
                    else:
                        continue
                        
                    if success:
                        results['success'] += 1
                    else:
                        results['errors'] += 1
                        
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            
        return results
    
    def export_to_csv(self, export_type: str = 'students', class_id: str = None) -> Path:
        """Export student or class data to CSV."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_type == 'students' and class_id:
            filename = f"class_roster_{class_id}_{timestamp}.csv"
            roster = self.get_class_roster(class_id)
            
            fieldnames = ['student_id', 'first_name', 'last_name', 'grade_level', 'email', 'enrollment_date']
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(roster)
                
        elif export_type == 'all_students':
            filename = f"all_students_{timestamp}.csv"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE active_status = 1')
            students = cursor.fetchall()
            conn.close()
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'first_name', 'last_name', 'grade_level', 
                               'email', 'guardian_email', 'enrollment_date', 'notes'])
                writer.writerows(students)
                
        return Path(filename)

class StudentAccountGUI:
    """GUI interface for student account management."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.manager = StudentAccountManager()
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main GUI interface."""
        self.root = tk.Tk()
        self.root.title("Student Account Management System")
        self.root.geometry("1000x700")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Students tab
        self.students_frame = ttk.Frame(notebook)
        notebook.add(self.students_frame, text="Students")
        self.setup_students_tab()
        
        # Classes tab
        self.classes_frame = ttk.Frame(notebook)
        notebook.add(self.classes_frame, text="Classes")
        self.setup_classes_tab()
        
        # Reports tab
        self.reports_frame = ttk.Frame(notebook)
        notebook.add(self.reports_frame, text="Reports")
        self.setup_reports_tab()
        
    def setup_students_tab(self):
        """Setup the students management tab."""
        # Add student form
        form_frame = ttk.LabelFrame(self.students_frame, text="Add New Student")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Form fields
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.first_name_entry = ttk.Entry(form_frame)
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Last Name:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.last_name_entry = ttk.Entry(form_frame)
        self.last_name_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Grade Level:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.grade_entry = ttk.Spinbox(form_frame, from_=1, to=12)
        self.grade_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Import CSV", command=self.import_students_csv).pack(side='left', padx=5)
        
        # Students list
        list_frame = ttk.LabelFrame(self.students_frame, text="Current Students")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('ID', 'First Name', 'Last Name', 'Grade', 'Email')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150)
            
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def setup_classes_tab(self):
        """Setup the class management tab."""
        # Add class form
        form_frame = ttk.LabelFrame(self.classes_frame, text="Create New Class")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(form_frame, text="Class ID:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.class_id_entry = ttk.Entry(form_frame)
        self.class_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Class Name:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.class_name_entry = ttk.Entry(form_frame)
        self.class_name_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(form_frame, text="Create Class", command=self.create_class).grid(row=1, column=0, columnspan=4, pady=10)
        
    def setup_reports_tab(self):
        """Setup the reports and export tab."""
        export_frame = ttk.LabelFrame(self.reports_frame, text="Export Options")
        export_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(export_frame, text="Export All Students", 
                  command=lambda: self.export_data('all_students')).pack(pady=5)
        ttk.Button(export_frame, text="Export Class Roster", 
                  command=lambda: self.export_data('class_roster')).pack(pady=5)
        
    def add_student(self):
        """Add a new student from the form."""
        student_data = {
            'first_name': self.first_name_entry.get(),
            'last_name': self.last_name_entry.get(),
            'grade_level': int(self.grade_entry.get()) if self.grade_entry.get() else None,
            'email': self.email_entry.get()
        }
        
        if not student_data['first_name'] or not student_data['last_name']:
            messagebox.showerror("Error", "First and last name are required!")
            return
            
        if self.manager.add_student(student_data):
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_student_form()
            self.refresh_students_list()
        else:
            messagebox.showerror("Error", "Failed to add student. ID may already exist.")
    
    def create_class(self):
        """Create a new class from the form."""
        class_data = {
            'class_id': self.class_id_entry.get(),
            'class_name': self.class_name_entry.get(),
            'teacher_name': 'Current Teacher'  # Could be made configurable
        }
        
        if not class_data['class_id'] or not class_data['class_name']:
            messagebox.showerror("Error", "Class ID and name are required!")
            return
            
        if self.manager.create_class(class_data):
            messagebox.showinfo("Success", "Class created successfully!")
            self.clear_class_form()
        else:
            messagebox.showerror("Error", "Failed to create class. ID may already exist.")
    
    def clear_student_form(self):
        """Clear the student form fields."""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
    def clear_class_form(self):
        """Clear the class form fields."""
        self.class_id_entry.delete(0, tk.END)
        self.class_name_entry.delete(0, tk.END)
        
    def refresh_students_list(self):
        """Refresh the students list display."""
        # Implementation for refreshing the treeview
        pass
        
    def import_students_csv(self):
        """Import students from CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            results = self.manager.import_from_csv(Path(file_path), 'students')
            messagebox.showinfo("Import Results", 
                              f"Successfully imported: {results['success']}\nErrors: {results['errors']}")
            self.refresh_students_list()
    
    def export_data(self, export_type: str):
        """Export data to CSV."""
        try:
            if export_type == 'class_roster':
                # Would need class selection dialog
                class_id = "CYBER101"  # Placeholder
                file_path = self.manager.export_to_csv('students', class_id)
            else:
                file_path = self.manager.export_to_csv(export_type)
                
            messagebox.showinfo("Export Complete", f"Data exported to: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main function to run the student account management system."""
    print("🏫 Student Account Management System")
    print("=" * 50)
    print()
    print("Starting GUI interface...")
    
    app = StudentAccountGUI()
    app.run()

if __name__ == "__main__":
    main()