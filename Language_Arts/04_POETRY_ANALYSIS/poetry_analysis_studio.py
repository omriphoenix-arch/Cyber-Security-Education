#!/usr/bin/env python3
"""
Language Arts - Poetry Analysis Studio
An interactive platform for exploring and analyzing poetry
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
from datetime import datetime
import re

class PoetryAnalysisStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Poetry Analysis Studio - Language Arts Education")
        self.root.geometry("1400x900")
        self.root.configure(bg='#faf5ff')
        
        # Data storage
        self.poem_database = self.load_poem_database()
        self.literary_devices = self.load_literary_devices()
        self.current_poem = None
        self.analysis_notes = {}
        self.student_annotations = {}
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#faf5ff')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="🎭 Poetry Analysis Studio", 
                              font=('Arial', 24, 'bold'), bg='#faf5ff', fg='#581c87')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Discover the beauty and meaning in poetry", 
                                 font=('Arial', 12), bg='#faf5ff', fg='#7c3aed')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#faf5ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Tools and Navigation
        left_frame = tk.Frame(main_frame, bg='#e9d5ff', relief='raised', bd=2, width=300)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        nav_label = tk.Label(left_frame, text="Poetry Toolkit", font=('Arial', 14, 'bold'),
                            bg='#e9d5ff', fg='#581c87')
        nav_label.pack(pady=15)
        
        # Poetry Library section
        library_frame = tk.LabelFrame(left_frame, text="📚 Poetry Library", 
                                     font=('Arial', 12, 'bold'), bg='#e9d5ff')
        library_frame.pack(fill='x', padx=10, pady=5)
        
        library_buttons = [
            ("📖 Browse Poems", self.browse_poems),
            ("🎲 Random Poem", self.random_poem),
            ("📁 Upload Poem", self.upload_poem),
            ("⭐ Favorites", self.show_favorites)
        ]
        
        for text, command in library_buttons:
            btn = tk.Button(library_frame, text=text, command=command,
                          font=('Arial', 10), width=26, pady=3,
                          bg='#7c3aed', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Analysis Tools section
        analysis_frame = tk.LabelFrame(left_frame, text="🔍 Analysis Tools", 
                                      font=('Arial', 12, 'bold'), bg='#e9d5ff')
        analysis_frame.pack(fill='x', padx=10, pady=5)
        
        analysis_buttons = [
            ("🎨 Literary Devices", self.show_literary_devices),
            ("📊 Structure Analysis", self.analyze_structure),
            ("🎵 Sound & Rhythm", self.analyze_sound),
            ("🖼️ Imagery Explorer", self.explore_imagery),
            ("💭 Theme Tracker", self.track_themes)
        ]
        
        for text, command in analysis_buttons:
            btn = tk.Button(analysis_frame, text=text, command=command,
                          font=('Arial', 10), width=26, pady=3,
                          bg='#c026d3', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
            
        # Creative Tools section
        creative_frame = tk.LabelFrame(left_frame, text="✍️ Creative Tools", 
                                      font=('Arial', 12, 'bold'), bg='#e9d5ff')
        creative_frame.pack(fill='x', padx=10, pady=5)
        
        creative_buttons = [
            ("📝 Write Poetry", self.write_poetry),
            ("🎯 Poetry Prompts", self.poetry_prompts),
            ("🎪 Poetry Games", self.poetry_games)
        ]
        
        for text, command in creative_buttons:
            btn = tk.Button(creative_frame, text=text, command=command,
                          font=('Arial', 10), width=26, pady=3,
                          bg='#059669', fg='white', relief='flat')
            btn.pack(pady=2, padx=5)
        
        # Quick Reference
        reference_frame = tk.LabelFrame(left_frame, text="📋 Quick Reference", 
                                       font=('Arial', 11, 'bold'), bg='#e9d5ff')
        reference_frame.pack(fill='x', padx=10, pady=10)
        
        reference_text = """🎭 Poetry Forms:
• Sonnet (14 lines)
• Haiku (3 lines, 5-7-5)
• Free Verse (no rules)
• Limerick (5 lines, AABBA)

🎨 Literary Devices:
• Metaphor: comparison
• Simile: like/as comparison  
• Alliteration: same sounds
• Personification: human traits"""
        
        tk.Label(reference_frame, text=reference_text, font=('Arial', 8),
                bg='#e9d5ff', fg='#374151', justify='left').pack(padx=10, pady=10)
        
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
        tk.Label(welcome_frame, text="Welcome to Poetry Analysis Studio!", 
                font=('Arial', 22, 'bold'), bg='#ffffff', fg='#581c87').pack(pady=20)
        
        tk.Label(welcome_frame, text="Explore the art and craft of poetry through interactive analysis", 
                font=('Arial', 14), bg='#ffffff', fg='#7c3aed').pack(pady=10)
        
        # Featured poem of the day
        featured_frame = tk.LabelFrame(welcome_frame, text="🌟 Featured Poem", 
                                      font=('Arial', 14, 'bold'), bg='#ffffff')
        featured_frame.pack(fill='x', pady=30)
        
        featured_poem = random.choice(self.poem_database)
        
        # Poem title and author
        tk.Label(featured_frame, text=f'"{featured_poem["title"]}"', 
                font=('Arial', 16, 'bold'), bg='#ffffff', fg='#581c87').pack(pady=10)
        
        tk.Label(featured_frame, text=f"by {featured_poem['author']}", 
                font=('Arial', 12, 'italic'), bg='#ffffff', fg='#7c3aed').pack()
        
        # First few lines
        lines = featured_poem['text'].split('\n')[:4]
        poem_preview = '\n'.join(lines) + '\n...'
        
        tk.Label(featured_frame, text=poem_preview, font=('Georgia', 11),
                bg='#ffffff', fg='#374151', justify='center').pack(pady=15)
        
        tk.Button(featured_frame, text="📖 Read Full Poem", 
                 command=lambda: self.display_poem(featured_poem),
                 bg='#7c3aed', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Quick start options
        quickstart_frame = tk.LabelFrame(welcome_frame, text="Quick Start", 
                                        font=('Arial', 14, 'bold'), bg='#ffffff')
        quickstart_frame.pack(fill='x', pady=20)
        
        quick_options = [
            ("🎲 Surprise Me", "Discover a random poem", self.random_poem, '#c026d3'),
            ("📚 Browse Library", "Explore our poetry collection", self.browse_poems, '#7c3aed'),
            ("🎨 Learn Devices", "Study literary techniques", self.show_literary_devices, '#059669'),
            ("✍️ Write Poetry", "Create your own poems", self.write_poetry, '#dc2626')
        ]
        
        for i, (title, desc, command, color) in enumerate(quick_options):
            row = i // 2
            col = i % 2
            
            option_frame = tk.Frame(quickstart_frame, bg='#ffffff', relief='raised', bd=1)
            option_frame.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
            
            tk.Label(option_frame, text=title, font=('Arial', 12, 'bold'),
                    bg='#ffffff', fg=color).pack(pady=10)
            
            tk.Label(option_frame, text=desc, font=('Arial', 10),
                    bg='#ffffff', fg='#6b7280', wraplength=200).pack(pady=5)
            
            tk.Button(option_frame, text="Start", command=command,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     relief='flat', pady=5).pack(pady=10)
        
        for i in range(2):
            quickstart_frame.grid_columnconfigure(i, weight=1)
        
    def browse_poems(self):
        """Show poem browsing interface"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="📚 Poetry Library", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#581c87').pack(side='left')
        
        # Search and filter
        search_frame = tk.Frame(header_frame, bg='#ffffff')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10),
                bg='#ffffff').pack(side='left')
        
        search_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="🔍", command=lambda: self.search_poems(search_entry.get()),
                 bg='#7c3aed', fg='white', font=('Arial', 10)).pack(side='left', padx=2)
        
        # Filter options
        filter_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Era filter
        tk.Label(filter_frame, text="Era:", font=('Arial', 10, 'bold'),
                bg='#ffffff').pack(side='left')
        
        self.era_var = tk.StringVar(value="All")
        era_combo = ttk.Combobox(filter_frame, textvariable=self.era_var,
                                values=["All", "Classical", "Romantic", "Modern", "Contemporary"],
                                state="readonly", width=12)
        era_combo.pack(side='left', padx=5)
        era_combo.bind("<<ComboboxSelected>>", self.filter_poems)
        
        # Theme filter
        tk.Label(filter_frame, text="Theme:", font=('Arial', 10, 'bold'),
                bg='#ffffff').pack(side='left', padx=(20, 0))
        
        self.theme_var = tk.StringVar(value="All")
        theme_combo = ttk.Combobox(filter_frame, textvariable=self.theme_var,
                                  values=["All", "Nature", "Love", "Life", "Death", "Freedom"],
                                  state="readonly", width=12)
        theme_combo.pack(side='left', padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.filter_poems)
        
        # Poems display area
        self.poems_display_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        self.poems_display_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.display_poems_grid()
        
    def display_poems_grid(self):
        """Display poems in a grid layout"""
        for widget in self.poems_display_frame.winfo_children():
            widget.destroy()
        
        # Filter poems
        era = self.era_var.get()
        theme = self.theme_var.get()
        
        filtered_poems = self.poem_database
        if era != "All":
            filtered_poems = [p for p in filtered_poems if p.get('era') == era]
        if theme != "All":
            filtered_poems = [p for p in filtered_poems if theme.lower() in p.get('themes', [])]
        
        # Create scrollable frame
        canvas = tk.Canvas(self.poems_display_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.poems_display_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display poems in grid
        for i, poem in enumerate(filtered_poems):
            row = i // 3
            col = i % 3
            
            poem_frame = tk.LabelFrame(scrollable_frame, text=f'"{poem["title"]}"',
                                      font=('Arial', 11, 'bold'), bg='#ffffff')
            poem_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Author
            tk.Label(poem_frame, text=f"by {poem['author']}", 
                    font=('Arial', 10, 'italic'), bg='#ffffff', fg='#7c3aed').pack(pady=5)
            
            # Era and themes
            info_text = f"Era: {poem.get('era', 'Unknown')}\nThemes: {', '.join(poem.get('themes', []))}"
            tk.Label(poem_frame, text=info_text, font=('Arial', 9),
                    bg='#ffffff', fg='#6b7280').pack(pady=5)
            
            # Preview
            lines = poem['text'].split('\n')[:2]
            preview = '\n'.join(lines) + '...'
            tk.Label(poem_frame, text=preview, font=('Georgia', 9),
                    bg='#ffffff', fg='#374151', wraplength=180,
                    justify='center').pack(pady=10)
            
            # Buttons
            btn_frame = tk.Frame(poem_frame, bg='#ffffff')
            btn_frame.pack(fill='x', padx=10, pady=10)
            
            tk.Button(btn_frame, text="📖 Read", 
                     command=lambda p=poem: self.display_poem(p),
                     bg='#7c3aed', fg='white', font=('Arial', 9)).pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="🔍 Analyze", 
                     command=lambda p=poem: self.analyze_poem(p),
                     bg='#c026d3', fg='white', font=('Arial', 9)).pack(side='right', padx=2)
        
        for i in range(3):
            scrollable_frame.grid_columnconfigure(i, weight=1)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def display_poem(self, poem):
        """Display a poem for reading"""
        self.current_poem = poem
        self.clear_workspace()
        
        # Header with poem info
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        # Left side - poem info
        info_frame = tk.Frame(header_frame, bg='#ffffff')
        info_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(info_frame, text=f'"{poem["title"]}"', 
                font=('Arial', 18, 'bold'), bg='#ffffff', fg='#581c87').pack(anchor='w')
        
        tk.Label(info_frame, text=f"by {poem['author']}", 
                font=('Arial', 12, 'italic'), bg='#ffffff', fg='#7c3aed').pack(anchor='w')
        
        # Right side - action buttons
        action_frame = tk.Frame(header_frame, bg='#ffffff')
        action_frame.pack(side='right')
        
        tk.Button(action_frame, text="🔍 Analyze", command=lambda: self.analyze_poem(poem),
                 bg='#c026d3', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="📝 Annotate", command=self.toggle_annotation_mode,
                 bg='#059669', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="⭐ Favorite", command=lambda: self.add_to_favorites(poem),
                 bg='#f59e0b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        # Poem display area
        poem_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        poem_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create text widget for poem
        self.poem_text = scrolledtext.ScrolledText(poem_frame, wrap=tk.WORD,
                                                  font=('Georgia', 14), bg='#fefefe',
                                                  fg='#374151', relief='flat', bd=20)
        self.poem_text.pack(fill='both', expand=True)
        
        # Insert poem text
        self.poem_text.insert('1.0', poem['text'])
        
        # Make it read-only initially
        self.poem_text.configure(state='disabled')
        
        # Add poem metadata panel
        metadata_frame = tk.LabelFrame(self.workspace_frame, text="About This Poem",
                                      font=('Arial', 11, 'bold'), bg='#ffffff')
        metadata_frame.pack(fill='x', padx=20, pady=10)
        
        metadata_text = f"""Era: {poem.get('era', 'Unknown')} | 
Themes: {', '.join(poem.get('themes', ['None listed']))} | 
Form: {poem.get('form', 'Free verse')} | 
Published: {poem.get('year', 'Unknown')}"""
        
        tk.Label(metadata_frame, text=metadata_text, font=('Arial', 10),
                bg='#ffffff', fg='#6b7280').pack(padx=15, pady=10)
        
    def analyze_poem(self, poem):
        """Start detailed analysis of a poem"""
        self.current_poem = poem
        self.clear_workspace()
        
        # Create analysis interface with tabs
        notebook = ttk.Notebook(self.workspace_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Structure Analysis
        structure_frame = ttk.Frame(notebook)
        notebook.add(structure_frame, text="📊 Structure")
        self.create_structure_analysis_tab(structure_frame, poem)
        
        # Tab 2: Literary Devices
        devices_frame = ttk.Frame(notebook)
        notebook.add(devices_frame, text="🎨 Literary Devices")
        self.create_devices_analysis_tab(devices_frame, poem)
        
        # Tab 3: Sound & Rhythm
        sound_frame = ttk.Frame(notebook)
        notebook.add(sound_frame, text="🎵 Sound & Rhythm")
        self.create_sound_analysis_tab(sound_frame, poem)
        
        # Tab 4: Themes & Meaning
        theme_frame = ttk.Frame(notebook)
        notebook.add(theme_frame, text="💭 Themes & Meaning")
        self.create_theme_analysis_tab(theme_frame, poem)
        
    def create_structure_analysis_tab(self, parent, poem):
        """Create structure analysis tab"""
        # Poem info header
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(header_frame, text=f'Analyzing: "{poem["title"]}" by {poem["author"]}', 
                font=('Arial', 14, 'bold'), bg='#ffffff', fg='#581c87').pack()
        
        # Analysis content
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - poem text
        poem_frame = tk.LabelFrame(content_frame, text="Poem Text", 
                                  font=('Arial', 11, 'bold'), bg='#ffffff')
        poem_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        poem_display = scrolledtext.ScrolledText(poem_frame, wrap=tk.WORD,
                                                font=('Georgia', 11), height=20,
                                                bg='#fefefe', state='disabled')
        poem_display.pack(fill='both', expand=True, padx=10, pady=10)
        poem_display.configure(state='normal')
        poem_display.insert('1.0', poem['text'])
        poem_display.configure(state='disabled')
        
        # Right side - analysis
        analysis_frame = tk.LabelFrame(content_frame, text="Structure Analysis", 
                                      font=('Arial', 11, 'bold'), bg='#ffffff', width=300)
        analysis_frame.pack(side='right', fill='y')
        analysis_frame.pack_propagate(False)
        
        # Analyze structure
        lines = poem['text'].split('\n')
        stanzas = [s for s in poem['text'].split('\n\n') if s.strip()]
        words = poem['text'].split()
        
        analysis_text = f"""📏 POEM STRUCTURE

📖 Basic Counts:
• Lines: {len(lines)}
• Stanzas: {len(stanzas)}
• Words: {len(words)}
• Characters: {len(poem['text'])}

📐 Line Analysis:
• Average words per line: {len(words) // max(1, len(lines))}
• Shortest line: {min([len(line.split()) for line in lines if line.strip()], default=0)} words
• Longest line: {max([len(line.split()) for line in lines if line.strip()], default=0)} words

📋 Stanza Pattern:
• Number of stanzas: {len(stanzas)}
• Lines per stanza: {[len(s.split('\\n')) for s in stanzas]}

🎭 Poem Form:
{poem.get('form', 'Free verse - no regular pattern')}

💡 Structural Notes:
{self.get_structural_notes(poem)}"""
        
        tk.Label(analysis_frame, text=analysis_text, font=('Arial', 9),
                bg='#ffffff', fg='#374151', justify='left').pack(padx=10, pady=10, anchor='nw')
        
    def create_devices_analysis_tab(self, parent, poem):
        """Create literary devices analysis tab"""
        # Split into left (poem) and right (devices)
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - poem with highlighting
        poem_frame = tk.LabelFrame(content_frame, text="Poem Text (Click to highlight devices)", 
                                  font=('Arial', 11, 'bold'), bg='#ffffff')
        poem_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.devices_poem_text = scrolledtext.ScrolledText(poem_frame, wrap=tk.WORD,
                                                          font=('Georgia', 11), height=25,
                                                          bg='#fefefe')
        self.devices_poem_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.devices_poem_text.insert('1.0', poem['text'])
        
        # Right side - devices panel
        devices_frame = tk.LabelFrame(content_frame, text="Literary Devices Found", 
                                     font=('Arial', 11, 'bold'), bg='#ffffff', width=350)
        devices_frame.pack(side='right', fill='y')
        devices_frame.pack_propagate(False)
        
        # Detect literary devices (simplified)
        detected_devices = self.detect_literary_devices(poem['text'])
        
        devices_display = scrolledtext.ScrolledText(devices_frame, wrap=tk.WORD,
                                                   font=('Arial', 10), bg='#fefefe')
        devices_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        devices_text = "🎨 LITERARY DEVICES DETECTED:\n\n"
        for device, examples in detected_devices.items():
            devices_text += f"📍 {device.upper()}:\n"
            for example in examples[:3]:  # Show first 3 examples
                devices_text += f"  • {example}\n"
            devices_text += "\n"
        
        devices_display.insert('1.0', devices_text)
        devices_display.configure(state='disabled')
        
    def create_sound_analysis_tab(self, parent, poem):
        """Create sound and rhythm analysis tab"""
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sound analysis
        sound_analysis = self.analyze_sound_patterns(poem['text'])
        
        sound_text = f"""🎵 SOUND & RHYTHM ANALYSIS

🔤 ALLITERATION:
{sound_analysis['alliteration']}

🎶 RHYME SCHEME:
{sound_analysis['rhyme_scheme']}

⚡ RHYTHM PATTERNS:
{sound_analysis['rhythm']}

🎭 ASSONANCE & CONSONANCE:
{sound_analysis['vowel_consonant']}

📏 METER ANALYSIS:
{sound_analysis['meter']}"""
        
        sound_display = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD,
                                                 font=('Arial', 11), bg='#fefefe')
        sound_display.pack(fill='both', expand=True)
        sound_display.insert('1.0', sound_text)
        sound_display.configure(state='disabled')
        
    def create_theme_analysis_tab(self, parent, poem):
        """Create theme and meaning analysis tab"""
        content_frame = tk.Frame(parent, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Theme analysis
        theme_analysis = self.analyze_themes(poem)
        
        theme_text = f"""💭 THEMES & MEANING ANALYSIS

🎯 PRIMARY THEMES:
{theme_analysis['primary_themes']}

🖼️ IMAGERY PATTERNS:
{theme_analysis['imagery']}

💡 SYMBOLISM:
{theme_analysis['symbolism']}

🎭 MOOD & TONE:
{theme_analysis['mood_tone']}

📖 INTERPRETATION GUIDE:
{theme_analysis['interpretation']}

❓ DISCUSSION QUESTIONS:
{theme_analysis['questions']}"""
        
        theme_display = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD,
                                                 font=('Arial', 11), bg='#fefefe')
        theme_display.pack(fill='both', expand=True)
        theme_display.insert('1.0', theme_text)
        theme_display.configure(state='disabled')
        
    def show_literary_devices(self):
        """Show literary devices reference"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="🎨 Literary Devices Reference", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#581c87').pack()
        
        # Devices display
        devices_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        devices_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create scrollable text
        devices_text = scrolledtext.ScrolledText(devices_frame, wrap=tk.WORD,
                                                font=('Arial', 11), bg='#fefefe')
        devices_text.pack(fill='both', expand=True)
        
        # Literary devices content
        devices_content = """🎨 LITERARY DEVICES IN POETRY

📍 SOUND DEVICES:
• Alliteration: Repetition of beginning sounds ("wild and windy")
• Assonance: Repetition of vowel sounds ("hear the mellow wedding bells")
• Consonance: Repetition of consonant sounds ("pitter patter")
• Rhyme: Matching ending sounds ("cat" and "hat")
• Onomatopoeia: Words that sound like what they describe ("buzz", "crash")

🖼️ IMAGERY DEVICES:
• Metaphor: Direct comparison ("Life is a journey")
• Simile: Comparison using "like" or "as" ("brave as a lion")
• Personification: Giving human qualities to non-human things ("the wind whispered")
• Hyperbole: Extreme exaggeration ("I've told you a million times")
• Symbolism: Objects representing deeper meanings (dove = peace)

📐 STRUCTURAL DEVICES:
• Repetition: Repeating words or phrases for emphasis
• Parallelism: Similar grammatical structures
• Juxtaposition: Placing contrasting elements side by side
• Enjambment: Lines that continue without pause to the next line
• Caesura: A pause or break in the middle of a line

💭 MEANING DEVICES:
• Irony: Saying one thing but meaning another
• Paradox: A seemingly contradictory statement that reveals truth
• Oxymoron: Contradictory terms together ("deafening silence")
• Synecdoche: Part representing the whole ("all hands on deck")
• Metonymy: Related term substituting for the actual thing ("the crown" for royalty)

🎭 MOOD & TONE DEVICES:
• Diction: Word choice that creates mood
• Connotation: Implied meanings of words
• Allusion: Reference to other works or historical events
• Allegory: Extended metaphor throughout the entire work"""

        devices_text.insert('1.0', devices_content)
        devices_text.configure(state='disabled')
        
    def write_poetry(self):
        """Show poetry writing interface"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_frame, text="✍️ Poetry Writing Studio", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#581c87').pack(side='left')
        
        tk.Button(header_frame, text="💾 Save Poem", command=self.save_poem,
                 bg='#059669', fg='white', font=('Arial', 10)).pack(side='right', padx=5)
        
        tk.Button(header_frame, text="🎯 Get Prompt", command=self.get_writing_prompt,
                 bg='#f59e0b', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Writing area
        writing_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        writing_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - writing area
        editor_frame = tk.LabelFrame(writing_frame, text="Your Poem", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
        editor_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Title input
        title_frame = tk.Frame(editor_frame, bg='#ffffff')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(title_frame, text="Title:", font=('Arial', 10, 'bold'),
                bg='#ffffff').pack(side='left')
        
        self.poem_title_entry = tk.Entry(title_frame, font=('Arial', 11))
        self.poem_title_entry.pack(side='left', fill='x', expand=True, padx=10)
        
        # Text area
        self.poetry_editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD,
                                                      font=('Georgia', 12), bg='#fefefe',
                                                      height=25)
        self.poetry_editor.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right side - writing tools
        tools_frame = tk.LabelFrame(writing_frame, text="Writing Tools", 
                                   font=('Arial', 12, 'bold'), bg='#ffffff', width=300)
        tools_frame.pack(side='right', fill='y')
        tools_frame.pack_propagate(False)
        
        # Poetry forms
        forms_frame = tk.LabelFrame(tools_frame, text="Poetry Forms", 
                                   font=('Arial', 10, 'bold'), bg='#ffffff')
        forms_frame.pack(fill='x', padx=10, pady=5)
        
        forms = ["Free Verse", "Haiku", "Sonnet", "Limerick", "Acrostic"]
        for form in forms:
            tk.Button(forms_frame, text=form, 
                     command=lambda f=form: self.load_poetry_form(f),
                     bg='#7c3aed', fg='white', font=('Arial', 9),
                     width=15).pack(pady=2)
        
        # Writing tips
        tips_frame = tk.LabelFrame(tools_frame, text="Writing Tips", 
                                  font=('Arial', 10, 'bold'), bg='#ffffff')
        tips_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tips_text = """💡 POETRY WRITING TIPS:

• Start with a strong image
• Use concrete, specific words
• Show, don't tell
• Read your poem aloud
• Play with line breaks
• Use metaphors and similes
• Create a mood with word choice
• End with impact

🎨 Try These Techniques:
• Alliteration for sound
• Repetition for emphasis  
• Enjambment for flow
• Imagery for pictures
• Rhythm for music"""
        
        tk.Label(tips_frame, text=tips_text, font=('Arial', 8),
                bg='#ffffff', fg='#374151', justify='left').pack(padx=10, pady=10, anchor='nw')
        
    def clear_workspace(self):
        """Clear the workspace frame"""
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
    def load_poem_database(self):
        """Load the poem database"""
        return [
            {
                "title": "The Road Not Taken",
                "author": "Robert Frost",
                "era": "Modern",
                "year": "1916",
                "form": "Narrative poem",
                "themes": ["choice", "life", "regret"],
                "text": """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever be back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""
            },
            {
                "title": "Hope is the thing with feathers",
                "author": "Emily Dickinson", 
                "era": "Romantic",
                "year": "1861",
                "form": "Lyric poem",
                "themes": ["hope", "nature", "perseverance"],
                "text": """Hope is the thing with feathers
That perches in the soul,
And sings the tune without the words,
And never stops at all,

And sweetest in the gale is heard;
And sore must be the storm
That could abash the little bird
That kept so many warm.

I've heard it in the chilliest land,
And on the strangest sea;
Yet, never, in extremity,
It asked a crumb of me."""
            },
            {
                "title": "Stopping by Woods on a Snowy Evening",
                "author": "Robert Frost",
                "era": "Modern", 
                "year": "1922",
                "form": "Lyric poem",
                "themes": ["nature", "duty", "beauty"],
                "text": """Whose woods these are I think I know.   
His house is in the village though;   
He will not see me stopping here   
To watch his woods fill up with snow.   

My little horse must think it queer   
To stop without a farmhouse near   
Between the woods and frozen lake   
The darkest evening of the year.   

He gives his harness bells a shake   
To ask if there is some mistake.   
The only other sound's the sweep   
Of easy wind and downy flake.   

The woods are lovely, dark and deep,   
But I have promises to keep,   
And miles to go before I sleep,   
And miles to go before I sleep."""
            }
        ]
        
    def load_literary_devices(self):
        """Load literary devices database"""
        return {
            "metaphor": "A direct comparison between two unlike things",
            "simile": "A comparison using 'like' or 'as'",
            "alliteration": "Repetition of beginning consonant sounds",
            "personification": "Giving human characteristics to non-human things",
            "symbolism": "Using objects to represent deeper meanings",
            "imagery": "Vivid descriptive language that appeals to the senses",
            "repetition": "Repeating words or phrases for emphasis",
            "rhyme": "Matching sounds at the end of lines",
            "rhythm": "The beat or pattern of stressed and unstressed syllables"
        }
        
    def get_structural_notes(self, poem):
        """Generate structural analysis notes"""
        lines = poem['text'].split('\n')
        
        if len(lines) == 14:
            return "This appears to be a sonnet (14 lines)"
        elif len(lines) == 3:
            return "This could be a haiku (3 lines)"
        elif len(lines) == 5:
            return "This might be a limerick (5 lines)"
        else:
            return "Free verse structure with varied line lengths"
            
    def detect_literary_devices(self, text):
        """Detect literary devices in poem text (simplified)"""
        devices = {}
        
        # Simple alliteration detection
        words = text.lower().split()
        alliterations = []
        for i in range(len(words) - 1):
            if words[i] and words[i+1] and words[i][0] == words[i+1][0]:
                alliterations.append(f"{words[i]} {words[i+1]}")
        
        if alliterations:
            devices["Alliteration"] = alliterations[:3]
        
        # Simple repetition detection
        word_counts = {}
        for word in words:
            if len(word) > 3:  # Only count longer words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        repetitions = [word for word, count in word_counts.items() if count > 1]
        if repetitions:
            devices["Repetition"] = repetitions[:3]
        
        # Look for similes
        if " like " in text.lower() or " as " in text.lower():
            devices["Simile"] = ["Look for comparisons using 'like' or 'as'"]
        
        # Look for metaphors (very basic)
        if " is " in text.lower():
            devices["Metaphor"] = ["Look for direct comparisons using 'is'"]
            
        return devices
        
    def analyze_sound_patterns(self, text):
        """Analyze sound patterns in poem"""
        lines = text.split('\n')
        
        # Basic rhyme scheme detection
        last_words = [line.split()[-1].lower() if line.split() else '' for line in lines]
        rhyme_scheme = "Analyze ending sounds: " + ", ".join(last_words[:4])
        
        # Simple alliteration analysis
        alliteration = "Look for repeated beginning sounds in nearby words"
        
        return {
            "alliteration": alliteration,
            "rhyme_scheme": rhyme_scheme,
            "rhythm": "Count stressed and unstressed syllables for rhythm patterns",
            "vowel_consonant": "Listen for repeated vowel or consonant sounds within lines",
            "meter": "Pattern of stressed/unstressed syllables creates the poem's beat"
        }
        
    def analyze_themes(self, poem):
        """Analyze themes and meaning"""
        return {
            "primary_themes": f"Listed themes: {', '.join(poem.get('themes', ['None listed']))}",
            "imagery": "Look for sensory details that create mental pictures",
            "symbolism": "Consider what objects or images might represent deeper ideas",
            "mood_tone": "Notice the emotional feeling and author's attitude",
            "interpretation": "What message or insight does the poet want to share?",
            "questions": "• What is the central message?\n• How do literary devices support the theme?\n• What emotions does this evoke?"
        }
        
    # Placeholder methods for additional features
    def random_poem(self):
        poem = random.choice(self.poem_database)
        self.display_poem(poem)
        
    def upload_poem(self):
        messagebox.showinfo("Upload Poem", "File upload feature would be available here.")
        
    def show_favorites(self):
        messagebox.showinfo("Favorites", "Your favorite poems would be displayed here.")
        
    def search_poems(self, query):
        messagebox.showinfo("Search", f"Searching for: {query}")
        
    def filter_poems(self, event=None):
        self.display_poems_grid()
        
    def toggle_annotation_mode(self):
        messagebox.showinfo("Annotation", "Annotation mode would be enabled here.")
        
    def add_to_favorites(self, poem):
        messagebox.showinfo("Favorites", f"'{poem['title']}' added to favorites!")
        
    def analyze_structure(self):
        messagebox.showinfo("Structure Analysis", "Structure analysis tools would open here.")
        
    def analyze_sound(self):
        messagebox.showinfo("Sound Analysis", "Sound and rhythm analysis would open here.")
        
    def explore_imagery(self):
        messagebox.showinfo("Imagery Explorer", "Imagery analysis tools would open here.")
        
    def track_themes(self):
        messagebox.showinfo("Theme Tracker", "Theme tracking tools would open here.")
        
    def poetry_prompts(self):
        prompts = [
            "Write about a moment of change in nature",
            "Describe a color without naming it", 
            "Write a poem from an object's perspective",
            "Capture a childhood memory in verse",
            "Write about the sound of silence"
        ]
        prompt = random.choice(prompts)
        messagebox.showinfo("Poetry Prompt", f"Writing prompt:\n\n{prompt}")
        
    def poetry_games(self):
        messagebox.showinfo("Poetry Games", "Interactive poetry games would be available here.")
        
    def save_poem(self):
        if hasattr(self, 'poetry_editor'):
            title = self.poem_title_entry.get() or "Untitled Poem"
            content = self.poetry_editor.get('1.0', tk.END + '-1c')
            messagebox.showinfo("Poem Saved", f"'{title}' has been saved!")
        
    def get_writing_prompt(self):
        self.poetry_prompts()
        
    def load_poetry_form(self, form):
        if not hasattr(self, 'poetry_editor'):
            return
            
        templates = {
            "Haiku": "Line 1 (5 syllables)\nLine 2 (7 syllables)\nLine 3 (5 syllables)",
            "Sonnet": "14 lines, typically about love or beauty\nUsually follows ABAB CDCD EFEF GG rhyme scheme",
            "Limerick": "5 lines with AABBA rhyme scheme\nTypically humorous",
            "Acrostic": "Each line begins with letters spelling a word vertically",
            "Free Verse": "No specific rules - let your creativity flow!"
        }
        
        template = templates.get(form, "Write freely in this form")
        self.poetry_editor.delete('1.0', tk.END)
        self.poetry_editor.insert('1.0', f"Writing a {form}:\n{template}\n\n")

def main():
    root = tk.Tk()
    app = PoetryAnalysisStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()