#!/usr/bin/env python3
"""
Interactive Math Studio - K-12 Mathematics Learning Platform
A comprehensive visual math learning tool with interactive manipulatives and demonstrations
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import random
from datetime import datetime
import json

class InteractiveMathStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Math Studio - Visual Mathematics Learning")
        self.root.geometry("1400x900")
        
        # Student data
        self.student_name = "Student"
        self.student_level = "Elementary"
        self.points = 0
        self.achievements = []
        
        # Color scheme
        self.bg_color = "#f0f4f8"
        self.primary_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_ui()
        self.load_student_data()
        
    def create_ui(self):
        """Create the main user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🔢 Interactive Math Studio",
                              font=("Arial", 24, "bold"), bg=self.primary_color, fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Student info
        self.info_label = tk.Label(header_frame, text=f"👤 {self.student_name} | ⭐ {self.points} pts",
                                   font=("Arial", 12), bg=self.primary_color, fg="white")
        self.info_label.pack(side=tk.RIGHT, padx=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Activity selection
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        
        tk.Label(left_panel, text="📚 Math Activities", font=("Arial", 16, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        # Activity buttons
        activities = [
            ("🔢 Number Line Explorer", self.show_number_line),
            ("➕ Addition & Subtraction", self.show_addition),
            ("✖️ Multiplication Tables", self.show_multiplication),
            ("📊 Fraction Visualizer", self.show_fractions),
            ("📐 Shape Explorer", self.show_shapes),
            ("📈 Graphing Calculator", self.show_graphing),
            ("🎲 Math Games", self.show_games),
            ("📊 Progress Tracker", self.show_progress)
        ]
        
        for text, command in activities:
            btn = tk.Button(left_panel, text=text, font=("Arial", 11),
                          bg=self.accent_color, fg="white",
                          command=command, width=25, height=2)
            btn.pack(pady=5, padx=10)
        
        # Right panel - Activity area
        self.activity_frame = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=2)
        self.activity_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.show_welcome()
        
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_activity_frame()
        
        welcome_frame = tk.Frame(self.activity_frame, bg="white")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(welcome_frame, text="Welcome to Interactive Math Studio! 🎉",
                font=("Arial", 22, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        intro_text = """
        Explore mathematics through interactive visualizations and hands-on activities!
        
        ✨ Features:
        • Visual number line for understanding operations
        • Interactive fraction models
        • Geometric shape exploration
        • Graphing and coordinate systems
        • Engaging math games and challenges
        • Real-time progress tracking
        
        🎯 Learning Objectives:
        • Build number sense and fluency
        • Understand mathematical relationships
        • Visualize abstract concepts
        • Develop problem-solving skills
        
        Select an activity from the left menu to begin your mathematical journey!
        """
        
        tk.Label(welcome_frame, text=intro_text, font=("Arial", 12),
                bg="white", fg=self.primary_color, justify=tk.LEFT).pack(pady=20)
        
        # Quick start buttons
        quick_frame = tk.Frame(welcome_frame, bg="white")
        quick_frame.pack(pady=20)
        
        tk.Button(quick_frame, text="🎮 Start with Games", font=("Arial", 12, "bold"),
                 bg=self.success_color, fg="white", command=self.show_games,
                 width=20, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(quick_frame, text="📊 View Progress", font=("Arial", 12, "bold"),
                 bg=self.accent_color, fg="white", command=self.show_progress,
                 width=20, height=2).pack(side=tk.LEFT, padx=10)
    
    def show_number_line(self):
        """Interactive number line activity"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="🔢 Number Line Explorer",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        # Canvas for number line
        canvas_frame = tk.Frame(self.activity_frame, bg="white")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.number_canvas = tk.Canvas(canvas_frame, bg="white", height=200)
        self.number_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Controls
        control_frame = tk.Frame(self.activity_frame, bg="white")
        control_frame.pack(pady=20)
        
        tk.Label(control_frame, text="Start:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.start_var = tk.StringVar(value="0")
        tk.Entry(control_frame, textvariable=self.start_var, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="End:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.end_var = tk.StringVar(value="10")
        tk.Entry(control_frame, textvariable=self.end_var, width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Draw Number Line", font=("Arial", 11),
                 bg=self.accent_color, fg="white",
                 command=self.draw_number_line).pack(side=tk.LEFT, padx=10)
        
        # Operation controls
        op_frame = tk.Frame(self.activity_frame, bg="white")
        op_frame.pack(pady=10)
        
        tk.Label(op_frame, text="Demonstrate:", font=("Arial", 11, "bold"), bg="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(op_frame, text="Add 3", bg=self.success_color, fg="white",
                 command=lambda: self.demonstrate_operation("add", 3)).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="Subtract 2", bg=self.warning_color, fg="white",
                 command=lambda: self.demonstrate_operation("subtract", 2)).pack(side=tk.LEFT, padx=5)
        
        self.draw_number_line()
    
    def draw_number_line(self):
        """Draw an interactive number line"""
        try:
            start = int(self.start_var.get())
            end = int(self.end_var.get())
        except:
            messagebox.showerror("Error", "Please enter valid numbers")
            return
        
        self.number_canvas.delete("all")
        
        width = self.number_canvas.winfo_width() - 100
        height = self.number_canvas.winfo_height()
        
        if width < 100:
            width = 800
        
        y_pos = height // 2
        x_start = 50
        x_end = x_start + width
        
        # Draw main line
        self.number_canvas.create_line(x_start, y_pos, x_end, y_pos, width=3, fill=self.primary_color)
        
        # Draw tick marks and labels
        num_range = end - start
        if num_range > 0:
            spacing = width / num_range
            
            for i in range(num_range + 1):
                x = x_start + (i * spacing)
                num = start + i
                
                # Tick mark
                self.number_canvas.create_line(x, y_pos - 10, x, y_pos + 10,
                                              width=2, fill=self.primary_color)
                
                # Number label
                self.number_canvas.create_text(x, y_pos + 30, text=str(num),
                                              font=("Arial", 12, "bold"), fill=self.primary_color)
    
    def demonstrate_operation(self, operation, value):
        """Demonstrate arithmetic operation on number line"""
        messagebox.showinfo("Demo", f"Demonstrating {operation} {value} on the number line!")
        self.add_points(5)
    
    def show_addition(self):
        """Addition and subtraction practice"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="➕ Addition & Subtraction Practice",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        # Problem display
        self.problem_frame = tk.Frame(self.activity_frame, bg="white")
        self.problem_frame.pack(pady=30)
        
        self.problem_label = tk.Label(self.problem_frame, text="", font=("Arial", 32, "bold"),
                                      bg="white", fg=self.primary_color)
        self.problem_label.pack()
        
        # Answer input
        answer_frame = tk.Frame(self.activity_frame, bg="white")
        answer_frame.pack(pady=20)
        
        tk.Label(answer_frame, text="Your Answer:", font=("Arial", 14), bg="white").pack(side=tk.LEFT, padx=10)
        
        self.answer_var = tk.StringVar()
        answer_entry = tk.Entry(answer_frame, textvariable=self.answer_var,
                               font=("Arial", 18), width=10)
        answer_entry.pack(side=tk.LEFT, padx=10)
        answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        tk.Button(answer_frame, text="Check", font=("Arial", 12, "bold"),
                 bg=self.success_color, fg="white",
                 command=self.check_answer, width=10).pack(side=tk.LEFT, padx=10)
        
        # Result display
        self.result_label = tk.Label(self.activity_frame, text="", font=("Arial", 16, "bold"),
                                     bg="white")
        self.result_label.pack(pady=20)
        
        # Level selection
        level_frame = tk.Frame(self.activity_frame, bg="white")
        level_frame.pack(pady=20)
        
        tk.Label(level_frame, text="Difficulty:", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulties = ["Easy (1-10)", "Medium (1-50)", "Hard (1-100)", "Expert (1-1000)"]
        difficulty_menu = ttk.Combobox(level_frame, textvariable=self.difficulty_var,
                                      values=difficulties, state="readonly", width=15)
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Button(level_frame, text="New Problem", font=("Arial", 11),
                 bg=self.accent_color, fg="white",
                 command=self.generate_problem).pack(side=tk.LEFT, padx=10)
        
        # Statistics
        self.stats_label = tk.Label(self.activity_frame, text="Correct: 0 | Incorrect: 0 | Streak: 0",
                                    font=("Arial", 12), bg="white", fg=self.primary_color)
        self.stats_label.pack(pady=10)
        
        self.correct_count = 0
        self.incorrect_count = 0
        self.streak = 0
        self.current_answer = 0
        
        self.generate_problem()
    
    def generate_problem(self):
        """Generate a new math problem"""
        difficulty = self.difficulty_var.get()
        
        if "Easy" in difficulty:
            max_num = 10
        elif "Medium" in difficulty:
            max_num = 50
        elif "Hard" in difficulty:
            max_num = 100
        else:
            max_num = 1000
        
        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            self.current_answer = num1 + num2
            problem_text = f"{num1} + {num2} = ?"
        else:
            # Ensure positive result
            if num1 < num2:
                num1, num2 = num2, num1
            self.current_answer = num1 - num2
            problem_text = f"{num1} - {num2} = ?"
        
        self.problem_label.config(text=problem_text)
        self.answer_var.set("")
        self.result_label.config(text="")
    
    def check_answer(self):
        """Check if the answer is correct"""
        try:
            user_answer = int(self.answer_var.get())
            
            if user_answer == self.current_answer:
                self.result_label.config(text="✅ Correct! Great job!", fg=self.success_color)
                self.correct_count += 1
                self.streak += 1
                self.add_points(10)
                
                if self.streak >= 5:
                    messagebox.showinfo("Achievement!", "🔥 Amazing! You're on fire with a 5-problem streak!")
                    self.add_points(50)
            else:
                self.result_label.config(text=f"❌ Incorrect. The answer is {self.current_answer}",
                                        fg=self.warning_color)
                self.incorrect_count += 1
                self.streak = 0
            
            self.stats_label.config(text=f"Correct: {self.correct_count} | "
                                        f"Incorrect: {self.incorrect_count} | "
                                        f"Streak: {self.streak}")
            
            self.root.after(1500, self.generate_problem)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def show_multiplication(self):
        """Multiplication tables practice"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="✖️ Multiplication Tables",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        # Table display
        table_frame = tk.Frame(self.activity_frame, bg="white")
        table_frame.pack(pady=20)
        
        tk.Label(table_frame, text="Select table:", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)
        
        self.table_var = tk.StringVar(value="5")
        table_spin = tk.Spinbox(table_frame, from_=1, to=12, textvariable=self.table_var,
                               font=("Arial", 12), width=5)
        table_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(table_frame, text="Show Table", font=("Arial", 11),
                 bg=self.accent_color, fg="white",
                 command=self.show_times_table).pack(side=tk.LEFT, padx=10)
        
        # Table display area
        self.table_text = scrolledtext.ScrolledText(self.activity_frame, width=40, height=15,
                                                    font=("Courier", 14), bg="#f9f9f9")
        self.table_text.pack(pady=20)
        
        self.show_times_table()
    
    def show_times_table(self):
        """Display multiplication table"""
        try:
            table_num = int(self.table_var.get())
            self.table_text.delete(1.0, tk.END)
            
            self.table_text.insert(tk.END, f"Multiplication Table for {table_num}\n")
            self.table_text.insert(tk.END, "=" * 35 + "\n\n")
            
            for i in range(1, 13):
                result = table_num * i
                line = f"{table_num:2} × {i:2} = {result:3}\n"
                self.table_text.insert(tk.END, line)
            
            self.add_points(2)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def show_fractions(self):
        """Fraction visualizer"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="📊 Fraction Visualizer",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        tk.Label(self.activity_frame, text="Visualize fractions as parts of a whole!",
                font=("Arial", 12), bg="white", fg=self.primary_color).pack(pady=10)
        
        # Fraction input
        input_frame = tk.Frame(self.activity_frame, bg="white")
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="Numerator:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.numerator_var = tk.StringVar(value="1")
        tk.Spinbox(input_frame, from_=0, to=20, textvariable=self.numerator_var,
                  font=("Arial", 11), width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Label(input_frame, text="Denominator:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.denominator_var = tk.StringVar(value="4")
        tk.Spinbox(input_frame, from_=1, to=20, textvariable=self.denominator_var,
                  font=("Arial", 11), width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="Visualize", font=("Arial", 11, "bold"),
                 bg=self.accent_color, fg="white",
                 command=self.draw_fraction).pack(side=tk.LEFT, padx=10)
        
        # Canvas for visualization
        self.fraction_canvas = tk.Canvas(self.activity_frame, bg="white", height=300)
        self.fraction_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.draw_fraction()
    
    def draw_fraction(self):
        """Draw visual representation of fraction"""
        try:
            numerator = int(self.numerator_var.get())
            denominator = int(self.denominator_var.get())
            
            if denominator == 0:
                messagebox.showerror("Error", "Denominator cannot be zero!")
                return
            
            self.fraction_canvas.delete("all")
            
            # Draw circle divided into parts
            cx = 250
            cy = 150
            radius = 100
            
            angle_per_part = 360 / denominator
            
            for i in range(denominator):
                start_angle = i * angle_per_part
                color = self.success_color if i < numerator else "#e0e0e0"
                
                self.fraction_canvas.create_arc(cx - radius, cy - radius,
                                               cx + radius, cy + radius,
                                               start=start_angle, extent=angle_per_part,
                                               fill=color, outline=self.primary_color, width=2)
            
            # Display fraction
            fraction_text = f"{numerator}/{denominator}"
            if numerator == denominator:
                fraction_text += " = 1 (whole)"
            elif numerator > denominator:
                whole = numerator // denominator
                remainder = numerator % denominator
                fraction_text += f" = {whole} {remainder}/{denominator}"
            
            self.fraction_canvas.create_text(cx + 200, cy, text=fraction_text,
                                            font=("Arial", 24, "bold"), fill=self.primary_color)
            
            self.add_points(3)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def show_shapes(self):
        """Geometric shape explorer"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="📐 Shape Explorer",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        # Shape selection
        shape_frame = tk.Frame(self.activity_frame, bg="white")
        shape_frame.pack(pady=20)
        
        shapes = ["Circle", "Square", "Rectangle", "Triangle", "Pentagon", "Hexagon"]
        
        for shape in shapes:
            tk.Button(shape_frame, text=shape, font=("Arial", 11),
                     bg=self.accent_color, fg="white", width=12,
                     command=lambda s=shape: self.show_shape_info(s)).pack(side=tk.LEFT, padx=5)
        
        # Info display
        self.shape_info = tk.Text(self.activity_frame, width=60, height=20,
                                 font=("Arial", 11), bg="#f9f9f9", wrap=tk.WORD)
        self.shape_info.pack(pady=20, padx=20)
        
        self.show_shape_info("Circle")
    
    def show_shape_info(self, shape):
        """Display information about a shape"""
        self.shape_info.delete(1.0, tk.END)
        
        info = {
            "Circle": """
🔵 CIRCLE

Properties:
• No sides or corners
• All points equidistant from center
• Perfectly round

Formulas:
• Circumference = 2πr (or πd)
• Area = πr²

Where:
• r = radius (distance from center to edge)
• d = diameter (distance across circle)
• π ≈ 3.14159

Real-world examples:
• Wheels, coins, pizza, clock faces
            """,
            "Square": """
⬜ SQUARE

Properties:
• 4 equal sides
• 4 right angles (90°)
• All sides parallel

Formulas:
• Perimeter = 4 × side
• Area = side²

Real-world examples:
• Chess board squares, tiles, windows
            """,
            "Rectangle": """
▭ RECTANGLE

Properties:
• 4 sides (opposite sides equal)
• 4 right angles (90°)
• Opposite sides parallel

Formulas:
• Perimeter = 2(length + width)
• Area = length × width

Real-world examples:
• Doors, books, screens, paper
            """,
            "Triangle": """
🔺 TRIANGLE

Properties:
• 3 sides
• 3 angles
• Sum of angles = 180°

Types:
• Equilateral: all sides equal
• Isosceles: 2 sides equal
• Scalene: no sides equal

Formulas:
• Perimeter = side1 + side2 + side3
• Area = ½ × base × height

Real-world examples:
• Pyramids, road signs, roof trusses
            """,
            "Pentagon": """
⬟ PENTAGON

Properties:
• 5 sides
• 5 angles
• Sum of angles = 540°

Regular Pentagon:
• All sides equal
• All angles equal (108° each)

Real-world examples:
• The Pentagon building, home plate in baseball
            """,
            "Hexagon": """
⬡ HEXAGON

Properties:
• 6 sides
• 6 angles
• Sum of angles = 720°

Regular Hexagon:
• All sides equal
• All angles equal (120° each)

Real-world examples:
• Honeycomb cells, nuts and bolts
            """
        }
        
        self.shape_info.insert(1.0, info.get(shape, "Shape information not available."))
        self.add_points(2)
    
    def show_graphing(self):
        """Graphing calculator"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="📈 Graphing Calculator",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        tk.Label(self.activity_frame, text="Plot points and explore coordinate systems!",
                font=("Arial", 12), bg="white").pack(pady=10)
        
        # Coordinate input
        coord_frame = tk.Frame(self.activity_frame, bg="white")
        coord_frame.pack(pady=20)
        
        tk.Label(coord_frame, text="X:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.x_var = tk.StringVar(value="0")
        tk.Entry(coord_frame, textvariable=self.x_var, width=8).pack(side=tk.LEFT, padx=5)
        
        tk.Label(coord_frame, text="Y:", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)
        self.y_var = tk.StringVar(value="0")
        tk.Entry(coord_frame, textvariable=self.y_var, width=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(coord_frame, text="Plot Point", font=("Arial", 11),
                 bg=self.accent_color, fg="white",
                 command=self.plot_point).pack(side=tk.LEFT, padx=10)
        
        tk.Button(coord_frame, text="Clear", font=("Arial", 11),
                 bg=self.warning_color, fg="white",
                 command=self.clear_graph).pack(side=tk.LEFT, padx=5)
        
        # Graph canvas
        self.graph_canvas = tk.Canvas(self.activity_frame, bg="white", height=400)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.draw_coordinate_system()
    
    def draw_coordinate_system(self):
        """Draw coordinate system"""
        self.graph_canvas.delete("all")
        
        width = 600
        height = 400
        cx = width // 2
        cy = height // 2
        
        # Draw axes
        self.graph_canvas.create_line(0, cy, width, cy, fill=self.primary_color, width=2)
        self.graph_canvas.create_line(cx, 0, cx, height, fill=self.primary_color, width=2)
        
        # Draw grid
        for i in range(-10, 11):
            x = cx + i * 30
            y = cy + i * 30
            
            if i != 0:
                self.graph_canvas.create_line(x, 0, x, height, fill="#e0e0e0", dash=(2, 4))
                self.graph_canvas.create_line(0, y, width, y, fill="#e0e0e0", dash=(2, 4))
        
        # Labels
        self.graph_canvas.create_text(width - 20, cy + 20, text="X", font=("Arial", 12, "bold"))
        self.graph_canvas.create_text(cx + 20, 20, text="Y", font=("Arial", 12, "bold"))
    
    def plot_point(self):
        """Plot a point on the graph"""
        try:
            x = float(self.x_var.get())
            y = float(self.y_var.get())
            
            cx = 300
            cy = 200
            scale = 30
            
            px = cx + x * scale
            py = cy - y * scale
            
            # Draw point
            self.graph_canvas.create_oval(px - 5, py - 5, px + 5, py + 5,
                                         fill=self.accent_color, outline=self.primary_color, width=2)
            
            # Label
            self.graph_canvas.create_text(px, py - 15, text=f"({x},{y})",
                                         font=("Arial", 9), fill=self.primary_color)
            
            self.add_points(3)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def clear_graph(self):
        """Clear all points from graph"""
        self.draw_coordinate_system()
    
    def show_games(self):
        """Math games menu"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="🎲 Math Games",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        games_text = """
        Choose a game to practice your math skills:
        
        🎯 Number Guess - Practice number sense
        ⚡ Speed Math - Quick calculation challenges
        🧩 Pattern Puzzle - Identify mathematical patterns
        🎪 Math Bingo - Practice operations with bingo
        
        Coming soon: More exciting math games!
        """
        
        tk.Label(self.activity_frame, text=games_text, font=("Arial", 12),
                bg="white", justify=tk.LEFT).pack(pady=20)
        
        tk.Button(self.activity_frame, text="Play Number Guess", font=("Arial", 14, "bold"),
                 bg=self.success_color, fg="white", width=20, height=2,
                 command=self.play_number_guess).pack(pady=10)
    
    def play_number_guess(self):
        """Simple number guessing game"""
        target = random.randint(1, 100)
        guesses = 0
        max_guesses = 7
        
        def check_guess():
            nonlocal guesses
            try:
                guess = int(guess_var.get())
                guesses += 1
                
                if guess == target:
                    result = f"🎉 Correct! You found {target} in {guesses} guesses!"
                    messagebox.showinfo("Winner!", result)
                    self.add_points(50)
                    game_window.destroy()
                elif guesses >= max_guesses:
                    messagebox.showinfo("Game Over", f"Out of guesses! The number was {target}")
                    game_window.destroy()
                elif guess < target:
                    feedback_label.config(text=f"Too low! Guesses left: {max_guesses - guesses}")
                else:
                    feedback_label.config(text=f"Too high! Guesses left: {max_guesses - guesses}")
                
                guess_var.set("")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        game_window = tk.Toplevel(self.root)
        game_window.title("Number Guess Game")
        game_window.geometry("400x300")
        game_window.configure(bg="white")
        
        tk.Label(game_window, text="🎯 Guess the Number!", font=("Arial", 18, "bold"),
                bg="white").pack(pady=20)
        tk.Label(game_window, text="I'm thinking of a number between 1 and 100",
                font=("Arial", 12), bg="white").pack(pady=10)
        
        guess_var = tk.StringVar()
        tk.Entry(game_window, textvariable=guess_var, font=("Arial", 16), width=15).pack(pady=10)
        
        tk.Button(game_window, text="Guess", font=("Arial", 12, "bold"),
                 bg=self.accent_color, fg="white", width=15,
                 command=check_guess).pack(pady=10)
        
        feedback_label = tk.Label(game_window, text=f"You have {max_guesses} guesses",
                                 font=("Arial", 12), bg="white")
        feedback_label.pack(pady=10)
    
    def show_progress(self):
        """Show student progress"""
        self.clear_activity_frame()
        
        tk.Label(self.activity_frame, text="📊 Your Progress",
                font=("Arial", 20, "bold"), bg="white", fg=self.primary_color).pack(pady=20)
        
        progress_text = f"""
        Student: {self.student_name}
        Level: {self.student_level}
        
        ⭐ Total Points: {self.points}
        🏆 Achievements Earned: {len(self.achievements)}
        
        Keep practicing to earn more points and achievements!
        
        Recent Achievements:
        """
        
        tk.Label(self.activity_frame, text=progress_text, font=("Arial", 12),
                bg="white", justify=tk.LEFT).pack(pady=20)
        
        if self.achievements:
            for achievement in self.achievements[-5:]:
                tk.Label(self.activity_frame, text=f"🏅 {achievement}",
                        font=("Arial", 11), bg="white").pack(pady=2)
        else:
            tk.Label(self.activity_frame, text="No achievements yet. Keep learning!",
                    font=("Arial", 11), bg="white", fg=self.primary_color).pack(pady=10)
    
    def add_points(self, points):
        """Add points to student score"""
        self.points += points
        self.info_label.config(text=f"👤 {self.student_name} | ⭐ {self.points} pts")
        
        # Check for milestones
        if self.points >= 100 and "First 100 Points" not in self.achievements:
            self.achievements.append("First 100 Points")
            messagebox.showinfo("Achievement!", "🏆 You earned your first 100 points!")
        elif self.points >= 500 and "500 Point Master" not in self.achievements:
            self.achievements.append("500 Point Master")
            messagebox.showinfo("Achievement!", "🏆 You're a 500 Point Master!")
    
    def clear_activity_frame(self):
        """Clear the activity frame"""
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
    
    def load_student_data(self):
        """Load student data from file"""
        try:
            with open("math_studio_data.json", "r") as f:
                data = json.load(f)
                self.student_name = data.get("name", "Student")
                self.points = data.get("points", 0)
                self.achievements = data.get("achievements", [])
                self.info_label.config(text=f"👤 {self.student_name} | ⭐ {self.points} pts")
        except FileNotFoundError:
            pass
    
    def save_student_data(self):
        """Save student data to file"""
        data = {
            "name": self.student_name,
            "points": self.points,
            "achievements": self.achievements
        }
        with open("math_studio_data.json", "w") as f:
            json.dump(data, f, indent=2)

def main():
    root = tk.Tk()
    app = InteractiveMathStudio(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.save_student_data(), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    main()
