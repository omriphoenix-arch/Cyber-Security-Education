#!/usr/bin/env python3
"""
Standards Alignment System for Cybersecurity Education
=====================================================
Comprehensive mapping to educational standards including CSTA, Common Core,
and state-specific cybersecurity education requirements.

Features:
- CSTA (Computer Science Teachers Association) standards alignment
- Common Core Math/Science integration
- State cybersecurity education standards
- CTE (Career and Technical Education) pathway mapping
- Automated standards reporting for curriculum compliance
"""

import json
import os
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Standard:
    """Educational standard definition"""
    standard_id: str
    organization: str  # CSTA, Common Core, State, CTE
    grade_level: str
    title: str
    description: str
    category: str
    subcategory: str = ""

@dataclass
class LessonAlignment:
    """Lesson to standards alignment"""
    lesson_id: str
    lesson_title: str
    aligned_standards: List[str]
    evidence_of_alignment: str
    assessment_methods: List[str]

class StandardsAlignmentSystem:
    """
    Comprehensive standards alignment and reporting system.
    """
    
    def __init__(self):
        self.standards_db = {}
        self.lesson_alignments = {}
        self.load_standards_database()
    
    def load_standards_database(self):
        """Load comprehensive standards database"""
        
        # CSTA (Computer Science Teachers Association) Standards
        csta_standards = {
            # Grades K-2
            "1A-CS-01": Standard(
                "1A-CS-01", "CSTA", "K-2", 
                "Computing Systems - Devices",
                "Select and operate appropriate software to perform a variety of tasks, and recognize that users have different needs and preferences for the technology they use.",
                "Computing Systems", "Devices"
            ),
            "1A-CS-02": Standard(
                "1A-CS-02", "CSTA", "K-2",
                "Computing Systems - Hardware and Software", 
                "Use appropriate terminology in identifying and describing the function of common physical components of computing systems (hardware).",
                "Computing Systems", "Hardware and Software"
            ),
            "1A-CS-03": Standard(
                "1A-CS-03", "CSTA", "K-2",
                "Computing Systems - Troubleshooting",
                "Describe basic hardware and software problems using accurate terminology.",
                "Computing Systems", "Troubleshooting"
            ),
            
            # Grades 3-5 (Elementary)
            "1B-CS-01": Standard(
                "1B-CS-01", "CSTA", "3-5",
                "Computing Systems - Devices",
                "Describe how internal and external parts of computing devices function to form a system.",
                "Computing Systems", "Devices"
            ),
            "1B-CS-02": Standard(
                "1B-CS-02", "CSTA", "3-5",
                "Computing Systems - Hardware and Software",
                "Model how computer hardware and software work together as a system to accomplish tasks.",
                "Computing Systems", "Hardware and Software"
            ),
            "1B-CS-03": Standard(
                "1B-CS-03", "CSTA", "3-5",
                "Computing Systems - Troubleshooting",
                "Determine potential solutions to solve simple hardware and software problems using common troubleshooting strategies.",
                "Computing Systems", "Troubleshooting"
            ),
            "1B-NI-04": Standard(
                "1B-NI-04", "CSTA", "3-5",
                "Networks and the Internet - Cybersecurity",
                "Explain what passwords are and why we use them, and use strong passwords to protect devices and information from unauthorized access.",
                "Networks and the Internet", "Cybersecurity"
            ),
            "1B-NI-05": Standard(
                "1B-NI-05", "CSTA", "3-5",
                "Networks and the Internet - Cybersecurity", 
                "Explain why information should be shared with care and discuss the positive and negative effects of sharing information through online communication.",
                "Networks and the Internet", "Cybersecurity"
            ),
            
            # Grades 6-8 (Middle School)
            "2-CS-01": Standard(
                "2-CS-01", "CSTA", "6-8",
                "Computing Systems - Devices",
                "Recommend improvements to the design of computing devices, based on an analysis of how users interact with the devices.",
                "Computing Systems", "Devices"
            ),
            "2-CS-02": Standard(
                "2-CS-02", "CSTA", "6-8",
                "Computing Systems - Hardware and Software",
                "Design projects that combine hardware and software components to collect and exchange data.",
                "Computing Systems", "Hardware and Software"
            ),
            "2-CS-03": Standard(
                "2-CS-03", "CSTA", "6-8",
                "Computing Systems - Troubleshooting",
                "Systematically identify and fix problems with computing devices and their components.",
                "Computing Systems", "Troubleshooting"
            ),
            "2-NI-04": Standard(
                "2-NI-04", "CSTA", "6-8",
                "Networks and the Internet - Cybersecurity",
                "Model the role of protocols in transmitting data across networks and the Internet.",
                "Networks and the Internet", "Network Communication and Organization"
            ),
            "2-NI-05": Standard(
                "2-NI-05", "CSTA", "6-8",
                "Networks and the Internet - Cybersecurity",
                "Explain how physical and digital security measures protect electronic information.",
                "Networks and the Internet", "Cybersecurity"
            ),
            "2-NI-06": Standard(
                "2-NI-06", "CSTA", "6-8", 
                "Networks and the Internet - Cybersecurity",
                "Apply multiple methods of encryption to model the secure transmission of information.",
                "Networks and the Internet", "Cybersecurity"
            ),
            
            # Grades 9-12 (High School)
            "3A-CS-01": Standard(
                "3A-CS-01", "CSTA", "9-12",
                "Computing Systems - Devices",
                "Explain how abstractions hide the underlying implementation details of computing systems embedded in everyday objects.",
                "Computing Systems", "Devices"
            ),
            "3A-CS-02": Standard(
                "3A-CS-02", "CSTA", "9-12",
                "Computing Systems - Hardware and Software", 
                "Compare levels of abstraction and interactions between application software, system software, and hardware layers.",
                "Computing Systems", "Hardware and Software"
            ),
            "3A-CS-03": Standard(
                "3A-CS-03", "CSTA", "9-12",
                "Computing Systems - Troubleshooting",
                "Develop guidelines that convey systematic troubleshooting strategies that others can use to identify and fix errors.",
                "Computing Systems", "Troubleshooting"
            ),
            "3A-NI-04": Standard(
                "3A-NI-04", "CSTA", "9-12",
                "Networks and the Internet - Network Communication",
                "Evaluate the scalability and reliability of networks, by describing the relationship between routers, switches, servers, topology, and addressing.",
                "Networks and the Internet", "Network Communication and Organization"
            ),
            "3A-NI-05": Standard(
                "3A-NI-05", "CSTA", "9-12",
                "Networks and the Internet - Cybersecurity",
                "Give examples to illustrate how sensitive data can be affected by malware and other attacks.",
                "Networks and the Internet", "Cybersecurity"
            ),
            "3A-NI-06": Standard(
                "3A-NI-06", "CSTA", "9-12",
                "Networks and the Internet - Cybersecurity",
                "Recommend security measures to address various scenarios based on factors such as efficiency, feasibility, and ethical impacts.",
                "Networks and the Internet", "Cybersecurity"
            ),
            "3A-NI-07": Standard(
                "3A-NI-07", "CSTA", "9-12", 
                "Networks and the Internet - Cybersecurity",
                "Compare various security measures, considering tradeoffs between the usability and security of a computing system.",
                "Networks and the Internet", "Cybersecurity"
            ),
            "3A-NI-08": Standard(
                "3A-NI-08", "CSTA", "9-12",
                "Networks and the Internet - Cybersecurity",
                "Explain tradeoffs when selecting and implementing cybersecurity recommendations.",
                "Networks and the Internet", "Cybersecurity"
            )
        }
        
        # Common Core Mathematics Standards (relevant to cryptography/cybersecurity)
        common_core_math = {
            "CCSS.MATH.6.EE.A.1": Standard(
                "CCSS.MATH.6.EE.A.1", "Common Core Math", "6",
                "Expressions and Equations",
                "Write and evaluate numerical expressions involving whole-number exponents.",
                "Expressions and Equations", "Apply and extend understanding"
            ),
            "CCSS.MATH.8.F.B.4": Standard(
                "CCSS.MATH.8.F.B.4", "Common Core Math", "8", 
                "Functions",
                "Construct a function to model a linear relationship between two quantities.",
                "Functions", "Linear Functions"
            ),
            "CCSS.MATH.HSA.SSE.B.3": Standard(
                "CCSS.MATH.HSA.SSE.B.3", "Common Core Math", "9-12",
                "Seeing Structure in Expressions",
                "Choose and produce an equivalent form of an expression to reveal and explain properties.",
                "Algebra", "Seeing Structure in Expressions"
            )
        }
        
        # Career and Technical Education (CTE) Standards
        cte_standards = {
            "CTE.IT.1": Standard(
                "CTE.IT.1", "CTE", "9-12",
                "Information Technology Career Pathway",
                "Demonstrate knowledge of information technology career opportunities and requirements.",
                "Information Technology", "Career Exploration"
            ),
            "CTE.IT.2": Standard(
                "CTE.IT.2", "CTE", "9-12", 
                "Cybersecurity Fundamentals",
                "Identify and analyze cybersecurity threats, vulnerabilities, and attack methods.",
                "Information Technology", "Cybersecurity"
            ),
            "CTE.IT.3": Standard(
                "CTE.IT.3", "CTE", "9-12",
                "Network Security",
                "Design and implement network security solutions including firewalls, intrusion detection, and access controls.",
                "Information Technology", "Network Security"
            ),
            "CTE.IT.4": Standard(
                "CTE.IT.4", "CTE", "9-12",
                "Ethical Hacking and Penetration Testing", 
                "Conduct ethical penetration testing and vulnerability assessments following legal and ethical guidelines.",
                "Information Technology", "Ethical Hacking"
            )
        }
        
        # Combine all standards
        self.standards_db.update(csta_standards)
        self.standards_db.update(common_core_math)
        self.standards_db.update(cte_standards)
    
    def get_standards_by_grade(self, grade_level: str) -> List[Standard]:
        """Get all standards for a specific grade level"""
        standards = []
        for standard in self.standards_db.values():
            if self._grade_matches(standard.grade_level, grade_level):
                standards.append(standard)
        return standards
    
    def _grade_matches(self, standard_grade: str, target_grade: str) -> bool:
        """Check if grade levels match"""
        grade_mappings = {
            'elementary': ['K-2', '3-5'],
            'middle_school': ['6-8'],
            'high_school': ['9-12']
        }
        
        if target_grade in grade_mappings:
            return standard_grade in grade_mappings[target_grade]
        
        return standard_grade == target_grade
    
    def align_lesson_to_standards(self, lesson_id: str, lesson_title: str, 
                                standard_ids: List[str], evidence: str,
                                assessment_methods: List[str]) -> bool:
        """Align a lesson to specific standards"""
        try:
            # Validate standards exist
            for std_id in standard_ids:
                if std_id not in self.standards_db:
                    print(f"Warning: Standard {std_id} not found in database")
            
            alignment = LessonAlignment(
                lesson_id=lesson_id,
                lesson_title=lesson_title,
                aligned_standards=standard_ids,
                evidence_of_alignment=evidence,
                assessment_methods=assessment_methods
            )
            
            self.lesson_alignments[lesson_id] = alignment
            return True
        except Exception as e:
            print(f"Error aligning lesson: {e}")
            return False
    
    def get_lesson_standards(self, lesson_id: str) -> List[Standard]:
        """Get all standards aligned to a specific lesson"""
        if lesson_id not in self.lesson_alignments:
            return []
        
        alignment = self.lesson_alignments[lesson_id]
        return [self.standards_db[std_id] for std_id in alignment.aligned_standards 
                if std_id in self.standards_db]
    
    def generate_standards_report(self, grade_level: str = None, 
                                organization: str = None) -> Dict:
        """Generate comprehensive standards alignment report"""
        
        # Filter standards based on criteria
        filtered_standards = []
        for standard in self.standards_db.values():
            include = True
            
            if grade_level and not self._grade_matches(standard.grade_level, grade_level):
                include = False
            
            if organization and standard.organization != organization:
                include = False
            
            if include:
                filtered_standards.append(standard)
        
        # Analyze coverage
        covered_standards = set()
        for alignment in self.lesson_alignments.values():
            covered_standards.update(alignment.aligned_standards)
        
        report = {
            'report_date': datetime.now().isoformat(),
            'filters': {
                'grade_level': grade_level,
                'organization': organization
            },
            'summary': {
                'total_standards': len(filtered_standards),
                'covered_standards': len(covered_standards.intersection(
                    {std.standard_id for std in filtered_standards}
                )),
                'coverage_percentage': 0.0
            },
            'standards_by_category': {},
            'lesson_alignments': [],
            'uncovered_standards': []
        }
        
        # Calculate coverage percentage
        if filtered_standards:
            covered_count = len(covered_standards.intersection(
                {std.standard_id for std in filtered_standards}
            ))
            report['summary']['coverage_percentage'] = round(
                (covered_count / len(filtered_standards)) * 100, 1
            )
        
        # Group standards by category
        for standard in filtered_standards:
            category = standard.category
            if category not in report['standards_by_category']:
                report['standards_by_category'][category] = {
                    'total': 0,
                    'covered': 0,
                    'standards': []
                }
            
            report['standards_by_category'][category]['total'] += 1
            report['standards_by_category'][category]['standards'].append(asdict(standard))
            
            if standard.standard_id in covered_standards:
                report['standards_by_category'][category]['covered'] += 1
        
        # Add lesson alignment details
        for alignment in self.lesson_alignments.values():
            report['lesson_alignments'].append(asdict(alignment))
        
        # Find uncovered standards
        for standard in filtered_standards:
            if standard.standard_id not in covered_standards:
                report['uncovered_standards'].append(asdict(standard))
        
        return report
    
    def export_standards_compliance(self, output_path: str, grade_level: str = None) -> bool:
        """Export standards compliance report for administrators"""
        try:
            report = self.generate_standards_report(grade_level)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Standards Alignment Report - Cybersecurity Education</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: #2c5aa0; color: white; padding: 15px; }}
                    .summary {{ background: #f5f5f5; padding: 15px; margin: 10px 0; }}
                    .coverage-good {{ color: green; font-weight: bold; }}
                    .coverage-warning {{ color: orange; font-weight: bold; }}
                    .coverage-poor {{ color: red; font-weight: bold; }}
                    .standards-table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                    .standards-table th, .standards-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    .standards-table th {{ background: #f2f2f2; }}
                    .covered {{ background: #e8f5e8; }}
                    .uncovered {{ background: #ffeaea; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Standards Alignment Report</h1>
                    <h2>Cybersecurity Education Platform</h2>
                    <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f"<p>Grade Level Filter: {grade_level}</p>" if grade_level else ""}
                </div>
                
                <div class="summary">
                    <h3>Coverage Summary</h3>
                    <p><strong>Total Standards:</strong> {report['summary']['total_standards']}</p>
                    <p><strong>Covered Standards:</strong> {report['summary']['covered_standards']}</p>
            """
            
            # Color-code coverage percentage
            coverage = report['summary']['coverage_percentage']
            coverage_class = "coverage-good" if coverage >= 80 else "coverage-warning" if coverage >= 60 else "coverage-poor"
            
            html_content += f"""
                    <p><strong>Coverage Percentage:</strong> <span class="{coverage_class}">{coverage}%</span></p>
                </div>
                
                <h3>Standards by Category</h3>
            """
            
            # Category breakdown
            for category, data in report['standards_by_category'].items():
                category_coverage = (data['covered'] / data['total'] * 100) if data['total'] > 0 else 0
                category_class = "coverage-good" if category_coverage >= 80 else "coverage-warning" if category_coverage >= 60 else "coverage-poor"
                
                html_content += f"""
                <h4>{category}</h4>
                <p>Coverage: <span class="{category_class}">{data['covered']}/{data['total']} ({category_coverage:.1f}%)</span></p>
                
                <table class="standards-table">
                    <tr>
                        <th>Standard ID</th>
                        <th>Organization</th>
                        <th>Grade Level</th>
                        <th>Title</th>
                        <th>Status</th>
                    </tr>
                """
                
                for standard in data['standards']:
                    is_covered = standard['standard_id'] in [
                        std_id for alignment in report['lesson_alignments'] 
                        for std_id in alignment['aligned_standards']
                    ]
                    status_class = "covered" if is_covered else "uncovered"
                    status_text = "✅ Covered" if is_covered else "❌ Not Covered"
                    
                    html_content += f"""
                    <tr class="{status_class}">
                        <td>{standard['standard_id']}</td>
                        <td>{standard['organization']}</td>
                        <td>{standard['grade_level']}</td>
                        <td>{standard['title']}</td>
                        <td>{status_text}</td>
                    </tr>
                    """
                
                html_content += "</table>"
            
            # Lesson alignments
            html_content += """
                <h3>Lesson to Standards Alignments</h3>
                <table class="standards-table">
                    <tr>
                        <th>Lesson</th>
                        <th>Aligned Standards</th>
                        <th>Evidence</th>
                        <th>Assessment Methods</th>
                    </tr>
            """
            
            for alignment in report['lesson_alignments']:
                standards_list = ", ".join(alignment['aligned_standards'])
                assessment_list = ", ".join(alignment['assessment_methods'])
                
                html_content += f"""
                <tr>
                    <td>{alignment['lesson_title']}</td>
                    <td>{standards_list}</td>
                    <td>{alignment['evidence_of_alignment']}</td>
                    <td>{assessment_list}</td>
                </tr>
                """
            
            html_content += """
                </table>
                
                <div class="summary">
                    <h3>Recommendations</h3>
            """
            
            if coverage >= 80:
                html_content += "<p>✅ <strong>Excellent standards coverage!</strong> Your curriculum aligns well with educational standards.</p>"
            elif coverage >= 60:
                html_content += "<p>⚠️ <strong>Good coverage with room for improvement.</strong> Consider adding lessons for uncovered standards.</p>"
            else:
                html_content += "<p>❌ <strong>Standards coverage needs improvement.</strong> Significant gaps exist that should be addressed.</p>"
            
            html_content += """
                    <p>Review the uncovered standards listed in this report and consider developing additional lesson content to improve alignment.</p>
                </div>
            </body>
            </html>
            """
            
            # Write report file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            return True
        except Exception as e:
            print(f"Error exporting compliance report: {e}")
            return False
    
    def load_default_alignments(self):
        """Load default lesson alignments for cybersecurity education platform"""
        
        # Elementary Password Safety Lesson
        self.align_lesson_to_standards(
            "elementary_001", "Password Power and Digital Safety",
            ["1B-NI-04", "1B-NI-05"],
            "Students learn to create strong passwords and understand why passwords protect information. Interactive activities demonstrate safe information sharing online.",
            ["Password creation activity", "Digital citizenship quiz", "Safe sharing scenarios"]
        )
        
        # Middle School Cryptography
        self.align_lesson_to_standards(
            "middle_001", "Cryptography Mystery Lab", 
            ["2-NI-06", "CCSS.MATH.6.EE.A.1"],
            "Students explore encryption methods and mathematical patterns in cryptography. Hands-on activities with Caesar ciphers and basic encryption algorithms.",
            ["Cipher creation project", "Mathematical pattern analysis", "Encryption/decryption challenges"]
        )
        
        # Middle School Network Security
        self.align_lesson_to_standards(
            "middle_002", "Network Security and Protection",
            ["2-NI-04", "2-NI-05"],
            "Students learn about network protocols and security measures. Simulation activities show how data travels across networks and common security threats.",
            ["Network diagram creation", "Security threat identification", "Protocol analysis exercise"]
        )
        
        # High School Ethical Hacking
        self.align_lesson_to_standards(
            "high_001", "Ethical Hacking and Penetration Testing",
            ["3A-NI-05", "3A-NI-06", "3A-NI-07", "CTE.IT.4"],
            "Advanced students learn ethical hacking principles, legal frameworks, and penetration testing methodologies in controlled environments.",
            ["Controlled penetration testing lab", "Legal/ethical framework analysis", "Vulnerability assessment project"]
        )
        
        # High School Career Exploration
        self.align_lesson_to_standards(
            "high_002", "Cybersecurity Career Pathways",
            ["CTE.IT.1", "CTE.IT.2"],
            "Students explore cybersecurity career opportunities, required skills, and certification pathways. Industry professionals provide real-world insights.",
            ["Career research project", "Industry professional interviews", "Certification pathway planning"]
        )
        
        # Systems Thinking
        self.align_lesson_to_standards(
            "high_003", "Computing Systems and Security Architecture", 
            ["3A-CS-01", "3A-CS-02", "3A-CS-03"],
            "Students understand how computing systems work together and identify security considerations at different levels of abstraction.",
            ["System architecture analysis", "Security layer identification", "Troubleshooting methodology development"]
        )

def interactive_standards_alignment():
    """Interactive standards alignment interface"""
    system = StandardsAlignmentSystem()
    system.load_default_alignments()
    
    while True:
        print("\n🎯 STANDARDS ALIGNMENT SYSTEM")
        print("=" * 50)
        print("1. 📚 View Standards by Grade Level")
        print("2. 🔗 Align Lesson to Standards")  
        print("3. 📊 Generate Standards Report")
        print("4. 📤 Export Compliance Report")
        print("5. 🎓 View Lesson Alignments")
        print("6. 📋 Load Default Alignments")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            print("\n📚 Standards by Grade Level")
            print("Available: elementary, middle_school, high_school, K-2, 3-5, 6-8, 9-12")
            grade = input("Grade level: ").strip()
            
            standards = system.get_standards_by_grade(grade)
            
            if standards:
                print(f"\n📖 Standards for {grade}:")
                for std in standards[:10]:  # Show first 10
                    print(f"  {std.standard_id} ({std.organization}): {std.title}")
                if len(standards) > 10:
                    print(f"  ... and {len(standards) - 10} more")
            else:
                print("No standards found for that grade level.")
        
        elif choice == "2":
            print("\n🔗 Align Lesson to Standards")
            lesson_id = input("Lesson ID: ").strip()
            lesson_title = input("Lesson Title: ").strip()
            print("Enter standard IDs separated by commas (e.g., 1B-NI-04, 2-NI-05)")
            standards_input = input("Standards: ").strip()
            standard_ids = [s.strip() for s in standards_input.split(',')]
            evidence = input("Evidence of alignment: ").strip()
            print("Enter assessment methods separated by commas")
            assessment_input = input("Assessment methods: ").strip()
            assessment_methods = [a.strip() for a in assessment_input.split(',')]
            
            if system.align_lesson_to_standards(lesson_id, lesson_title, standard_ids, 
                                              evidence, assessment_methods):
                print("✅ Lesson alignment created successfully!")
            else:
                print("❌ Error creating alignment.")
        
        elif choice == "3":
            print("\n📊 Generate Standards Report")
            grade = input("Grade level (optional): ").strip()
            org = input("Organization filter (CSTA, Common Core Math, CTE) (optional): ").strip()
            
            report = system.generate_standards_report(
                grade if grade else None,
                org if org else None
            )
            
            print(f"\n📈 Standards Report Summary:")
            print(f"Total Standards: {report['summary']['total_standards']}")
            print(f"Covered Standards: {report['summary']['covered_standards']}")
            print(f"Coverage: {report['summary']['coverage_percentage']}%")
            
            print("\nCoverage by Category:")
            for category, data in report['standards_by_category'].items():
                coverage = (data['covered'] / data['total'] * 100) if data['total'] > 0 else 0
                print(f"  {category}: {data['covered']}/{data['total']} ({coverage:.1f}%)")
        
        elif choice == "4":
            print("\n📤 Export Compliance Report")
            filename = input("Output filename (e.g., compliance_report.html): ").strip()
            grade = input("Grade level filter (optional): ").strip()
            
            if system.export_standards_compliance(filename, grade if grade else None):
                print(f"✅ Compliance report exported to {filename}")
            else:
                print("❌ Export failed.")
        
        elif choice == "5":
            print("\n🎓 Current Lesson Alignments:")
            for lesson_id, alignment in system.lesson_alignments.items():
                print(f"\n📚 {alignment.lesson_title} ({lesson_id})")
                print(f"  Standards: {', '.join(alignment.aligned_standards)}")
                print(f"  Evidence: {alignment.evidence_of_alignment}")
        
        elif choice == "6":
            system.load_default_alignments()
            print("✅ Default alignments loaded!")
        
        elif choice == "7":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    interactive_standards_alignment()