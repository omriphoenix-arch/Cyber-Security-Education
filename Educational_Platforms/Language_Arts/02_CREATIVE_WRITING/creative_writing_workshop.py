#!/usr/bin/env python3
"""
Language Arts - Creative Writing Workshop
An interactive platform for developing writing skills and creativity
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
from datetime import datetime
import os

class CreativeWritingWorkshop:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative Writing Workshop - Language Arts Education")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')
        
        # Data storage
        self.writing_projects = {}
        self.current_project = None
        self.writing_prompts = self.load_writing_prompts()
        self.writing_tips = self.load_writing_tips()
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f8f9fa')
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="✍️ Creative Writing Workshop", 
                              font=('Arial', 24, 'bold'), bg='#f8f9fa', fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Express your creativity through the power of words", 
                                 font=('Arial', 12), bg='#f8f9fa', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Navigation and Tools
        left_frame = tk.Frame(main_frame, bg='#e9ecef', relief='raised', bd=2, width=250)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        nav_label = tk.Label(left_frame, text="Writing Tools", font=('Arial', 14, 'bold'),
                            bg='#e9ecef', fg='#2c3e50')
        nav_label.pack(pady=10)
        
        # Navigation buttons
        nav_buttons = [
            ("📝 New Project", self.new_project),
            ("📂 Open Project", self.open_project),
            ("💡 Writing Prompts", self.show_prompts),
            ("🎨 Genre Explorer", self.show_genres),
            ("📚 Story Elements", self.show_story_elements),
            ("🔧 Writing Tools", self.show_writing_tools),
            ("📊 Progress Tracker", self.show_progress),
            ("🏆 Publishing Center", self.show_publishing)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(left_frame, text=text, command=command,
                          font=('Arial', 10), width=22, pady=5,
                          bg='#6c5ce7', fg='white', relief='flat')
            btn.pack(pady=2, padx=10)
            
        # Writing tips panel
        tips_frame = tk.LabelFrame(left_frame, text="💭 Writing Tip", 
                                  font=('Arial', 11, 'bold'), bg='#e9ecef')
        tips_frame.pack(fill='x', padx=10, pady=20)
        
        self.tip_label = tk.Label(tips_frame, text=random.choice(self.writing_tips),
                                 font=('Arial', 9), bg='#e9ecef', fg='#2c3e50',
                                 wraplength=200, justify='left')
        self.tip_label.pack(padx=10, pady=10)
        
        tk.Button(tips_frame, text="New Tip", command=self.show_new_tip,
                 font=('Arial', 8), bg='#00b894', fg='white').pack(pady=5)
        
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
        
        # Welcome message
        tk.Label(welcome_frame, text="Welcome to Your Writing Workshop!", 
                font=('Arial', 20, 'bold'), bg='#ffffff', fg='#2c3e50').pack(pady=20)
        
        tk.Label(welcome_frame, text="Ready to create amazing stories, poems, and essays?", 
                font=('Arial', 14), bg='#ffffff', fg='#7f8c8d').pack(pady=10)
        
        # Quick start options
        quick_frame = tk.LabelFrame(welcome_frame, text="Quick Start", 
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        quick_frame.pack(fill='x', pady=30)
        
        quick_buttons = [
            ("📝 Start Writing Now", self.new_project, '#e17055'),
            ("💡 Get a Prompt", self.random_prompt, '#00b894'),
            ("📚 Learn About Genres", self.show_genres, '#6c5ce7'),
            ("🎯 Writing Challenge", self.start_challenge, '#fdcb6e')
        ]
        
        for i, (text, command, color) in enumerate(quick_buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(quick_frame, text=text, command=command,
                          font=('Arial', 12), pady=15, width=25,
                          bg=color, fg='white', relief='flat')
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
        quick_frame.grid_columnconfigure(0, weight=1)
        quick_frame.grid_columnconfigure(1, weight=1)
        
        # Recent projects
        recent_frame = tk.LabelFrame(welcome_frame, text="Recent Projects", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
        recent_frame.pack(fill='x', pady=20)
        
        if self.writing_projects:
            for project_name in list(self.writing_projects.keys())[-3:]:
                project_btn = tk.Button(recent_frame, text=f"📄 {project_name}",
                                      command=lambda p=project_name: self.load_project(p),
                                      font=('Arial', 10), bg='#ddd', fg='#2c3e50',
                                      relief='flat', anchor='w')
                project_btn.pack(fill='x', padx=10, pady=2)
        else:
            tk.Label(recent_frame, text="No recent projects. Start writing to see them here!",
                    font=('Arial', 10), bg='#ffffff', fg='#7f8c8d').pack(padx=10, pady=10)
        
    def new_project(self):
        """Create a new writing project"""
        # Project setup dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("New Writing Project")
        dialog.geometry("400x300")
        dialog.configure(bg='#ffffff')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        tk.Label(dialog, text="Create New Project", font=('Arial', 16, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(pady=20)
        
        # Project name
        name_frame = tk.Frame(dialog, bg='#ffffff')
        name_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(name_frame, text="Project Name:", font=('Arial', 11),
                bg='#ffffff').pack(anchor='w')
        name_entry = tk.Entry(name_frame, font=('Arial', 11), width=40)
        name_entry.pack(fill='x', pady=5)
        name_entry.focus()
        
        # Genre selection
        genre_frame = tk.Frame(dialog, bg='#ffffff')
        genre_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(genre_frame, text="Writing Type:", font=('Arial', 11),
                bg='#ffffff').pack(anchor='w')
        
        genre_var = tk.StringVar(value="Story")
        genre_combo = ttk.Combobox(genre_frame, textvariable=genre_var,
                                  values=["Story", "Poem", "Essay", "Script", "Journal", "Letter"],
                                  state="readonly", font=('Arial', 11))
        genre_combo.pack(fill='x', pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#ffffff')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        def create_project():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a project name")
                return
                
            if name in self.writing_projects:
                messagebox.showerror("Error", "Project name already exists")
                return
                
            # Create new project
            self.current_project = {
                'name': name,
                'genre': genre_var.get(),
                'content': '',
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'word_count': 0,
                'notes': ''
            }
            
            self.writing_projects[name] = self.current_project
            dialog.destroy()
            self.show_writing_interface()
            
        tk.Button(button_frame, text="Create", command=create_project,
                 bg='#00b894', fg='white', font=('Arial', 11), pady=5).pack(side='right', padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#636e72', fg='white', font=('Arial', 11), pady=5).pack(side='right')
        
    def show_writing_interface(self):
        """Show the main writing interface"""
        self.clear_workspace()
        
        if not self.current_project:
            self.show_welcome_screen()
            return
        
        # Header with project info
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text=f"📝 {self.current_project['name']}", 
                font=('Arial', 18, 'bold'), bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Label(header_frame, text=f"Type: {self.current_project['genre']}", 
                font=('Arial', 11), bg='#ffffff', fg='#7f8c8d').pack(side='right')
        
        # Writing area
        writing_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        writing_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Toolbar
        toolbar_frame = tk.Frame(writing_frame, bg='#ffffff')
        toolbar_frame.pack(fill='x', pady=(0, 10))
        
        toolbar_buttons = [
            ("💾 Save", self.save_project, '#00b894'),
            ("📊 Word Count", self.show_word_count, '#6c5ce7'),
            ("🎨 Format", self.show_formatting, '#e17055'),
            ("💡 Get Help", self.show_writing_help, '#fdcb6e'),
            ("📝 Notes", self.show_notes, '#74b9ff')
        ]
        
        for text, command, color in toolbar_buttons:
            btn = tk.Button(toolbar_frame, text=text, command=command,
                          font=('Arial', 9), bg=color, fg='white',
                          relief='flat', padx=10)
            btn.pack(side='left', padx=2)
        
        # Status bar
        self.status_label = tk.Label(toolbar_frame, text=f"Words: {self.current_project['word_count']}", 
                                    font=('Arial', 9), bg='#ffffff', fg='#7f8c8d')
        self.status_label.pack(side='right')
        
        # Main text area
        self.text_area = scrolledtext.ScrolledText(writing_frame, wrap=tk.WORD,
                                                  font=('Georgia', 12), bg='#fefefe',
                                                  fg='#2c3e50', insertbackground='#2c3e50',
                                                  selectbackground='#74b9ff',
                                                  relief='flat', bd=10)
        self.text_area.pack(fill='both', expand=True)
        
        # Load existing content
        if self.current_project['content']:
            self.text_area.insert('1.0', self.current_project['content'])
        
        # Bind events
        self.text_area.bind('<KeyRelease>', self.update_word_count)
        self.text_area.bind('<Button-1>', self.update_word_count)
        
        # Focus on text area
        self.text_area.focus()
        
    def show_prompts(self):
        """Show writing prompts"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="💡 Writing Prompts", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(side='left')
        
        tk.Button(header_frame, text="🎲 Random Prompt", command=self.random_prompt,
                 bg='#00b894', fg='white', font=('Arial', 10)).pack(side='right')
        
        # Categories
        categories_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        categories_frame.pack(fill='x', padx=20, pady=10)
        
        categories = ["All", "Story", "Poetry", "Essay", "Creative", "Personal"]
        
        self.category_var = tk.StringVar(value="All")
        for category in categories:
            btn = tk.Radiobutton(categories_frame, text=category, variable=self.category_var,
                               value=category, font=('Arial', 10), bg='#ffffff',
                               command=self.filter_prompts)
            btn.pack(side='left', padx=10)
        
        # Prompts display
        self.prompts_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        self.prompts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.display_prompts()
        
    def display_prompts(self):
        """Display filtered prompts"""
        for widget in self.prompts_frame.winfo_children():
            widget.destroy()
            
        category = self.category_var.get()
        filtered_prompts = self.writing_prompts
        
        if category != "All":
            filtered_prompts = [p for p in self.writing_prompts if p['category'] == category]
        
        # Scrollable frame for prompts
        canvas = tk.Canvas(self.prompts_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.prompts_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display prompts
        for i, prompt in enumerate(filtered_prompts):
            prompt_frame = tk.LabelFrame(scrollable_frame, text=f"{prompt['category']} Prompt #{i+1}",
                                        font=('Arial', 11, 'bold'), bg='#ffffff')
            prompt_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(prompt_frame, text=prompt['text'], font=('Arial', 11),
                    bg='#ffffff', wraplength=600, justify='left').pack(anchor='w', padx=10, pady=10)
            
            btn_frame = tk.Frame(prompt_frame, bg='#ffffff')
            btn_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Button(btn_frame, text="✍️ Use This Prompt", 
                     command=lambda p=prompt: self.use_prompt(p),
                     bg='#6c5ce7', fg='white', font=('Arial', 9)).pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def show_genres(self):
        """Show genre information and examples"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🎨 Genre Explorer", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Genre grid
        genres_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        genres_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        genres = [
            ("📚 Fiction", "Create imaginary stories and characters", '#e17055'),
            ("📖 Non-Fiction", "Write about real events and facts", '#00b894'),
            ("🎭 Drama", "Write plays and scripts", '#6c5ce7'),
            ("🎵 Poetry", "Express feelings through verse", '#fdcb6e'),
            ("✉️ Personal", "Journals, letters, and memoirs", '#74b9ff'),
            ("📰 Journalism", "News articles and reports", '#a29bfe')
        ]
        
        for i, (title, description, color) in enumerate(genres):
            row = i // 2
            col = i % 2
            
            genre_frame = tk.LabelFrame(genres_frame, text=title, font=('Arial', 12, 'bold'),
                                       bg='#ffffff', fg=color)
            genre_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Label(genre_frame, text=description, font=('Arial', 11),
                    bg='#ffffff', wraplength=200).pack(padx=10, pady=10)
            
            tk.Button(genre_frame, text="Learn More", 
                     command=lambda g=title: self.show_genre_details(g),
                     bg=color, fg='white', font=('Arial', 9)).pack(pady=5)
        
        for i in range(2):
            genres_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            genres_frame.grid_rowconfigure(i, weight=1)
            
    def show_story_elements(self):
        """Show story elements and structure"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="📚 Story Elements", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Content
        content_text = """
🎭 CHARACTER DEVELOPMENT
• Protagonist: The main character
• Antagonist: The character who opposes the main character  
• Supporting Characters: Help develop the story
• Character Arc: How characters change throughout the story

📍 SETTING
• Time: When the story takes place
• Place: Where the story happens
• Mood: The atmosphere of the story
• Context: Historical or cultural background

📖 PLOT STRUCTURE
• Exposition: Introduction of characters and setting
• Rising Action: Building tension and conflict
• Climax: The turning point of the story
• Falling Action: Events after the climax
• Resolution: How the story ends

🎯 POINT OF VIEW
• First Person: "I" - narrator is a character in the story
• Second Person: "You" - reader is addressed directly
• Third Person Limited: "He/She" - one character's perspective
• Third Person Omniscient: "He/She" - multiple perspectives

🎨 LITERARY DEVICES
• Metaphor: Comparing two unlike things
• Simile: Comparison using "like" or "as"
• Symbolism: Objects that represent ideas
• Foreshadowing: Hints about future events
• Irony: When reality differs from expectation

✍️ WRITING TECHNIQUES
• Show, Don't Tell: Use actions and dialogue instead of explanation
• Dialogue: What characters say to each other
• Description: Paint pictures with words
• Pacing: Control the speed of your story
• Transition: Smooth movement between scenes
        """
        
        content_display = scrolledtext.ScrolledText(self.workspace_frame, wrap=tk.WORD,
                                                   font=('Arial', 11), bg='#fefefe',
                                                   state='normal')
        content_display.pack(fill='both', expand=True, padx=20, pady=10)
        content_display.insert('1.0', content_text)
        content_display.configure(state='disabled')
        
    def show_writing_tools(self):
        """Show writing assistance tools"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🔧 Writing Tools", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Tools grid
        tools_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        tools_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tools = [
            ("📝 Outline Builder", "Create story outlines and plot structures", self.show_outline_tool),
            ("👥 Character Creator", "Develop detailed character profiles", self.show_character_tool),
            ("🗺️ World Builder", "Design settings and worlds", self.show_world_tool),
            ("💬 Dialogue Helper", "Practice writing conversations", self.show_dialogue_tool),
            ("🎨 Style Analyzer", "Improve your writing style", self.show_style_tool),
            ("📖 Research Assistant", "Find information for your stories", self.show_research_tool)
        ]
        
        for i, (title, description, command) in enumerate(tools):
            row = i // 2
            col = i % 2
            
            tool_frame = tk.LabelFrame(tools_frame, text=title, font=('Arial', 12, 'bold'),
                                      bg='#ffffff')
            tool_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            tk.Label(tool_frame, text=description, font=('Arial', 10),
                    bg='#ffffff', wraplength=250).pack(padx=15, pady=10)
            
            tk.Button(tool_frame, text="Open Tool", command=command,
                     bg='#6c5ce7', fg='white', font=('Arial', 10)).pack(pady=10)
        
        for i in range(2):
            tools_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            tools_frame.grid_rowconfigure(i, weight=1)
        
    def show_progress(self):
        """Show writing progress and statistics"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="📊 Writing Progress", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Statistics
        stats_frame = tk.LabelFrame(self.workspace_frame, text="Your Writing Statistics",
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        total_projects = len(self.writing_projects)
        total_words = sum(p['word_count'] for p in self.writing_projects.values())
        
        stats_text = f"""
        📚 Total Projects: {total_projects}
        📝 Total Words Written: {total_words:,}
        🎯 Average Words per Project: {total_words // max(1, total_projects):,}
        ⭐ Longest Project: {max([p['word_count'] for p in self.writing_projects.values()], default=0):,} words
        """
        
        tk.Label(stats_frame, text=stats_text, font=('Arial', 11),
                bg='#ffffff', justify='left').pack(padx=20, pady=15)
        
        # Projects list
        projects_frame = tk.LabelFrame(self.workspace_frame, text="Your Projects",
                                      font=('Arial', 12, 'bold'), bg='#ffffff')
        projects_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        if self.writing_projects:
            # Create treeview for projects
            tree = ttk.Treeview(projects_frame, columns=('Genre', 'Words', 'Created'), show='headings')
            tree.heading('#0', text='Project Name')
            tree.heading('Genre', text='Type')
            tree.heading('Words', text='Words')
            tree.heading('Created', text='Created')
            
            for name, project in self.writing_projects.items():
                tree.insert('', 'end', text=name, values=(
                    project['genre'],
                    f"{project['word_count']:,}",
                    project['created'].split()[0]
                ))
            
            tree.pack(fill='both', expand=True, padx=10, pady=10)
        else:
            tk.Label(projects_frame, text="No projects yet. Start writing to see your progress!",
                    font=('Arial', 12), bg='#ffffff', fg='#7f8c8d').pack(expand=True)
        
    def show_publishing(self):
        """Show publishing and sharing options"""
        self.clear_workspace()
        
        # Header
        header_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🏆 Publishing Center", font=('Arial', 18, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack()
        
        # Publishing options
        options_frame = tk.Frame(self.workspace_frame, bg='#ffffff')
        options_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        publishing_options = [
            ("📄 Export as PDF", "Create a professional PDF of your work", self.export_pdf),
            ("📝 Export as Text", "Save your work as a text file", self.export_text),
            ("🌐 Create Web Page", "Turn your story into a webpage", self.create_webpage),
            ("📖 Make a Book", "Format your work like a real book", self.make_book),
            ("🎨 Add Illustrations", "Include pictures with your story", self.add_illustrations),
            ("📢 Share Online", "Share your work with others", self.share_online)
        ]
        
        for i, (title, description, command) in enumerate(publishing_options):
            row = i // 2
            col = i % 2
            
            option_frame = tk.LabelFrame(options_frame, text=title, font=('Arial', 12, 'bold'),
                                        bg='#ffffff')
            option_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            tk.Label(option_frame, text=description, font=('Arial', 10),
                    bg='#ffffff', wraplength=250).pack(padx=15, pady=10)
            
            tk.Button(option_frame, text="Get Started", command=command,
                     bg='#00b894', fg='white', font=('Arial', 10)).pack(pady=10)
        
        for i in range(2):
            options_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            options_frame.grid_rowconfigure(i, weight=1)
        
    def clear_workspace(self):
        """Clear the workspace frame"""
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()
            
    def load_writing_prompts(self):
        """Load writing prompts"""
        return [
            {
                "category": "Story",
                "text": "You find a mysterious key in your backyard. Where does it lead and what does it unlock?"
            },
            {
                "category": "Story", 
                "text": "Write about a world where colors have personalities and can talk to humans."
            },
            {
                "category": "Poetry",
                "text": "Write a poem about your favorite season using all five senses."
            },
            {
                "category": "Essay",
                "text": "Describe a person who has influenced your life and explain how they changed you."
            },
            {
                "category": "Creative",
                "text": "Imagine you could have dinner with any three people from history. Who would you choose and what would you discuss?"
            },
            {
                "category": "Personal",
                "text": "Write about a time when you had to be brave. What happened and how did you feel?"
            }
        ]
        
    def load_writing_tips(self):
        """Load writing tips"""
        return [
            "Read your work aloud to catch errors and improve flow.",
            "Start with a strong opening sentence to hook your readers.", 
            "Use specific details to make your writing come alive.",
            "Show emotions through actions instead of just telling.",
            "Keep a notebook to jot down interesting ideas.",
            "Don't worry about being perfect in your first draft.",
            "Use dialogue to reveal character personalities.",
            "Vary your sentence length to create rhythm.",
            "End chapters or sections with cliffhangers.",
            "Research unfamiliar topics to add authenticity."
        ]
        
    def show_new_tip(self):
        """Show a new random writing tip"""
        new_tip = random.choice(self.writing_tips)
        self.tip_label.configure(text=new_tip)
        
    def random_prompt(self):
        """Get a random writing prompt"""
        prompt = random.choice(self.writing_prompts)
        messagebox.showinfo("Random Prompt", f"Category: {prompt['category']}\n\n{prompt['text']}")
        
    def filter_prompts(self):
        """Filter prompts by category"""
        if hasattr(self, 'prompts_frame'):
            self.display_prompts()
            
    def use_prompt(self, prompt):
        """Use a selected prompt for writing"""
        if not self.current_project:
            # Create new project with prompt
            project_name = f"Prompt Story - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.current_project = {
                'name': project_name,
                'genre': prompt['category'],
                'content': f"Writing Prompt: {prompt['text']}\n\n",
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'word_count': 0,
                'notes': ''
            }
            self.writing_projects[project_name] = self.current_project
        else:
            # Add prompt to current project
            self.current_project['content'] += f"\n\nNew Prompt: {prompt['text']}\n\n"
            
        self.show_writing_interface()
        
    def open_project(self):
        """Open an existing project"""
        if not self.writing_projects:
            messagebox.showinfo("No Projects", "You haven't created any projects yet.")
            return
            
        # Project selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Open Project")
        dialog.geometry("400x300")
        dialog.configure(bg='#ffffff')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Select Project to Open", font=('Arial', 14, 'bold'),
                bg='#ffffff', fg='#2c3e50').pack(pady=20)
        
        # Project listbox
        listbox_frame = tk.Frame(dialog, bg='#ffffff')
        listbox_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        listbox = tk.Listbox(listbox_frame, font=('Arial', 11))
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        for name in self.writing_projects.keys():
            listbox.insert(tk.END, name)
            
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#ffffff')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        def open_selected():
            selection = listbox.curselection()
            if selection:
                project_name = listbox.get(selection[0])
                self.load_project(project_name)
                dialog.destroy()
            else:
                messagebox.showwarning("No Selection", "Please select a project to open.")
                
        tk.Button(button_frame, text="Open", command=open_selected,
                 bg='#00b894', fg='white', font=('Arial', 11)).pack(side='right', padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#636e72', fg='white', font=('Arial', 11)).pack(side='right')
        
    def load_project(self, project_name):
        """Load a specific project"""
        if project_name in self.writing_projects:
            self.current_project = self.writing_projects[project_name]
            self.show_writing_interface()
            
    def save_project(self):
        """Save the current project"""
        if not self.current_project or not hasattr(self, 'text_area'):
            return
            
        content = self.text_area.get('1.0', tk.END + '-1c')
        self.current_project['content'] = content
        self.current_project['word_count'] = len(content.split())
        
        messagebox.showinfo("Saved", f"Project '{self.current_project['name']}' saved successfully!")
        
    def update_word_count(self, event=None):
        """Update the word count display"""
        if hasattr(self, 'text_area') and hasattr(self, 'status_label'):
            content = self.text_area.get('1.0', tk.END + '-1c')
            word_count = len(content.split()) if content.strip() else 0
            
            if self.current_project:
                self.current_project['word_count'] = word_count
                
            self.status_label.configure(text=f"Words: {word_count}")
            
    def show_word_count(self):
        """Show detailed word count statistics"""
        if not hasattr(self, 'text_area'):
            return
            
        content = self.text_area.get('1.0', tk.END + '-1c')
        
        words = len(content.split()) if content.strip() else 0
        characters = len(content)
        characters_no_spaces = len(content.replace(' ', ''))
        paragraphs = len([p for p in content.split('\n\n') if p.strip()])
        
        stats = f"""Word Count Statistics:
        
📝 Words: {words:,}
📄 Characters (with spaces): {characters:,}
📄 Characters (no spaces): {characters_no_spaces:,}
📖 Paragraphs: {paragraphs}
⏱️ Estimated reading time: {words // 200} minutes"""
        
        messagebox.showinfo("Word Count", stats)
        
    def start_challenge(self):
        """Start a writing challenge"""
        challenges = [
            "Write a 100-word story using only dialogue",
            "Create a story that takes place in one room",
            "Write a poem with exactly 10 lines",
            "Tell a story backwards, starting with the ending",
            "Write about your day as if you were a detective"
        ]
        
        challenge = random.choice(challenges)
        response = messagebox.askyesno("Writing Challenge", f"Ready for a challenge?\n\n{challenge}\n\nStart now?")
        
        if response:
            self.new_project()
            
    # Placeholder methods for advanced features
    def show_formatting(self):
        messagebox.showinfo("Formatting", "Text formatting options would be available here.")
        
    def show_writing_help(self):
        messagebox.showinfo("Writing Help", "Writing assistance and grammar help would be available here.")
        
    def show_notes(self):
        messagebox.showinfo("Notes", "Project notes and research area would be available here.")
        
    def show_genre_details(self, genre):
        messagebox.showinfo("Genre Details", f"Detailed information about {genre} would be displayed here.")
        
    def show_outline_tool(self):
        messagebox.showinfo("Outline Builder", "Interactive story outline tool would open here.")
        
    def show_character_tool(self):
        messagebox.showinfo("Character Creator", "Character development tool would open here.")
        
    def show_world_tool(self):
        messagebox.showinfo("World Builder", "World building tool would open here.")
        
    def show_dialogue_tool(self):
        messagebox.showinfo("Dialogue Helper", "Dialogue writing assistant would open here.")
        
    def show_style_tool(self):
        messagebox.showinfo("Style Analyzer", "Writing style analysis tool would open here.")
        
    def show_research_tool(self):
        messagebox.showinfo("Research Assistant", "Research tools and resources would open here.")
        
    def export_pdf(self):
        messagebox.showinfo("Export PDF", "PDF export feature would be available here.")
        
    def export_text(self):
        messagebox.showinfo("Export Text", "Text file export would be available here.")
        
    def create_webpage(self):
        messagebox.showinfo("Web Page", "HTML webpage creation would be available here.")
        
    def make_book(self):
        messagebox.showinfo("Make Book", "Book formatting tool would be available here.")
        
    def add_illustrations(self):
        messagebox.showinfo("Illustrations", "Illustration tools would be available here.")
        
    def share_online(self):
        messagebox.showinfo("Share Online", "Online sharing options would be available here.")

def main():
    root = tk.Tk()
    app = CreativeWritingWorkshop(root)
    root.mainloop()

if __name__ == "__main__":
    main()