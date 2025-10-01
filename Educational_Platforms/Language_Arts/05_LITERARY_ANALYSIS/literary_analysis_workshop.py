#!/usr/bin/env python3
"""
Language Arts - Literary Analysis Workshop
An interactive platform for analyzing literature and developing critical thinking skills
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
from datetime import datetime
import re

class LiteraryAnalysisWorkshop:
    def __init__(self, root):
        self.root = root
        self.root.title("Literary Analysis Workshop - Language Arts Education")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0fdf4')
        
        # Data storage
        self.literary_works = self.load_literary_works()
        self.analysis_frameworks = self.load_analysis_frameworks()
        self.current_work = None
        self.student_analyses = {}
        self.critical_lenses = self.load_critical_lenses()
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f0fdf4')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="📖 Literary Analysis Workshop", 
                              font=('Arial', 24, 'bold'), bg='#f0fdf4', fg='#14532d')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Develop critical thinking through deep literary exploration", 
                                 font=('Arial', 12), bg='#f0fdf4', fg='#16a34a')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0fdf4')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Navigation and Tools
        left_frame = tk.Frame(main_frame, bg='#dcfce7', relief='raised', bd=2, width=320)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        nav_label = tk.Label(left_frame, text="Analysis Toolkit", font=('Arial', 14, 'bold'),
                            bg='#dcfce7', fg='#14532d')
        nav_label.pack(pady=15)
        
        # Literature Library section
        library_frame = tk.LabelFrame(left_frame, text="📚 Literature Library", 
                                     font=('Arial', 12, 'bold'), bg='#dcfce7')
        library_frame.pack(fill='x', padx=10, pady=5)
        
        library_buttons = [
            ("📖 Browse Works", self.browse_literature),
            ("🎲 Random Selection", self.random_literature),
            ("📁 Upload Text", self.upload_literature),
            ("📋 Reading List", self.show_reading_list)
        ]
        
        for text, command in library_buttons:
            btn = tk.Button(library_frame, text=text, command=command,
                          font=('Arial', 10), width=28, pady=3,
                          bg='#16a34a', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Analysis Methods section
        methods_frame = tk.LabelFrame(left_frame, text="🔍 Analysis Methods", 
                                     font=('Arial', 12, 'bold'), bg='#dcfce7')
        methods_frame.pack(fill='x', padx=10, pady=5)
        
        methods_buttons = [
            ("🎭 Character Analysis", self.character_analysis),
            ("📊 Plot Structure", self.plot_analysis),
            ("🎨 Theme Exploration", self.theme_analysis),
            ("🔍 Close Reading", self.close_reading),
            ("🌍 Historical Context", self.historical_context)
        ]
        
        for text, command in methods_buttons:
            btn = tk.Button(methods_frame, text=text, command=command,
                          font=('Arial', 10), width=28, pady=3,
                          bg='#ca8a04', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Critical Lenses section
        lenses_frame = tk.LabelFrame(left_frame, text="🔬 Critical Lenses", 
                                    font=('Arial', 12, 'bold'), bg='#dcfce7')
        lenses_frame.pack(fill='x', padx=10, pady=5)
        
        lenses_buttons = [
            ("👥 Feminist Criticism", lambda: self.apply_critical_lens("feminist")),
            ("📚 Historical Criticism", lambda: self.apply_critical_lens("historical")),
            ("🧠 Psychological Criticism", lambda: self.apply_critical_lens("psychological")),
            ("📖 Formalist Criticism", lambda: self.apply_critical_lens("formalist"))
        ]
        
        for text, command in lenses_buttons:
            btn = tk.Button(lenses_frame, text=text, command=command,
                          font=('Arial', 10), width=28, pady=3,
                          bg='#dc2626', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Writing Tools section
        writing_frame = tk.LabelFrame(left_frame, text="✍️ Writing Tools", 
                                     font=('Arial', 12, 'bold'), bg='#dcfce7')
        writing_frame.pack(fill='x', padx=10, pady=5)
        
        writing_buttons = [
            ("📝 Analysis Essay", self.write_analysis_essay),
            ("💭 Discussion Posts", self.write_discussion),
            ("📊 Comparison Chart", self.create_comparison)
        ]
        
        for text, command in writing_buttons:
            btn = tk.Button(writing_frame, text=text, command=command,
                          font=('Arial', 10), width=28, pady=3,
                          bg='#7c3aed', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Quick Reference
        reference_frame = tk.LabelFrame(left_frame, text="📋 Quick Reference", 
                                       font=('Arial', 11, 'bold'), bg='#dcfce7')
        reference_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        reference_text = """📖 Literary Elements:
• Plot: sequence of events
• Character: people in story
• Setting: time and place
• Theme: central message
• Point of View: perspective
• Style: author's technique

🔍 Analysis Questions:
• What is the author's purpose?
• How do characters develop?
• What symbols appear?
• How does setting affect plot?
• What themes emerge?"""
        
        tk.Label(reference_frame, text=reference_text, font=('Arial', 8),
                bg='#dcfce7', fg='#374151', justify='left').pack(padx=10, pady=10)
        
        # Right panel - Main workspace
        self.workspace_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        self.workspace_frame.pack(side='right', fill='both', expand=True)
        
        # Show welcome screen by default
        self.show_welcome_screen()
        
    def show_welcome_screen(self):
        """Show the welcome screen"""
        self.clear_workspace()
        
        welcome_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        welcome_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Welcome header
        tk.Label(welcome_frame, text="Welcome to Literary Analysis Workshop!", 
                font=('Arial', 22, 'bold'), bg='#ffffff', fg='#14532d').pack(pady=20)
        
        tk.Label(welcome_frame, text="Develop critical thinking skills through deep literary exploration", 
                font=('Arial', 14), bg='#ffffff', fg='#16a34a').pack(pady=10)
        
        # Featured work
        featured_frame = tk.LabelFrame(welcome_frame, text="📖 Featured Work", 
                                      font=('Arial', 14, 'bold'), bg='#ffffff')
        featured_frame.pack(fill='x', pady=30)
        
        featured_work = random.choice(self.literary_works)
        
        # Work info
        tk.Label(featured_frame, text=featured_work["title"], 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack(pady=10)
        
        tk.Label(featured_frame, text=f"by {featured_work['author']}", 
                font=('Arial', 12, 'italic'), bg='#ffffff', fg='#16a34a').pack()
        
        # Description
        tk.Label(featured_frame, text=featured_work['description'][:200] + "...", 
                font=('Arial', 11), bg='#ffffff', fg='#374151',
                wraplength=600, justify='center').pack(pady=15)
        
        tk.Button(featured_frame, text="📚 Start Analysis", 
                 command=lambda: self.start_analysis(featured_work),
                 bg='#16a34a', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Analysis approaches
        approaches_frame = tk.LabelFrame(welcome_frame, text="Analysis Approaches", 
                                        font=('Arial', 14, 'bold'), bg='#ffffff')
        approaches_frame.pack(fill='x', pady=20)
        
        approaches = [
            ("🎭 Character Study", "Analyze character development and relationships", self.character_analysis, '#ca8a04'),
            ("📊 Thematic Analysis", "Explore central themes and messages", self.theme_analysis, '#dc2626'),
            ("🔍 Close Reading", "Examine language and literary devices", self.close_reading, '#7c3aed'),
            ("🌍 Contextual Analysis", "Consider historical and cultural context", self.historical_context, '#059669')
        ]
        
        for i, (title, desc, command, color) in enumerate(approaches):
            row = i // 2
            col = i % 2
            
            approach_frame = tk.Frame(approaches_frame, bg='#ffffff', relief='raised', bd=1)
            approach_frame.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
            
            tk.Label(approach_frame, text=title, font=('Arial', 12, 'bold'),
                    bg='#ffffff', fg=color).pack(pady=10)
            
            tk.Label(approach_frame, text=desc, font=('Arial', 10),
                    bg='#ffffff', fg='#6b7280', wraplength=250).pack(pady=5)
            
            tk.Button(approach_frame, text="Learn More", command=command,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     relief='flat', pady=5).pack(pady=10)
        
        for i in range(2):
            approaches_frame.grid_columnconfigure(i, weight=1)
        
    def browse_literature(self):
        """Show literature browsing interface"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="📚 Literature Library", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#14532d').pack(side='left')
        
        # Filter options
        filter_frame = tk.Frame(header_frame, bg='#ffffff')
        filter_frame.pack(side='right')
        
        # Genre filter
        tk.Label(filter_frame, text="Genre:", font=('Arial', 10, 'bold'),
                bg='#ffffff').pack(side='left')
        
        self.genre_var = tk.StringVar(value="All")
        genre_combo = ttk.Combobox(filter_frame, textvariable=self.genre_var,
                                  values=["All", "Fiction", "Drama", "Poetry", "Non-fiction"],
                                  state="readonly", width=12)
        genre_combo.pack(side='left', padx=5)
        genre_combo.bind("<<ComboboxSelected>>", self.filter_literature)
        
        # Period filter
        tk.Label(filter_frame, text="Period:", font=('Arial', 10, 'bold'),
                bg='#ffffff').pack(side='left', padx=(20, 0))
        
        self.period_var = tk.StringVar(value="All")
        period_combo = ttk.Combobox(filter_frame, textvariable=self.period_var,
                                   values=["All", "Classical", "Medieval", "Renaissance", "Modern", "Contemporary"],
                                   state="readonly", width=12)
        period_combo.pack(side='left', padx=5)
        period_combo.bind("<<ComboboxSelected>>", self.filter_literature)
        
        # Literature display area
        self.literature_display_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        self.literature_display_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.display_literature_grid()
        
    def display_literature_grid(self):
        """Display literature works in grid"""
        for widget in self.literature_display_frame.winfo_children():
            widget.destroy()
        
        # Filter works
        genre = self.genre_var.get()
        period = self.period_var.get()
        
        filtered_works = self.literary_works
        if genre != "All":
            filtered_works = [w for w in filtered_works if w.get('genre') == genre]
        if period != "All":
            filtered_works = [w for w in filtered_works if w.get('period') == period]
        
        # Create scrollable frame
        canvas = tk.Canvas(self.literature_display_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.literature_display_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display works in grid
        for i, work in enumerate(filtered_works):
            row = i // 2
            col = i % 2
            
            work_frame = tk.LabelFrame(scrollable_frame, text=work["title"],
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
            work_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Author and info
            tk.Label(work_frame, text=f"by {work['author']}", 
                    font=('Arial', 11, 'italic'), bg='#ffffff', fg='#16a34a').pack(pady=5)
            
            info_text = f"{work.get('genre', 'Unknown')} • {work.get('period', 'Unknown')} • {work.get('year', 'Unknown')}"
            tk.Label(work_frame, text=info_text, font=('Arial', 9),
                    bg='#ffffff', fg='#6b7280').pack(pady=2)
            
            # Description
            tk.Label(work_frame, text=work['description'][:150] + "...", 
                    font=('Arial', 10), bg='#ffffff', fg='#374151',
                    wraplength=300, justify='left').pack(pady=10, padx=10)
            
            # Buttons
            btn_frame = tk.Frame(work_frame, bg='#ffffff')
            btn_frame.pack(fill='x', padx=15, pady=10)
            
            tk.Button(btn_frame, text="📖 Read", 
                     command=lambda w=work: self.read_work(w),
                     bg='#16a34a', fg='white', font=('Arial', 9)).pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="🔍 Analyze", 
                     command=lambda w=work: self.start_analysis(w),
                     bg='#ca8a04', fg='white', font=('Arial', 9)).pack(side='right', padx=2)
        
        for i in range(2):
            scrollable_frame.grid_columnconfigure(i, weight=1)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def start_analysis(self, work):
        """Start analyzing a literary work"""
        self.current_work = work
        self.clear_workspace()
        
        # Create tabbed analysis interface
        notebook = ttk.Notebook(self.workspace_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Text & Overview
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="📖 Text & Overview")
        self.create_text_overview_tab(text_frame, work)
        
        # Tab 2: Character Analysis
        char_frame = ttk.Frame(notebook)
        notebook.add(char_frame, text="🎭 Characters")
        self.create_character_tab(char_frame, work)
        
        # Tab 3: Themes & Symbols
        theme_frame = ttk.Frame(notebook)
        notebook.add(theme_frame, text="🎨 Themes & Symbols")
        self.create_themes_tab(theme_frame, work)
        
        # Tab 4: Literary Devices
        devices_frame = ttk.Frame(notebook)
        notebook.add(devices_frame, text="🔧 Literary Devices")
        self.create_devices_tab(devices_frame, work)
        
        # Tab 5: Critical Analysis
        critical_frame = ttk.Frame(notebook)
        notebook.add(critical_frame, text="🔬 Critical Analysis")
        self.create_critical_tab(critical_frame, work)
        
        # Tab 6: My Notes
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="📝 My Notes")
        self.create_notes_tab(notes_frame, work)
        
    def create_text_overview_tab(self, parent, work):
        """Create text and overview tab"""
        # Work header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text=work["title"], 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack()
        
        tk.Label(header_frame, text=f"by {work['author']}", 
                font=('Arial', 12, 'italic'), bg='#ffffff', fg='#16a34a').pack()
        
        # Main content area
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Left side - text excerpt
        text_frame = tk.LabelFrame(content_frame, text="Text Excerpt", 
                                  font=('Arial', 12, 'bold'), bg='#ffffff')
        text_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        text_display = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                font=('Georgia', 11), bg='#fefefe')
        text_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Insert text excerpt
        text_excerpt = work.get('text', work['description'])
        text_display.insert('1.0', text_excerpt)
        text_display.configure(state='disabled')
        
        # Right side - overview
        overview_frame = tk.LabelFrame(content_frame, text="Work Overview", 
                                      font=('Arial', 12, 'bold'), bg='#ffffff', width=350)
        overview_frame.pack(side='right', fill='y')
        overview_frame.pack_propagate(False)
        
        # Work information
        info_text = f"""📚 WORK INFORMATION

📖 Title: {work['title']}
👤 Author: {work['author']}
📅 Year: {work.get('year', 'Unknown')}
🎭 Genre: {work.get('genre', 'Unknown')}
⏰ Period: {work.get('period', 'Unknown')}

📋 SUMMARY:
{work['description']}

🎯 MAJOR THEMES:
{', '.join(work.get('themes', ['To be explored']))}

📊 LITERARY SIGNIFICANCE:
{work.get('significance', 'A significant work in literary history')}

🔍 ANALYSIS FOCUS:
• Character development
• Thematic elements
• Literary techniques
• Historical context
• Symbolic meaning"""
        
        info_display = scrolledtext.ScrolledText(overview_frame, wrap=tk.WORD,
                                                font=('Arial', 10), bg='#fefefe')
        info_display.pack(fill='both', expand=True, padx=10, pady=10)
        info_display.insert('1.0', info_text)
        info_display.configure(state='disabled')
        
    def create_character_tab(self, parent, work):
        """Create character analysis tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text="🎭 Character Analysis", 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack()
        
        # Character analysis content
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Characters from work data
        characters = work.get('characters', [])
        if not characters:
            # Generate sample character analysis
            characters = [
                {"name": "Protagonist", "role": "Main character", "traits": ["brave", "conflicted", "determined"]},
                {"name": "Antagonist", "role": "Opposing force", "traits": ["complex", "motivated", "challenging"]}
            ]
        
        # Character cards
        for i, char in enumerate(characters):
            char_frame = tk.LabelFrame(content_frame, text=f"{char['name']} - {char['role']}", 
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
            char_frame.pack(fill='x', pady=10)
            
            # Character traits
            traits_text = f"Key Traits: {', '.join(char.get('traits', ['Complex', 'Well-developed']))}"
            tk.Label(char_frame, text=traits_text, font=('Arial', 11),
                    bg='#ffffff', fg='#374151').pack(anchor='w', padx=15, pady=5)
            
            # Analysis questions
            questions_text = f"""Analysis Questions for {char['name']}:
• How does this character change throughout the work?
• What motivates this character's actions?
• How do other characters relate to this character?
• What does this character represent symbolically?
• What conflicts does this character face?"""
            
            tk.Label(char_frame, text=questions_text, font=('Arial', 10),
                    bg='#ffffff', fg='#6b7280', justify='left').pack(anchor='w', padx=15, pady=10)
        
        # Character analysis framework
        framework_frame = tk.LabelFrame(content_frame, text="Character Analysis Framework", 
                                       font=('Arial', 12, 'bold'), bg='#ffffff')
        framework_frame.pack(fill='x', pady=10)
        
        framework_text = """🎭 CHARACTER ANALYSIS GUIDE:

1. CHARACTERIZATION METHODS:
   • Direct characterization: What the author tells us
   • Indirect characterization: What we learn through actions, dialogue, thoughts

2. CHARACTER DEVELOPMENT:
   • Static vs. Dynamic characters
   • Flat vs. Round characters
   • Character arcs and growth

3. RELATIONSHIPS:
   • How characters interact with each other
   • Power dynamics and conflicts
   • Foils and parallels

4. SYMBOLIC FUNCTION:
   • What larger ideas does the character represent?
   • How does the character serve the theme?"""
        
        tk.Label(framework_frame, text=framework_text, font=('Arial', 10),
                bg='#ffffff', fg='#374151', justify='left').pack(padx=15, pady=10, anchor='w')
        
    def create_themes_tab(self, parent, work):
        """Create themes and symbols tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text="🎨 Themes & Symbols", 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack()
        
        # Content
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Major themes
        themes_frame = tk.LabelFrame(content_frame, text="Major Themes", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
        themes_frame.pack(fill='x', pady=10)
        
        themes = work.get('themes', ['Love', 'Power', 'Identity', 'Justice'])
        for theme in themes:
            theme_item_frame = tk.Frame(themes_frame, bg='#ffffff')
            theme_item_frame.pack(fill='x', padx=15, pady=5)
            
            tk.Label(theme_item_frame, text=f"🎯 {theme}", 
                    font=('Arial', 11, 'bold'), bg='#ffffff', fg='#ca8a04').pack(side='left')
            
            tk.Label(theme_item_frame, text=f"How is the theme of {theme.lower()} developed in this work?", 
                    font=('Arial', 10), bg='#ffffff', fg='#6b7280').pack(side='left', padx=10)
        
        # Symbol analysis
        symbols_frame = tk.LabelFrame(content_frame, text="Symbol Analysis", 
                                     font=('Arial', 12, 'bold'), bg='#ffffff')
        symbols_frame.pack(fill='x', pady=10)
        
        symbols_text = """🔍 FINDING SYMBOLS:

Look for objects, colors, or images that appear repeatedly or seem to have deeper meaning:

• Objects that characters value or interact with frequently
• Natural elements (weather, seasons, animals)
• Colors that appear in significant moments
• Places that hold special meaning
• Actions or rituals that carry weight

📝 ANALYZING SYMBOLS:
1. What is the literal meaning?
2. What might it represent symbolically?
3. How does context affect its meaning?
4. How does it connect to the themes?
5. How does it develop throughout the work?"""
        
        tk.Label(symbols_frame, text=symbols_text, font=('Arial', 10),
                bg='#ffffff', fg='#374151', justify='left').pack(padx=15, pady=10, anchor='w')
        
        # Theme development tracker
        tracker_frame = tk.LabelFrame(content_frame, text="Theme Development Tracker", 
                                     font=('Arial', 12, 'bold'), bg='#ffffff')
        tracker_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(tracker_frame, text="Track how themes develop through the work:", 
                font=('Arial', 11), bg='#ffffff', fg='#374151').pack(padx=15, pady=5, anchor='w')
        
        # Simple tracking table
        tracker_text = scrolledtext.ScrolledText(tracker_frame, height=8, 
                                                font=('Arial', 10), bg='#fefefe')
        tracker_text.pack(fill='both', expand=True, padx=15, pady=10)
        
        tracker_content = """Beginning → Middle → End

Theme 1: How does it appear? → How does it develop? → How is it resolved?

Theme 2: How does it appear? → How does it develop? → How is it resolved?

Use this space to track thematic development throughout your reading..."""
        
        tracker_text.insert('1.0', tracker_content)
        
    def create_devices_tab(self, parent, work):
        """Create literary devices tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text="🔧 Literary Devices", 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack()
        
        # Content
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Literary devices reference
        devices_text = """🔧 LITERARY DEVICES TO ANALYZE:

📝 NARRATIVE TECHNIQUES:
• Point of View: Who tells the story? How does this affect our understanding?
• Foreshadowing: Hints about future events
• Flashback: Scenes from the past
• Irony: Dramatic, verbal, or situational
• Symbolism: Objects representing deeper meanings

🎨 FIGURATIVE LANGUAGE:
• Metaphor: Direct comparison ("Life is a journey")
• Simile: Comparison with "like" or "as" ("brave as a lion")
• Personification: Human qualities to non-human things
• Hyperbole: Deliberate exaggeration
• Imagery: Vivid sensory descriptions

📐 STRUCTURAL ELEMENTS:
• Plot Structure: Exposition, rising action, climax, falling action, resolution
• Pacing: How quickly or slowly events unfold
• Parallel Structure: Similar patterns in language or events
• Juxtaposition: Contrasting elements placed side by side

💭 THEMATIC DEVICES:
• Allegory: Extended metaphor throughout the work
• Allusion: Reference to other works or historical events
• Motif: Recurring elements that develop themes
• Paradox: Seemingly contradictory statements that reveal truth

🔍 ANALYSIS QUESTIONS:
• How does the author use these devices?
• What effect do they create?
• How do they support the themes?
• What would be lost without them?
• How do they affect the reader's experience?

📋 DEVICE TRACKING EXERCISE:
Choose 2-3 devices and track them throughout the work. Note:
• Where they appear
• How they're used
• What effect they create
• How they develop or change"""
        
        devices_display = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD,
                                                   font=('Arial', 11), bg='#fefefe')
        devices_display.pack(fill='both', expand=True)
        devices_display.insert('1.0', devices_text)
        devices_display.configure(state='disabled')
        
    def create_critical_tab(self, parent, work):
        """Create critical analysis tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text="🔬 Critical Analysis", 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack()
        
        # Critical lenses
        lenses_frame = tk.LabelFrame(parent, text="Critical Lenses", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
        lenses_frame.pack(fill='x', padx=15, pady=10)
        
        lens_buttons_frame = tk.Frame(lenses_frame, bg='#ffffff')
        lens_buttons_frame.pack(fill='x', padx=15, pady=10)
        
        lens_buttons = [
            ("👥 Feminist", "feminist"),
            ("📚 Historical", "historical"),
            ("🧠 Psychological", "psychological"),
            ("📖 Formalist", "formalist")
        ]
        
        for text, lens_type in lens_buttons:
            btn = tk.Button(lens_buttons_frame, text=text, 
                           command=lambda l=lens_type: self.show_critical_lens(l),
                           bg='#dc2626', fg='white', font=('Arial', 10))
            btn.pack(side='left', padx=5)
        
        # Analysis workspace
        self.critical_workspace = tk.LabelFrame(parent, text="Analysis Workspace", 
                                               font=('Arial', 12, 'bold'), bg='#ffffff')
        self.critical_workspace.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Default content
        default_text = """🔬 CRITICAL ANALYSIS WORKSPACE

Select a critical lens above to begin your analysis, or use this general framework:

📋 ANALYTICAL FRAMEWORK:

1. THESIS DEVELOPMENT:
   • What is your main argument about this work?
   • What specific elements support your thesis?

2. EVIDENCE GATHERING:
   • Direct quotes from the text
   • Specific examples of literary devices
   • Character actions and dialogue
   • Symbolic elements

3. ANALYSIS STRUCTURE:
   • Introduction with thesis statement
   • Body paragraphs with evidence and analysis
   • Conclusion that reinforces your argument

4. CRITICAL QUESTIONS:
   • What is the author's purpose?
   • How does the work reflect its historical period?
   • What universal themes does it explore?
   • How does it compare to other works?
   • What is its relevance today?

Use this space to develop your critical analysis..."""
        
        self.critical_text = scrolledtext.ScrolledText(self.critical_workspace, 
                                                      wrap=tk.WORD, font=('Arial', 11), 
                                                      bg='#fefefe')
        self.critical_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.critical_text.insert('1.0', default_text)
        
    def create_notes_tab(self, parent, work):
        """Create personal notes tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame, text="📝 My Analysis Notes", 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#14532d').pack(side='left')
        
        tk.Button(header_frame, text="💾 Save Notes", command=self.save_notes,
                 bg='#16a34a', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Notes area
        notes_frame = tk.Frame(parent, bg='#ffffff')
        notes_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, wrap=tk.WORD,
                                                   font=('Arial', 11), bg='#fefefe')
        self.notes_text.pack(fill='both', expand=True)
        
        # Load existing notes if any
        work_id = f"{work['title']}_{work['author']}"
        if work_id in self.student_analyses:
            self.notes_text.insert('1.0', self.student_analyses[work_id])
        else:
            starter_text = f"""📝 ANALYSIS NOTES FOR "{work['title']}"

Use this space to record your thoughts, observations, and analysis as you read.

💡 READING LOG:
• Date: 
• Pages/Chapters read:
• Key events:
• Important quotes:
• Questions that arise:

🎭 CHARACTER OBSERVATIONS:
• Character development:
• Relationships:
• Motivations:

🎨 THEMES & SYMBOLS:
• Recurring themes:
• Symbolic elements:
• Author's message:

🔧 LITERARY TECHNIQUES:
• Notable devices:
• Writing style:
• Structure:

💭 PERSONAL RESPONSE:
• What stood out to you?
• How did you feel while reading?
• What questions do you have?
• Connections to other works or experiences:"""
            
            self.notes_text.insert('1.0', starter_text)
        
    def show_critical_lens(self, lens_type):
        """Show specific critical lens analysis"""
        lens_content = self.critical_lenses.get(lens_type, {})
        
        analysis_text = f"""🔬 {lens_content.get('name', lens_type.upper())} ANALYSIS

📋 FOCUS QUESTIONS:
{lens_content.get('questions', 'No specific questions available')}

🔍 KEY CONCEPTS:
{lens_content.get('concepts', 'No specific concepts available')}

💡 APPLICATION TO THIS WORK:
Consider how this critical lens applies to "{self.current_work['title']}":

{lens_content.get('application', 'Apply the lens concepts to analyze this specific work')}

📝 YOUR ANALYSIS:
Write your analysis using this critical lens below..."""
        
        self.critical_text.delete('1.0', tk.END)
        self.critical_text.insert('1.0', analysis_text)
        
    def clear_workspace(self):
        """Clear the workspace frame"""
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
    def load_literary_works(self):
        """Load literary works database"""
        return [
            {
                "title": "Romeo and Juliet",
                "author": "William Shakespeare",
                "genre": "Drama",
                "period": "Renaissance", 
                "year": "1597",
                "description": "A tragic play about two young star-crossed lovers whose deaths ultimately unite their feuding families. Set in Verona, Italy, the play explores themes of love, fate, family conflict, and the destructive nature of hatred.",
                "themes": ["Love", "Fate", "Family", "Death", "Youth vs Age"],
                "characters": [
                    {"name": "Romeo", "role": "Male protagonist", "traits": ["passionate", "impulsive", "romantic"]},
                    {"name": "Juliet", "role": "Female protagonist", "traits": ["determined", "mature", "brave"]},
                    {"name": "Friar Lawrence", "role": "Mentor figure", "traits": ["wise", "well-meaning", "conflicted"]}
                ],
                "significance": "One of Shakespeare's most famous tragedies, exploring timeless themes of love and conflict."
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "genre": "Fiction",
                "period": "Modern",
                "year": "1960",
                "description": "Set in 1930s Alabama, the novel follows Scout Finch as she observes her father Atticus defend a black man falsely accused of rape. The story explores themes of racial injustice, moral growth, and loss of innocence.",
                "themes": ["Justice", "Prejudice", "Growing Up", "Morality", "Social Class"],
                "characters": [
                    {"name": "Scout Finch", "role": "Narrator/Protagonist", "traits": ["curious", "tomboyish", "developing morally"]},
                    {"name": "Atticus Finch", "role": "Moral center", "traits": ["principled", "courageous", "compassionate"]},
                    {"name": "Boo Radley", "role": "Mysterious neighbor", "traits": ["misunderstood", "gentle", "protective"]}
                ],
                "significance": "Pulitzer Prize winner addressing racial inequality and moral courage."
            },
            {
                "title": "The Great Gatsby", 
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "period": "Modern",
                "year": "1925",
                "description": "Set in 1922, the novel tells the story of Jay Gatsby's obsessive pursuit of Daisy Buchanan against the backdrop of the Jazz Age. It critiques the American Dream and explores themes of wealth, love, and moral decay.",
                "themes": ["American Dream", "Love", "Wealth", "Moral Decay", "Past vs Present"],
                "characters": [
                    {"name": "Jay Gatsby", "role": "Tragic hero", "traits": ["idealistic", "mysterious", "obsessed"]},
                    {"name": "Nick Carraway", "role": "Narrator", "traits": ["observant", "moral", "somewhat naive"]},
                    {"name": "Daisy Buchanan", "role": "Object of desire", "traits": ["beautiful", "shallow", "careless"]}
                ],
                "significance": "Masterpiece of American literature capturing the Jazz Age and critiquing the American Dream."
            }
        ]
        
    def load_analysis_frameworks(self):
        """Load analysis frameworks"""
        return {
            "character": {
                "questions": [
                    "How does this character change throughout the story?",
                    "What motivates this character's actions?",
                    "How do other characters relate to this character?",
                    "What does this character represent symbolically?"
                ]
            },
            "theme": {
                "questions": [
                    "What is the central message of this work?", 
                    "How do different elements support this theme?",
                    "How does this theme relate to universal human experiences?",
                    "What is the author's purpose in exploring this theme?"
                ]
            }
        }
        
    def load_critical_lenses(self):
        """Load critical analysis lenses"""
        return {
            "feminist": {
                "name": "Feminist Criticism",
                "questions": """• How are women portrayed in this work?
• What power relationships exist between male and female characters?
• How does gender affect character opportunities and choices?
• Does the work challenge or reinforce gender stereotypes?
• What roles do women play in the narrative structure?""",
                "concepts": """• Gender roles and expectations
• Power dynamics between sexes
• Female agency and voice
• Patriarchal structures
• Intersectionality (race, class, gender)""",
                "application": "Examine how gender influences character development, plot events, and thematic content."
            },
            "historical": {
                "name": "Historical Criticism", 
                "questions": """• What historical period does this work reflect?
• How do historical events influence the story?
• What social conditions are depicted?
• How does the work reflect the values of its time?
• What historical context is necessary to understand this work?""",
                "concepts": """• Historical context and period
• Social and political conditions
• Cultural values and beliefs
• Economic systems
• Technological influences""",
                "application": "Consider how historical context shapes the work's meaning and relevance."
            },
            "psychological": {
                "name": "Psychological Criticism",
                "questions": """• What psychological motivations drive the characters?
• How do unconscious desires affect behavior?
• What psychological conflicts exist?
• How do characters cope with trauma or stress?
• What psychological themes emerge?""",
                "concepts": """• Conscious and unconscious mind
• Defense mechanisms
• Psychological trauma
• Human development stages
• Mental health and illness""",
                "application": "Analyze characters' psychological depth and the work's exploration of human psychology."
            },
            "formalist": {
                "name": "Formalist Criticism",
                "questions": """• How do literary elements work together?
• What patterns exist in language and structure?
• How does form contribute to meaning?
• What techniques create specific effects?
• How do all elements unite to create the whole?""",
                "concepts": """• Literary elements and techniques
• Structure and form
• Language patterns
• Symbolism and imagery
• Unity and coherence""",
                "application": "Focus on how the work's formal elements create meaning and artistic effect."
            }
        }
        
    # Placeholder methods for additional features
    def random_literature(self):
        work = random.choice(self.literary_works)
        self.start_analysis(work)
        
    def upload_literature(self):
        messagebox.showinfo("Upload Literature", "File upload feature would be available here.")
        
    def show_reading_list(self):
        messagebox.showinfo("Reading List", "Personal reading list would be displayed here.")
        
    def filter_literature(self, event=None):
        self.display_literature_grid()
        
    def read_work(self, work):
        messagebox.showinfo("Read Work", f"Full text of '{work['title']}' would be available here.")
        
    def character_analysis(self):
        if self.current_work:
            messagebox.showinfo("Character Analysis", "Advanced character analysis tools would open here.")
        else:
            messagebox.showinfo("Character Analysis", "Please select a work to analyze first.")
            
    def plot_analysis(self):
        messagebox.showinfo("Plot Analysis", "Plot structure analysis tools would open here.")
        
    def theme_analysis(self):
        messagebox.showinfo("Theme Analysis", "Thematic analysis tools would open here.")
        
    def close_reading(self):
        messagebox.showinfo("Close Reading", "Close reading analysis tools would open here.")
        
    def historical_context(self):
        messagebox.showinfo("Historical Context", "Historical context resources would open here.")
        
    def apply_critical_lens(self, lens_type):
        if self.current_work:
            self.show_critical_lens(lens_type)
        else:
            messagebox.showinfo("Critical Lens", f"Please select a work to apply {lens_type} criticism.")
            
    def write_analysis_essay(self):
        messagebox.showinfo("Analysis Essay", "Essay writing interface would open here.")
        
    def write_discussion(self):
        messagebox.showinfo("Discussion Posts", "Discussion writing interface would open here.")
        
    def create_comparison(self):
        messagebox.showinfo("Comparison Chart", "Comparison chart creator would open here.")
        
    def save_notes(self):
        if self.current_work and hasattr(self, 'notes_text'):
            work_id = f"{self.current_work['title']}_{self.current_work['author']}"
            content = self.notes_text.get('1.0', tk.END + '-1c')
            self.student_analyses[work_id] = content
            messagebox.showinfo("Notes Saved", "Your analysis notes have been saved!")

def main():
    root = tk.Tk()
    app = LiteraryAnalysisWorkshop(root)
    root.mainloop()

if __name__ == "__main__":
    main()