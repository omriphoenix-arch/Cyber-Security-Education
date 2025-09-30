#!/usr/bin/env python3
"""
Cybersecurity Education Dashboard
================================
A comprehensive learning management system for cybersecurity education
designed specifically for school environments.

Features:
- Student progress tracking
- Lesson plans and curriculum
- Interactive quizzes and assessments
- Difficulty levels for different grades
- Teacher dashboard with analytics
- Safe learning environment controls
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib
import secrets

class CyberSecurityEducationHub:
    """
    Educational hub for managing cybersecurity learning in school environments.
    """
    
    def __init__(self):
        self.students_file = "student_progress.json"
        self.lessons_file = "lesson_plans.json"
        self.quizzes_file = "quiz_results.json"
        
        self.students = self._load_data(self.students_file, {})
        self.lesson_plans = self._load_lesson_plans()
        self.quiz_results = self._load_data(self.quizzes_file, {})
        
        print("🎓 Cybersecurity Education Hub Initialized")
        print("🏫 Safe learning environment for schools")
    
    def _load_data(self, filename: str, default: dict) -> dict:
        """Load JSON data with error handling."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return default
        except (json.JSONDecodeError, IOError):
            return default
    
    def _save_data(self, filename: str, data: dict) -> None:
        """Save data to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"❌ Failed to save {filename}: {e}")
    
    def _load_lesson_plans(self) -> Dict:
        """Load comprehensive lesson plans for different grade levels."""
        return {
            "elementary": {
                "grade_3_5": [
                    {
                        "id": "elem_001",
                        "title": "What is a Password?",
                        "description": "Learn about creating strong passwords",
                        "duration": 30,
                        "activities": [
                            "Password creation game",
                            "Interactive password strength checker",
                            "Drawing exercise: visualize password security"
                        ],
                        "learning_objectives": [
                            "Understand why passwords are important",
                            "Learn what makes a password strong",
                            "Practice creating secure passwords"
                        ]
                    },
                    {
                        "id": "elem_002", 
                        "title": "Internet Safety Basics",
                        "description": "How to stay safe online",
                        "duration": 45,
                        "activities": [
                            "Online safety scenarios",
                            "Identify safe vs unsafe websites",
                            "Role-playing exercise"
                        ],
                        "learning_objectives": [
                            "Recognize safe online behavior",
                            "Identify potential online dangers",
                            "Know when to ask for adult help"
                        ]
                    }
                ]
            },
            "middle_school": {
                "grade_6_8": [
                    {
                        "id": "middle_001",
                        "title": "Introduction to Cybersecurity",
                        "description": "Overview of cybersecurity concepts and careers",
                        "duration": 50,
                        "activities": [
                            "Cybersecurity career exploration",
                            "Basic encryption activity",
                            "Password analyzer tool demonstration"
                        ],
                        "learning_objectives": [
                            "Understand cybersecurity as a field",
                            "Learn basic security concepts",
                            "Explore cybersecurity career paths"
                        ]
                    },
                    {
                        "id": "middle_002",
                        "title": "Social Engineering Awareness",
                        "description": "Understanding manipulation techniques used by attackers",
                        "duration": 45,
                        "activities": [
                            "Phishing email identification game",
                            "Social engineering scenario analysis",
                            "Create awareness poster"
                        ],
                        "learning_objectives": [
                            "Recognize social engineering attempts",
                            "Understand psychological manipulation tactics",
                            "Develop critical thinking about communications"
                        ]
                    },
                    {
                        "id": "middle_003",
                        "title": "Hash Functions and Encryption Basics",
                        "description": "Introduction to cryptography concepts",
                        "duration": 60,
                        "activities": [
                            "Hash generator demonstration",
                            "Caesar cipher activity", 
                            "Digital signature simulation"
                        ],
                        "learning_objectives": [
                            "Understand basic encryption concepts",
                            "Learn about hash functions",
                            "Appreciate importance of cryptography"
                        ]
                    }
                ]
            },
            "high_school": {
                "grade_9_12": [
                    {
                        "id": "high_001",
                        "title": "Network Security Fundamentals",
                        "description": "Understanding network attacks and defenses",
                        "duration": 90,
                        "activities": [
                            "Network discovery tool demonstration",
                            "Port scanning exercise (controlled environment)",
                            "Firewall configuration simulation"
                        ],
                        "learning_objectives": [
                            "Understand network security principles",
                            "Learn about common network attacks",
                            "Explore defensive technologies"
                        ]
                    },
                    {
                        "id": "high_002",
                        "title": "Web Application Security",
                        "description": "SQL injection and web vulnerabilities",
                        "duration": 120,
                        "activities": [
                            "Banking database simulation (user perspective)",
                            "SQL injection demonstration (ethical hacker simulation)",
                            "Secure coding workshop"
                        ],
                        "learning_objectives": [
                            "Understand web application vulnerabilities",
                            "Learn about SQL injection attacks",
                            "Practice secure coding techniques"
                        ]
                    },
                    {
                        "id": "high_003",
                        "title": "Ethical Hacking Principles",
                        "description": "Introduction to ethical hacking and penetration testing",
                        "duration": 90,
                        "activities": [
                            "Timing attack vulnerability demonstration",
                            "Hash cracking exercise",
                            "Ethical hacking methodology overview"
                        ],
                        "learning_objectives": [
                            "Understand ethical hacking principles",
                            "Learn penetration testing methodology",
                            "Appreciate legal and ethical considerations"
                        ]
                    },
                    {
                        "id": "high_004",
                        "title": "Cybersecurity Careers and Certifications",
                        "description": "Exploring cybersecurity career paths",
                        "duration": 60,
                        "activities": [
                            "Industry professional guest speaker",
                            "Certification pathway research",
                            "Portfolio development guidance"
                        ],
                        "learning_objectives": [
                            "Explore cybersecurity career options",
                            "Understand certification requirements",
                            "Develop career planning skills"
                        ]
                    }
                ]
            }
        }
    
    def register_student(self, student_id: str, name: str, grade_level: str, 
                        teacher: str = "Unknown") -> Tuple[bool, str]:
        """Register a new student in the system."""
        if student_id in self.students:
            return False, "Student already registered"
        
        self.students[student_id] = {
            "name": name,
            "grade_level": grade_level,
            "teacher": teacher,
            "registered_date": datetime.now().isoformat(),
            "completed_lessons": [],
            "quiz_scores": {},
            "badges_earned": [],
            "total_time_spent": 0,
            "last_activity": datetime.now().isoformat()
        }
        
        self._save_data(self.students_file, self.students)
        return True, f"Student {name} registered successfully"
    
    def get_lesson_plan(self, grade_category: str) -> List[Dict]:
        """Get lesson plans for a specific grade category."""
        if grade_category in self.lesson_plans:
            # Return lessons for the grade category
            for grade, lessons in self.lesson_plans[grade_category].items():
                return lessons
        return []
    
    def start_lesson(self, student_id: str, lesson_id: str) -> Tuple[bool, str, Dict]:
        """Start a lesson for a student."""
        if student_id not in self.students:
            return False, "Student not found", {}
        
        # Find the lesson
        lesson = None
        for category in self.lesson_plans.values():
            for grade_lessons in category.values():
                for l in grade_lessons:
                    if l["id"] == lesson_id:
                        lesson = l
                        break
        
        if not lesson:
            return False, "Lesson not found", {}
        
        # Update student activity
        self.students[student_id]["last_activity"] = datetime.now().isoformat()
        self._save_data(self.students_file, self.students)
        
        return True, f"Started lesson: {lesson['title']}", lesson
    
    def complete_lesson(self, student_id: str, lesson_id: str, 
                       time_spent: int, notes: str = "") -> Tuple[bool, str]:
        """Mark a lesson as completed for a student."""
        if student_id not in self.students:
            return False, "Student not found"
        
        student = self.students[student_id]
        
        if lesson_id not in student["completed_lessons"]:
            student["completed_lessons"].append(lesson_id)
            student["total_time_spent"] += time_spent
            student["last_activity"] = datetime.now().isoformat()
            
            # Award badges based on progress
            self._check_and_award_badges(student_id)
            
            self._save_data(self.students_file, self.students)
            return True, "Lesson marked as completed"
        
        return False, "Lesson already completed"
    
    def _check_and_award_badges(self, student_id: str) -> None:
        """Check and award badges based on student progress."""
        student = self.students[student_id]
        completed_count = len(student["completed_lessons"])
        
        badges = [
            ("First Steps", 1, "Completed your first cybersecurity lesson"),
            ("Learner", 3, "Completed 3 lessons"),
            ("Explorer", 5, "Completed 5 lessons"),
            ("Expert", 10, "Completed 10 lessons"),
            ("Time Investment", None, "Spent over 5 hours learning"),
        ]
        
        for badge_name, requirement, description in badges:
            if badge_name not in student["badges_earned"]:
                if badge_name == "Time Investment":
                    if student["total_time_spent"] >= 300:  # 5 hours in minutes
                        student["badges_earned"].append(badge_name)
                elif requirement and completed_count >= requirement:
                    student["badges_earned"].append(badge_name)
    
    def take_quiz(self, student_id: str, lesson_id: str, 
                  answers: List[str]) -> Tuple[bool, str, Dict]:
        """Process quiz submission and calculate score."""
        if student_id not in self.students:
            return False, "Student not found", {}
        
        # Sample quiz questions (in real implementation, these would be loaded from files)
        quiz_questions = {
            "elem_001": {
                "questions": [
                    {"question": "What makes a password strong?", "correct": "A", 
                     "options": ["A) Long and complex", "B) Your birthday", "C) Your pet's name"]},
                    {"question": "Should you share your password?", "correct": "B",
                     "options": ["A) Yes, with friends", "B) No, never", "C) Only with family"]},
                ],
                "total_points": 100
            },
            "middle_001": {
                "questions": [
                    {"question": "What is cybersecurity?", "correct": "A",
                     "options": ["A) Protecting digital information", "B) Building computers", "C) Creating websites"]},
                    {"question": "What is encryption?", "correct": "B",
                     "options": ["A) Deleting files", "B) Scrambling data for security", "C) Copying files"]},
                ],
                "total_points": 100
            }
        }
        
        if lesson_id not in quiz_questions:
            return False, "Quiz not available for this lesson", {}
        
        quiz = quiz_questions[lesson_id]
        correct_answers = 0
        
        for i, answer in enumerate(answers):
            if i < len(quiz["questions"]) and answer == quiz["questions"][i]["correct"]:
                correct_answers += 1
        
        score = int((correct_answers / len(quiz["questions"])) * quiz["total_points"])
        
        # Save quiz result
        if student_id not in self.quiz_results:
            self.quiz_results[student_id] = {}
        
        self.quiz_results[student_id][lesson_id] = {
            "score": score,
            "date_taken": datetime.now().isoformat(),
            "correct_answers": correct_answers,
            "total_questions": len(quiz["questions"])
        }
        
        self.students[student_id]["quiz_scores"][lesson_id] = score
        self._save_data(self.quizzes_file, self.quiz_results)
        self._save_data(self.students_file, self.students)
        
        result = {
            "score": score,
            "correct": correct_answers,
            "total": len(quiz["questions"]),
            "percentage": int((correct_answers / len(quiz["questions"])) * 100)
        }
        
        return True, f"Quiz completed! Score: {score}/100", result
    
    def get_student_progress(self, student_id: str) -> Tuple[bool, str, Dict]:
        """Get detailed progress report for a student."""
        if student_id not in self.students:
            return False, "Student not found", {}
        
        student = self.students[student_id]
        
        progress = {
            "student_info": {
                "name": student["name"],
                "grade_level": student["grade_level"],
                "teacher": student["teacher"]
            },
            "learning_statistics": {
                "lessons_completed": len(student["completed_lessons"]),
                "total_time_spent": student["total_time_spent"],
                "badges_earned": len(student["badges_earned"]),
                "average_quiz_score": self._calculate_average_quiz_score(student_id)
            },
            "recent_activity": student["last_activity"],
            "badges": student["badges_earned"],
            "completed_lessons": student["completed_lessons"]
        }
        
        return True, "Progress retrieved", progress
    
    def _calculate_average_quiz_score(self, student_id: str) -> float:
        """Calculate average quiz score for a student."""
        if student_id not in self.students or not self.students[student_id]["quiz_scores"]:
            return 0.0
        
        scores = list(self.students[student_id]["quiz_scores"].values())
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_class_analytics(self, teacher: str) -> Dict:
        """Get analytics for all students of a specific teacher."""
        teacher_students = {
            student_id: student for student_id, student in self.students.items()
            if student.get("teacher", "") == teacher
        }
        
        if not teacher_students:
            return {"error": "No students found for this teacher"}
        
        total_students = len(teacher_students)
        total_lessons_completed = sum(len(s["completed_lessons"]) for s in teacher_students.values())
        total_time_spent = sum(s["total_time_spent"] for s in teacher_students.values())
        
        # Find most/least active students
        most_active = max(teacher_students.items(), 
                         key=lambda x: len(x[1]["completed_lessons"]))
        least_active = min(teacher_students.items(), 
                          key=lambda x: len(x[1]["completed_lessons"]))
        
        return {
            "class_overview": {
                "total_students": total_students,
                "average_lessons_per_student": total_lessons_completed / total_students,
                "total_class_time": total_time_spent,
                "average_time_per_student": total_time_spent / total_students
            },
            "student_performance": {
                "most_active_student": {
                    "name": most_active[1]["name"], 
                    "lessons_completed": len(most_active[1]["completed_lessons"])
                },
                "least_active_student": {
                    "name": least_active[1]["name"],
                    "lessons_completed": len(least_active[1]["completed_lessons"])
                }
            },
            "recent_activity": self._get_recent_class_activity(teacher_students)
        }
    
    def _get_recent_class_activity(self, teacher_students: Dict) -> List[Dict]:
        """Get recent activity for the class."""
        activities = []
        
        for student_id, student in teacher_students.items():
            if student["last_activity"]:
                activities.append({
                    "student_name": student["name"],
                    "last_activity": student["last_activity"],
                    "lessons_completed": len(student["completed_lessons"])
                })
        
        # Sort by last activity (most recent first)
        activities.sort(key=lambda x: x["last_activity"], reverse=True)
        return activities[:10]  # Return last 10 activities


def teacher_dashboard():
    """Interactive teacher dashboard for managing cybersecurity education."""
    print("\n👩‍🏫 TEACHER DASHBOARD")
    print("=" * 40)
    
    hub = CyberSecurityEducationHub()
    
    while True:
        print("\n🎓 Cybersecurity Education Management")
        print("1. Register New Student")
        print("2. View Student Progress")
        print("3. View Class Analytics")
        print("4. Assign Lesson")
        print("5. View Available Lessons")
        print("6. Generate Progress Report")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            print("\n📝 Register New Student:")
            student_id = input("Student ID: ").strip()
            name = input("Student Name: ").strip()
            grade_level = input("Grade Level (elementary/middle_school/high_school): ").strip()
            teacher = input("Teacher Name: ").strip()
            
            success, message = hub.register_student(student_id, name, grade_level, teacher)
            print(f"{'✅' if success else '❌'} {message}")
        
        elif choice == "2":
            student_id = input("Enter Student ID: ").strip()
            success, message, progress = hub.get_student_progress(student_id)
            
            if success:
                print(f"\n📊 Progress for {progress['student_info']['name']}")
                print(f"Grade Level: {progress['student_info']['grade_level']}")
                print(f"Lessons Completed: {progress['learning_statistics']['lessons_completed']}")
                print(f"Time Spent: {progress['learning_statistics']['total_time_spent']} minutes")
                print(f"Badges Earned: {', '.join(progress['badges']) if progress['badges'] else 'None'}")
                print(f"Average Quiz Score: {progress['learning_statistics']['average_quiz_score']:.1f}%")
            else:
                print(f"❌ {message}")
        
        elif choice == "3":
            teacher = input("Enter Teacher Name: ").strip()
            analytics = hub.get_class_analytics(teacher)
            
            if "error" in analytics:
                print(f"❌ {analytics['error']}")
            else:
                print(f"\n📈 Class Analytics for {teacher}")
                print(f"Total Students: {analytics['class_overview']['total_students']}")
                print(f"Average Lessons per Student: {analytics['class_overview']['average_lessons_per_student']:.1f}")
                print(f"Most Active: {analytics['student_performance']['most_active_student']['name']} ({analytics['student_performance']['most_active_student']['lessons_completed']} lessons)")
        
        elif choice == "4":
            student_id = input("Student ID: ").strip()
            lesson_id = input("Lesson ID (e.g., elem_001, middle_001, high_001): ").strip()
            
            success, message, lesson = hub.start_lesson(student_id, lesson_id)
            if success:
                print(f"✅ {message}")
                print(f"Lesson: {lesson.get('title', 'Unknown')}")
                print(f"Duration: {lesson.get('duration', 0)} minutes")
            else:
                print(f"❌ {message}")
        
        elif choice == "5":
            print("\n📚 Available Lessons by Grade Level:")
            for category, grades in hub.lesson_plans.items():
                print(f"\n{category.upper()}:")
                for grade, lessons in grades.items():
                    print(f"  {grade}:")
                    for lesson in lessons:
                        print(f"    {lesson['id']}: {lesson['title']} ({lesson['duration']} min)")
        
        elif choice == "6":
            teacher = input("Generate report for teacher: ").strip()
            analytics = hub.get_class_analytics(teacher)
            
            # Generate and save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"class_report_{teacher}_{timestamp}.txt"
            
            with open(report_file, 'w') as f:
                f.write(f"Cybersecurity Education Progress Report\n")
                f.write(f"Teacher: {teacher}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n")
                
                if "error" not in analytics:
                    f.write(f"Class Overview:\n")
                    f.write(f"  Total Students: {analytics['class_overview']['total_students']}\n")
                    f.write(f"  Average Lessons per Student: {analytics['class_overview']['average_lessons_per_student']:.1f}\n")
                    f.write(f"  Total Class Time: {analytics['class_overview']['total_class_time']} minutes\n")
            
            print(f"✅ Report saved as {report_file}")
        
        elif choice == "7":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice.")


def student_interface():
    """Interactive student interface for cybersecurity learning."""
    print("\n👨‍🎓 STUDENT LEARNING INTERFACE")
    print("=" * 40)
    
    hub = CyberSecurityEducationHub()
    
    # Student login
    student_id = input("Enter your Student ID: ").strip()
    
    if student_id not in hub.students:
        print("❌ Student not found! Please ask your teacher to register you.")
        return
    
    student = hub.students[student_id]
    print(f"\n🎉 Welcome back, {student['name']}!")
    
    while True:
        print(f"\n🎓 Learning Dashboard for {student['name']}")
        print("=" * 40)
        print("1. View My Progress")
        print("2. Browse Available Lessons")
        print("3. Take a Quiz")
        print("4. View My Badges")
        print("5. Continue Learning")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            success, message, progress = hub.get_student_progress(student_id)
            if success:
                print(f"\n📊 Your Progress Summary:")
                print(f"   Lessons Completed: {progress['learning_statistics']['lessons_completed']}")
                print(f"   Time Spent Learning: {progress['learning_statistics']['total_time_spent']} minutes")
                print(f"   Badges Earned: {progress['learning_statistics']['badges_earned']}")
                print(f"   Average Quiz Score: {progress['learning_statistics']['average_quiz_score']:.1f}%")
        
        elif choice == "2":
            grade_category = student['grade_level']
            lessons = hub.get_lesson_plan(grade_category)
            
            print(f"\n📚 Lessons for {grade_category}:")
            for lesson in lessons:
                completed = "✅" if lesson['id'] in student['completed_lessons'] else "⭐"
                print(f"{completed} {lesson['id']}: {lesson['title']}")
                print(f"   Duration: {lesson['duration']} minutes")
                print(f"   Description: {lesson['description']}")
        
        elif choice == "3":
            lesson_id = input("Enter lesson ID for quiz (e.g., elem_001): ").strip()
            
            if lesson_id == "elem_001":
                print("\n📝 Password Security Quiz:")
                print("1. What makes a password strong?")
                print("   A) Long and complex")
                print("   B) Your birthday") 
                print("   C) Your pet's name")
                answer1 = input("Your answer (A/B/C): ").strip().upper()
                
                print("\n2. Should you share your password?")
                print("   A) Yes, with friends")
                print("   B) No, never")
                print("   C) Only with family")
                answer2 = input("Your answer (A/B/C): ").strip().upper()
                
                success, message, result = hub.take_quiz(student_id, lesson_id, [answer1, answer2])
                if success:
                    print(f"\n🎉 {message}")
                    print(f"You got {result['correct']}/{result['total']} questions correct!")
                    print(f"Percentage: {result['percentage']}%")
            else:
                print("❌ Quiz not available for this lesson yet.")
        
        elif choice == "4":
            badges = student['badges_earned']
            if badges:
                print(f"\n🏆 Your Badges ({len(badges)}):")
                for badge in badges:
                    print(f"   🎖️ {badge}")
            else:
                print("\n🏆 No badges yet - keep learning to earn your first badge!")
        
        elif choice == "5":
            print("\n🚀 Continue your cybersecurity learning journey!")
            print("Ask your teacher about the next lesson or choose from available lessons.")
            
        elif choice == "6":
            print(f"👋 Goodbye, {student['name']}! Keep learning!")
            break
        
        else:
            print("❌ Invalid choice.")


def main():
    """Main function for cybersecurity education hub."""
    print("🎓 CYBERSECURITY EDUCATION HUB")
    print("=" * 50)
    print("Interactive learning management for school cybersecurity education")
    print("=" * 50)
    
    while True:
        print("\n🏫 Main Menu:")
        print("1. 👩‍🏫 Teacher Dashboard")
        print("2. 👨‍🎓 Student Interface")
        print("3. 📋 System Information")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            teacher_dashboard()
        elif choice == "2":
            student_interface()
        elif choice == "3":
            print("\n📋 Cybersecurity Education Hub Information:")
            print("   • Designed for K-12 cybersecurity education")
            print("   • Supports multiple grade levels with age-appropriate content")
            print("   • Tracks student progress and engagement")
            print("   • Provides analytics for teachers")
            print("   • Integrates with hands-on cybersecurity simulations")
            print("   • Safe, controlled learning environment")
        elif choice == "4":
            print("🎓 Thank you for using the Cybersecurity Education Hub!")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()