#!/usr/bin/env python3
"""
Language Arts - Reading Comprehension Studio
An interactive platform for developing reading skills and comprehension abilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
from datetime import datetime
import os

class ReadingComprehensionStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Reading Comprehension Studio - Language Arts Education")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Data storage
        self.passages = self.load_sample_passages()
        self.student_progress = {}
        self.current_passage = None
        self.current_questions = []
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f8ff')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="📚 Reading Comprehension Studio", 
                              font=('Arial', 24, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Develop critical reading and analysis skills", 
                                 font=('Arial', 12), bg='#f0f8ff', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Navigation
        left_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        nav_label = tk.Label(left_frame, text="Navigation", font=('Arial', 14, 'bold'),
                            bg='#ecf0f1', fg='#2c3e50')
        nav_label.pack(pady=10)
        
        # Navigation buttons
        nav_buttons = [
            ("📖 Read Passage", self.show_reading_area),
            ("❓ Answer Questions", self.show_questions_area),
            ("📊 Progress Tracker", self.show_progress_tracker),
            ("🎯 Reading Strategies", self.show_reading_strategies),
            ("📝 Vocabulary Builder", self.show_vocabulary_builder),
            ("🏆 Achievement Center", self.show_achievements),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(left_frame, text=text, command=command,
                          font=('Arial', 10), width=20, pady=5,
                          bg='#3498db', fg='white', relief='flat')
            btn.pack(pady=2, padx=10)
            
        # Right panel - Main content
        self.content_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Show reading area by default
        self.show_reading_area()
        
    def show_reading_area(self):
        """Show the reading passage area"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="📖 Reading Area", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        # Passage selection
        selection_frame = tk.Frame(self.content_frame, bg='#ffffff')
        selection_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(selection_frame, text="Select Reading Level:", 
                font=('Arial', 12, 'bold'), bg='#ffffff').pack(side='left')
        
        self.level_var = tk.StringVar(value="Elementary")
        level_combo = ttk.Combobox(selection_frame, textvariable=self.level_var,
                                  values=["Elementary", "Middle School", "High School"],
                                  state="readonly")
        level_combo.pack(side='left', padx=10)
        level_combo.bind("<<ComboboxSelected>>", self.load_passage_by_level)
        
        tk.Button(selection_frame, text="Load Random Passage", command=self.load_random_passage,
                 bg='#27ae60', fg='white', font=('Arial', 10)).pack(side='left', padx=10)
        
        tk.Button(selection_frame, text="Load Custom Text", command=self.load_custom_text,
                 bg='#e67e22', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Reading area
        reading_frame = tk.Frame(self.content_frame, bg='#ffffff')
        reading_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Passage info
        self.passage_info_label = tk.Label(reading_frame, text="Select a passage to begin reading",
                                          font=('Arial', 11), bg='#ffffff', fg='#7f8c8d')
        self.passage_info_label.pack(anchor='w')
        
        # Reading text area
        self.reading_text = scrolledtext.ScrolledText(reading_frame, wrap=tk.WORD,
                                                     font=('Georgia', 12), height=20,
                                                     bg='#fefefe', fg='#2c3e50')
        self.reading_text.pack(fill='both', expand=True, pady=10)
        
        # Reading tools
        tools_frame = tk.Frame(reading_frame, bg='#ffffff')
        tools_frame.pack(fill='x', pady=5)
        
        tk.Button(tools_frame, text="🔍 Highlight Text", command=self.highlight_text,
                 bg='#f39c12', fg='white').pack(side='left', padx=5)
        
        tk.Button(tools_frame, text="📝 Add Note", command=self.add_note,
                 bg='#9b59b6', fg='white').pack(side='left', padx=5)
        
        tk.Button(tools_frame, text="🔊 Read Aloud", command=self.read_aloud,
                 bg='#1abc9c', fg='white').pack(side='left', padx=5)
        
        # Load initial passage
        self.load_random_passage()
        
    def show_questions_area(self):
        """Show the comprehension questions area"""
        if not self.current_passage:
            messagebox.showwarning("No Passage", "Please read a passage first!")
            return
            
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="❓ Comprehension Questions", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        # Passage title
        title_frame = tk.Frame(self.content_frame, bg='#ffffff')
        title_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(title_frame, text=f"Passage: {self.current_passage['title']}", 
                font=('Arial', 12, 'bold'), bg='#ffffff', fg='#3498db').pack(anchor='w')
        
        # Questions area
        questions_frame = tk.Frame(self.content_frame, bg='#ffffff')
        questions_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Generate questions if not already done
        if not self.current_questions:
            self.generate_questions()
            
        # Display questions
        self.question_widgets = []
        for i, question in enumerate(self.current_questions):
            q_frame = tk.LabelFrame(questions_frame, text=f"Question {i+1}", 
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
            q_frame.pack(fill='x', pady=10)
            
            # Question text
            tk.Label(q_frame, text=question['question'], font=('Arial', 11),
                    bg='#ffffff', wraplength=600, justify='left').pack(anchor='w', padx=10, pady=5)
            
            # Answer options or text input
            answer_var = tk.StringVar()
            if question['type'] == 'multiple_choice':
                for option in question['options']:
                    tk.Radiobutton(q_frame, text=option, variable=answer_var, value=option,
                                  font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=20)
            else:
                answer_entry = tk.Text(q_frame, height=3, font=('Arial', 10))
                answer_entry.pack(fill='x', padx=10, pady=5)
                answer_var.entry_widget = answer_entry
            
            self.question_widgets.append({
                'question': question,
                'answer_var': answer_var,
                'frame': q_frame
            })
        
        # Submit button
        submit_frame = tk.Frame(self.content_frame, bg='#ffffff')
        submit_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(submit_frame, text="📝 Submit Answers", command=self.submit_answers,
                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white', 
                 pady=10).pack(side='right')
        
    def show_progress_tracker(self):
        """Show student progress tracking"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="📊 Progress Tracker", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Progress stats
        stats_frame = tk.LabelFrame(self.content_frame, text="Reading Statistics", 
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Calculate stats
        total_read = len(self.student_progress)
        avg_score = sum([p['score'] for p in self.student_progress.values()]) / max(1, total_read)
        
        stats_text = f"""
        📚 Passages Read: {total_read}
        📊 Average Score: {avg_score:.1f}%
        🎯 Reading Level: {self.level_var.get()}
        ⭐ Best Score: {max([p['score'] for p in self.student_progress.values()], default=0):.1f}%
        """
        
        tk.Label(stats_frame, text=stats_text, font=('Arial', 11),
                bg='#ffffff', justify='left').pack(padx=20, pady=10)
        
        # Recent activity
        activity_frame = tk.LabelFrame(self.content_frame, text="Recent Activity", 
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
        activity_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Activity list
        activity_tree = ttk.Treeview(activity_frame, columns=('Date', 'Passage', 'Score'), 
                                    show='headings')
        activity_tree.heading('Date', text='Date')
        activity_tree.heading('Passage', text='Passage')
        activity_tree.heading('Score', text='Score')
        
        # Populate with recent activity
        for passage_id, progress in self.student_progress.items():
            activity_tree.insert('', 'end', values=(
                progress.get('date', 'Unknown'),
                progress.get('title', passage_id),
                f"{progress['score']:.1f}%"
            ))
        
        activity_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
    def show_reading_strategies(self):
        """Show reading strategies and tips"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🎯 Reading Strategies", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Strategies content
        strategies_text = """
📖 EFFECTIVE READING STRATEGIES

🔍 BEFORE READING:
• Preview the title, headings, and images
• Predict what the text might be about
• Set a purpose for reading
• Activate prior knowledge

👁️ WHILE READING:
• Ask questions about the text
• Make connections to your life and other texts
• Visualize what you're reading
• Monitor your understanding
• Take notes or highlight important information

🤔 AFTER READING:
• Summarize the main ideas
• Reflect on what you learned
• Ask questions about unclear parts
• Connect new information to what you already know

💡 COMPREHENSION TECHNIQUES:
• SQ3R Method (Survey, Question, Read, Recite, Review)
• KWL Chart (Know, Want to know, Learned)
• Main idea and supporting details identification
• Context clues for vocabulary
• Making inferences and drawing conclusions

📝 CRITICAL THINKING QUESTIONS:
• What is the author's purpose?
• What evidence supports the main idea?
• How reliable is this information?
• What questions do you still have?
• How does this connect to other knowledge?

🎯 ACTIVE READING TIPS:
• Read at an appropriate pace
• Re-read difficult sections
• Use graphic organizers
• Discuss with others
• Apply reading strategies flexibly
        """
        
        strategies_display = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD,
                                                      font=('Arial', 11), bg='#fefefe')
        strategies_display.pack(fill='both', expand=True, padx=20, pady=10)
        strategies_display.insert('1.0', strategies_text)
        strategies_display.configure(state='disabled')
        
    def show_vocabulary_builder(self):
        """Show vocabulary building tools"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="📝 Vocabulary Builder", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Vocabulary tools
        tools_frame = tk.Frame(self.content_frame, bg='#ffffff')
        tools_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(tools_frame, text="📚 Word Bank", command=self.show_word_bank,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(tools_frame, text="🔍 Context Clues", command=self.practice_context_clues,
                 bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(tools_frame, text="🎮 Word Games", command=self.show_word_games,
                 bg='#f39c12', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Current passage vocabulary
        if self.current_passage:
            vocab_frame = tk.LabelFrame(self.content_frame, text="Vocabulary from Current Passage",
                                       font=('Arial', 12, 'bold'), bg='#ffffff')
            vocab_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Extract vocabulary words (simplified)
            vocab_words = self.extract_vocabulary_words()
            
            vocab_text = scrolledtext.ScrolledText(vocab_frame, height=15, font=('Arial', 11))
            vocab_text.pack(fill='both', expand=True, padx=10, pady=10)
            
            for word, definition in vocab_words.items():
                vocab_text.insert(tk.END, f"📝 {word.upper()}\n")
                vocab_text.insert(tk.END, f"   Definition: {definition}\n")
                vocab_text.insert(tk.END, f"   Example: Use this word in a sentence.\n\n")
            
            vocab_text.configure(state='disabled')
        
    def show_achievements(self):
        """Show achievement system"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🏆 Achievement Center", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Achievements grid
        achievements = [
            ("📚 First Reader", "Complete your first passage", True),
            ("🔥 Reading Streak", "Read for 5 days in a row", False),
            ("🎯 Perfect Score", "Get 100% on comprehension questions", False),
            ("📖 Bookworm", "Read 10 different passages", False),
            ("🧠 Critical Thinker", "Answer 50 questions correctly", False),
            ("⭐ Rising Star", "Improve reading level", False),
            ("🏅 Vocabulary Master", "Learn 100 new words", False),
            ("🎪 Story Explorer", "Read passages from all genres", False)
        ]
        
        achievements_frame = tk.Frame(self.content_frame, bg='#ffffff')
        achievements_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        for i, (title, description, earned) in enumerate(achievements):
            row = i // 2
            col = i % 2
            
            achievement_frame = tk.LabelFrame(achievements_frame, text=title,
                                            font=('Arial', 11, 'bold'), bg='#ffffff')
            achievement_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            color = '#27ae60' if earned else '#bdc3c7'
            status = "✅ EARNED" if earned else "🔒 LOCKED"
            
            tk.Label(achievement_frame, text=description, font=('Arial', 10),
                    bg='#ffffff', wraplength=200).pack(padx=10, pady=5)
            
            tk.Label(achievement_frame, text=status, font=('Arial', 10, 'bold'),
                    bg='#ffffff', fg=color).pack(padx=10, pady=5)
        
        achievements_frame.grid_columnconfigure(0, weight=1)
        achievements_frame.grid_columnconfigure(1, weight=1)
        
    def show_settings(self):
        """Show application settings"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="⚙️ Settings", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Settings options
        settings_frame = tk.LabelFrame(self.content_frame, text="Reading Preferences",
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        # Font size
        font_frame = tk.Frame(settings_frame, bg='#ffffff')
        font_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(font_frame, text="Reading Font Size:", font=('Arial', 11),
                bg='#ffffff').pack(side='left')
        
        font_var = tk.StringVar(value="Medium")
        font_combo = ttk.Combobox(font_frame, textvariable=font_var,
                                 values=["Small", "Medium", "Large", "Extra Large"],
                                 state="readonly")
        font_combo.pack(side='right')
        
        # Reading speed
        speed_frame = tk.Frame(settings_frame, bg='#ffffff')
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(speed_frame, text="Reading Speed Goal:", font=('Arial', 11),
                bg='#ffffff').pack(side='left')
        
        speed_var = tk.StringVar(value="Normal")
        speed_combo = ttk.Combobox(speed_frame, textvariable=speed_var,
                                  values=["Slow", "Normal", "Fast"],
                                  state="readonly")
        speed_combo.pack(side='right')
        
        # Save button
        tk.Button(settings_frame, text="💾 Save Settings", 
                 bg='#27ae60', fg='white', font=('Arial', 11)).pack(pady=10)
        
    def clear_content_frame(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def load_sample_passages(self):
        """Load sample reading passages"""
        return {
            "elementary_1": {
                "title": "The Friendly Dragon",
                "level": "Elementary",
                "genre": "Fantasy",
                "text": """Once upon a time, in a land far away, there lived a friendly dragon named Spark. Unlike other dragons who were fierce and scary, Spark was kind and gentle. He had bright green scales that sparkled in the sunlight and warm brown eyes that twinkled when he smiled.

Spark lived in a cozy cave at the top of a mountain, but he often came down to visit the village below. The children in the village loved Spark because he would tell them wonderful stories and sometimes give them rides on his back through the clouds.

One day, the village was in trouble. A terrible storm had knocked down the bridge that connected the village to the outside world. The villagers needed supplies, but they couldn't cross the deep river without the bridge.

Spark knew he had to help. He flew back and forth across the river, carrying supplies and people safely to the other side. Thanks to Spark's kindness and bravery, the village was saved. From that day on, everyone knew that not all dragons were scary – some were the best friends you could ever have.""",
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "What color were Spark's scales?",
                        "options": ["Blue", "Green", "Red", "Gold"],
                        "correct": "Green"
                    },
                    {
                        "type": "multiple_choice", 
                        "question": "Where did Spark live?",
                        "options": ["In the village", "In a cave", "By the river", "In the forest"],
                        "correct": "In a cave"
                    }
                ]
            },
            "middle_1": {
                "title": "The Science of Weather Prediction",
                "level": "Middle School",
                "genre": "Science",
                "text": """Weather prediction has come a long way from ancient methods of reading natural signs. Today, meteorologists use sophisticated technology and scientific principles to forecast weather patterns with remarkable accuracy.

The process begins with data collection. Weather stations around the world continuously monitor temperature, humidity, air pressure, wind speed, and precipitation. Satellites orbiting Earth provide images of cloud formations and storm systems, while weather balloons carry instruments high into the atmosphere to measure conditions at different altitudes.

All this information is fed into powerful computer models that simulate the atmosphere's behavior. These models use complex mathematical equations based on the laws of physics to predict how weather systems will develop and move. The more data available, the more accurate the predictions become.

However, weather prediction isn't perfect. The atmosphere is a chaotic system, meaning small changes can have large effects. This is why weather forecasts become less reliable the further into the future they extend. While today's forecast might be 95% accurate, a five-day forecast is only about 75% accurate.

Despite these limitations, modern weather prediction saves lives by providing early warnings for dangerous storms, helps farmers plan their crops, and allows people to make informed decisions about their daily activities.""",
                "questions": [
                    {
                        "type": "multiple_choice",
                        "question": "What is the main purpose of weather satellites?",
                        "options": ["Measure ground temperature", "Provide images of cloud formations", "Control weather patterns", "Send weather balloons"],
                        "correct": "Provide images of cloud formations"
                    },
                    {
                        "type": "open_ended",
                        "question": "Explain why weather forecasts become less accurate the further into the future they predict."
                    }
                ]
            }
        }
        
    def load_passage_by_level(self, event=None):
        """Load a passage based on selected level"""
        level = self.level_var.get()
        available_passages = [p for p in self.passages.values() if p['level'] == level]
        if available_passages:
            self.current_passage = random.choice(available_passages)
            self.display_passage()
            
    def load_random_passage(self):
        """Load a random passage"""
        self.current_passage = random.choice(list(self.passages.values()))
        self.display_passage()
        
    def load_custom_text(self):
        """Load custom text from file"""
        filename = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.current_passage = {
                        "title": os.path.basename(filename),
                        "level": "Custom",
                        "genre": "Custom",
                        "text": content
                    }
                    self.display_passage()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
                
    def display_passage(self):
        """Display the current passage"""
        if self.current_passage and hasattr(self, 'reading_text'):
            # Update passage info
            info_text = f"Title: {self.current_passage['title']} | Level: {self.current_passage['level']} | Genre: {self.current_passage['genre']}"
            self.passage_info_label.configure(text=info_text)
            
            # Display text
            self.reading_text.delete('1.0', tk.END)
            self.reading_text.insert('1.0', self.current_passage['text'])
            
            # Reset questions
            self.current_questions = []
            
    def generate_questions(self):
        """Generate comprehension questions for current passage"""
        if self.current_passage and 'questions' in self.current_passage:
            self.current_questions = self.current_passage['questions']
        else:
            # Generate basic questions
            self.current_questions = [
                {
                    "type": "open_ended",
                    "question": "What is the main idea of this passage?"
                },
                {
                    "type": "open_ended", 
                    "question": "What are three important details from the text?"
                },
                {
                    "type": "open_ended",
                    "question": "What questions do you still have after reading?"
                }
            ]
            
    def submit_answers(self):
        """Submit and evaluate answers"""
        if not self.question_widgets:
            return
            
        score = 0
        total = len(self.question_widgets)
        
        for widget in self.question_widgets:
            question = widget['question']
            answer_var = widget['answer_var']
            
            if question['type'] == 'multiple_choice' and 'correct' in question:
                if answer_var.get() == question['correct']:
                    score += 1
            else:
                # For open-ended questions, give credit for any answer
                if hasattr(answer_var, 'entry_widget'):
                    answer_text = answer_var.entry_widget.get('1.0', tk.END).strip()
                    if answer_text:
                        score += 1
                        
        percentage = (score / total) * 100
        
        # Save progress
        passage_id = f"{self.current_passage['title']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.student_progress[passage_id] = {
            'title': self.current_passage['title'],
            'score': percentage,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'level': self.current_passage['level']
        }
        
        # Show results
        messagebox.showinfo("Results", f"Score: {score}/{total} ({percentage:.1f}%)\n\nGreat job reading!")
        
    def highlight_text(self):
        """Highlight selected text"""
        try:
            selection = self.reading_text.selection_get()
            start = self.reading_text.index(tk.SEL_FIRST)
            end = self.reading_text.index(tk.SEL_LAST)
            self.reading_text.tag_add("highlight", start, end)
            self.reading_text.tag_config("highlight", background="yellow")
        except tk.TclError:
            messagebox.showinfo("Highlight", "Please select text to highlight")
            
    def add_note(self):
        """Add a note about selected text"""
        try:
            selection = self.reading_text.selection_get()
            note = tk.simpledialog.askstring("Add Note", f"Add a note about: '{selection[:50]}...'")
            if note:
                messagebox.showinfo("Note Added", f"Note saved: {note}")
        except tk.TclError:
            messagebox.showinfo("Note", "Please select text to add a note")
            
    def read_aloud(self):
        """Simulate read-aloud feature"""
        messagebox.showinfo("Read Aloud", "Text-to-speech would read the passage aloud.\n(Feature simulated)")
        
    def extract_vocabulary_words(self):
        """Extract vocabulary words from current passage"""
        # Simplified vocabulary extraction
        sample_words = {
            "magnificent": "extremely beautiful or impressive",
            "perseverance": "continuing to try despite difficulties", 
            "hypothesis": "an educated guess that can be tested",
            "demonstrate": "to show clearly by example",
            "analyze": "to examine something carefully"
        }
        return sample_words
        
    def show_word_bank(self):
        """Show vocabulary word bank"""
        messagebox.showinfo("Word Bank", "Interactive vocabulary word bank would be displayed here.")
        
    def practice_context_clues(self):
        """Practice using context clues"""
        messagebox.showinfo("Context Clues", "Interactive context clues practice would start here.")
        
    def show_word_games(self):
        """Show vocabulary games"""
        messagebox.showinfo("Word Games", "Fun vocabulary games would be available here.")

def main():
    root = tk.Tk()
    app = ReadingComprehensionStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()