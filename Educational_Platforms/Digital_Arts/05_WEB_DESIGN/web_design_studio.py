#!/usr/bin/env python3
"""
Web Design Studio
=================
Interactive web design and development tool for K-12 digital arts education.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
import webbrowser
import os
import tempfile

class WebDesignStudio:
    """Interactive web design and development platform."""
    
    def __init__(self):
        """Initialize the web design studio."""
        self.setup_web_variables()
        self.setup_gui()
        
    def setup_web_variables(self):
        """Initialize web design state variables."""
        self.current_project = {
            'name': 'My Website',
            'pages': ['index.html'],
            'current_page': 0,
            'html_content': '',
            'css_content': '',
            'js_content': '',
            'assets': []
        }
        self.preview_server_running = False
        self.code_templates = self.load_code_templates()
        
    def setup_gui(self):
        """Create the main web design studio interface."""
        self.root = tk.Tk()
        self.root.title("🌐 Web Design Studio - Digital Arts Platform")
        self.root.geometry("1600x900")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_designer_tab()
        self.setup_code_editor_tab()
        self.setup_templates_tab()
        self.setup_responsive_tab()
        self.setup_learn_web_tab()
        
    def setup_designer_tab(self):
        """Setup the visual web designer tab."""
        designer_frame = ttk.Frame(self.notebook)
        self.notebook.add(designer_frame, text="🎨 Visual Designer")
        
        # Top toolbar
        toolbar = ttk.Frame(designer_frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        # File operations
        file_frame = ttk.LabelFrame(toolbar, text="📁 Project")
        file_frame.pack(side='left', padx=5)
        
        ttk.Button(file_frame, text="🆕 New", command=self.new_website).pack(side='left', padx=2)
        ttk.Button(file_frame, text="📁 Open", command=self.open_website).pack(side='left', padx=2)
        ttk.Button(file_frame, text="💾 Save", command=self.save_website).pack(side='left', padx=2)
        ttk.Button(file_frame, text="👁️ Preview", command=self.preview_website).pack(side='left', padx=2)
        ttk.Button(file_frame, text="🌐 Publish", command=self.publish_website).pack(side='left', padx=2)
        
        # Page management
        page_frame = ttk.LabelFrame(toolbar, text="📄 Pages")
        page_frame.pack(side='left', padx=5)
        
        ttk.Button(page_frame, text="➕ Add Page", command=self.add_page).pack(side='left', padx=2)
        ttk.Button(page_frame, text="📝 Rename", command=self.rename_page).pack(side='left', padx=2)
        ttk.Button(page_frame, text="🗑️ Delete", command=self.delete_page).pack(side='left', padx=2)
        
        # Current page selector
        ttk.Label(page_frame, text="Current:").pack(side='left', padx=5)
        self.page_var = tk.StringVar(value="index.html")
        page_combo = ttk.Combobox(page_frame, textvariable=self.page_var, width=15,
                                 values=self.current_project['pages'])
        page_combo.pack(side='left', padx=2)
        page_combo.bind('<<ComboboxSelected>>', self.switch_page)
        
        # Device preview
        device_frame = ttk.LabelFrame(toolbar, text="📱 Device Preview")
        device_frame.pack(side='left', padx=5)
        
        devices = [("🖥️ Desktop", "desktop"), ("💻 Laptop", "laptop"), 
                  ("📱 Mobile", "mobile"), ("📱 Tablet", "tablet")]
        
        self.device_var = tk.StringVar(value="desktop")
        
        for name, device in devices:
            ttk.Radiobutton(device_frame, text=name, variable=self.device_var,
                           value=device, command=self.change_preview_device).pack(side='left', padx=2)
        
        # Main workspace
        workspace = ttk.Frame(designer_frame)
        workspace.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Elements panel (left)
        elements_panel = ttk.LabelFrame(workspace, text="🧩 Website Elements")
        elements_panel.pack(side='left', fill='y', padx=5)
        
        # Layout elements
        layout_frame = ttk.LabelFrame(elements_panel, text="📐 Layout")
        layout_frame.pack(fill='x', padx=5, pady=5)
        
        layout_elements = [
            ("📄 Header", "header"),
            ("🧭 Navigation", "nav"),
            ("📝 Content Section", "section"),
            ("📊 Sidebar", "sidebar"),
            ("🦶 Footer", "footer"),
            ("🔲 Container", "div"),
            ("📋 Article", "article")
        ]
        
        for name, element in layout_elements:
            ttk.Button(layout_frame, text=name,
                      command=lambda e=element: self.add_layout_element(e)).pack(fill='x', pady=1)
        
        # Content elements
        content_frame = ttk.LabelFrame(elements_panel, text="📝 Content")
        content_frame.pack(fill='x', padx=5, pady=5)
        
        content_elements = [
            ("📰 Heading", "h1"),
            ("📄 Paragraph", "p"),
            ("🖼️ Image", "img"),
            ("🎬 Video", "video"),
            ("🔗 Link", "a"),
            ("📋 List", "ul"),
            ("📊 Table", "table"),
            ("📝 Form", "form")
        ]
        
        for name, element in content_elements:
            ttk.Button(content_frame, text=name,
                      command=lambda e=element: self.add_content_element(e)).pack(fill='x', pady=1)
        
        # Interactive elements
        interactive_frame = ttk.LabelFrame(elements_panel, text="🎯 Interactive")
        interactive_frame.pack(fill='x', padx=5, pady=5)
        
        interactive_elements = [
            ("🔘 Button", "button"),
            ("📝 Text Input", "input_text"),
            ("☑️ Checkbox", "checkbox"),
            ("🔄 Dropdown", "select"),
            ("🎚️ Slider", "range"),
            ("📅 Date Picker", "date"),
            ("🎨 Color Picker", "color")
        ]
        
        for name, element in interactive_elements:
            ttk.Button(interactive_frame, text=name,
                      command=lambda e=element: self.add_interactive_element(e)).pack(fill='x', pady=1)
        
        # Visual designer canvas (center)
        canvas_frame = ttk.LabelFrame(workspace, text="🖼️ Visual Designer")
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Canvas with device frame
        self.setup_device_canvas(canvas_frame)
        
        # Properties panel (right)
        properties_panel = ttk.LabelFrame(workspace, text="⚙️ Element Properties")
        properties_panel.pack(side='right', fill='y', padx=5)
        
        # Element info
        element_info = ttk.LabelFrame(properties_panel, text="📦 Selected Element")
        element_info.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(element_info, text="Tag:").pack(anchor='w', padx=5)
        self.element_tag_label = ttk.Label(element_info, text="None")
        self.element_tag_label.pack(anchor='w', padx=5)
        
        ttk.Label(element_info, text="ID:").pack(anchor='w', padx=5)
        self.element_id_var = tk.StringVar()
        ttk.Entry(element_info, textvariable=self.element_id_var).pack(fill='x', padx=5, pady=2)
        
        ttk.Label(element_info, text="Class:").pack(anchor='w', padx=5)
        self.element_class_var = tk.StringVar()
        ttk.Entry(element_info, textvariable=self.element_class_var).pack(fill='x', padx=5, pady=2)
        
        # Style properties
        style_props = ttk.LabelFrame(properties_panel, text="🎨 Styling")
        style_props.pack(fill='x', padx=5, pady=5)
        
        # Background color
        bg_frame = ttk.Frame(style_props)
        bg_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(bg_frame, text="Background:").pack(side='left')
        self.bg_color_btn = tk.Button(bg_frame, bg="#FFFFFF", width=5, height=1,
                                     command=self.choose_bg_color)
        self.bg_color_btn.pack(side='right')
        
        # Text color
        text_frame = ttk.Frame(style_props)
        text_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(text_frame, text="Text Color:").pack(side='left')
        self.text_color_btn = tk.Button(text_frame, bg="#000000", width=5, height=1,
                                       command=self.choose_text_color)
        self.text_color_btn.pack(side='right')
        
        # Font properties
        ttk.Label(style_props, text="Font Family:").pack(anchor='w', padx=5)
        self.font_family_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(style_props, textvariable=self.font_family_var,
                                 values=["Arial", "Times", "Helvetica", "Georgia", "Verdana"])
        font_combo.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(style_props, text="Font Size:").pack(anchor='w', padx=5)
        self.font_size_var = tk.StringVar(value="16px")
        font_size_entry = ttk.Entry(style_props, textvariable=self.font_size_var)
        font_size_entry.pack(fill='x', padx=5, pady=2)
        
        # Layout properties
        layout_props = ttk.LabelFrame(properties_panel, text="📐 Layout")
        layout_props.pack(fill='x', padx=5, pady=5)
        
        # Width and height
        size_frame = ttk.Frame(layout_props)
        size_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0, padx=2)
        self.width_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=2)
        
        ttk.Label(size_frame, text="Height:").grid(row=0, column=2, padx=2)
        self.height_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=0, column=3, padx=2)
        
        # Margin and padding
        ttk.Label(layout_props, text="Margin:").pack(anchor='w', padx=5)
        self.margin_var = tk.StringVar(value="0px")
        ttk.Entry(layout_props, textvariable=self.margin_var).pack(fill='x', padx=5, pady=2)
        
        ttk.Label(layout_props, text="Padding:").pack(anchor='w', padx=5)
        self.padding_var = tk.StringVar(value="0px")
        ttk.Entry(layout_props, textvariable=self.padding_var).pack(fill='x', padx=5, pady=2)
        
        # Apply changes button
        ttk.Button(properties_panel, text="✅ Apply Changes", 
                  command=self.apply_element_changes).pack(fill='x', padx=5, pady=10)
        
    def setup_device_canvas(self, parent):
        """Setup the device preview canvas."""
        canvas_container = ttk.Frame(parent)
        canvas_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Device frame dimensions
        device_sizes = {
            'desktop': (1200, 800),
            'laptop': (1000, 700),
            'tablet': (768, 1024),
            'mobile': (375, 667)
        }
        
        self.current_device_size = device_sizes['desktop']
        
        # Create canvas with scrollbars
        self.web_canvas = tk.Canvas(canvas_container, bg='white', 
                                   width=self.current_device_size[0], 
                                   height=self.current_device_size[1])
        
        h_scrollbar = ttk.Scrollbar(canvas_container, orient='horizontal', command=self.web_canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical', command=self.web_canvas.yview)
        self.web_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack canvas and scrollbars
        self.web_canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind canvas events
        self.web_canvas.bind("<Button-1>", self.canvas_click)
        self.web_canvas.bind("<B1-Motion>", self.canvas_drag)
        self.web_canvas.bind("<ButtonRelease-1>", self.canvas_release)
        
        # Draw initial page structure
        self.draw_initial_page()
        
    def setup_code_editor_tab(self):
        """Setup the code editor tab."""
        code_frame = ttk.Frame(self.notebook)
        self.notebook.add(code_frame, text="💻 Code Editor")
        
        # Code editor toolbar
        code_toolbar = ttk.Frame(code_frame)
        code_toolbar.pack(fill='x', padx=5, pady=5)
        
        # Language selector
        lang_frame = ttk.LabelFrame(code_toolbar, text="📝 Language")
        lang_frame.pack(side='left', padx=5)
        
        languages = [("📄 HTML", "html"), ("🎨 CSS", "css"), ("⚡ JavaScript", "js")]
        
        self.code_lang_var = tk.StringVar(value="html")
        
        for name, lang in languages:
            ttk.Radiobutton(lang_frame, text=name, variable=self.code_lang_var,
                           value=lang, command=self.switch_code_language).pack(side='left', padx=5)
        
        # Code tools
        tools_frame = ttk.LabelFrame(code_toolbar, text="🛠️ Tools")
        tools_frame.pack(side='left', padx=5)
        
        ttk.Button(tools_frame, text="🔍 Format Code", command=self.format_code).pack(side='left', padx=2)
        ttk.Button(tools_frame, text="✅ Validate", command=self.validate_code).pack(side='left', padx=2)
        ttk.Button(tools_frame, text="🔄 Auto-Complete", command=self.auto_complete).pack(side='left', padx=2)
        ttk.Button(tools_frame, text="💾 Save", command=self.save_code).pack(side='left', padx=2)
        
        # Code editor workspace
        code_workspace = ttk.Frame(code_frame)
        code_workspace.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Line numbers and editor
        editor_frame = ttk.LabelFrame(code_workspace, text="📝 Code Editor")
        editor_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Create text editor with line numbers
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_container, width=4, height=20, bg='lightgray', 
                                   state='disabled', font=('Courier', 10))
        self.line_numbers.pack(side='left', fill='y')
        
        # Code editor
        self.code_editor = tk.Text(editor_container, font=('Courier', 10), wrap='none',
                                  undo=True, maxundo=-1, autoseparators=True)
        self.code_editor.pack(side='left', fill='both', expand=True)
        
        # Scrollbars for code editor
        code_v_scroll = ttk.Scrollbar(editor_container, orient='vertical', command=self.code_editor.yview)
        code_h_scroll = ttk.Scrollbar(editor_frame, orient='horizontal', command=self.code_editor.xview)
        
        self.code_editor.configure(yscrollcommand=code_v_scroll.set, xscrollcommand=code_h_scroll.set)
        
        code_v_scroll.pack(side='right', fill='y')
        code_h_scroll.pack(side='bottom', fill='x')
        
        # Bind events for line numbers
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.code_editor.bind('<MouseWheel>', self.update_line_numbers)
        
        # Code snippets panel
        snippets_frame = ttk.LabelFrame(code_workspace, text="📚 Code Snippets")
        snippets_frame.pack(side='right', fill='y', padx=5)
        
        # HTML snippets
        html_snippets = ttk.LabelFrame(snippets_frame, text="📄 HTML")
        html_snippets.pack(fill='x', padx=5, pady=5)
        
        html_snippets_list = [
            ("Basic Page", "html_basic"),
            ("Header", "html_header"),
            ("Navigation", "html_nav"),
            ("Form", "html_form"),
            ("Table", "html_table"),
            ("Card", "html_card")
        ]
        
        for name, snippet in html_snippets_list:
            ttk.Button(html_snippets, text=name,
                      command=lambda s=snippet: self.insert_snippet(s)).pack(fill='x', pady=1)
        
        # CSS snippets
        css_snippets = ttk.LabelFrame(snippets_frame, text="🎨 CSS")
        css_snippets.pack(fill='x', padx=5, pady=5)
        
        css_snippets_list = [
            ("Reset Styles", "css_reset"),
            ("Flexbox", "css_flexbox"),
            ("Grid", "css_grid"),
            ("Button Style", "css_button"),
            ("Card Style", "css_card"),
            ("Animation", "css_animation")
        ]
        
        for name, snippet in css_snippets_list:
            ttk.Button(css_snippets, text=name,
                      command=lambda s=snippet: self.insert_snippet(s)).pack(fill='x', pady=1)
        
        # Load initial HTML content
        self.load_initial_code()
        
    def setup_templates_tab(self):
        """Setup the website templates tab."""
        templates_frame = ttk.Frame(self.notebook)
        self.notebook.add(templates_frame, text="📋 Templates")
        
        # Template categories
        category_frame = ttk.LabelFrame(templates_frame, text="📂 Template Categories")
        category_frame.pack(fill='x', padx=5, pady=5)
        
        categories = [
            ("🏢 Business", "business"),
            ("🎓 Education", "education"),
            ("🎨 Portfolio", "portfolio"),
            ("📝 Blog", "blog"),
            ("🛍️ E-commerce", "ecommerce"),
            ("🎪 Event", "event"),
            ("📱 Landing Page", "landing"),
            ("👤 Personal", "personal")
        ]
        
        self.template_category_var = tk.StringVar(value="education")
        
        for name, category in categories:
            ttk.Radiobutton(category_frame, text=name, variable=self.template_category_var,
                           value=category, command=self.load_template_category).pack(side='left', padx=10)
        
        # Templates display
        templates_display = ttk.LabelFrame(templates_frame, text="🎨 Website Templates")
        templates_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Template grid
        templates_container = ttk.Frame(templates_display)
        templates_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.templates_canvas = tk.Canvas(templates_container, bg='white')
        templates_scrollbar = ttk.Scrollbar(templates_container, orient='vertical', 
                                           command=self.templates_canvas.yview)
        self.templates_canvas.configure(yscrollcommand=templates_scrollbar.set)
        
        self.templates_canvas.pack(side='left', fill='both', expand=True)
        templates_scrollbar.pack(side='right', fill='y')
        
        # Load initial templates
        self.load_template_category()
        
        # Template actions
        template_actions = ttk.LabelFrame(templates_frame, text="🎯 Template Actions")
        template_actions.pack(fill='x', padx=5, pady=5)
        
        actions_frame = ttk.Frame(template_actions)
        actions_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(actions_frame, text="Selected Template:").pack(side='left', padx=5)
        self.selected_template_var = tk.StringVar(value="None")
        ttk.Label(actions_frame, textvariable=self.selected_template_var).pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="👁️ Preview", command=self.preview_template).pack(side='right', padx=5)
        ttk.Button(actions_frame, text="🎨 Use Template", command=self.use_template).pack(side='right', padx=5)
        ttk.Button(actions_frame, text="📝 Customize", command=self.customize_template).pack(side='right', padx=5)
        
    def setup_responsive_tab(self):
        """Setup the responsive design tab."""
        responsive_frame = ttk.Frame(self.notebook)
        self.notebook.add(responsive_frame, text="📱 Responsive")
        
        # Responsive controls
        responsive_controls = ttk.LabelFrame(responsive_frame, text="📐 Responsive Design Tools")
        responsive_controls.pack(fill='x', padx=5, pady=5)
        
        # Breakpoint management
        breakpoint_frame = ttk.Frame(responsive_controls)
        breakpoint_frame.pack(side='left', padx=5, pady=5)
        
        ttk.Label(breakpoint_frame, text="Breakpoints:").pack(anchor='w')
        
        breakpoints = [
            ("📱 Mobile (320px-767px)", "mobile"),
            ("📱 Tablet (768px-1023px)", "tablet"), 
            ("💻 Desktop (1024px+)", "desktop")
        ]
        
        self.breakpoint_var = tk.StringVar(value="desktop")
        
        for name, bp in breakpoints:
            ttk.Radiobutton(breakpoint_frame, text=name, variable=self.breakpoint_var,
                           value=bp, command=self.switch_breakpoint).pack(anchor='w')
        
        # CSS media queries
        media_frame = ttk.Frame(responsive_controls)
        media_frame.pack(side='left', padx=5, pady=5)
        
        ttk.Label(media_frame, text="Media Query Generator:").pack(anchor='w')
        
        ttk.Button(media_frame, text="📱 Mobile First", 
                  command=self.generate_mobile_first_css).pack(fill='x', pady=2)
        ttk.Button(media_frame, text="🖥️ Desktop First", 
                  command=self.generate_desktop_first_css).pack(fill='x', pady=2)
        ttk.Button(media_frame, text="🎨 Flexible Grid", 
                  command=self.generate_flexible_grid).pack(fill='x', pady=2)
        
        # Responsive testing
        testing_frame = ttk.Frame(responsive_controls)
        testing_frame.pack(side='right', padx=5, pady=5)
        
        ttk.Label(testing_frame, text="Test Responsiveness:").pack(anchor='w')
        
        ttk.Button(testing_frame, text="🔍 Check All Sizes", 
                  command=self.test_all_sizes).pack(fill='x', pady=2)
        ttk.Button(testing_frame, text="📊 Performance", 
                  command=self.check_performance).pack(fill='x', pady=2)
        ttk.Button(testing_frame, text="♿ Accessibility", 
                  command=self.check_accessibility).pack(fill='x', pady=2)
        
        # Multi-device preview
        preview_frame = ttk.LabelFrame(responsive_frame, text="📱 Multi-Device Preview")
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Device frames
        devices_container = ttk.Frame(preview_frame)
        devices_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Mobile preview
        mobile_frame = ttk.LabelFrame(devices_container, text="📱 Mobile")
        mobile_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.mobile_canvas = tk.Canvas(mobile_frame, width=375, height=600, bg='white')
        self.mobile_canvas.pack(padx=5, pady=5)
        
        # Tablet preview
        tablet_frame = ttk.LabelFrame(devices_container, text="📱 Tablet")
        tablet_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.tablet_canvas = tk.Canvas(tablet_frame, width=500, height=400, bg='white')
        self.tablet_canvas.pack(padx=5, pady=5)
        
        # Desktop preview
        desktop_frame = ttk.LabelFrame(devices_container, text="🖥️ Desktop")
        desktop_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.desktop_canvas = tk.Canvas(desktop_frame, width=600, height=400, bg='white')
        self.desktop_canvas.pack(padx=5, pady=5)
        
        # Load sample responsive content
        self.load_responsive_examples()
        
    def setup_learn_web_tab(self):
        """Setup the web development learning tab."""
        learn_frame = ttk.Frame(self.notebook)
        self.notebook.add(learn_frame, text="🎓 Learn Web Dev")
        
        # Learning path selector
        path_frame = ttk.LabelFrame(learn_frame, text="🛤️ Learning Path")
        path_frame.pack(fill='x', padx=5, pady=5)
        
        learning_paths = [
            ("🌱 Beginner - HTML Basics", "html_basics"),
            ("🎨 Styling with CSS", "css_basics"),
            ("⚡ Interactive JavaScript", "js_basics"),
            ("📱 Responsive Design", "responsive"),
            ("🎯 Advanced Techniques", "advanced"),
            ("🚀 Web Performance", "performance")
        ]
        
        self.learning_path_var = tk.StringVar(value="html_basics")
        
        for name, path in learning_paths:
            ttk.Radiobutton(path_frame, text=name, variable=self.learning_path_var,
                           value=path, command=self.load_learning_content).pack(side='left', padx=10)
        
        # Learning content
        content_frame = ttk.LabelFrame(learn_frame, text="📚 Learning Content")
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Content display
        content_display = ttk.Frame(content_frame)
        content_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Lesson content
        lesson_frame = ttk.Frame(content_display)
        lesson_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.learning_text = tk.Text(lesson_frame, wrap=tk.WORD, font=('Arial', 11))
        learning_scrollbar = ttk.Scrollbar(lesson_frame, orient='vertical', command=self.learning_text.yview)
        self.learning_text.configure(yscrollcommand=learning_scrollbar.set)
        
        self.learning_text.pack(side='left', fill='both', expand=True)
        learning_scrollbar.pack(side='right', fill='y')
        
        # Practice exercises
        practice_frame = ttk.LabelFrame(content_display, text="💪 Practice")
        practice_frame.pack(side='right', fill='y', padx=5)
        
        ttk.Label(practice_frame, text="Hands-on Exercises:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=5, pady=5)
        
        exercises = [
            ("🏗️ Build Your First Page", "first_page"),
            ("🎨 Style with CSS", "style_page"),
            ("📱 Make it Responsive", "responsive_page"),
            ("⚡ Add Interactions", "interactive_page"),
            ("🎯 Complete Project", "final_project")
        ]
        
        for name, exercise in exercises:
            ttk.Button(practice_frame, text=name,
                      command=lambda e=exercise: self.start_exercise(e)).pack(fill='x', padx=5, pady=2)
        
        # Quick reference
        reference_frame = ttk.LabelFrame(practice_frame, text="📖 Quick Reference")
        reference_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(reference_frame, text="📄 HTML Tags", 
                  command=self.show_html_reference).pack(fill='x', pady=1)
        ttk.Button(reference_frame, text="🎨 CSS Properties", 
                  command=self.show_css_reference).pack(fill='x', pady=1)
        ttk.Button(reference_frame, text="⚡ JS Functions", 
                  command=self.show_js_reference).pack(fill='x', pady=1)
        ttk.Button(reference_frame, text="🌐 Web APIs", 
                  command=self.show_api_reference).pack(fill='x', pady=1)
        
        # Load initial learning content
        self.load_learning_content()
    
    def load_code_templates(self):
        """Load code templates and snippets."""
        return {
            'html_basic': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to My Website</h1>
    </header>
    
    <nav>
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    
    <main>
        <section id="home">
            <h2>Home Section</h2>
            <p>This is the main content area.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 My Website. All rights reserved.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>''',
            
            'css_reset': '''/* CSS Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}''',
            
            'css_flexbox': '''.flex-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.flex-item {
    flex: 1 1 300px;
    padding: 1rem;
    background: #f4f4f4;
    border-radius: 5px;
}'''
        }
    
    def load_learning_content(self, event=None):
        """Load learning content based on selected path."""
        content_map = {
            'html_basics': '''
🌐 HTML BASICS - BUILDING YOUR FIRST WEBPAGE

HTML (HyperText Markup Language) is the foundation of every website. It provides the structure and content of web pages using elements called "tags."

📄 BASIC HTML STRUCTURE:
Every HTML page starts with the same basic structure:

<!DOCTYPE html>              ← Tells browser this is HTML5
<html>                       ← Root element
<head>                       ← Information about the page
    <title>Page Title</title> ← Shows in browser tab
</head>
<body>                       ← Visible content goes here
    <h1>My First Heading</h1>
    <p>My first paragraph.</p>
</body>
</html>

🏷️ COMMON HTML TAGS:

Headings (largest to smallest):
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>

Text Content:
<p>This is a paragraph of text.</p>
<strong>Bold text</strong>
<em>Italic text</em>
<br> ← Line break

Lists:
<ul>                         ← Unordered (bullet) list
    <li>First item</li>
    <li>Second item</li>
</ul>

<ol>                         ← Ordered (numbered) list
    <li>Step one</li>
    <li>Step two</li>
</ol>

Links and Images:
<a href="https://example.com">Visit Example</a>
<img src="photo.jpg" alt="Description of photo">

🎯 YOUR FIRST CHALLENGE:
Create a simple webpage about yourself with:
• A main heading with your name
• A paragraph describing your hobbies
• A list of your favorite subjects
• An image (can be any image for now)

💡 TIPS:
• Always close your tags: <p>text</p>
• Use proper indentation to make code readable
• Test your page by opening the HTML file in a browser
• Use meaningful alt text for images
            ''',
            
            'css_basics': '''
🎨 CSS BASICS - STYLING YOUR WEBSITE

CSS (Cascading Style Sheets) controls how your HTML looks. It handles colors, fonts, layout, and visual effects.

🔗 CONNECTING CSS TO HTML:
Three ways to add CSS:

1. Inline (in the HTML tag):
<p style="color: blue;">Blue text</p>

2. Internal (in the <head> section):
<style>
    p { color: blue; }
</style>

3. External (separate .css file):
<link rel="stylesheet" href="styles.css">

🎯 CSS SELECTORS:
CSS uses selectors to target HTML elements:

Element selector:
p { color: blue; }                ← All paragraphs

Class selector:
.highlight { background: yellow; } ← Elements with class="highlight"

ID selector:
#header { font-size: 24px; }      ← Element with id="header"

🎨 COMMON CSS PROPERTIES:

Text Styling:
color: red;                       ← Text color
font-family: Arial, sans-serif;   ← Font type
font-size: 18px;                  ← Text size
font-weight: bold;                ← Text thickness
text-align: center;               ← Text alignment

Background and Borders:
background-color: lightblue;      ← Background color
background-image: url('bg.jpg');  ← Background image
border: 2px solid black;          ← Border style
border-radius: 10px;              ← Rounded corners

Spacing:
margin: 20px;                     ← Space outside element
padding: 15px;                    ← Space inside element
width: 300px;                     ← Element width
height: 200px;                    ← Element height

📐 THE BOX MODEL:
Every HTML element is a rectangular box with:
• Content (the actual text/images)
• Padding (space around content)
• Border (line around padding)
• Margin (space outside border)

🎯 STYLING CHALLENGE:
Style your webpage from the HTML lesson:
• Change the heading color and font
• Add a background color to the page
• Style your list items with different colors
• Add padding and margins for better spacing

💡 PRO TIPS:
• Use web-safe fonts like Arial, Georgia, Times
• Stick to a color scheme (2-3 main colors)
• Test your styles in different browsers
• Use CSS comments: /* This is a comment */
            '''
        }
        
        selected_path = self.learning_path_var.get()
        content = content_map.get(selected_path, "Loading content...")
        
        self.learning_text.delete(1.0, tk.END)
        self.learning_text.insert(1.0, content)
    
    def run(self):
        """Start the web design studio application."""
        self.root.mainloop()

def main():
    """Main function to run the web design studio."""
    print("🌐 Web Design Studio")
    print("=" * 20)
    print("🎨 Create amazing websites and learn web development")
    print("📱 Design responsive, modern web experiences")
    print()
    print("Starting Web Design Studio...")
    
    studio = WebDesignStudio()
    studio.run()

if __name__ == "__main__":
    main()