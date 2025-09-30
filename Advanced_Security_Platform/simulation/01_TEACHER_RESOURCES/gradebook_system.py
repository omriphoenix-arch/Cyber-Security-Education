#!/usr/bin/env python3
"""
Enhanced Gradebook System for Cybersecurity Education
===================================================
Professional gradebook with export capabilities, parent reports,
and school information system integration.

Features:
- Grade export to CSV/Excel formats
- Parent progress reports generation
- Administrative reporting for district requirements
- Integration hooks for school LMS systems
"""

import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Grade:
    """Individual grade record"""
    student_id: str
    assignment_name: str
    category: str  # quiz, lab, project, participation
    points_earned: float
    points_possible: float
    date_recorded: str
    teacher_notes: str = ""
    
    @property
    def percentage(self) -> float:
        return (self.points_earned / self.points_possible * 100) if self.points_possible > 0 else 0

@dataclass
class StudentSummary:
    """Student grade summary"""
    student_id: str
    student_name: str
    current_grade: float
    letter_grade: str
    assignments_completed: int
    assignments_total: int
    last_activity: str
    strengths: List[str]
    needs_improvement: List[str]

class EnhancedGradebook:
    """
    Professional gradebook system for cybersecurity education.
    """
    
    def __init__(self, db_path: str = "gradebook.db"):
        self.db_path = db_path
        self.init_database()
        
        # Grade scale configuration
        self.grade_scale = {
            'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 0
        }
        
        # Assignment categories and weights
        self.category_weights = {
            'quiz': 0.30,        # 30% - Quizzes and assessments
            'lab': 0.40,         # 40% - Hands-on labs and projects
            'project': 0.20,     # 20% - Major projects
            'participation': 0.10 # 10% - Class participation
        }
    
    def init_database(self):
        """Initialize the gradebook database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade_level TEXT,
            teacher TEXT,
            parent_email TEXT,
            enrollment_date TEXT,
            active BOOLEAN DEFAULT 1
        )
        ''')
        
        # Grades table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            assignment_name TEXT,
            category TEXT,
            points_earned REAL,
            points_possible REAL,
            date_recorded TEXT,
            teacher_notes TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
        ''')
        
        # Assignments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            points_possible REAL,
            due_date TEXT,
            description TEXT,
            standards_aligned TEXT  -- JSON string of standards
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student(self, student_id: str, name: str, grade_level: str, 
                   teacher: str, parent_email: str = "") -> bool:
        """Add a new student to the gradebook"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT OR REPLACE INTO students 
            (student_id, name, grade_level, teacher, parent_email, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, grade_level, teacher, parent_email, 
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False
    
    def record_grade(self, student_id: str, assignment_name: str, 
                    category: str, points_earned: float, points_possible: float,
                    teacher_notes: str = "") -> bool:
        """Record a grade for a student"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO grades 
            (student_id, assignment_name, category, points_earned, points_possible, 
             date_recorded, teacher_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, assignment_name, category, points_earned, 
                  points_possible, datetime.now().isoformat(), teacher_notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording grade: {e}")
            return False
    
    def calculate_student_grade(self, student_id: str) -> Tuple[float, str]:
        """Calculate weighted grade for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT category, points_earned, points_possible
        FROM grades WHERE student_id = ?
        ''', (student_id,))
        
        grades = cursor.fetchall()
        conn.close()
        
        if not grades:
            return 0.0, "No Grades"
        
        # Calculate category averages
        category_totals = {}
        for category, earned, possible in grades:
            if category not in category_totals:
                category_totals[category] = {'earned': 0, 'possible': 0}
            category_totals[category]['earned'] += earned
            category_totals[category]['possible'] += possible
        
        # Calculate weighted grade
        weighted_score = 0.0
        total_weight = 0.0
        
        for category, totals in category_totals.items():
            if category in self.category_weights and totals['possible'] > 0:
                category_avg = totals['earned'] / totals['possible'] * 100
                weight = self.category_weights[category]
                weighted_score += category_avg * weight
                total_weight += weight
        
        if total_weight > 0:
            final_grade = weighted_score / total_weight
        else:
            final_grade = 0.0
        
        # Determine letter grade
        letter_grade = 'F'
        for letter, threshold in self.grade_scale.items():
            if final_grade >= threshold:
                letter_grade = letter
                break
        
        return round(final_grade, 2), letter_grade
    
    def get_student_summary(self, student_id: str) -> Optional[StudentSummary]:
        """Get comprehensive student summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute('''
        SELECT name FROM students WHERE student_id = ?
        ''', (student_id,))
        
        student_result = cursor.fetchone()
        if not student_result:
            conn.close()
            return None
        
        student_name = student_result[0]
        
        # Get grades and calculate summary
        cursor.execute('''
        SELECT assignment_name, category, points_earned, points_possible, date_recorded
        FROM grades WHERE student_id = ?
        ORDER BY date_recorded DESC
        ''', (student_id,))
        
        grades = cursor.fetchall()
        conn.close()
        
        current_grade, letter_grade = self.calculate_student_grade(student_id)
        
        # Analyze strengths and weaknesses
        strengths = []
        needs_improvement = []
        
        category_performance = {}
        for _, category, earned, possible, _ in grades:
            if category not in category_performance:
                category_performance[category] = {'earned': 0, 'possible': 0}
            category_performance[category]['earned'] += earned
            category_performance[category]['possible'] += possible
        
        for category, totals in category_performance.items():
            if totals['possible'] > 0:
                avg = totals['earned'] / totals['possible'] * 100
                if avg >= 85:
                    strengths.append(f"Strong in {category} ({avg:.1f}%)")
                elif avg < 70:
                    needs_improvement.append(f"Needs work in {category} ({avg:.1f}%)")
        
        last_activity = grades[0][4] if grades else "No activity"
        
        return StudentSummary(
            student_id=student_id,
            student_name=student_name,
            current_grade=current_grade,
            letter_grade=letter_grade,
            assignments_completed=len(grades),
            assignments_total=len(grades),  # This would need assignment tracking
            last_activity=last_activity,
            strengths=strengths,
            needs_improvement=needs_improvement
        )
    
    def export_grades_csv(self, output_path: str, class_filter: str = None) -> bool:
        """Export grades to CSV format for school information systems"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all students and their grades
            query = '''
            SELECT s.student_id, s.name, s.grade_level, s.teacher,
                   g.assignment_name, g.category, g.points_earned, 
                   g.points_possible, g.date_recorded
            FROM students s
            LEFT JOIN grades g ON s.student_id = g.student_id
            WHERE s.active = 1
            '''
            
            if class_filter:
                query += " AND s.teacher = ?"
                cursor.execute(query, (class_filter,))
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.close()
            
            # Write CSV file
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header row
                writer.writerow([
                    'Student ID', 'Student Name', 'Grade Level', 'Teacher',
                    'Assignment', 'Category', 'Points Earned', 'Points Possible',
                    'Percentage', 'Date Recorded'
                ])
                
                # Data rows
                for row in results:
                    if row[6] is not None:  # Has grade data
                        percentage = (row[6] / row[7] * 100) if row[7] > 0 else 0
                        writer.writerow([
                            row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6], row[7], f"{percentage:.1f}%", row[8]
                        ])
                    else:  # Student with no grades
                        writer.writerow([
                            row[0], row[1], row[2], row[3], 
                            "No assignments", "", "", "", "", ""
                        ])
            
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False
    
    def generate_parent_report(self, student_id: str, output_path: str) -> bool:
        """Generate detailed parent progress report"""
        summary = self.get_student_summary(student_id)
        if not summary:
            return False
        
        try:
            # Get detailed grade breakdown
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT assignment_name, category, points_earned, points_possible, 
                   date_recorded, teacher_notes
            FROM grades WHERE student_id = ?
            ORDER BY date_recorded DESC
            ''', (student_id,))
            
            grades = cursor.fetchall()
            conn.close()
            
            # Generate HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Progress Report - {summary.student_name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: #2c5aa0; color: white; padding: 15px; }}
                    .summary {{ background: #f5f5f5; padding: 15px; margin: 10px 0; }}
                    .grade-table {{ width: 100%; border-collapse: collapse; }}
                    .grade-table th, .grade-table td {{ border: 1px solid #ddd; padding: 8px; }}
                    .grade-table th {{ background: #f2f2f2; }}
                    .strengths {{ color: green; }}
                    .needs-work {{ color: orange; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Cybersecurity Education Progress Report</h1>
                    <h2>{summary.student_name} (ID: {summary.student_id})</h2>
                    <p>Report Generated: {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="summary">
                    <h3>Overall Performance Summary</h3>
                    <p><strong>Current Grade:</strong> {summary.current_grade:.1f}% ({summary.letter_grade})</p>
                    <p><strong>Assignments Completed:</strong> {summary.assignments_completed}</p>
                    <p><strong>Last Activity:</strong> {summary.last_activity}</p>
                </div>
                
                <div class="summary">
                    <h3>Strengths</h3>
                    <ul class="strengths">
            """
            
            for strength in summary.strengths:
                html_content += f"<li>{strength}</li>"
            
            html_content += """
                    </ul>
                    
                    <h3>Areas for Improvement</h3>
                    <ul class="needs-work">
            """
            
            for improvement in summary.needs_improvement:
                html_content += f"<li>{improvement}</li>"
            
            html_content += """
                    </ul>
                </div>
                
                <h3>Recent Assignment Details</h3>
                <table class="grade-table">
                    <tr>
                        <th>Assignment</th>
                        <th>Category</th>
                        <th>Score</th>
                        <th>Percentage</th>
                        <th>Date</th>
                        <th>Teacher Notes</th>
                    </tr>
            """
            
            for assignment, category, earned, possible, date, notes in grades[:10]:  # Last 10 assignments
                percentage = (earned / possible * 100) if possible > 0 else 0
                date_formatted = datetime.fromisoformat(date).strftime('%m/%d/%Y')
                
                html_content += f"""
                    <tr>
                        <td>{assignment}</td>
                        <td>{category.title()}</td>
                        <td>{earned}/{possible}</td>
                        <td>{percentage:.1f}%</td>
                        <td>{date_formatted}</td>
                        <td>{notes}</td>
                    </tr>
                """
            
            html_content += """
                </table>
                
                <div class="summary">
                    <h3>About Our Cybersecurity Program</h3>
                    <p>Your student is participating in a comprehensive cybersecurity education program that covers:</p>
                    <ul>
                        <li>Digital citizenship and online safety</li>
                        <li>Password security and encryption basics</li>
                        <li>Ethical hacking and security principles</li>
                        <li>Programming and problem-solving skills</li>
                        <li>Career preparation in cybersecurity fields</li>
                    </ul>
                    <p>For questions about your student's progress, please contact their teacher.</p>
                </div>
            </body>
            </html>
            """
            
            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            return True
        except Exception as e:
            print(f"Error generating parent report: {e}")
            return False
    
    def get_class_summary(self, teacher: str) -> Dict:
        """Generate class performance summary for teachers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all students for this teacher
        cursor.execute('''
        SELECT student_id, name FROM students 
        WHERE teacher = ? AND active = 1
        ''', (teacher,))
        
        students = cursor.fetchall()
        conn.close()
        
        class_data = {
            'teacher': teacher,
            'total_students': len(students),
            'students': [],
            'class_average': 0.0,
            'grade_distribution': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        }
        
        total_grade = 0.0
        for student_id, name in students:
            grade, letter = self.calculate_student_grade(student_id)
            class_data['students'].append({
                'id': student_id,
                'name': name,
                'grade': grade,
                'letter': letter
            })
            total_grade += grade
            class_data['grade_distribution'][letter] += 1
        
        if students:
            class_data['class_average'] = round(total_grade / len(students), 2)
        
        return class_data

def interactive_gradebook():
    """Interactive gradebook interface for teachers"""
    gradebook = EnhancedGradebook()
    
    while True:
        print("\n📊 ENHANCED GRADEBOOK SYSTEM")
        print("=" * 50)
        print("1. 👨‍🎓 Add Student")
        print("2. 📝 Record Grade")
        print("3. 📊 View Student Summary")
        print("4. 📈 Class Performance Summary")
        print("5. 📤 Export Grades to CSV")
        print("6. 📧 Generate Parent Report")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            print("\n👨‍🎓 Add New Student")
            student_id = input("Student ID: ").strip()
            name = input("Student Name: ").strip()
            grade_level = input("Grade Level (elementary/middle_school/high_school): ").strip()
            teacher = input("Teacher Name: ").strip()
            parent_email = input("Parent Email (optional): ").strip()
            
            if gradebook.add_student(student_id, name, grade_level, teacher, parent_email):
                print("✅ Student added successfully!")
            else:
                print("❌ Error adding student.")
        
        elif choice == "2":
            print("\n📝 Record Grade")
            student_id = input("Student ID: ").strip()
            assignment = input("Assignment Name: ").strip()
            print("Categories: quiz, lab, project, participation")
            category = input("Category: ").strip()
            try:
                earned = float(input("Points Earned: "))
                possible = float(input("Points Possible: "))
                notes = input("Teacher Notes (optional): ").strip()
                
                if gradebook.record_grade(student_id, assignment, category, earned, possible, notes):
                    print("✅ Grade recorded successfully!")
                else:
                    print("❌ Error recording grade.")
            except ValueError:
                print("❌ Invalid point values.")
        
        elif choice == "3":
            print("\n📊 Student Summary")
            student_id = input("Student ID: ").strip()
            summary = gradebook.get_student_summary(student_id)
            
            if summary:
                print(f"\n🎓 {summary.student_name}")
                print(f"Current Grade: {summary.current_grade}% ({summary.letter_grade})")
                print(f"Assignments: {summary.assignments_completed}")
                print(f"Strengths: {', '.join(summary.strengths) if summary.strengths else 'None noted'}")
                print(f"Needs Work: {', '.join(summary.needs_improvement) if summary.needs_improvement else 'None noted'}")
            else:
                print("❌ Student not found.")
        
        elif choice == "4":
            print("\n📈 Class Performance Summary")
            teacher = input("Teacher Name: ").strip()
            summary = gradebook.get_class_summary(teacher)
            
            print(f"\nClass: {teacher}")
            print(f"Students: {summary['total_students']}")
            print(f"Class Average: {summary['class_average']}%")
            print("\nGrade Distribution:")
            for grade, count in summary['grade_distribution'].items():
                print(f"  {grade}: {count} students")
        
        elif choice == "5":
            print("\n📤 Export Grades")
            filename = input("Output filename (e.g., grades.csv): ").strip()
            teacher = input("Teacher filter (optional): ").strip()
            
            if gradebook.export_grades_csv(filename, teacher if teacher else None):
                print(f"✅ Grades exported to {filename}")
            else:
                print("❌ Export failed.")
        
        elif choice == "6":
            print("\n📧 Generate Parent Report")
            student_id = input("Student ID: ").strip()
            filename = input("Output filename (e.g., report.html): ").strip()
            
            if gradebook.generate_parent_report(student_id, filename):
                print(f"✅ Parent report generated: {filename}")
            else:
                print("❌ Report generation failed.")
        
        elif choice == "7":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    interactive_gradebook()