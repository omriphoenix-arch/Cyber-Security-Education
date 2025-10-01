#!/usr/bin/env python3
"""
Language Arts - Grammar and Vocabulary Master
An interactive platform for mastering grammar rules and building vocabulary
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import random
from datetime import datetime
import re

class GrammarVocabularyMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Grammar & Vocabulary Master - Language Arts Education")
        self.root.geometry("1300x800")
        self.root.configure(bg='#f5f6fa')
        
        # Data storage
        self.grammar_lessons = self.load_grammar_lessons()
        self.vocabulary_words = self.load_vocabulary_database()
        self.student_progress = {}
        self.current_lesson = None
        self.quiz_scores = []
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f5f6fa')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="📝 Grammar & Vocabulary Master", 
                              font=('Arial', 24, 'bold'), bg='#f5f6fa', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Master the building blocks of great communication", 
                                 font=('Arial', 12), bg='#f5f6fa', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f5f6fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Navigation
        left_frame = tk.Frame(main_frame, bg='#ddd6fe', relief='raised', bd=2, width=280)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        nav_label = tk.Label(left_frame, text="Learning Center", font=('Arial', 14, 'bold'),
                            bg='#ddd6fe', fg='#2c3e50')
        nav_label.pack(pady=15)
        
        # Navigation sections
        grammar_frame = tk.LabelFrame(left_frame, text="📚 Grammar", 
                                     font=('Arial', 12, 'bold'), bg='#ddd6fe')
        grammar_frame.pack(fill='x', padx=10, pady=5)
        
        grammar_buttons = [
            ("📖 Grammar Lessons", self.show_grammar_lessons),
            ("✏️ Grammar Practice", self.show_grammar_practice),
            ("🎯 Grammar Quiz", self.start_grammar_quiz)
        ]
        
        for text, command in grammar_buttons:
            btn = tk.Button(grammar_frame, text=text, command=command,
                          font=('Arial', 10), width=24, pady=3,
                          bg='#7c3aed', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        vocab_frame = tk.LabelFrame(left_frame, text="📝 Vocabulary", 
                                   font=('Arial', 12, 'bold'), bg='#ddd6fe')
        vocab_frame.pack(fill='x', padx=10, pady=5)
        
        vocab_buttons = [
            ("📚 Word Study", self.show_vocabulary_study),
            ("🎮 Vocabulary Games", self.show_vocabulary_games),
            ("🏆 Vocabulary Challenge", self.start_vocab_challenge)
        ]
        
        for text, command in vocab_buttons:
            btn = tk.Button(vocab_frame, text=text, command=command,
                          font=('Arial', 10), width=24, pady=3,
                          bg='#059669', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        tools_frame = tk.LabelFrame(left_frame, text="🔧 Tools", 
                                   font=('Arial', 12, 'bold'), bg='#ddd6fe')
        tools_frame.pack(fill='x', padx=10, pady=5)
        
        tool_buttons = [
            ("📊 Progress Tracker", self.show_progress_tracker),
            ("🎯 Skill Assessment", self.show_skill_assessment),
            ("📋 Study Planner", self.show_study_planner),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in tool_buttons:
            btn = tk.Button(tools_frame, text=text, command=command,
                          font=('Arial', 10), width=24, pady=3,
                          bg='#dc2626', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Progress summary
        progress_frame = tk.LabelFrame(left_frame, text="📈 Today's Progress", 
                                      font=('Arial', 11, 'bold'), bg='#ddd6fe')
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_label = tk.Label(progress_frame, 
                                      text="Lessons: 0\nQuizzes: 0\nWords Learned: 0",
                                      font=('Arial', 10), bg='#ddd6fe', fg='#374151')
        self.progress_label.pack(pady=10)
        
        # Right panel - Main content
        self.content_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Show welcome screen by default
        self.show_welcome_screen()
        
    def show_welcome_screen(self):
        """Show the welcome dashboard"""
        self.clear_content_frame()
        
        welcome_frame = tk.Frame(self.content_frame, bg='#ffffff')
        welcome_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Welcome header
        tk.Label(welcome_frame, text="Welcome to Grammar & Vocabulary Master!", 
                font=('Arial', 20, 'bold'), bg='#ffffff', fg='#2c3e50').pack(pady=20)
        
        tk.Label(welcome_frame, text="Choose your learning path and start improving your language skills!", 
                font=('Arial', 12), bg='#ffffff', fg='#7f8c8d').pack(pady=5)
        
        # Quick start grid
        quick_frame = tk.LabelFrame(welcome_frame, text="Quick Start", 
                                   font=('Arial', 14, 'bold'), bg='#ffffff')
        quick_frame.pack(fill='x', pady=30)
        
        quick_options = [
            ("📚 Start Grammar Lesson", "Learn essential grammar rules", self.show_grammar_lessons, '#7c3aed'),
            ("📝 Build Vocabulary", "Expand your word knowledge", self.show_vocabulary_study, '#059669'),
            ("🎯 Take a Quiz", "Test your current skills", self.quick_assessment, '#dc2626'),
            ("🎮 Play Word Games", "Learn while having fun", self.show_vocabulary_games, '#f59e0b')
        ]
        
        for i, (title, desc, command, color) in enumerate(quick_options):
            row = i // 2
            col = i % 2
            
            option_frame = tk.Frame(quick_frame, bg='#ffffff', relief='raised', bd=1)
            option_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            tk.Label(option_frame, text=title, font=('Arial', 12, 'bold'),
                    bg='#ffffff', fg=color).pack(pady=10)
            
            tk.Label(option_frame, text=desc, font=('Arial', 10),
                    bg='#ffffff', fg='#7f8c8d', wraplength=200).pack(pady=5)
            
            tk.Button(option_frame, text="Start", command=command,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     relief='flat', pady=5).pack(pady=10)
        
        for i in range(2):
            quick_frame.grid_columnconfigure(i, weight=1)
        
        # Daily tip
        tip_frame = tk.LabelFrame(welcome_frame, text="💡 Grammar Tip of the Day", 
                                 font=('Arial', 12, 'bold'), bg='#ffffff')
        tip_frame.pack(fill='x', pady=20)
        
        daily_tips = [
            "Remember: 'A lot' is two words, not 'alot'!",
            "Use 'who' for people and 'that' for things.",
            "Its = possessive, It's = it is or it has",
            "Effect is a noun, Affect is a verb (usually)",
            "Use commas to separate items in a series of three or more."
        ]
        
        tip_text = random.choice(daily_tips)
        tk.Label(tip_frame, text=tip_text, font=('Arial', 11),
                bg='#ffffff', fg='#374151').pack(padx=20, pady=15)
        
    def show_grammar_lessons(self):
        """Show grammar lessons interface"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="📚 Grammar Lessons", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Button(header_frame, text="🎲 Random Lesson", command=self.random_grammar_lesson,
                 bg='#7c3aed', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Lesson categories
        categories_frame = tk.Frame(self.content_frame, bg='#ffffff')
        categories_frame.pack(fill='x', padx=20, pady=10)
        
        categories = list(set([lesson['category'] for lesson in self.grammar_lessons]))
        
        self.grammar_category_var = tk.StringVar(value="All")
        tk.Label(categories_frame, text="Category:", font=('Arial', 12, 'bold'),
                bg='#ffffff').pack(side='left', padx=(0, 10))
        
        category_combo = ttk.Combobox(categories_frame, textvariable=self.grammar_category_var,
                                     values=["All"] + categories, state="readonly")
        category_combo.pack(side='left')
        category_combo.bind("<<ComboboxSelected>>", self.filter_grammar_lessons)
        
        # Lessons display area
        self.lessons_display_frame = tk.Frame(self.content_frame, bg='#ffffff')
        self.lessons_display_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.display_grammar_lessons()
        
    def display_grammar_lessons(self):
        """Display filtered grammar lessons"""
        for widget in self.lessons_display_frame.winfo_children():
            widget.destroy()
        
        category = self.grammar_category_var.get()
        filtered_lessons = self.grammar_lessons
        
        if category != "All":
            filtered_lessons = [l for l in self.grammar_lessons if l['category'] == category]
        
        # Create scrollable frame
        canvas = tk.Canvas(self.lessons_display_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.lessons_display_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display lessons
        for i, lesson in enumerate(filtered_lessons):
            lesson_frame = tk.LabelFrame(scrollable_frame, 
                                        text=f"{lesson['title']} ({lesson['category']})",
                                        font=('Arial', 12, 'bold'), bg='#ffffff')
            lesson_frame.pack(fill='x', padx=10, pady=8)
            
            # Lesson description
            tk.Label(lesson_frame, text=lesson['description'], 
                    font=('Arial', 11), bg='#ffffff', fg='#374151',
                    wraplength=600, justify='left').pack(anchor='w', padx=15, pady=10)
            
            # Difficulty and duration
            info_frame = tk.Frame(lesson_frame, bg='#ffffff')
            info_frame.pack(fill='x', padx=15, pady=5)
            
            difficulty_colors = {'Beginner': '#10b981', 'Intermediate': '#f59e0b', 'Advanced': '#dc2626'}
            difficulty_color = difficulty_colors.get(lesson['difficulty'], '#6b7280')
            
            tk.Label(info_frame, text=f"Level: {lesson['difficulty']}", 
                    font=('Arial', 9), bg='#ffffff', fg=difficulty_color).pack(side='left')
            
            tk.Label(info_frame, text=f"Duration: {lesson['duration']}", 
                    font=('Arial', 9), bg='#ffffff', fg='#6b7280').pack(side='left', padx=(20, 0))
            
            tk.Button(info_frame, text="📖 Start Lesson", 
                     command=lambda l=lesson: self.start_grammar_lesson(l),
                     bg='#7c3aed', fg='white', font=('Arial', 10)).pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def start_grammar_lesson(self, lesson):
        """Start a specific grammar lesson"""
        self.current_lesson = lesson
        self.clear_content_frame()
        
        # Lesson header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text=f"📖 {lesson['title']}", 
                font=('Arial', 18, 'bold'), bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Button(header_frame, text="📝 Practice Exercises", 
                 command=self.show_lesson_exercises,
                 bg='#059669', fg='white', font=('Arial', 10)).pack(side='right', padx=5)
        
        tk.Button(header_frame, text="🏠 Back to Lessons", 
                 command=self.show_grammar_lessons,
                 bg='#6b7280', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Lesson content
        content_frame = tk.Frame(self.content_frame, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Lesson text display
        lesson_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD,
                                               font=('Georgia', 12), bg='#fefefe',
                                               height=25, relief='flat', bd=10)
        lesson_text.pack(fill='both', expand=True)
        
        # Insert lesson content
        lesson_content = lesson['content']
        lesson_text.insert('1.0', lesson_content)
        lesson_text.configure(state='disabled')
        
        # Highlight key terms
        self.highlight_grammar_terms(lesson_text, lesson.get('key_terms', []))
        
    def show_lesson_exercises(self):
        """Show practice exercises for current lesson"""
        if not self.current_lesson:
            return
            
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text=f"📝 Practice: {self.current_lesson['title']}", 
                font=('Arial', 18, 'bold'), bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Button(header_frame, text="📖 Back to Lesson", 
                 command=lambda: self.start_grammar_lesson(self.current_lesson),
                 bg='#7c3aed', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Exercises
        exercises_frame = tk.Frame(self.content_frame, bg='#ffffff')
        exercises_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Generate exercises based on lesson type
        exercises = self.generate_exercises(self.current_lesson)
        
        self.exercise_widgets = []
        for i, exercise in enumerate(exercises):
            ex_frame = tk.LabelFrame(exercises_frame, text=f"Exercise {i+1}", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
            ex_frame.pack(fill='x', pady=10)
            
            # Exercise instruction
            tk.Label(ex_frame, text=exercise['instruction'], 
                    font=('Arial', 11), bg='#ffffff', fg='#374151',
                    wraplength=700, justify='left').pack(anchor='w', padx=15, pady=10)
            
            # Exercise content
            if exercise['type'] == 'multiple_choice':
                question_frame = tk.Frame(ex_frame, bg='#ffffff')
                question_frame.pack(fill='x', padx=15, pady=5)
                
                tk.Label(question_frame, text=exercise['question'], 
                        font=('Arial', 11), bg='#ffffff').pack(anchor='w')
                
                answer_var = tk.StringVar()
                for option in exercise['options']:
                    tk.Radiobutton(question_frame, text=option, variable=answer_var, 
                                  value=option, font=('Arial', 10), bg='#ffffff').pack(anchor='w')
                
                self.exercise_widgets.append({
                    'type': 'multiple_choice',
                    'answer_var': answer_var,
                    'correct': exercise['correct']
                })
                
            elif exercise['type'] == 'fill_blank':
                sentence_frame = tk.Frame(ex_frame, bg='#ffffff')
                sentence_frame.pack(fill='x', padx=15, pady=5)
                
                tk.Label(sentence_frame, text=exercise['sentence'], 
                        font=('Arial', 11), bg='#ffffff').pack(anchor='w')
                
                answer_entry = tk.Entry(sentence_frame, font=('Arial', 11), width=20)
                answer_entry.pack(anchor='w', pady=5)
                
                self.exercise_widgets.append({
                    'type': 'fill_blank',
                    'answer_var': answer_entry,
                    'correct': exercise['correct']
                })
        
        # Submit button
        submit_frame = tk.Frame(self.content_frame, bg='#ffffff')
        submit_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Button(submit_frame, text="✅ Check Answers", 
                 command=self.check_exercise_answers,
                 font=('Arial', 12, 'bold'), bg='#059669', fg='white', 
                 pady=8).pack(side='right')
        
    def show_grammar_practice(self):
        """Show grammar practice activities"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="✏️ Grammar Practice", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Practice options
        practice_frame = tk.Frame(self.content_frame, bg='#ffffff')
        practice_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        practice_options = [
            ("✍️ Sentence Builder", "Build correct sentences step by step", self.sentence_builder),
            ("🔍 Error Detective", "Find and fix grammar mistakes", self.error_detective),
            ("🎯 Parts of Speech", "Identify nouns, verbs, adjectives, etc.", self.parts_of_speech_game),
            ("📝 Punctuation Practice", "Master commas, periods, and more", self.punctuation_practice),
            ("🔗 Sentence Combining", "Learn to combine simple sentences", self.sentence_combining),
            ("📖 Paragraph Editor", "Edit paragraphs for grammar errors", self.paragraph_editor)
        ]
        
        for i, (title, description, command) in enumerate(practice_options):
            row = i // 2
            col = i % 2
            
            option_frame = tk.LabelFrame(practice_frame, text=title, 
                                        font=('Arial', 12, 'bold'), bg='#ffffff')
            option_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            tk.Label(option_frame, text=description, font=('Arial', 11),
                    bg='#ffffff', fg='#374151', wraplength=250).pack(padx=15, pady=15)
            
            tk.Button(option_frame, text="Start Practice", command=command,
                     bg='#7c3aed', fg='white', font=('Arial', 10)).pack(pady=10)
        
        for i in range(2):
            practice_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            practice_frame.grid_rowconfigure(i, weight=1)
            
    def show_vocabulary_study(self):
        """Show vocabulary study interface"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="📚 Vocabulary Study", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Button(header_frame, text="📊 My Word List", command=self.show_personal_word_list,
                 bg='#059669', fg='white', font=('Arial', 10)).pack(side='right', padx=5)
        
        tk.Button(header_frame, text="🎲 Random Words", command=self.random_vocab_words,
                 bg='#f59e0b', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Level selection
        level_frame = tk.Frame(self.content_frame, bg='#ffffff')
        level_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(level_frame, text="Choose Level:", font=('Arial', 12, 'bold'),
                bg='#ffffff').pack(side='left')
        
        self.vocab_level_var = tk.StringVar(value="Elementary")
        level_combo = ttk.Combobox(level_frame, textvariable=self.vocab_level_var,
                                  values=["Elementary", "Middle School", "High School", "Advanced"],
                                  state="readonly")
        level_combo.pack(side='left', padx=10)
        level_combo.bind("<<ComboboxSelected>>", self.load_vocab_by_level)
        
        # Words display
        self.vocab_display_frame = tk.Frame(self.content_frame, bg='#ffffff')
        self.vocab_display_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.display_vocabulary_words()
        
    def display_vocabulary_words(self):
        """Display vocabulary words for selected level"""
        for widget in self.vocab_display_frame.winfo_children():
            widget.destroy()
        
        level = self.vocab_level_var.get()
        words = [w for w in self.vocabulary_words if w['level'] == level][:10]  # Show first 10
        
        if not words:
            tk.Label(self.vocab_display_frame, text="No words available for this level",
                    font=('Arial', 12), bg='#ffffff', fg='#7f8c8d').pack(expand=True)
            return
        
        # Create word cards
        cards_frame = tk.Frame(self.vocab_display_frame, bg='#ffffff')
        cards_frame.pack(fill='both', expand=True)
        
        for i, word in enumerate(words):
            row = i // 2
            col = i % 2
            
            card_frame = tk.LabelFrame(cards_frame, text=word['word'].upper(), 
                                      font=('Arial', 14, 'bold'), bg='#ffffff')
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Definition
            tk.Label(card_frame, text=f"Definition: {word['definition']}", 
                    font=('Arial', 11), bg='#ffffff', fg='#374151',
                    wraplength=300, justify='left').pack(anchor='w', padx=15, pady=5)
            
            # Example sentence
            if 'example' in word:
                tk.Label(card_frame, text=f"Example: {word['example']}", 
                        font=('Arial', 10, 'italic'), bg='#ffffff', fg='#6b7280',
                        wraplength=300, justify='left').pack(anchor='w', padx=15, pady=5)
            
            # Action buttons
            btn_frame = tk.Frame(card_frame, bg='#ffffff')
            btn_frame.pack(fill='x', padx=15, pady=10)
            
            tk.Button(btn_frame, text="💾 Save", 
                     command=lambda w=word: self.save_word_to_list(w),
                     bg='#10b981', fg='white', font=('Arial', 9)).pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="🔊 Pronounce", 
                     command=lambda w=word: self.pronounce_word(w),
                     bg='#3b82f6', fg='white', font=('Arial', 9)).pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="📝 Quiz Me", 
                     command=lambda w=word: self.quiz_word(w),
                     bg='#8b5cf6', fg='white', font=('Arial', 9)).pack(side='right')
        
        for i in range(2):
            cards_frame.grid_columnconfigure(i, weight=1)
            
    def show_vocabulary_games(self):
        """Show vocabulary games"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="🎮 Vocabulary Games", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Games grid
        games_frame = tk.Frame(self.content_frame, bg='#ffffff')
        games_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        games = [
            ("🎯 Word Match", "Match words with their definitions", self.word_match_game, '#e74c3c'),
            ("🔤 Spelling Bee", "Test your spelling skills", self.spelling_bee_game, '#f39c12'),
            ("🧩 Word Builder", "Build words from letter tiles", self.word_builder_game, '#9b59b6'),
            ("🎪 Synonym Circus", "Find words with similar meanings", self.synonym_game, '#1abc9c'),
            ("🎭 Antonym Theater", "Discover opposite meanings", self.antonym_game, '#34495e'),
            ("⚡ Lightning Round", "Quick-fire vocabulary challenge", self.lightning_round_game, '#e67e22')
        ]
        
        for i, (title, description, command, color) in enumerate(games):
            row = i // 2
            col = i % 2
            
            game_frame = tk.LabelFrame(games_frame, text=title, 
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
            game_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            tk.Label(game_frame, text=description, font=('Arial', 11),
                    bg='#ffffff', fg='#374151', wraplength=250).pack(padx=15, pady=15)
            
            tk.Button(game_frame, text="🎮 Play Game", command=command,
                     bg=color, fg='white', font=('Arial', 11, 'bold')).pack(pady=10)
        
        for i in range(2):
            games_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            games_frame.grid_rowconfigure(i, weight=1)
            
    def show_progress_tracker(self):
        """Show progress tracking interface"""
        self.clear_content_frame()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="📊 Progress Tracker", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Stats overview
        stats_frame = tk.LabelFrame(self.content_frame, text="Learning Statistics",
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Calculate stats
        total_lessons = len(self.student_progress)
        avg_quiz_score = sum(self.quiz_scores) / max(1, len(self.quiz_scores))
        
        stats_text = f"""
📚 Lessons Completed: {total_lessons}
📝 Quizzes Taken: {len(self.quiz_scores)}
📊 Average Quiz Score: {avg_quiz_score:.1f}%
🏆 Best Quiz Score: {max(self.quiz_scores, default=0):.1f}%
🎯 Words Learned: {len(getattr(self, 'personal_word_list', []))}
        """
        
        tk.Label(stats_frame, text=stats_text, font=('Arial', 11),
                bg='#ffffff', fg='#374151', justify='left').pack(padx=20, pady=15)
        
        # Progress chart (simplified)
        chart_frame = tk.LabelFrame(self.content_frame, text="Progress Chart",
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        chart_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(chart_frame, text="📈 Visual progress chart would be displayed here",
                font=('Arial', 12), bg='#ffffff', fg='#7f8c8d').pack(expand=True)
        
    def clear_content_frame(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def load_grammar_lessons(self):
        """Load grammar lessons database"""
        return [
            {
                "title": "Nouns and Pronouns",
                "category": "Parts of Speech",
                "difficulty": "Beginner",
                "duration": "15 minutes",
                "description": "Learn about naming words and words that replace them",
                "content": """NOUNS AND PRONOUNS

🏷️ WHAT ARE NOUNS?
Nouns are naming words. They tell us the names of people, places, things, or ideas.

Types of Nouns:
• Common Nouns: General names (dog, city, book)
• Proper Nouns: Specific names (Rover, New York, Harry Potter)
• Concrete Nouns: Things you can touch (table, apple, car)
• Abstract Nouns: Ideas you cannot touch (love, happiness, freedom)

Examples:
• Person: teacher, Sarah, doctor
• Place: school, Paris, kitchen
• Thing: pencil, computer, sandwich
• Idea: courage, friendship, excitement

📍 WHAT ARE PRONOUNS?
Pronouns are words that take the place of nouns. They help us avoid repeating the same nouns over and over.

Common Pronouns:
• Personal: I, you, he, she, it, we, they
• Possessive: my, your, his, her, its, our, their
• Demonstrative: this, that, these, those

Examples:
• Instead of: "John went to John's car"
• We say: "John went to his car"

• Instead of: "The books are on the table. The books are heavy."
• We say: "The books are on the table. They are heavy."

✍️ PRACTICE TIPS:
1. Look around you and name 10 nouns you can see
2. Replace repeated nouns in your writing with pronouns
3. Make sure pronouns clearly refer to the correct noun""",
                "key_terms": ["noun", "pronoun", "common", "proper", "concrete", "abstract"]
            },
            {
                "title": "Subject-Verb Agreement", 
                "category": "Grammar Rules",
                "difficulty": "Intermediate",
                "duration": "20 minutes",
                "description": "Master the rules for matching subjects and verbs",
                "content": """SUBJECT-VERB AGREEMENT

🤝 THE BASIC RULE
The subject and verb in a sentence must agree in number. This means:
• Singular subjects take singular verbs
• Plural subjects take plural verbs

SINGULAR EXAMPLES:
• The cat runs fast. (cat = singular, runs = singular verb)
• She is happy. (she = singular, is = singular verb)
• The book was interesting. (book = singular, was = singular verb)

PLURAL EXAMPLES:
• The cats run fast. (cats = plural, run = plural verb)
• They are happy. (they = plural, are = plural verb)
• The books were interesting. (books = plural, were = plural verb)

🎯 TRICKY SITUATIONS:

1. Words Between Subject and Verb:
• The box of chocolates IS delicious. (box is the subject, not chocolates)
• The students in the class ARE studying. (students is the subject)

2. Compound Subjects with "and":
• Tom and Jerry ARE friends. (Tom and Jerry = plural)

3. Compound Subjects with "or":
• Either Tom or Jerry IS coming. (Use verb that matches the closer subject)

4. Collective Nouns:
• The team IS playing well. (team = one unit)
• The team ARE arguing among themselves. (team = individual members)

5. Indefinite Pronouns:
• Everyone IS here. (everyone = singular)
• Both ARE correct. (both = plural)

✅ QUICK CHECK:
Ask yourself: "Who or what is doing the action?" That's your subject. Then make sure your verb matches!""",
                "key_terms": ["subject", "verb", "agreement", "singular", "plural", "compound"]
            }
        ]
        
    def load_vocabulary_database(self):
        """Load vocabulary words database"""
        return [
            {
                "word": "abundant",
                "definition": "existing in large quantities; plentiful",
                "level": "Middle School",
                "example": "The garden had an abundant harvest of vegetables.",
                "synonyms": ["plentiful", "copious", "ample"],
                "antonyms": ["scarce", "sparse", "insufficient"]
            },
            {
                "word": "benevolent", 
                "definition": "kind and generous",
                "level": "High School",
                "example": "The benevolent king helped the poor villagers.",
                "synonyms": ["kind", "generous", "charitable"],
                "antonyms": ["malevolent", "cruel", "selfish"]
            },
            {
                "word": "curious",
                "definition": "eager to learn or know something",
                "level": "Elementary",
                "example": "The curious child asked many questions.",
                "synonyms": ["inquisitive", "interested", "wondering"],
                "antonyms": ["indifferent", "uninterested", "apathetic"]
            },
            {
                "word": "diligent",
                "definition": "showing careful and persistent effort",
                "level": "Middle School", 
                "example": "The diligent student completed all homework on time.",
                "synonyms": ["hardworking", "careful", "thorough"],
                "antonyms": ["lazy", "careless", "negligent"]
            },
            {
                "word": "eloquent",
                "definition": "fluent and persuasive in speaking or writing",
                "level": "High School",
                "example": "The eloquent speaker moved the audience to tears.",
                "synonyms": ["articulate", "fluent", "persuasive"],
                "antonyms": ["inarticulate", "tongue-tied", "unclear"]
            }
        ]
        
    def generate_exercises(self, lesson):
        """Generate practice exercises for a lesson"""
        exercises = []
        
        if lesson['category'] == "Parts of Speech":
            exercises = [
                {
                    "type": "multiple_choice",
                    "instruction": "Identify the noun in the sentence:",
                    "question": "The beautiful butterfly landed on the flower.",
                    "options": ["beautiful", "butterfly", "landed", "on"],
                    "correct": "butterfly"
                },
                {
                    "type": "fill_blank",
                    "instruction": "Replace the repeated noun with a pronoun:",
                    "sentence": "Sarah loves Sarah's new bicycle.",
                    "correct": "her"
                }
            ]
        elif lesson['category'] == "Grammar Rules":
            exercises = [
                {
                    "type": "multiple_choice",
                    "instruction": "Choose the correct verb:",
                    "question": "The group of students _____ working together.",
                    "options": ["is", "are"],
                    "correct": "is"
                },
                {
                    "type": "fill_blank",
                    "instruction": "Fill in the correct verb form:",
                    "sentence": "Either the cats or the dog _____ making noise.",
                    "correct": "is"
                }
            ]
            
        return exercises
        
    def highlight_grammar_terms(self, text_widget, key_terms):
        """Highlight key grammar terms in lesson text"""
        for term in key_terms:
            # Simple highlighting - find and highlight term
            start_pos = "1.0"
            while True:
                pos = text_widget.search(term, start_pos, tk.END)
                if not pos:
                    break
                end_pos = f"{pos}+{len(term)}c"
                text_widget.tag_add("highlight", pos, end_pos)
                start_pos = end_pos
                
        text_widget.tag_config("highlight", background="#fef3c7", foreground="#92400e")
        
    def check_exercise_answers(self):
        """Check answers for current exercises"""
        if not hasattr(self, 'exercise_widgets'):
            return
            
        score = 0
        total = len(self.exercise_widgets)
        
        for widget in self.exercise_widgets:
            if widget['type'] == 'multiple_choice':
                if widget['answer_var'].get() == widget['correct']:
                    score += 1
            elif widget['type'] == 'fill_blank':
                answer = widget['answer_var'].get().strip().lower()
                correct = widget['correct'].lower()
                if answer == correct:
                    score += 1
                    
        percentage = (score / total) * 100
        self.quiz_scores.append(percentage)
        
        messagebox.showinfo("Exercise Results", 
                           f"Score: {score}/{total} ({percentage:.1f}%)\n\nGreat work practicing!")
        
    # Placeholder methods for advanced features
    def random_grammar_lesson(self):
        lesson = random.choice(self.grammar_lessons)
        self.start_grammar_lesson(lesson)
        
    def filter_grammar_lessons(self, event=None):
        self.display_grammar_lessons()
        
    def start_grammar_quiz(self):
        messagebox.showinfo("Grammar Quiz", "Interactive grammar quiz would start here.")
        
    def quick_assessment(self):
        messagebox.showinfo("Quick Assessment", "Skill assessment quiz would start here.")
        
    def sentence_builder(self):
        messagebox.showinfo("Sentence Builder", "Interactive sentence building tool would open here.")
        
    def error_detective(self):
        messagebox.showinfo("Error Detective", "Grammar error detection game would start here.")
        
    def parts_of_speech_game(self):
        messagebox.showinfo("Parts of Speech", "Parts of speech identification game would start here.")
        
    def punctuation_practice(self):
        messagebox.showinfo("Punctuation Practice", "Punctuation practice activities would start here.")
        
    def sentence_combining(self):
        messagebox.showinfo("Sentence Combining", "Sentence combining exercises would start here.")
        
    def paragraph_editor(self):
        messagebox.showinfo("Paragraph Editor", "Interactive paragraph editing tool would open here.")
        
    def load_vocab_by_level(self, event=None):
        self.display_vocabulary_words()
        
    def random_vocab_words(self):
        words = random.sample(self.vocabulary_words, min(5, len(self.vocabulary_words)))
        word_list = "\n".join([f"• {w['word']}: {w['definition']}" for w in words])
        messagebox.showinfo("Random Words", f"Here are some words to study:\n\n{word_list}")
        
    def show_personal_word_list(self):
        messagebox.showinfo("Personal Word List", "Your saved vocabulary words would be displayed here.")
        
    def save_word_to_list(self, word):
        messagebox.showinfo("Word Saved", f"'{word['word']}' has been added to your word list!")
        
    def pronounce_word(self, word):
        messagebox.showinfo("Pronunciation", f"Pronunciation for '{word['word']}' would be played here.")
        
    def quiz_word(self, word):
        messagebox.showinfo("Word Quiz", f"Quiz for '{word['word']}' would start here.")
        
    def start_vocab_challenge(self):
        messagebox.showinfo("Vocabulary Challenge", "Vocabulary challenge would start here.")
        
    def word_match_game(self):
        messagebox.showinfo("Word Match", "Word matching game would start here.")
        
    def spelling_bee_game(self):
        messagebox.showinfo("Spelling Bee", "Spelling bee game would start here.")
        
    def word_builder_game(self):
        messagebox.showinfo("Word Builder", "Word building game would start here.")
        
    def synonym_game(self):
        messagebox.showinfo("Synonym Game", "Synonym matching game would start here.")
        
    def antonym_game(self):
        messagebox.showinfo("Antonym Game", "Antonym matching game would start here.")
        
    def lightning_round_game(self):
        messagebox.showinfo("Lightning Round", "Lightning round vocabulary game would start here.")
        
    def show_skill_assessment(self):
        messagebox.showinfo("Skill Assessment", "Comprehensive skill assessment would be available here.")
        
    def show_study_planner(self):
        messagebox.showinfo("Study Planner", "Personalized study planning tool would be available here.")
        
    def show_settings(self):
        messagebox.showinfo("Settings", "Application settings would be available here.")

def main():
    root = tk.Tk()
    app = GrammarVocabularyMaster(root)
    root.mainloop()

if __name__ == "__main__":
    main()