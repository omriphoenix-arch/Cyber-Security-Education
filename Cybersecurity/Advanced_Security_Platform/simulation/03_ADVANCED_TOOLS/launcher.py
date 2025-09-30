#!/usr/bin/env python3
"""
🏫 School Cybersecurity Education Platform - Easy Launcher
==========================================================

A simple, user-friendly launcher for all cybersecurity education tools.
Designed for K-12 school environments with appropriate safeguards and guidance.

Created for educational purposes to teach cybersecurity concepts safely and ethically.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime

class CybersecurityEducationLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏫 Cybersecurity Education Platform")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Get current directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create main interface
        self.create_widgets()
        
        # Track usage for educational analytics
        self.usage_log = []
        
    def create_widgets(self):
        """Create the main launcher interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🏫 School Cybersecurity Education Platform",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Teaching Cybersecurity Through Safe, Ethical, and Hands-On Learning",
            font=('Arial', 10),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Tool selection
        left_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tools_label = tk.Label(
            left_frame,
            text="📚 Educational Tools",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        tools_label.pack(pady=10)
        
        # Tool buttons frame
        tools_frame = tk.Frame(left_frame, bg='white')
        tools_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Define available tools
        self.tools = [
            {
                'name': '🎓 Education Hub',
                'description': 'Student registration, progress tracking, and lesson management',
                'file': 'education_hub.py',
                'grade_level': 'All Grades (K-12)',
                'duration': '15-30 minutes setup, ongoing use',
                'safety': 'Safe - No security demonstrations, pure educational management'
            },
            {
                'name': '📝 Assessment Tools',
                'description': 'Quizzes, challenges, and performance tracking',
                'file': 'assessment_tools.py',
                'grade_level': 'All Grades (Age-appropriate content)',
                'duration': '10-45 minutes per assessment',
                'safety': 'Safe - Educational quizzes and interactive challenges only'
            },
            {
                'name': '🏦 Banking Simulation (Defensive)',
                'description': 'Experience secure banking from user perspective',
                'file': 'secure_bank_database.py',
                'grade_level': 'Middle & High School (Grades 6-12)',
                'duration': '30-60 minutes',
                'safety': 'Safe - User experience only, no attack demonstrations'
            },
            {
                'name': '🛡️ Ethical Hacker Simulation',
                'description': 'Learn attack methodologies in controlled environment',
                'file': 'hacker_simulation.py',
                'grade_level': 'High School Only (Grades 9-12)',
                'duration': '45-90 minutes',
                'safety': 'Supervised - Requires teacher oversight and ethical guidelines'
            },
            {
                'name': '⚠️ Timing Attack Demo',
                'description': 'Advanced vulnerability demonstration',
                'file': '../timing_attack_demo/timing_attack_demo.py',
                'grade_level': 'High School Advanced (Grades 11-12)',
                'duration': '60+ minutes',
                'safety': 'Teacher Only - Advanced demonstration requiring expert guidance'
            },
            {
                'name': '🔧 Network Tools Demo',
                'description': 'Network discovery and analysis tools',
                'file': '../network_tools/network_discovery.py',
                'grade_level': 'High School Advanced (Grades 10-12)',
                'duration': '30-45 minutes',
                'safety': 'Controlled Environment - Requires isolated network setup'
            }
        ]
        
        # Create tool selection
        self.tool_var = tk.StringVar()
        self.selected_tool = None
        
        for i, tool in enumerate(self.tools):
            tool_frame = tk.Frame(tools_frame, bg='#ecf0f1', relief='raised', bd=1)
            tool_frame.pack(fill='x', pady=5)
            
            # Radio button for selection
            radio = tk.Radiobutton(
                tool_frame,
                text=tool['name'],
                variable=self.tool_var,
                value=str(i),
                font=('Arial', 10, 'bold'),
                bg='#ecf0f1',
                command=lambda idx=i: self.select_tool(idx)
            )
            radio.pack(anchor='w', padx=10, pady=5)
            
            # Description
            desc_label = tk.Label(
                tool_frame,
                text=tool['description'],
                font=('Arial', 9),
                bg='#ecf0f1',
                fg='#34495e',
                wraplength=300
            )
            desc_label.pack(anchor='w', padx=30, pady=(0, 5))
        
        # Right panel - Tool details and controls
        right_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        details_label = tk.Label(
            right_frame,
            text="🔍 Tool Details",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        details_label.pack(pady=10)
        
        # Details display
        self.details_frame = tk.Frame(right_frame, bg='white')
        self.details_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Default message
        self.show_default_message()
        
        # Bottom control panel
        control_frame = tk.Frame(self.root, bg='#34495e', height=80)
        control_frame.pack(fill='x', padx=10, pady=10)
        control_frame.pack_propagate(False)
        
        # Launch button
        self.launch_btn = tk.Button(
            control_frame,
            text="🚀 Launch Selected Tool",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.launch_tool,
            state='disabled',
            height=2
        )
        self.launch_btn.pack(side='left', padx=20, pady=15)
        
        # Teacher guide button
        guide_btn = tk.Button(
            control_frame,
            text="📖 Teacher Guide",
            font=('Arial', 10),
            bg='#3498db',
            fg='white',
            command=self.open_teacher_guide,
            height=2
        )
        guide_btn.pack(side='left', padx=10, pady=15)
        
        # Safety guidelines button
        safety_btn = tk.Button(
            control_frame,
            text="🔒 Safety Guidelines",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            command=self.show_safety_guidelines,
            height=2
        )
        safety_btn.pack(side='left', padx=10, pady=15)
        
        # Exit button
        exit_btn = tk.Button(
            control_frame,
            text="❌ Exit",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            command=self.root.quit,
            height=2
        )
        exit_btn.pack(side='right', padx=20, pady=15)
        
    def show_default_message(self):
        """Show default welcome message"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
            
        welcome_text = """
🎯 Welcome to the Cybersecurity Education Platform!

This platform provides comprehensive, age-appropriate cybersecurity education tools designed specifically for K-12 school environments.

👈 Select a tool from the left panel to view details and launch

🔑 Key Features:
• Age-appropriate content for all grade levels
• Hands-on interactive learning experiences
• Comprehensive teacher resources and guides
• Built-in safety measures and ethical guidelines
• Progress tracking and assessment tools

🛡️ Safety First:
All simulations are designed for educational purposes only and include appropriate safeguards for school use.

📚 Getting Started:
1. Review the Teacher Guide for curriculum integration
2. Select appropriate tools for your grade level
3. Follow safety guidelines for supervised activities
4. Track student progress through assessment tools

For technical support or questions, please refer to the documentation in the project folder.
        """
        
        text_widget = scrolledtext.ScrolledText(
            self.details_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='#f8f9fa',
            relief='sunken',
            bd=1
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', welcome_text)
        text_widget.config(state='disabled')
        
    def select_tool(self, index):
        """Handle tool selection"""
        self.selected_tool = self.tools[index]
        self.show_tool_details()
        self.launch_btn.config(state='normal')
        
    def show_tool_details(self):
        """Display details for selected tool"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
            
        if not self.selected_tool:
            return
            
        # Tool name
        name_label = tk.Label(
            self.details_frame,
            text=self.selected_tool['name'],
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        name_label.pack(anchor='w', pady=(0, 10))
        
        # Details frame
        details_text = f"""
📋 Description:
{self.selected_tool['description']}

🎓 Recommended Grade Level:
{self.selected_tool['grade_level']}

⏱️ Estimated Duration:
{self.selected_tool['duration']}

🔒 Safety Classification:
{self.selected_tool['safety']}

📁 File Location:
{self.selected_tool['file']}
        """
        
        text_widget = scrolledtext.ScrolledText(
            self.details_frame,
            wrap=tk.WORD,
            height=15,
            font=('Arial', 10),
            bg='#f8f9fa',
            relief='sunken',
            bd=1
        )
        text_widget.pack(fill='both', expand=True, pady=10)
        text_widget.insert('1.0', details_text.strip())
        text_widget.config(state='disabled')
        
        # Safety warning for advanced tools
        if 'Teacher Only' in self.selected_tool['safety'] or 'Supervised' in self.selected_tool['safety']:
            warning_frame = tk.Frame(self.details_frame, bg='#fff3cd', relief='raised', bd=2)
            warning_frame.pack(fill='x', pady=10)
            
            warning_label = tk.Label(
                warning_frame,
                text="⚠️ IMPORTANT: This tool requires teacher supervision and appropriate safeguards!",
                font=('Arial', 10, 'bold'),
                bg='#fff3cd',
                fg='#856404',
                wraplength=400
            )
            warning_label.pack(padx=10, pady=10)
            
    def launch_tool(self):
        """Launch the selected tool"""
        if not self.selected_tool:
            messagebox.showerror("Error", "Please select a tool first!")
            return
            
        # Log usage
        self.log_usage(self.selected_tool['name'])
        
        # Safety confirmation for supervised tools
        if 'Teacher Only' in self.selected_tool['safety']:
            result = messagebox.askyesno(
                "Teacher Verification Required",
                "This tool requires expert teacher supervision and should only be used by qualified instructors.\n\n"
                "Have you reviewed the safety guidelines and are you qualified to supervise this activity?\n\n"
                "Click 'Yes' only if you are a qualified teacher with appropriate cybersecurity knowledge."
            )
            if not result:
                return
                
        elif 'Supervised' in self.selected_tool['safety']:
            result = messagebox.askyesno(
                "Supervision Required",
                "This tool requires teacher supervision and ethical guidelines discussion.\n\n"
                "Have you prepared appropriate ethical guidelines and will you supervise student activity?\n\n"
                "Click 'Yes' only if you will provide appropriate supervision."
            )
            if not result:
                return
                
        elif 'Controlled Environment' in self.selected_tool['safety']:
            result = messagebox.askyesno(
                "Network Isolation Required",
                "This tool should only be used in an isolated, controlled network environment.\n\n"
                "Have you ensured this system is isolated from production networks and the internet?\n\n"
                "Click 'Yes' only if appropriate network isolation is in place."
            )
            if not result:
                return
        
        # Construct file path
        file_path = os.path.join(self.base_dir, self.selected_tool['file'])
        
        # Check if file exists
        if not os.path.exists(file_path):
            messagebox.showerror(
                "File Not Found",
                f"Could not find the file: {file_path}\n\n"
                "Please ensure all educational tools are properly installed."
            )
            return
            
        # Launch the tool
        try:
            if sys.platform.startswith('win'):
                subprocess.Popen(['python', file_path], shell=True)
            else:
                subprocess.Popen(['python3', file_path])
                
            messagebox.showinfo(
                "Tool Launched",
                f"Successfully launched: {self.selected_tool['name']}\n\n"
                "The tool will open in a separate window.\n"
                "Please refer to the Teacher Guide for usage instructions."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch tool: {str(e)}\n\n"
                "Please check that Python is properly installed and the file exists."
            )
            
    def log_usage(self, tool_name):
        """Log tool usage for educational analytics"""
        usage_entry = {
            'tool': tool_name,
            'timestamp': datetime.now().isoformat(),
            'user': os.getenv('USERNAME', 'unknown')
        }
        self.usage_log.append(usage_entry)
        
        # Save to file (optional for analytics)
        try:
            log_file = os.path.join(self.base_dir, 'usage_log.json')
            with open(log_file, 'a') as f:
                json.dump(usage_entry, f)
                f.write('\n')
        except:
            pass  # Don't fail if logging doesn't work
            
    def open_teacher_guide(self):
        """Open the teacher guide"""
        guide_path = os.path.join(self.base_dir, 'TEACHER_GUIDE.md')
        
        if os.path.exists(guide_path):
            try:
                if sys.platform.startswith('win'):
                    os.startfile(guide_path)
                elif sys.platform.startswith('darwin'):
                    subprocess.Popen(['open', guide_path])
                else:
                    subprocess.Popen(['xdg-open', guide_path])
            except:
                messagebox.showinfo(
                    "Teacher Guide",
                    f"Please open the teacher guide manually at:\n{guide_path}"
                )
        else:
            messagebox.showerror(
                "Guide Not Found",
                "Teacher guide not found. Please ensure TEACHER_GUIDE.md is in the simulation folder."
            )
            
    def show_safety_guidelines(self):
        """Display safety guidelines window"""
        safety_window = tk.Toplevel(self.root)
        safety_window.title("🔒 Safety Guidelines")
        safety_window.geometry("600x500")
        safety_window.configure(bg='white')
        
        # Header
        header_label = tk.Label(
            safety_window,
            text="🔒 Cybersecurity Education Safety Guidelines",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#e74c3c'
        )
        header_label.pack(pady=20)
        
        # Safety text
        safety_text = """
🎯 FUNDAMENTAL PRINCIPLES

1. EDUCATIONAL PURPOSE ONLY
   All tools are designed exclusively for educational use in controlled school environments.

2. ETHICAL BOUNDARIES
   Students must understand the difference between ethical learning and malicious activity.

3. SUPERVISED LEARNING
   Advanced tools require qualified teacher supervision at all times.

4. CONTROLLED ENVIRONMENT
   Network tools should only be used in isolated, controlled environments.

🚫 PROHIBITED ACTIVITIES

• Never attempt to hack real systems or networks
• Never use school tools against actual websites or servers
• Never attempt to access unauthorized information
• Never share attack techniques outside educational context
• Never use knowledge to harm others or violate privacy

✅ REQUIRED SAFEGUARDS

• Obtain proper authorization before running any security demonstration
• Ensure isolated network environment for network tools
• Discuss ethical implications before and after each lesson
• Monitor student activities during hands-on exercises
• Maintain clear consequences for policy violations

🎓 TEACHER RESPONSIBILITIES

• Review all tools before student use
• Understand technical implications of each demonstration
• Prepare appropriate ethical guidelines discussion
• Monitor student behavior during and after lessons
• Report any misuse immediately

👨‍🎓 STUDENT RESPONSIBILITIES

• Follow all school technology policies
• Use cybersecurity knowledge constructively
• Report security vulnerabilities to appropriate authorities
• Respect privacy and confidentiality of all information
• Ask questions when ethical boundaries are unclear

📞 SUPPORT AND REPORTING

If you encounter any issues or have questions about appropriate use:
• Consult your school's technology coordinator
• Review the complete Teacher Guide
• Contact educational technology support
• Report any security concerns immediately

Remember: The goal is to create informed digital citizens who understand
both cybersecurity principles and their ethical responsibilities!
        """
        
        text_widget = scrolledtext.ScrolledText(
            safety_window,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='#f8f9fa'
        )
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget.insert('1.0', safety_text.strip())
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            safety_window,
            text="Close",
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            command=safety_window.destroy
        )
        close_btn.pack(pady=10)
        
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🏫 Starting Cybersecurity Education Platform Launcher...")
    print("Designed for K-12 school environments with appropriate safeguards.")
    print("Please review safety guidelines before using advanced tools.")
    print("-" * 60)
    
    launcher = CybersecurityEducationLauncher()
    launcher.run()

if __name__ == "__main__":
    main()