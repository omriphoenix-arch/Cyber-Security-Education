#!/usr/bin/env python3
"""
Cybersecurity Assessment and Quiz Generator
==========================================
Comprehensive assessment tools for cybersecurity education with
age-appropriate quizzes, interactive challenges, and progress tracking.

Designed for school environments with multiple difficulty levels.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class CyberSecurityAssessments:
    """
    Comprehensive assessment system for cybersecurity education.
    """
    
    def __init__(self):
        self.quiz_bank = self._load_quiz_bank()
        self.interactive_challenges = self._load_interactive_challenges()
        
    def _load_quiz_bank(self) -> Dict:
        """Load comprehensive quiz questions for all grade levels."""
        return {
            "elementary": {
                "password_basics": [
                    {
                        "question": "What should a strong password have?",
                        "options": [
                            "A) Only letters",
                            "B) Letters, numbers, and symbols",
                            "C) Just your name",
                            "D) Only numbers"
                        ],
                        "correct": "B",
                        "explanation": "Strong passwords use a mix of letters, numbers, and symbols to make them harder to guess."
                    },
                    {
                        "question": "Should you tell your friends your password?",
                        "options": [
                            "A) Yes, best friends only",
                            "B) No, never tell anyone",
                            "C) Only if they ask nicely",
                            "D) Yes, but only family"
                        ],
                        "correct": "B",
                        "explanation": "Passwords should be kept secret. Never share them with anyone, even friends or family."
                    },
                    {
                        "question": "What is a good way to remember your password?",
                        "options": [
                            "A) Write it on a sticky note",
                            "B) Tell your teacher",
                            "C) Use a password manager with adult help",
                            "D) Use your birthday"
                        ],
                        "correct": "C",
                        "explanation": "Password managers are safe tools that help remember passwords. Ask an adult to help you set one up."
                    }
                ],
                "internet_safety": [
                    {
                        "question": "What should you do if someone online asks for your address?",
                        "options": [
                            "A) Tell them right away",
                            "B) Ask your parents first",
                            "C) Never give personal information online",
                            "D) Only tell them your street name"
                        ],
                        "correct": "C",
                        "explanation": "Never share personal information like your address, phone number, or real name with strangers online."
                    },
                    {
                        "question": "What makes a website safe to visit?",
                        "options": [
                            "A) It has lots of colors",
                            "B) It starts with 'https://' and has a lock icon",
                            "C) It has many advertisements",
                            "D) It asks for your password right away"
                        ],
                        "correct": "B",
                        "explanation": "Safe websites start with 'https://' and show a lock icon. This means the website is secure."
                    }
                ]
            },
            "middle_school": {
                "cybersecurity_basics": [
                    {
                        "question": "What does 'cybersecurity' mean?",
                        "options": [
                            "A) Building robots",
                            "B) Protecting computers and information from attacks",
                            "C) Creating video games",
                            "D) Fixing broken computers"
                        ],
                        "correct": "B",
                        "explanation": "Cybersecurity is about protecting digital information and computer systems from threats and attacks."
                    },
                    {
                        "question": "What is social engineering?",
                        "options": [
                            "A) Building social media websites",
                            "B) Tricking people to reveal information",
                            "C) Engineering social robots",
                            "D) Creating social networks"
                        ],
                        "correct": "B",
                        "explanation": "Social engineering is when attackers trick people into revealing sensitive information or doing something harmful."
                    }
                ],
                "encryption_basics": [
                    {
                        "question": "What is encryption?",
                        "options": [
                            "A) Deleting files permanently",
                            "B) Making copies of data",
                            "C) Scrambling data so only authorized people can read it",
                            "D) Organizing files in folders"
                        ],
                        "correct": "C",
                        "explanation": "Encryption transforms readable data into scrambled data that can only be read with the correct key."
                    },
                    {
                        "question": "What is a hash function?",
                        "options": [
                            "A) A cooking recipe",
                            "B) A function that creates a unique fingerprint for data",
                            "C) A way to delete files",
                            "D) A method to copy data"
                        ],
                        "correct": "B",
                        "explanation": "A hash function creates a unique 'fingerprint' for data. If the data changes, the fingerprint changes too."
                    }
                ]
            },
            "high_school": {
                "network_security": [
                    {
                        "question": "What is the purpose of a firewall?",
                        "options": [
                            "A) To put out fires in computers",
                            "B) To filter network traffic and block unauthorized access",
                            "C) To make computers run faster",
                            "D) To create backups of data"
                        ],
                        "correct": "B",
                        "explanation": "Firewalls act as barriers between trusted internal networks and untrusted external networks, filtering traffic."
                    },
                    {
                        "question": "What information can port scanning reveal?",
                        "options": [
                            "A) The weather forecast",
                            "B) What services are running on a target system",
                            "C) The system's physical location",
                            "D) The user's password"
                        ],
                        "correct": "B",
                        "explanation": "Port scanning reveals what network services are running on a system, which can indicate potential vulnerabilities."
                    }
                ],
                "web_security": [
                    {
                        "question": "What is SQL injection?",
                        "options": [
                            "A) Injecting medicine into databases",
                            "B) A type of cyber attack that exploits vulnerabilities in database queries",
                            "C) A way to speed up databases",
                            "D) A method to backup databases"
                        ],
                        "correct": "B",
                        "explanation": "SQL injection attacks exploit vulnerabilities in web applications to access or manipulate databases illegally."
                    },
                    {
                        "question": "How can developers prevent SQL injection?",
                        "options": [
                            "A) Use faster computers",
                            "B) Use parameterized queries instead of string concatenation",
                            "C) Make databases smaller",
                            "D) Use more colors in the website"
                        ],
                        "correct": "B",
                        "explanation": "Parameterized queries separate SQL code from user input, preventing malicious code injection."
                    }
                ],
                "ethical_hacking": [
                    {
                        "question": "What is the difference between ethical hacking and malicious hacking?",
                        "options": [
                            "A) Ethical hacking is done with permission to improve security",
                            "B) There is no difference",
                            "C) Ethical hacking is slower",
                            "D) Malicious hacking uses better tools"
                        ],
                        "correct": "A",
                        "explanation": "Ethical hacking is authorized testing to find and fix vulnerabilities, while malicious hacking is unauthorized and illegal."
                    },
                    {
                        "question": "What should an ethical hacker do when they find a vulnerability?",
                        "options": [
                            "A) Exploit it for personal gain",
                            "B) Share it on social media",
                            "C) Report it responsibly to the organization",
                            "D) Sell it to criminals"
                        ],
                        "correct": "C",
                        "explanation": "Ethical hackers must report vulnerabilities responsibly to help organizations fix security issues."
                    }
                ]
            }
        }
    
    def _load_interactive_challenges(self) -> Dict:
        """Load interactive cybersecurity challenges."""
        return {
            "password_strength_game": {
                "title": "Password Strength Challenge",
                "description": "Rate these passwords from weakest to strongest",
                "grade_levels": ["elementary", "middle_school"],
                "passwords": [
                    {"password": "123456", "strength": "Very Weak", "reasons": ["Too short", "All numbers", "Common password"]},
                    {"password": "password", "strength": "Very Weak", "reasons": ["Common word", "No numbers", "No symbols"]},
                    {"password": "MyDog123", "strength": "Weak", "reasons": ["Predictable pattern", "Personal information"]},
                    {"password": "Tr0ub4dor&3", "strength": "Strong", "reasons": ["Good length", "Mix of characters", "Unpredictable"]},
                    {"password": "correct horse battery staple", "strength": "Very Strong", "reasons": ["Very long", "Unpredictable", "Easy to remember"]}
                ]
            },
            "phishing_detector": {
                "title": "Phishing Email Detective",
                "description": "Identify which emails are phishing attempts",
                "grade_levels": ["middle_school", "high_school"],
                "emails": [
                    {
                        "subject": "Urgent: Verify Your Account Now!",
                        "sender": "security@your-bank.com",
                        "content": "Click here immediately to verify your account or it will be closed!",
                        "is_phishing": True,
                        "red_flags": ["Urgent language", "Suspicious sender domain", "Pressure tactics"]
                    },
                    {
                        "subject": "Monthly Account Statement",
                        "sender": "statements@yourbank.com",
                        "content": "Your monthly statement is ready. Log in to your account to view it.",
                        "is_phishing": False,
                        "red_flags": []
                    }
                ]
            },
            "network_detective": {
                "title": "Network Security Detective",
                "description": "Analyze network traffic for suspicious activity",
                "grade_levels": ["high_school"],
                "scenarios": [
                    {
                        "description": "Multiple failed login attempts from the same IP address",
                        "threat_level": "High",
                        "attack_type": "Brute Force Attack",
                        "response": "Block IP address, alert security team"
                    },
                    {
                        "description": "Large amounts of data being uploaded to an unknown server",
                        "threat_level": "Critical",
                        "attack_type": "Data Exfiltration",
                        "response": "Immediately block connection, investigate source"
                    }
                ]
            }
        }
    
    def generate_quiz(self, grade_level: str, topic: str, num_questions: int = 5) -> Dict:
        """Generate a customized quiz for a specific grade level and topic."""
        if grade_level not in self.quiz_bank:
            return {"error": f"Grade level '{grade_level}' not available"}
        
        if topic not in self.quiz_bank[grade_level]:
            available_topics = list(self.quiz_bank[grade_level].keys())
            return {"error": f"Topic '{topic}' not available. Available topics: {available_topics}"}
        
        questions = self.quiz_bank[grade_level][topic]
        
        # Select random questions or all if fewer than requested
        selected_questions = random.sample(questions, min(num_questions, len(questions)))
        
        quiz = {
            "quiz_info": {
                "grade_level": grade_level,
                "topic": topic,
                "total_questions": len(selected_questions),
                "generated_at": datetime.now().isoformat()
            },
            "questions": []
        }
        
        for i, question in enumerate(selected_questions, 1):
            quiz_question = {
                "question_number": i,
                "question": question["question"],
                "options": question["options"],
                "correct_answer": question["correct"],
                "explanation": question["explanation"]
            }
            quiz["questions"].append(quiz_question)
        
        return quiz
    
    def grade_quiz(self, quiz: Dict, student_answers: List[str]) -> Dict:
        """Grade a completed quiz and provide detailed feedback."""
        if "questions" not in quiz:
            return {"error": "Invalid quiz format"}
        
        total_questions = len(quiz["questions"])
        correct_count = 0
        detailed_results = []
        
        for i, question in enumerate(quiz["questions"]):
            student_answer = student_answers[i] if i < len(student_answers) else ""
            correct_answer = question["correct_answer"]
            is_correct = student_answer.upper() == correct_answer.upper()
            
            if is_correct:
                correct_count += 1
            
            result = {
                "question_number": question["question_number"],
                "question": question["question"],
                "student_answer": student_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question["explanation"]
            }
            detailed_results.append(result)
        
        score_percentage = (correct_count / total_questions) * 100
        
        # Determine grade based on percentage
        if score_percentage >= 90:
            letter_grade = "A"
            feedback = "Excellent work! You have a strong understanding of cybersecurity concepts."
        elif score_percentage >= 80:
            letter_grade = "B"
            feedback = "Good job! You understand most concepts with room for minor improvement."
        elif score_percentage >= 70:
            letter_grade = "C"
            feedback = "Satisfactory work. Review the explanations and keep studying."
        elif score_percentage >= 60:
            letter_grade = "D"
            feedback = "You're on the right track but need more study time."
        else:
            letter_grade = "F"
            feedback = "Keep studying! Review the lessons and try again."
        
        return {
            "quiz_results": {
                "total_questions": total_questions,
                "correct_answers": correct_count,
                "score_percentage": round(score_percentage, 1),
                "letter_grade": letter_grade,
                "feedback": feedback
            },
            "detailed_results": detailed_results,
            "study_recommendations": self._generate_study_recommendations(detailed_results)
        }
    
    def _generate_study_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate personalized study recommendations based on quiz performance."""
        recommendations = []
        
        # Analyze incorrect answers for patterns
        incorrect_topics = []
        for result in results:
            if not result["is_correct"]:
                # Extract topic from question content (simple heuristic)
                question = result["question"].lower()
                if "password" in question:
                    incorrect_topics.append("password security")
                elif "encrypt" in question or "hash" in question:
                    incorrect_topics.append("cryptography")
                elif "network" in question or "firewall" in question:
                    incorrect_topics.append("network security")
                elif "sql" in question or "injection" in question:
                    incorrect_topics.append("web security")
                elif "phishing" in question or "social" in question:
                    incorrect_topics.append("social engineering")
        
        # Generate specific recommendations
        unique_topics = list(set(incorrect_topics))
        
        if "password security" in unique_topics:
            recommendations.append("Review password creation best practices and try the password strength challenge")
        
        if "cryptography" in unique_topics:
            recommendations.append("Practice with the hash generator tool to understand cryptographic concepts")
        
        if "network security" in unique_topics:
            recommendations.append("Explore the network discovery tools to learn about network security")
        
        if "web security" in unique_topics:
            recommendations.append("Try the SQL injection simulation to understand web vulnerabilities")
        
        if "social engineering" in unique_topics:
            recommendations.append("Practice with the phishing email detector challenge")
        
        if not recommendations:
            recommendations.append("Great job! Continue exploring advanced cybersecurity topics")
        
        return recommendations
    
    def run_interactive_challenge(self, challenge_name: str, grade_level: str) -> Dict:
        """Run an interactive cybersecurity challenge."""
        if challenge_name not in self.interactive_challenges:
            return {"error": f"Challenge '{challenge_name}' not found"}
        
        challenge = self.interactive_challenges[challenge_name]
        
        if grade_level not in challenge["grade_levels"]:
            return {"error": f"Challenge not appropriate for grade level '{grade_level}'"}
        
        return {
            "challenge_info": {
                "title": challenge["title"],
                "description": challenge["description"],
                "grade_level": grade_level
            },
            "challenge_data": challenge
        }


def interactive_assessment_center():
    """Interactive assessment center for teachers and students."""
    print("\n📝 CYBERSECURITY ASSESSMENT CENTER")
    print("=" * 50)
    
    assessments = CyberSecurityAssessments()
    
    while True:
        print("\n🎯 Assessment Options:")
        print("1. 🧑‍🏫 Teacher: Generate Custom Quiz")
        print("2. 👨‍🎓 Student: Take Practice Quiz")
        print("3. 🎮 Interactive Challenge")
        print("4. 📊 Grade Quiz")
        print("5. 📋 View Available Topics")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🧑‍🏫 Quiz Generation for Teachers")
            
            print("\nAvailable Grade Levels: elementary, middle_school, high_school")
            grade_level = input("Enter grade level: ").strip()
            
            if grade_level in assessments.quiz_bank:
                topics = list(assessments.quiz_bank[grade_level].keys())
                print(f"\nAvailable topics for {grade_level}: {', '.join(topics)}")
                topic = input("Enter topic: ").strip()
                
                try:
                    num_questions = int(input("Number of questions (1-10): ").strip())
                    num_questions = max(1, min(10, num_questions))
                except ValueError:
                    num_questions = 5
                
                quiz = assessments.generate_quiz(grade_level, topic, num_questions)
                
                if "error" in quiz:
                    print(f"❌ {quiz['error']}")
                else:
                    # Save quiz to file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"quiz_{grade_level}_{topic}_{timestamp}.json"
                    
                    with open(filename, 'w') as f:
                        json.dump(quiz, f, indent=2)
                    
                    print(f"✅ Quiz generated and saved as '{filename}'")
                    print(f"📊 Quiz contains {quiz['quiz_info']['total_questions']} questions")
            else:
                print("❌ Invalid grade level")
        
        elif choice == "2":
            print("\n👨‍🎓 Practice Quiz for Students")
            
            print("\nSelect your grade level:")
            print("1. Elementary (Grades 3-5)")
            print("2. Middle School (Grades 6-8)")  
            print("3. High School (Grades 9-12)")
            
            grade_choice = input("Enter choice (1-3): ").strip()
            grade_map = {"1": "elementary", "2": "middle_school", "3": "high_school"}
            
            if grade_choice in grade_map:
                grade_level = grade_map[grade_choice]
                topics = list(assessments.quiz_bank[grade_level].keys())
                
                print(f"\nAvailable topics: {', '.join(topics)}")
                topic = input("Choose a topic: ").strip()
                
                quiz = assessments.generate_quiz(grade_level, topic, 3)  # 3 questions for practice
                
                if "error" not in quiz:
                    print(f"\n📝 {topic.replace('_', ' ').title()} Quiz")
                    print("=" * 40)
                    
                    student_answers = []
                    for question in quiz["questions"]:
                        print(f"\nQuestion {question['question_number']}: {question['question']}")
                        for option in question["options"]:
                            print(f"   {option}")
                        
                        answer = input("Your answer: ").strip().upper()
                        student_answers.append(answer)
                    
                    # Grade the quiz
                    results = assessments.grade_quiz(quiz, student_answers)
                    
                    print(f"\n🎉 Quiz Results:")
                    print(f"Score: {results['quiz_results']['correct_answers']}/{results['quiz_results']['total_questions']}")
                    print(f"Percentage: {results['quiz_results']['score_percentage']}%")
                    print(f"Grade: {results['quiz_results']['letter_grade']}")
                    print(f"Feedback: {results['quiz_results']['feedback']}")
                    
                    if results['study_recommendations']:
                        print(f"\n📚 Study Recommendations:")
                        for rec in results['study_recommendations']:
                            print(f"   • {rec}")
                else:
                    print(f"❌ {quiz['error']}")
            else:
                print("❌ Invalid choice")
        
        elif choice == "3":
            print("\n🎮 Interactive Challenges")
            
            challenges = list(assessments.interactive_challenges.keys())
            print(f"\nAvailable challenges:")
            for i, challenge in enumerate(challenges, 1):
                title = assessments.interactive_challenges[challenge]["title"]
                print(f"{i}. {title}")
            
            try:
                choice_idx = int(input(f"\nSelect challenge (1-{len(challenges)}): ").strip()) - 1
                if 0 <= choice_idx < len(challenges):
                    challenge_name = challenges[choice_idx]
                    
                    grade_choice = input("Your grade level (elementary/middle_school/high_school): ").strip()
                    
                    result = assessments.run_interactive_challenge(challenge_name, grade_choice)
                    
                    if "error" in result:
                        print(f"❌ {result['error']}")
                    else:
                        print(f"\n🎯 {result['challenge_info']['title']}")
                        print(f"📖 {result['challenge_info']['description']}")
                        print("\n🎮 Challenge loaded! (Implementation would be interactive)")
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "4":
            print("\n📊 Quiz Grading")
            print("This feature would allow teachers to grade student quizzes")
            print("and generate detailed performance reports.")
        
        elif choice == "5":
            print("\n📋 Available Assessment Topics by Grade Level:")
            for grade_level, topics in assessments.quiz_bank.items():
                print(f"\n{grade_level.replace('_', ' ').title()}:")
                for topic in topics.keys():
                    question_count = len(topics[topic])
                    print(f"   • {topic.replace('_', ' ').title()} ({question_count} questions)")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    interactive_assessment_center()