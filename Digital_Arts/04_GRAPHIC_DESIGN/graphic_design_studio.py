#!/usr/bin/env python3
"""
Graphic Design Studio
=====================
Professional graphic design tool for K-12 digital arts education.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import json
from datetime import datetime
import math
import random

class GraphicDesignStudio:
    """Professional graphic design creation and learning platform."""
    
    def __init__(self):
        """Initialize the graphic design studio."""
        self.setup_design_variables()
        self.setup_gui()
        
    def setup_design_variables(self):
        """Initialize design state variables."""
        self.current_project = {
            'name': 'Untitled Design',
            'type': 'poster',
            'dimensions': (800, 600),
            'elements': [],
            'layers': ['Background'],
            'current_layer': 0
        }
        self.selected_elements = []
        self.clipboard = []
        self.design_templates = self.load_design_templates()
        self.color_palette = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
        
    def setup_gui(self):
        """Create the main graphic design studio interface."""
        self.root = tk.Tk()
        self.root.title("🎨 Graphic Design Studio - Digital Arts Platform")
        self.root.geometry("1600x900")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_designer_tab()
        self.setup_templates_tab()
        self.setup_typography_tab()
        self.setup_branding_tab()
        self.setup_portfolio_tab()
        
    def setup_designer_tab(self):
        """Setup the main design workspace."""
        designer_frame = ttk.Frame(self.notebook)
        self.notebook.add(designer_frame, text="🎨 Designer")
        
        # Top toolbar
        toolbar = ttk.Frame(designer_frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        # File operations
        file_frame = ttk.LabelFrame(toolbar, text="📁 File")
        file_frame.pack(side='left', padx=5)
        
        ttk.Button(file_frame, text="📄 New", command=self.new_design).pack(side='left', padx=2)
        ttk.Button(file_frame, text="📁 Open", command=self.open_design).pack(side='left', padx=2)
        ttk.Button(file_frame, text="💾 Save", command=self.save_design).pack(side='left', padx=2)
        ttk.Button(file_frame, text="📤 Export", command=self.export_design).pack(side='left', padx=2)
        
        # Edit operations
        edit_frame = ttk.LabelFrame(toolbar, text="✏️ Edit")
        edit_frame.pack(side='left', padx=5)
        
        ttk.Button(edit_frame, text="↶ Undo", command=self.undo_action).pack(side='left', padx=2)
        ttk.Button(edit_frame, text="↷ Redo", command=self.redo_action).pack(side='left', padx=2)
        ttk.Button(edit_frame, text="📋 Copy", command=self.copy_elements).pack(side='left', padx=2)
        ttk.Button(edit_frame, text="📄 Paste", command=self.paste_elements).pack(side='left', padx=2)
        
        # View controls
        view_frame = ttk.LabelFrame(toolbar, text="👁️ View")
        view_frame.pack(side='left', padx=5)
        
        ttk.Label(view_frame, text="Zoom:").pack(side='left', padx=2)
        self.zoom_var = tk.StringVar(value="100%")
        zoom_combo = ttk.Combobox(view_frame, textvariable=self.zoom_var, width=8,
                                 values=["25%", "50%", "75%", "100%", "125%", "150%", "200%"])
        zoom_combo.pack(side='left', padx=2)
        
        ttk.Button(view_frame, text="📐 Grid", command=self.toggle_grid).pack(side='left', padx=2)
        ttk.Button(view_frame, text="📏 Rulers", command=self.toggle_rulers).pack(side='left', padx=2)
        
        # Main workspace
        workspace = ttk.Frame(designer_frame)
        workspace.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tools panel (left)
        tools_panel = ttk.LabelFrame(workspace, text="🛠️ Design Tools")
        tools_panel.pack(side='left', fill='y', padx=5)
        
        # Selection and drawing tools
        basic_tools = [
            ("🎯 Select", "select"),
            ("✏️ Pencil", "pencil"),
            ("🖌️ Brush", "brush"),
            ("📝 Text", "text"),
            ("🔵 Shape", "shape"),
            ("📏 Line", "line"),
            ("🪣 Fill", "fill"),
            ("🎨 Gradient", "gradient"),
            ("✨ Effects", "effects")
        ]
        
        self.tool_var = tk.StringVar(value="select")
        
        for name, tool in basic_tools:
            ttk.Radiobutton(tools_panel, text=name, variable=self.tool_var,
                           value=tool, command=lambda t=tool: self.select_tool(t)).pack(anchor='w', padx=5, pady=2)
        
        # Shape tools
        shapes_frame = ttk.LabelFrame(tools_panel, text="📐 Shapes")
        shapes_frame.pack(fill='x', padx=5, pady=5)
        
        shapes = [
            ("⭕ Circle", "circle"),
            ("⬜ Rectangle", "rectangle"),
            ("🔺 Triangle", "triangle"),
            ("⭐ Star", "star"),
            ("💬 Speech Bubble", "speech"),
            ("➡️ Arrow", "arrow")
        ]
        
        for name, shape in shapes:
            ttk.Button(shapes_frame, text=name, 
                      command=lambda s=shape: self.add_shape(s)).pack(fill='x', pady=1)
        
        # Quick elements
        elements_frame = ttk.LabelFrame(tools_panel, text="⚡ Quick Add")
        elements_frame.pack(fill='x', padx=5, pady=5)
        
        quick_elements = [
            ("🖼️ Image", "image"),
            ("📊 Chart", "chart"),
            ("🎨 Icon", "icon"),
            ("🔤 Logo", "logo"),
            ("📅 Date", "date"),
            ("🌐 QR Code", "qr_code")
        ]
        
        for name, element in quick_elements:
            ttk.Button(elements_frame, text=name,
                      command=lambda e=element: self.add_element(e)).pack(fill='x', pady=1)
        
        # Design canvas (center)
        canvas_frame = ttk.LabelFrame(workspace, text="🖼️ Design Canvas")
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Canvas container with scrollbars
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.design_canvas = tk.Canvas(canvas_container, width=800, height=600, bg='white',
                                      scrollregion=(0, 0, 1200, 900))
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_container, orient='horizontal', command=self.design_canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical', command=self.design_canvas.yview)
        self.design_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack canvas and scrollbars
        self.design_canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind canvas events
        self.design_canvas.bind("<Button-1>", self.canvas_click)
        self.design_canvas.bind("<B1-Motion>", self.canvas_drag)
        self.design_canvas.bind("<ButtonRelease-1>", self.canvas_release)
        self.design_canvas.bind("<Double-Button-1>", self.canvas_double_click)
        
        # Properties panel (right)
        props_panel = ttk.LabelFrame(workspace, text="⚙️ Properties")
        props_panel.pack(side='right', fill='y', padx=5)
        
        # Color palette
        color_frame = ttk.LabelFrame(props_panel, text="🎨 Colors")
        color_frame.pack(fill='x', padx=5, pady=5)
        
        # Current colors
        current_colors = ttk.Frame(color_frame)
        current_colors.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(current_colors, text="Fill:").grid(row=0, column=0, padx=2)
        self.fill_color_btn = tk.Button(current_colors, bg="#000000", width=5, height=2,
                                       command=self.choose_fill_color)
        self.fill_color_btn.grid(row=0, column=1, padx=2)
        
        ttk.Label(current_colors, text="Stroke:").grid(row=0, column=2, padx=2)
        self.stroke_color_btn = tk.Button(current_colors, bg="#FFFFFF", width=5, height=2,
                                         command=self.choose_stroke_color)
        self.stroke_color_btn.grid(row=0, column=3, padx=2)
        
        # Color palette grid
        palette_grid = ttk.Frame(color_frame)
        palette_grid.pack(pady=5)
        
        for i, color in enumerate(self.color_palette):
            row, col = i // 3, i % 3
            btn = tk.Button(palette_grid, bg=color, width=4, height=1,
                           command=lambda c=color: self.set_fill_color(c))
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Typography
        typography_frame = ttk.LabelFrame(props_panel, text="📝 Typography")
        typography_frame.pack(fill='x', padx=5, pady=5)
        
        # Font selection
        ttk.Label(typography_frame, text="Font:").pack(anchor='w', padx=5)
        self.font_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(typography_frame, textvariable=self.font_var, width=15,
                                 values=["Arial", "Times", "Helvetica", "Courier", "Comic Sans", 
                                        "Georgia", "Verdana", "Trebuchet MS"])
        font_combo.pack(fill='x', padx=5, pady=2)
        
        # Font size
        font_controls = ttk.Frame(typography_frame)
        font_controls.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(font_controls, text="Size:").pack(side='left')
        self.font_size_var = tk.IntVar(value=16)
        ttk.Spinbox(font_controls, from_=8, to=72, width=5, textvariable=self.font_size_var).pack(side='left', padx=5)
        
        # Font style
        style_frame = ttk.Frame(typography_frame)
        style_frame.pack(fill='x', padx=5, pady=2)
        
        self.bold_var = tk.BooleanVar()
        self.italic_var = tk.BooleanVar()
        self.underline_var = tk.BooleanVar()
        
        ttk.Checkbutton(style_frame, text="B", variable=self.bold_var, width=3).pack(side='left', padx=1)
        ttk.Checkbutton(style_frame, text="I", variable=self.italic_var, width=3).pack(side='left', padx=1)
        ttk.Checkbutton(style_frame, text="U", variable=self.underline_var, width=3).pack(side='left', padx=1)
        
        # Alignment
        align_frame = ttk.Frame(typography_frame)
        align_frame.pack(fill='x', padx=5, pady=2)
        
        self.align_var = tk.StringVar(value="left")
        ttk.Radiobutton(align_frame, text="⬅️", variable=self.align_var, value="left", width=4).pack(side='left')
        ttk.Radiobutton(align_frame, text="⬆️", variable=self.align_var, value="center", width=4).pack(side='left')
        ttk.Radiobutton(align_frame, text="➡️", variable=self.align_var, value="right", width=4).pack(side='left')
        
        # Transform properties
        transform_frame = ttk.LabelFrame(props_panel, text="🔄 Transform")
        transform_frame.pack(fill='x', padx=5, pady=5)
        
        # Position
        ttk.Label(transform_frame, text="Position:").pack(anchor='w', padx=5)
        pos_frame = ttk.Frame(transform_frame)
        pos_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(pos_frame, text="X:").pack(side='left')
        self.x_pos_var = tk.StringVar()
        ttk.Entry(pos_frame, textvariable=self.x_pos_var, width=8).pack(side='left', padx=2)
        
        ttk.Label(pos_frame, text="Y:").pack(side='left', padx=(5,0))
        self.y_pos_var = tk.StringVar()
        ttk.Entry(pos_frame, textvariable=self.y_pos_var, width=8).pack(side='left', padx=2)
        
        # Size
        ttk.Label(transform_frame, text="Size:").pack(anchor='w', padx=5)
        size_frame = ttk.Frame(transform_frame)
        size_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(size_frame, text="W:").pack(side='left')
        self.width_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.width_var, width=8).pack(side='left', padx=2)
        
        ttk.Label(size_frame, text="H:").pack(side='left', padx=(5,0))
        self.height_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.height_var, width=8).pack(side='left', padx=2)
        
        # Rotation and effects
        ttk.Label(transform_frame, text="Rotation:").pack(anchor='w', padx=5)
        self.rotation_var = tk.IntVar(value=0)
        ttk.Scale(transform_frame, from_=-180, to=180, orient='horizontal',
                 variable=self.rotation_var).pack(fill='x', padx=5, pady=2)
        
        ttk.Label(transform_frame, text="Opacity:").pack(anchor='w', padx=5)
        self.opacity_var = tk.IntVar(value=100)
        ttk.Scale(transform_frame, from_=0, to=100, orient='horizontal',
                 variable=self.opacity_var).pack(fill='x', padx=5, pady=2)
        
        # Layers panel
        layers_frame = ttk.LabelFrame(props_panel, text="📚 Layers")
        layers_frame.pack(fill='x', padx=5, pady=5)
        
        # Layer listbox
        self.layers_listbox = tk.Listbox(layers_frame, height=6)
        self.layers_listbox.pack(fill='x', padx=5, pady=5)
        
        # Layer controls
        layer_controls = ttk.Frame(layers_frame)
        layer_controls.pack(fill='x', padx=5)
        
        ttk.Button(layer_controls, text="➕", command=self.add_layer, width=3).pack(side='left', padx=1)
        ttk.Button(layer_controls, text="➖", command=self.delete_layer, width=3).pack(side='left', padx=1)
        ttk.Button(layer_controls, text="⬆️", command=self.move_layer_up, width=3).pack(side='left', padx=1)
        ttk.Button(layer_controls, text="⬇️", command=self.move_layer_down, width=3).pack(side='left', padx=1)
        
        # Initialize layers
        self.update_layers_display()
        
    def setup_templates_tab(self):
        """Setup the design templates tab."""
        templates_frame = ttk.Frame(self.notebook)
        self.notebook.add(templates_frame, text="📋 Templates")
        
        # Template categories
        category_frame = ttk.LabelFrame(templates_frame, text="📂 Categories")
        category_frame.pack(fill='x', padx=5, pady=5)
        
        categories = [
            "🎪 Posters", "📄 Flyers", "💼 Business Cards", "📊 Infographics", 
            "🎓 Certificates", "📱 Social Media", "🏷️ Labels", "📖 Brochures"
        ]
        
        self.category_var = tk.StringVar(value="🎪 Posters")
        
        for category in categories:
            ttk.Radiobutton(category_frame, text=category, variable=self.category_var,
                           value=category, command=self.load_category_templates).pack(side='left', padx=5)
        
        # Templates display
        templates_display = ttk.LabelFrame(templates_frame, text="🎨 Template Gallery")
        templates_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create template grid
        templates_container = ttk.Frame(templates_display)
        templates_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.templates_canvas = tk.Canvas(templates_container, bg='white')
        templates_scrollbar = ttk.Scrollbar(templates_container, orient='vertical', command=self.templates_canvas.yview)
        self.templates_canvas.configure(yscrollcommand=templates_scrollbar.set)
        
        self.templates_canvas.pack(side='left', fill='both', expand=True)
        templates_scrollbar.pack(side='right', fill='y')
        
        # Load initial templates
        self.load_category_templates()
        
        # Template info panel
        template_info = ttk.LabelFrame(templates_frame, text="ℹ️ Template Info")
        template_info.pack(fill='x', padx=5, pady=5)
        
        info_content = ttk.Frame(template_info)
        info_content.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(info_content, text="Selected Template:").pack(side='left', padx=5)
        self.selected_template_label = ttk.Label(info_content, text="None")
        self.selected_template_label.pack(side='left', padx=5)
        
        ttk.Button(info_content, text="🎨 Use Template", 
                  command=self.use_selected_template).pack(side='right', padx=5)
        ttk.Button(info_content, text="👁️ Preview", 
                  command=self.preview_template).pack(side='right', padx=5)
        
    def setup_typography_tab(self):
        """Setup the typography and text design tab."""
        typography_frame = ttk.Frame(self.notebook)
        self.notebook.add(typography_frame, text="📝 Typography")
        
        # Typography controls
        typo_controls = ttk.LabelFrame(typography_frame, text="🎯 Text Controls")
        typo_controls.pack(fill='x', padx=5, pady=5)
        
        # Text input
        text_input_frame = ttk.Frame(typo_controls)
        text_input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(text_input_frame, text="Text:").pack(side='left', padx=5)
        self.text_input = tk.Text(text_input_frame, height=3, width=50)
        self.text_input.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(text_input_frame, text="➕ Add Text", 
                  command=self.add_text_element).pack(side='right', padx=5)
        
        # Font showcase
        font_showcase = ttk.LabelFrame(typography_frame, text="🎨 Font Showcase")
        font_showcase.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Font families
        font_families = ttk.Frame(font_showcase)
        font_families.pack(side='left', fill='y', padx=5, pady=5)
        
        ttk.Label(font_families, text="Font Families:").pack(anchor='w')
        
        fonts = [
            ("Arial", "clean, modern sans-serif"),
            ("Times New Roman", "traditional serif"),
            ("Helvetica", "professional sans-serif"),
            ("Georgia", "readable serif for web"),
            ("Verdana", "screen-optimized sans-serif"),
            ("Comic Sans MS", "casual, playful"),
            ("Trebuchet MS", "contemporary sans-serif"),
            ("Courier New", "monospace typewriter"),
        ]
        
        self.font_showcase_var = tk.StringVar(value="Arial")
        
        for font, description in fonts:
            frame = ttk.Frame(font_families)
            frame.pack(fill='x', pady=2)
            
            ttk.Radiobutton(frame, text=font, variable=self.font_showcase_var, 
                           value=font, command=self.update_font_preview).pack(side='left')
            ttk.Label(frame, text=f"- {description}", font=('Arial', 8)).pack(side='left', padx=10)
        
        # Font preview
        preview_frame = ttk.Frame(font_showcase)
        preview_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="Font Preview:").pack(anchor='w')
        
        self.font_preview_canvas = tk.Canvas(preview_frame, width=400, height=300, bg='white')
        self.font_preview_canvas.pack(fill='both', expand=True, pady=5)
        
        # Typography tips
        tips_frame = ttk.LabelFrame(typography_frame, text="💡 Typography Tips")
        tips_frame.pack(fill='x', padx=5, pady=5)
        
        typography_tips = [
            "🎯 Choose fonts that match your design's mood and purpose",
            "📏 Use consistent spacing between lines and letters", 
            "⚡ Limit to 2-3 font families per design for cohesion",
            "📊 Create visual hierarchy with different font sizes",
            "🎨 Ensure good contrast between text and background",
            "📱 Consider readability at different sizes and distances"
        ]
        
        tips_text = tk.Text(tips_frame, height=4, wrap=tk.WORD, font=('Arial', 10))
        tips_text.pack(fill='x', padx=10, pady=5)
        
        tips_content = "\n".join(typography_tips)
        tips_text.insert(1.0, tips_content)
        tips_text.config(state='disabled')
        
    def setup_branding_tab(self):
        """Setup the branding and logo design tab."""
        branding_frame = ttk.Frame(self.notebook)
        self.notebook.add(branding_frame, text="🏢 Branding")
        
        # Brand elements
        brand_elements = ttk.LabelFrame(branding_frame, text="🎨 Brand Elements")
        brand_elements.pack(fill='x', padx=5, pady=5)
        
        # Logo creation tools
        logo_tools = ttk.Frame(brand_elements)
        logo_tools.pack(side='left', padx=5, pady=5)
        
        ttk.Label(logo_tools, text="Logo Creation:").pack(anchor='w')
        
        logo_types = [
            ("📝 Text Logo", "text_logo"),
            ("🎨 Icon + Text", "icon_text"),
            ("🔷 Symbol Only", "symbol"),
            ("🎭 Mascot", "mascot"),
            ("🌟 Badge", "badge")
        ]
        
        for name, ltype in logo_types:
            ttk.Button(logo_tools, text=name,
                      command=lambda t=ltype: self.create_logo_type(t)).pack(fill='x', pady=2)
        
        # Color schemes
        color_schemes = ttk.Frame(brand_elements)
        color_schemes.pack(side='left', padx=5, pady=5)
        
        ttk.Label(color_schemes, text="Brand Colors:").pack(anchor='w')
        
        # Predefined color schemes
        schemes = [
            ("🔴 Energetic", ["#FF4757", "#FF6B35", "#F8B500"]),
            ("🔵 Professional", ["#2C3E50", "#3498DB", "#95A5A6"]),
            ("🌿 Natural", ["#27AE60", "#2ECC71", "#F39C12"]),
            ("💜 Creative", ["#8E44AD", "#E74C3C", "#F39C12"]),
            ("🖤 Elegant", ["#2C3E50", "#BDC3C7", "#ECF0F1"])
        ]
        
        for name, colors in schemes:
            scheme_frame = ttk.Frame(color_schemes)
            scheme_frame.pack(fill='x', pady=2)
            
            ttk.Label(scheme_frame, text=name, width=12).pack(side='left')
            for color in colors:
                color_btn = tk.Button(scheme_frame, bg=color, width=2, height=1,
                                     command=lambda c=colors: self.apply_color_scheme(c))
                color_btn.pack(side='left', padx=1)
        
        # Brand identity workspace
        brand_workspace = ttk.LabelFrame(branding_frame, text="🎯 Brand Identity Workspace")
        brand_workspace.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Brand canvas
        brand_canvas_frame = ttk.Frame(brand_workspace)
        brand_canvas_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.brand_canvas = tk.Canvas(brand_canvas_frame, width=600, height=400, bg='white')
        self.brand_canvas.pack()
        
        # Brand guidelines panel
        guidelines_frame = ttk.Frame(brand_workspace)
        guidelines_frame.pack(side='right', fill='y', padx=5, pady=5)
        
        ttk.Label(guidelines_frame, text="Brand Guidelines:", font=('Arial', 12, 'bold')).pack(anchor='w')
        
        guidelines_text = """
🎨 VISUAL IDENTITY CHECKLIST:

✓ Logo Design
  • Clear and memorable
  • Works in black & white
  • Scalable (large to small)
  • Reflects brand personality

✓ Color Palette
  • Primary color (main brand color)
  • Secondary colors (2-3 supporting)
  • Accent color (for highlights)
  • Neutral colors (backgrounds)

✓ Typography
  • Primary font (headers, logo)
  • Secondary font (body text)
  • Consistent sizing system
  • Good readability

✓ Style Elements
  • Consistent shapes/patterns
  • Image treatment style
  • Icon style guidelines
  • Spacing and layout rules

💡 BRAND PERSONALITY:
Consider your target audience and the
feeling you want to convey:
• Professional vs. Playful
• Modern vs. Traditional  
• Bold vs. Subtle
• Friendly vs. Serious
        """
        
        guidelines_display = tk.Text(guidelines_frame, width=30, height=20, wrap=tk.WORD, 
                                   font=('Arial', 9))
        guidelines_display.pack(fill='both', expand=True)
        guidelines_display.insert(1.0, guidelines_text)
        guidelines_display.config(state='disabled')
        
    def setup_portfolio_tab(self):
        """Setup the portfolio and showcase tab."""
        portfolio_frame = ttk.Frame(self.notebook)
        self.notebook.add(portfolio_frame, text="🏆 Portfolio")
        
        # Portfolio controls
        portfolio_controls = ttk.LabelFrame(portfolio_frame, text="📁 Portfolio Management")
        portfolio_controls.pack(fill='x', padx=5, pady=5)
        
        controls_frame = ttk.Frame(portfolio_controls)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(controls_frame, text="➕ Add Project", 
                  command=self.add_to_portfolio).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="📁 Organize", 
                  command=self.organize_portfolio).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="🌐 Export Website", 
                  command=self.export_portfolio_website).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="📄 Export PDF", 
                  command=self.export_portfolio_pdf).pack(side='left', padx=5)
        
        # Portfolio display
        portfolio_display = ttk.LabelFrame(portfolio_frame, text="🎨 Your Design Portfolio")
        portfolio_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Portfolio grid
        portfolio_container = ttk.Frame(portfolio_display)
        portfolio_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.portfolio_canvas = tk.Canvas(portfolio_container, bg='lightgray')
        portfolio_scrollbar = ttk.Scrollbar(portfolio_container, orient='vertical', command=self.portfolio_canvas.yview)
        self.portfolio_canvas.configure(yscrollcommand=portfolio_scrollbar.set)
        
        self.portfolio_canvas.pack(side='left', fill='both', expand=True)
        portfolio_scrollbar.pack(side='right', fill='y')
        
        # Load sample portfolio items
        self.load_sample_portfolio()
        
        # Portfolio statistics
        stats_frame = ttk.LabelFrame(portfolio_frame, text="📊 Portfolio Statistics")
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        stats_content = ttk.Frame(stats_frame)
        stats_content.pack(fill='x', padx=10, pady=5)
        
        # Sample statistics
        stats = [
            ("Total Projects:", "12"),
            ("Completed This Month:", "3"),
            ("Favorite Style:", "Modern Minimalist"),
            ("Most Used Colors:", "Blue, White, Gray"),
            ("Portfolio Views:", "247")
        ]
        
        for label, value in stats:
            stat_frame = ttk.Frame(stats_content)
            stat_frame.pack(fill='x', pady=2)
            
            ttk.Label(stat_frame, text=label, font=('Arial', 10)).pack(side='left')
            ttk.Label(stat_frame, text=value, font=('Arial', 10, 'bold')).pack(side='right')
    
    def load_design_templates(self):
        """Load sample design templates."""
        return {
            "🎪 Posters": [
                {"name": "Event Poster", "style": "Modern", "colors": ["#FF6B6B", "#4ECDC4"]},
                {"name": "Concert Flyer", "style": "Vintage", "colors": ["#F39C12", "#E74C3C"]},
                {"name": "Movie Poster", "style": "Cinematic", "colors": ["#2C3E50", "#E74C3C"]}
            ],
            "💼 Business Cards": [
                {"name": "Professional", "style": "Clean", "colors": ["#2C3E50", "#3498DB"]},
                {"name": "Creative", "style": "Artistic", "colors": ["#8E44AD", "#E74C3C"]},
                {"name": "Minimalist", "style": "Simple", "colors": ["#34495E", "#BDC3C7"]}
            ]
        }
    
    def load_sample_portfolio(self):
        """Load sample portfolio items."""
        sample_projects = [
            {"name": "School Event Poster", "type": "Poster", "date": "2025-09-15"},
            {"name": "Club Logo Design", "type": "Logo", "date": "2025-09-10"},
            {"name": "Science Fair Flyer", "type": "Flyer", "date": "2025-09-05"},
            {"name": "Student ID Card", "type": "Card", "date": "2025-08-30"},
            {"name": "Newsletter Header", "type": "Banner", "date": "2025-08-25"},
            {"name": "Sports Team Badge", "type": "Logo", "date": "2025-08-20"}
        ]
        
        # Create portfolio grid
        row, col = 0, 0
        for i, project in enumerate(sample_projects):
            x = col * 150 + 20
            y = row * 120 + 20
            
            # Project thumbnail
            rect = self.portfolio_canvas.create_rectangle(x, y, x+120, y+90, 
                                                         fill='white', outline='gray')
            
            # Project type icon
            type_icons = {"Poster": "📄", "Logo": "🏷️", "Flyer": "📃", 
                         "Card": "💳", "Banner": "🏁", "Badge": "🎖️"}
            icon = type_icons.get(project["type"], "🎨")
            
            self.portfolio_canvas.create_text(x+60, y+30, text=icon, font=('Arial', 20))
            self.portfolio_canvas.create_text(x+60, y+60, text=project["name"], 
                                             font=('Arial', 8), width=110)
            self.portfolio_canvas.create_text(x+60, y+80, text=project["date"], 
                                             font=('Arial', 7), fill='gray')
            
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        # Update scroll region
        self.portfolio_canvas.configure(scrollregion=self.portfolio_canvas.bbox("all"))
    
    def run(self):
        """Start the graphic design studio application."""
        self.root.mainloop()

def main():
    """Main function to run the graphic design studio."""
    print("🎨 Graphic Design Studio")
    print("=" * 25)
    print("🎯 Create professional designs and branding")
    print("📚 Learn graphic design principles")
    print()
    print("Starting Design Studio...")
    
    studio = GraphicDesignStudio()
    studio.run()

if __name__ == "__main__":
    main()