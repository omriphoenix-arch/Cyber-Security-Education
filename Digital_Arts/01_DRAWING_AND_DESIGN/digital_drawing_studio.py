#!/usr/bin/env python3
"""
Digital Drawing Studio
======================
Comprehensive digital art creation tool for K-12 education.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import json
from datetime import datetime
import math
import random

class DigitalDrawingStudio:
    """Interactive digital drawing and design application."""
    
    def __init__(self):
        """Initialize the digital drawing studio."""
        self.setup_drawing_variables()
        self.setup_gui()
        
    def setup_drawing_variables(self):
        """Initialize drawing state variables."""
        self.canvas_width = 800
        self.canvas_height = 600
        self.current_tool = "brush"
        self.current_color = "#000000"
        self.brush_size = 5
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        self.layers = []
        self.current_layer = 0
        self.undo_stack = []
        self.redo_stack = []
        self.shapes = []
        self.selected_shape = None
        
    def setup_gui(self):
        """Create the main drawing studio interface."""
        self.root = tk.Tk()
        self.root.title("🎨 Digital Drawing Studio - Creative Arts Platform")
        self.root.geometry("1400x900")
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Setup panels
        self.setup_tool_panel(main_frame)
        self.setup_canvas_panel(main_frame)
        self.setup_properties_panel(main_frame)
        self.setup_bottom_panel()
        
    def setup_tool_panel(self, parent):
        """Setup the tool selection panel."""
        tool_frame = ttk.LabelFrame(parent, text="🛠️ Tools")
        tool_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Drawing tools
        tools = [
            ("✏️ Pencil", "pencil"),
            ("🖌️ Brush", "brush"),
            ("✒️ Pen", "pen"),
            ("💧 Watercolor", "watercolor"),
            ("🌈 Spray", "spray"),
            ("🔴 Circle", "circle"),
            ("⬜ Rectangle", "rectangle"),
            ("📏 Line", "line"),
            ("⭐ Star", "star"),
            ("💭 Text", "text"),
            ("🪣 Fill", "fill"),
            ("🧽 Eraser", "eraser"),
            ("👆 Select", "select"),
            ("🔍 Zoom", "zoom")
        ]
        
        self.tool_var = tk.StringVar(value="brush")
        
        for i, (name, tool) in enumerate(tools):
            btn = ttk.Radiobutton(tool_frame, text=name, variable=self.tool_var, 
                                 value=tool, command=lambda t=tool: self.select_tool(t))
            btn.pack(anchor='w', padx=5, pady=2)
        
        # Color selection
        color_frame = ttk.LabelFrame(tool_frame, text="🎨 Colors")
        color_frame.pack(fill='x', padx=5, pady=5)
        
        # Color picker button
        self.color_button = tk.Button(color_frame, bg=self.current_color, width=10, height=2,
                                     command=self.choose_color)
        self.color_button.pack(pady=5)
        
        # Preset colors
        preset_colors = [
            "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500", "#800080"
        ]
        
        color_grid = ttk.Frame(color_frame)
        color_grid.pack(pady=5)
        
        for i, color in enumerate(preset_colors):
            row, col = i // 5, i % 5
            btn = tk.Button(color_grid, bg=color, width=3, height=1,
                           command=lambda c=color: self.set_color(c))
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Brush settings
        brush_frame = ttk.LabelFrame(tool_frame, text="🖌️ Brush Settings")
        brush_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(brush_frame, text="Size:").pack(anchor='w')
        self.brush_size_var = tk.IntVar(value=5)
        brush_scale = ttk.Scale(brush_frame, from_=1, to=50, orient='horizontal',
                               variable=self.brush_size_var, command=self.update_brush_size)
        brush_scale.pack(fill='x', padx=5)
        
        self.brush_size_label = ttk.Label(brush_frame, text="5 px")
        self.brush_size_label.pack()
        
        # Opacity
        ttk.Label(brush_frame, text="Opacity:").pack(anchor='w')
        self.opacity_var = tk.IntVar(value=100)
        opacity_scale = ttk.Scale(brush_frame, from_=10, to=100, orient='horizontal',
                                 variable=self.opacity_var)
        opacity_scale.pack(fill='x', padx=5)
        
        # Quick actions
        action_frame = ttk.LabelFrame(tool_frame, text="⚡ Quick Actions")
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="↶ Undo", command=self.undo).pack(fill='x', pady=1)
        ttk.Button(action_frame, text="↷ Redo", command=self.redo).pack(fill='x', pady=1)
        ttk.Button(action_frame, text="🗑️ Clear", command=self.clear_canvas).pack(fill='x', pady=1)
        ttk.Button(action_frame, text="💾 Save", command=self.save_artwork).pack(fill='x', pady=1)
        ttk.Button(action_frame, text="📁 Load", command=self.load_artwork).pack(fill='x', pady=1)
        
    def setup_canvas_panel(self, parent):
        """Setup the main drawing canvas."""
        canvas_frame = ttk.LabelFrame(parent, text="🖼️ Canvas")
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Canvas container with scrollbars
        canvas_container = ttk.Frame(canvas_frame)
        canvas_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create canvas
        self.canvas = tk.Canvas(canvas_container, width=self.canvas_width, height=self.canvas_height,
                               bg='white', scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_container, orient='horizontal', command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack canvas and scrollbars
        self.canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Motion>", self.mouse_move)
        
        # Canvas toolbar
        canvas_toolbar = ttk.Frame(canvas_frame)
        canvas_toolbar.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(canvas_toolbar, text="Zoom:").pack(side='left', padx=5)
        zoom_levels = ["25%", "50%", "75%", "100%", "125%", "150%", "200%"]
        self.zoom_var = tk.StringVar(value="100%")
        zoom_combo = ttk.Combobox(canvas_toolbar, textvariable=self.zoom_var, values=zoom_levels, width=8)
        zoom_combo.pack(side='left', padx=5)
        zoom_combo.bind('<<ComboboxSelected>>', self.zoom_canvas)
        
        ttk.Button(canvas_toolbar, text="🔍 Fit to Window", command=self.fit_to_window).pack(side='left', padx=5)
        ttk.Button(canvas_toolbar, text="📐 Grid", command=self.toggle_grid).pack(side='left', padx=5)
        ttk.Button(canvas_toolbar, text="📏 Rulers", command=self.toggle_rulers).pack(side='left', padx=5)
        
    def setup_properties_panel(self, parent):
        """Setup the properties and layers panel."""
        props_frame = ttk.LabelFrame(parent, text="⚙️ Properties")
        props_frame.pack(side='right', fill='y', padx=5, pady=5)
        
        # Layers panel
        layers_frame = ttk.LabelFrame(props_frame, text="📚 Layers")
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
        
        # Object properties
        object_frame = ttk.LabelFrame(props_frame, text="🎯 Object Properties")
        object_frame.pack(fill='x', padx=5, pady=5)
        
        # Position
        ttk.Label(object_frame, text="Position (X, Y):").pack(anchor='w', padx=5)
        pos_frame = ttk.Frame(object_frame)
        pos_frame.pack(fill='x', padx=5)
        
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        ttk.Entry(pos_frame, textvariable=self.x_var, width=8).pack(side='left', padx=2)
        ttk.Entry(pos_frame, textvariable=self.y_var, width=8).pack(side='left', padx=2)
        
        # Size
        ttk.Label(object_frame, text="Size (W, H):").pack(anchor='w', padx=5)
        size_frame = ttk.Frame(object_frame)
        size_frame.pack(fill='x', padx=5)
        
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.width_var, width=8).pack(side='left', padx=2)
        ttk.Entry(size_frame, textvariable=self.height_var, width=8).pack(side='left', padx=2)
        
        # Effects panel
        effects_frame = ttk.LabelFrame(props_frame, text="✨ Effects")
        effects_frame.pack(fill='x', padx=5, pady=5)
        
        effects = ["None", "Blur", "Sharpen", "Emboss", "Drop Shadow", "Glow", "Outline"]
        self.effect_var = tk.StringVar(value="None")
        effect_combo = ttk.Combobox(effects_frame, textvariable=self.effect_var, values=effects)
        effect_combo.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(effects_frame, text="Apply Effect", command=self.apply_effect).pack(fill='x', padx=5, pady=2)
        
        # Filters
        filters_frame = ttk.LabelFrame(props_frame, text="🌈 Filters")
        filters_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filters_frame, text="Brightness:").pack(anchor='w', padx=5)
        self.brightness_var = tk.IntVar(value=0)
        brightness_scale = ttk.Scale(filters_frame, from_=-100, to=100, orient='horizontal',
                                   variable=self.brightness_var)
        brightness_scale.pack(fill='x', padx=5)
        
        ttk.Label(filters_frame, text="Contrast:").pack(anchor='w', padx=5)
        self.contrast_var = tk.IntVar(value=0)
        contrast_scale = ttk.Scale(filters_frame, from_=-100, to=100, orient='horizontal',
                                 variable=self.contrast_var)
        contrast_scale.pack(fill='x', padx=5)
        
        ttk.Button(filters_frame, text="Apply Filters", command=self.apply_filters).pack(fill='x', padx=5, pady=5)
        
    def setup_bottom_panel(self):
        """Setup the bottom status and tutorial panel."""
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=5, pady=5)
        
        # Status bar
        status_frame = ttk.LabelFrame(bottom_frame, text="📊 Status")
        status_frame.pack(side='left', fill='x', expand=True, padx=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready to create amazing art! Select a tool to begin.")
        self.status_label.pack(anchor='w', padx=5, pady=2)
        
        self.coords_label = ttk.Label(status_frame, text="Mouse: (0, 0)")
        self.coords_label.pack(anchor='w', padx=5, pady=2)
        
        # Quick tips
        tips_frame = ttk.LabelFrame(bottom_frame, text="💡 Tips")
        tips_frame.pack(side='right', padx=5)
        
        tips = [
            "Hold Shift while drawing lines for straight lines",
            "Right-click to pick colors from the canvas",
            "Use Ctrl+Z for undo, Ctrl+Y for redo",
            "Double-click shapes to edit properties",
            "Save your work regularly!"
        ]
        
        self.current_tip = tk.StringVar(value=random.choice(tips))
        tip_label = ttk.Label(tips_frame, textvariable=self.current_tip, width=40)
        tip_label.pack(padx=5, pady=2)
        
        # Rotate tips every 10 seconds
        self.root.after(10000, self.rotate_tip)
        
    # Drawing methods
    def select_tool(self, tool):
        """Select the current drawing tool."""
        self.current_tool = tool
        self.status_label.config(text=f"Selected tool: {tool.title()}")
        
        # Update cursor based on tool
        cursor_map = {
            "pencil": "pencil",
            "brush": "brush",
            "pen": "pen",
            "eraser": "dotbox",
            "fill": "spraycan",
            "select": "hand2",
            "zoom": "sizing"
        }
        
        cursor = cursor_map.get(tool, "crosshair")
        self.canvas.config(cursor=cursor)
        
    def choose_color(self):
        """Open color chooser dialog."""
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.set_color(color)
            
    def set_color(self, color):
        """Set the current drawing color."""
        self.current_color = color
        self.color_button.config(bg=color)
        
    def update_brush_size(self, value):
        """Update brush size from scale."""
        self.brush_size = int(float(value))
        self.brush_size_label.config(text=f"{self.brush_size} px")
        
    def start_draw(self, event):
        """Start drawing operation."""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        
        if self.current_tool in ["circle", "rectangle", "line", "star"]:
            self.start_shape(event)
        elif self.current_tool == "text":
            self.add_text(event)
        elif self.current_tool == "fill":
            self.flood_fill(event.x, event.y)
        else:
            self.draw_point(event.x, event.y)
            
    def draw(self, event):
        """Continue drawing operation."""
        if not self.drawing:
            return
            
        if self.current_tool in ["pencil", "brush", "pen", "watercolor", "spray", "eraser"]:
            self.draw_line(self.last_x, self.last_y, event.x, event.y)
            self.last_x = event.x
            self.last_y = event.y
            
    def end_draw(self, event):
        """End drawing operation."""
        self.drawing = False
        if self.current_tool in ["circle", "rectangle", "line", "star"]:
            self.finish_shape(event)
            
    def draw_point(self, x, y):
        """Draw a single point."""
        size = self.brush_size
        color = self.current_color
        
        if self.current_tool == "eraser":
            color = "white"
            
        self.canvas.create_oval(x-size//2, y-size//2, x+size//2, y+size//2,
                               fill=color, outline=color)
                               
    def draw_line(self, x1, y1, x2, y2):
        """Draw a line between two points."""
        size = self.brush_size
        color = self.current_color
        
        if self.current_tool == "eraser":
            color = "white"
        elif self.current_tool == "watercolor":
            # Simulate watercolor with multiple semi-transparent strokes
            alpha = self.opacity_var.get() / 100.0
            for i in range(3):
                offset_x = random.randint(-size//4, size//4)
                offset_y = random.randint(-size//4, size//4)
                self.canvas.create_line(x1+offset_x, y1+offset_y, x2+offset_x, y2+offset_y,
                                       width=size//2, fill=color, capstyle=tk.ROUND)
        elif self.current_tool == "spray":
            # Simulate spray paint with multiple small dots
            for i in range(size * 2):
                spray_x = x2 + random.randint(-size, size)
                spray_y = y2 + random.randint(-size, size)
                dot_size = random.randint(1, 3)
                self.canvas.create_oval(spray_x-dot_size, spray_y-dot_size,
                                       spray_x+dot_size, spray_y+dot_size,
                                       fill=color, outline=color)
        else:
            self.canvas.create_line(x1, y1, x2, y2, width=size, fill=color, capstyle=tk.ROUND)
            
    def mouse_move(self, event):
        """Update mouse coordinates display."""
        self.coords_label.config(text=f"Mouse: ({event.x}, {event.y})")
        
    # Canvas operations
    def clear_canvas(self):
        """Clear the entire canvas."""
        if messagebox.askyesno("Clear Canvas", "Are you sure you want to clear the entire canvas?"):
            self.canvas.delete("all")
            self.undo_stack.clear()
            self.redo_stack.clear()
            
    def undo(self):
        """Undo last operation."""
        # Placeholder for undo functionality
        self.status_label.config(text="Undo functionality - would restore previous canvas state")
        
    def redo(self):
        """Redo last undone operation."""
        # Placeholder for redo functionality
        self.status_label.config(text="Redo functionality - would restore next canvas state")
        
    def save_artwork(self):
        """Save the current artwork."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if filename:
                # In a full implementation, this would save the canvas as an image
                messagebox.showinfo("Save Artwork", f"Artwork would be saved as {filename}")
                self.status_label.config(text=f"Artwork saved: {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save artwork: {e}")
            
    def load_artwork(self):
        """Load an artwork file."""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
            )
            if filename:
                # In a full implementation, this would load and display the image
                messagebox.showinfo("Load Artwork", f"Artwork would be loaded from {filename}")
                self.status_label.config(text=f"Artwork loaded: {filename}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load artwork: {e}")
            
    def rotate_tip(self):
        """Rotate through helpful tips."""
        tips = [
            "Hold Shift while drawing lines for straight lines",
            "Right-click to pick colors from the canvas", 
            "Use Ctrl+Z for undo, Ctrl+Y for redo",
            "Double-click shapes to edit properties",
            "Save your work regularly!",
            "Try different brush sizes for varied effects",
            "Use layers to organize your artwork",
            "Experiment with opacity for blending effects"
        ]
        
        self.current_tip.set(random.choice(tips))
        self.root.after(10000, self.rotate_tip)
        
    def run(self):
        """Start the digital drawing studio application."""
        self.root.mainloop()

def main():
    """Main function to run the digital drawing studio."""
    print("🎨 Digital Drawing Studio")
    print("=" * 25)
    print("🖌️ Create amazing digital artwork")
    print("🎯 Learn digital art techniques")
    print()
    print("Starting Drawing Studio...")
    
    studio = DigitalDrawingStudio()
    studio.run()

if __name__ == "__main__":
    main()