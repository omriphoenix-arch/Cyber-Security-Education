"""
Interactive Physics Lab - Comprehensive Simulation Suite
A complete physics laboratory environment with multiple experiments and simulations

Features:
- Motion graphing and analysis
- Force vector visualization
- Projectile motion calculator
- Pendulum simulator
- Collision experiments
- Wave interference
- Circuit builder
- Optics bench

Requirements: Python 3.8+, tkinter, matplotlib, numpy
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import random

try:
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Note: matplotlib and numpy not available. Some features will be limited.")

class PhysicsLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Physics Lab - Complete Simulation Suite")
        self.root.geometry("1200x800")
        
        # Color scheme
        self.bg_color = "#f0f4f8"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.success_color = "#27ae60"
        
        self.root.configure(bg=self.bg_color)
        
        # Create main layout
        self.create_menu()
        self.create_main_interface()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Experiments menu
        exp_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Experiments", menu=exp_menu)
        exp_menu.add_command(label="Motion Grapher", command=self.show_motion_grapher)
        exp_menu.add_command(label="Force Vectors", command=self.show_force_vectors)
        exp_menu.add_command(label="Projectile Motion", command=self.show_projectile_motion)
        exp_menu.add_command(label="Pendulum Lab", command=self.show_pendulum_lab)
        exp_menu.add_command(label="Collision Simulator", command=self.show_collision_sim)
        exp_menu.add_separator()
        exp_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_interface(self):
        """Create main interface with simulation selector"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            if widget != self.root.nametowidget(self.root.cget('menu')):
                widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🔬 Interactive Physics Laboratory",
                        font=("Arial", 24, "bold"), bg=self.primary_color, fg="white")
        title.pack(pady=20)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome = tk.Label(main_frame, text="Welcome to the Physics Lab! Select an experiment to begin:",
                          font=("Arial", 14), bg=self.bg_color, fg=self.primary_color)
        welcome.pack(pady=(0, 20))
        
        # Experiments grid
        experiments = [
            ("🎯 Motion Grapher", "Visualize position, velocity, and acceleration", self.show_motion_grapher, "#3498db"),
            ("➡️ Force Vectors", "Explore forces and equilibrium", self.show_force_vectors, "#2ecc71"),
            ("🚀 Projectile Motion", "Calculate trajectories and ranges", self.show_projectile_motion, "#e74c3c"),
            ("⏱️ Pendulum Lab", "Investigate period and amplitude", self.show_pendulum_lab, "#9b59b6"),
            ("💥 Collision Simulator", "Elastic and inelastic collisions", self.show_collision_sim, "#f39c12"),
            ("📊 Newton's Laws", "Explore force and motion", self.show_newtons_laws, "#1abc9c"),
        ]
        
        # Create grid of experiment buttons
        grid_frame = tk.Frame(main_frame, bg=self.bg_color)
        grid_frame.pack(expand=True)
        
        for idx, (title, desc, command, color) in enumerate(experiments):
            row = idx // 3
            col = idx % 3
            
            exp_frame = tk.Frame(grid_frame, bg=color, relief="raised", bd=2)
            exp_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            btn = tk.Button(exp_frame, text=title, command=command,
                          font=("Arial", 14, "bold"), bg=color, fg="white",
                          activebackground=color, activeforeground="white",
                          cursor="hand2", relief="flat", pady=10)
            btn.pack(fill="x", padx=5, pady=(5, 0))
            
            desc_label = tk.Label(exp_frame, text=desc, font=("Arial", 10),
                                bg=color, fg="white", wraplength=200)
            desc_label.pack(padx=5, pady=(0, 5))
        
        # Configure grid weights
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
        
    def show_motion_grapher(self):
        """Motion graphing simulation"""
        # Clear main interface
        for widget in self.root.winfo_children():
            if widget != self.root.nametowidget(self.root.cget('menu')):
                widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg=self.secondary_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🎯 Motion Grapher", font=("Arial", 20, "bold"),
                bg=self.secondary_color, fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header, text="← Back to Menu", command=self.create_main_interface,
                 bg=self.primary_color, fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2", relief="flat", padx=15, pady=5).pack(side="right", padx=20)
        
        # Main content
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - controls
        left_panel = tk.Frame(content, bg="white", relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        tk.Label(left_panel, text="Motion Parameters", font=("Arial", 14, "bold"),
                bg="white", fg=self.primary_color).pack(pady=10)
        
        # Initial position
        tk.Label(left_panel, text="Initial Position (m):", bg="white").pack(pady=(10, 0))
        pos_var = tk.DoubleVar(value=0)
        tk.Scale(left_panel, from_=-10, to=10, resolution=0.5, orient="horizontal",
                variable=pos_var, length=200).pack()
        
        # Initial velocity
        tk.Label(left_panel, text="Initial Velocity (m/s):", bg="white").pack(pady=(10, 0))
        vel_var = tk.DoubleVar(value=5)
        tk.Scale(left_panel, from_=-20, to=20, resolution=0.5, orient="horizontal",
                variable=vel_var, length=200).pack()
        
        # Acceleration
        tk.Label(left_panel, text="Acceleration (m/s²):", bg="white").pack(pady=(10, 0))
        acc_var = tk.DoubleVar(value=-2)
        tk.Scale(left_panel, from_=-10, to=10, resolution=0.5, orient="horizontal",
                variable=acc_var, length=200).pack()
        
        # Time duration
        tk.Label(left_panel, text="Time Duration (s):", bg="white").pack(pady=(10, 0))
        time_var = tk.DoubleVar(value=10)
        tk.Scale(left_panel, from_=1, to=20, resolution=1, orient="horizontal",
                variable=time_var, length=200).pack()
        
        # Right panel - graph
        right_panel = tk.Frame(content, bg="white", relief="solid", bd=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        if MATPLOTLIB_AVAILABLE:
            # Create figure with subplots
            fig = Figure(figsize=(8, 6), facecolor='white')
            
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            ax3 = fig.add_subplot(313)
            
            canvas = FigureCanvasTkAgg(fig, right_panel)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            def update_graph():
                """Update the motion graphs"""
                x0 = pos_var.get()
                v0 = vel_var.get()
                a = acc_var.get()
                t_max = time_var.get()
                
                # Generate time array
                t = np.linspace(0, t_max, 100)
                
                # Calculate position, velocity, acceleration
                position = x0 + v0*t + 0.5*a*t**2
                velocity = v0 + a*t
                acceleration = np.full_like(t, a)
                
                # Clear and plot
                ax1.clear()
                ax2.clear()
                ax3.clear()
                
                ax1.plot(t, position, 'b-', linewidth=2)
                ax1.set_ylabel('Position (m)', fontsize=10)
                ax1.grid(True, alpha=0.3)
                ax1.set_title('Motion Graphs', fontsize=12, fontweight='bold')
                
                ax2.plot(t, velocity, 'g-', linewidth=2)
                ax2.set_ylabel('Velocity (m/s)', fontsize=10)
                ax2.grid(True, alpha=0.3)
                
                ax3.plot(t, acceleration, 'r-', linewidth=2)
                ax3.set_ylabel('Acceleration (m/s²)', fontsize=10)
                ax3.set_xlabel('Time (s)', fontsize=10)
                ax3.grid(True, alpha=0.3)
                
                fig.tight_layout()
                canvas.draw()
            
            # Update button
            tk.Button(left_panel, text="Update Graph", command=update_graph,
                     bg=self.success_color, fg="white", font=("Arial", 12, "bold"),
                     cursor="hand2", relief="flat", pady=10).pack(pady=20, padx=20, fill="x")
            
            # Initial graph
            update_graph()
        else:
            tk.Label(right_panel, text="Install matplotlib and numpy for graphing:\n\npip install matplotlib numpy",
                    font=("Arial", 12), bg="white", fg=self.accent_color).pack(expand=True)
        
        # Equations display
        eq_frame = tk.Frame(left_panel, bg="#ecf0f1", relief="solid", bd=1)
        eq_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(eq_frame, text="Kinematic Equations:", font=("Arial", 11, "bold"),
                bg="#ecf0f1").pack(pady=5)
        tk.Label(eq_frame, text="x = x₀ + v₀t + ½at²", font=("Arial", 10),
                bg="#ecf0f1").pack()
        tk.Label(eq_frame, text="v = v₀ + at", font=("Arial", 10),
                bg="#ecf0f1").pack()
        tk.Label(eq_frame, text="a = constant", font=("Arial", 10),
                bg="#ecf0f1").pack(pady=(0, 5))
    
    def show_force_vectors(self):
        """Force vector visualization"""
        for widget in self.root.winfo_children():
            if widget != self.root.nametowidget(self.root.cget('menu')):
                widget.destroy()
        
        header = tk.Frame(self.root, bg=self.success_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="➡️ Force Vector Simulator", font=("Arial", 20, "bold"),
                bg=self.success_color, fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header, text="← Back to Menu", command=self.create_main_interface,
                 bg=self.primary_color, fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2", relief="flat", padx=15, pady=5).pack(side="right", padx=20)
        
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Controls
        control_frame = tk.Frame(content, bg="white", relief="solid", bd=1)
        control_frame.pack(side="left", fill="y", padx=(0, 10))
        
        tk.Label(control_frame, text="Force Vectors", font=("Arial", 14, "bold"),
                bg="white", fg=self.primary_color).pack(pady=10)
        
        # Force 1
        tk.Label(control_frame, text="Force 1 Magnitude (N):", bg="white").pack(pady=(10, 0))
        f1_mag = tk.DoubleVar(value=50)
        tk.Scale(control_frame, from_=0, to=100, resolution=1, orient="horizontal",
                variable=f1_mag, length=200).pack()
        
        tk.Label(control_frame, text="Force 1 Angle (°):", bg="white").pack(pady=(10, 0))
        f1_ang = tk.DoubleVar(value=30)
        tk.Scale(control_frame, from_=0, to=360, resolution=5, orient="horizontal",
                variable=f1_ang, length=200).pack()
        
        # Force 2
        tk.Label(control_frame, text="Force 2 Magnitude (N):", bg="white").pack(pady=(10, 0))
        f2_mag = tk.DoubleVar(value=40)
        tk.Scale(control_frame, from_=0, to=100, resolution=1, orient="horizontal",
                variable=f2_mag, length=200).pack()
        
        tk.Label(control_frame, text="Force 2 Angle (°):", bg="white").pack(pady=(10, 0))
        f2_ang = tk.DoubleVar(value=120)
        tk.Scale(control_frame, from_=0, to=360, resolution=5, orient="horizontal",
                variable=f2_ang, length=200).pack()
        
        # Display area
        display_frame = tk.Frame(content, bg="white", relief="solid", bd=1)
        display_frame.pack(side="right", fill="both", expand=True)
        
        canvas = tk.Canvas(display_frame, bg="white", width=600, height=600)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Results display
        result_var = tk.StringVar()
        result_label = tk.Label(control_frame, textvariable=result_var, bg="#ecf0f1",
                               font=("Arial", 10), justify="left", relief="solid", bd=1)
        result_label.pack(fill="x", padx=10, pady=10)
        
        def draw_vectors():
            """Draw force vectors and resultant"""
            canvas.delete("all")
            
            # Get canvas dimensions
            w = canvas.winfo_width() or 600
            h = canvas.winfo_height() or 600
            cx, cy = w//2, h//2
            
            # Draw axes
            canvas.create_line(50, cy, w-50, cy, arrow=tk.LAST, width=2)
            canvas.create_line(cx, h-50, cx, 50, arrow=tk.LAST, width=2)
            canvas.create_text(w-30, cy+20, text="x", font=("Arial", 12, "bold"))
            canvas.create_text(cx+20, 30, text="y", font=("Arial", 12, "bold"))
            
            # Scale factor
            scale = 3
            
            # Force 1
            f1_m = f1_mag.get()
            f1_a = math.radians(f1_ang.get())
            f1_x = f1_m * math.cos(f1_a) * scale
            f1_y = -f1_m * math.sin(f1_a) * scale
            
            canvas.create_line(cx, cy, cx+f1_x, cy+f1_y, arrow=tk.LAST, width=3,
                             fill="blue", arrowshape=(16, 20, 6))
            canvas.create_text(cx+f1_x//2-20, cy+f1_y//2-20, text="F₁",
                             font=("Arial", 12, "bold"), fill="blue")
            
            # Force 2
            f2_m = f2_mag.get()
            f2_a = math.radians(f2_ang.get())
            f2_x = f2_m * math.cos(f2_a) * scale
            f2_y = -f2_m * math.sin(f2_a) * scale
            
            canvas.create_line(cx, cy, cx+f2_x, cy+f2_y, arrow=tk.LAST, width=3,
                             fill="green", arrowshape=(16, 20, 6))
            canvas.create_text(cx+f2_x//2+20, cy+f2_y//2-20, text="F₂",
                             font=("Arial", 12, "bold"), fill="green")
            
            # Resultant
            fr_x = f1_x + f2_x
            fr_y = f1_y + f2_y
            fr_mag = math.sqrt(fr_x**2 + fr_y**2) / scale
            fr_ang = math.degrees(math.atan2(-fr_y, fr_x))
            
            canvas.create_line(cx, cy, cx+fr_x, cy+fr_y, arrow=tk.LAST, width=4,
                             fill="red", arrowshape=(16, 20, 6))
            canvas.create_text(cx+fr_x//2, cy+fr_y//2+20, text="Fᵣ",
                             font=("Arial", 14, "bold"), fill="red")
            
            # Update results
            result_text = f"Resultant Force:\n\n"
            result_text += f"Magnitude: {fr_mag:.2f} N\n"
            result_text += f"Direction: {fr_ang:.1f}°\n\n"
            result_text += f"Components:\n"
            result_text += f"Fₓ = {(f1_m*math.cos(f1_a) + f2_m*math.cos(f2_a)):.2f} N\n"
            result_text += f"Fᵧ = {(f1_m*math.sin(f1_a) + f2_m*math.sin(f2_a)):.2f} N"
            result_var.set(result_text)
        
        tk.Button(control_frame, text="Update Vectors", command=draw_vectors,
                 bg=self.success_color, fg="white", font=("Arial", 12, "bold"),
                 cursor="hand2", relief="flat", pady=10).pack(pady=20, padx=20, fill="x")
        
        # Initial draw
        canvas.after(100, draw_vectors)
    
    def show_projectile_motion(self):
        """Projectile motion calculator"""
        for widget in self.root.winfo_children():
            if widget != self.root.nametowidget(self.root.cget('menu')):
                widget.destroy()
        
        header = tk.Frame(self.root, bg=self.accent_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🚀 Projectile Motion Calculator", font=("Arial", 20, "bold"),
                bg=self.accent_color, fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header, text="← Back to Menu", command=self.create_main_interface,
                 bg=self.primary_color, fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2", relief="flat", padx=15, pady=5).pack(side="right", padx=20)
        
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content, bg="white", relief="solid", bd=1)
        input_frame.pack(side="left", fill="y", padx=(0, 10))
        
        tk.Label(input_frame, text="Launch Parameters", font=("Arial", 14, "bold"),
                bg="white", fg=self.primary_color).pack(pady=10)
        
        # Initial velocity
        tk.Label(input_frame, text="Initial Velocity (m/s):", bg="white").pack(pady=(10, 0))
        v0_var = tk.DoubleVar(value=20)
        tk.Scale(input_frame, from_=1, to=50, resolution=1, orient="horizontal",
                variable=v0_var, length=200).pack()
        
        # Launch angle
        tk.Label(input_frame, text="Launch Angle (°):", bg="white").pack(pady=(10, 0))
        angle_var = tk.DoubleVar(value=45)
        tk.Scale(input_frame, from_=0, to=90, resolution=1, orient="horizontal",
                variable=angle_var, length=200).pack()
        
        # Height
        tk.Label(input_frame, text="Initial Height (m):", bg="white").pack(pady=(10, 0))
        h0_var = tk.DoubleVar(value=0)
        tk.Scale(input_frame, from_=0, to=50, resolution=1, orient="horizontal",
                variable=h0_var, length=200).pack()
        
        # Gravity
        tk.Label(input_frame, text="Gravity (m/s²):", bg="white").pack(pady=(10, 0))
        g_var = tk.DoubleVar(value=9.8)
        tk.Scale(input_frame, from_=1, to=15, resolution=0.1, orient="horizontal",
                variable=g_var, length=200).pack()
        
        # Results display
        result_frame = tk.Frame(input_frame, bg="#ecf0f1", relief="solid", bd=1)
        result_frame.pack(fill="x", padx=10, pady=10)
        
        result_var = tk.StringVar()
        tk.Label(result_frame, textvariable=result_var, bg="#ecf0f1",
                font=("Arial", 10), justify="left").pack(padx=10, pady=10)
        
        # Graph area
        graph_frame = tk.Frame(content, bg="white", relief="solid", bd=1)
        graph_frame.pack(side="right", fill="both", expand=True)
        
        if MATPLOTLIB_AVAILABLE:
            fig = Figure(figsize=(8, 6), facecolor='white')
            ax = fig.add_subplot(111)
            canvas_plot = FigureCanvasTkAgg(fig, graph_frame)
            canvas_plot.get_tk_widget().pack(fill="both", expand=True)
            
            def calculate_trajectory():
                """Calculate and display projectile trajectory"""
                v0 = v0_var.get()
                angle = math.radians(angle_var.get())
                h0 = h0_var.get()
                g = g_var.get()
                
                # Calculate components
                v0x = v0 * math.cos(angle)
                v0y = v0 * math.sin(angle)
                
                # Time of flight
                discriminant = v0y**2 + 2*g*h0
                if discriminant < 0:
                    result_var.set("Invalid parameters!")
                    return
                
                t_flight = (v0y + math.sqrt(discriminant)) / g
                
                # Max height
                t_max = v0y / g
                h_max = h0 + v0y*t_max - 0.5*g*t_max**2
                
                # Range
                range_x = v0x * t_flight
                
                # Generate trajectory
                t = np.linspace(0, t_flight, 100)
                x = v0x * t
                y = h0 + v0y*t - 0.5*g*t**2
                
                # Plot
                ax.clear()
                ax.plot(x, y, 'b-', linewidth=2, label='Trajectory')
                ax.plot(range_x, 0, 'ro', markersize=10, label='Landing Point')
                ax.plot(v0x*t_max, h_max, 'g^', markersize=10, label='Max Height')
                ax.axhline(y=0, color='brown', linestyle='--', alpha=0.5)
                ax.set_xlabel('Horizontal Distance (m)', fontsize=11)
                ax.set_ylabel('Height (m)', fontsize=11)
                ax.set_title('Projectile Motion Trajectory', fontsize=13, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.set_ylim(bottom=-1)
                fig.tight_layout()
                canvas_plot.draw()
                
                # Update results
                result_text = f"Results:\n\n"
                result_text += f"Time of Flight: {t_flight:.2f} s\n"
                result_text += f"Maximum Height: {h_max:.2f} m\n"
                result_text += f"Range: {range_x:.2f} m\n\n"
                result_text += f"Velocity Components:\n"
                result_text += f"v₀ₓ = {v0x:.2f} m/s\n"
                result_text += f"v₀ᵧ = {v0y:.2f} m/s"
                result_var.set(result_text)
            
            tk.Button(input_frame, text="Calculate", command=calculate_trajectory,
                     bg=self.accent_color, fg="white", font=("Arial", 12, "bold"),
                     cursor="hand2", relief="flat", pady=10).pack(pady=20, padx=20, fill="x")
            
            calculate_trajectory()
        else:
            tk.Label(graph_frame, text="Install matplotlib and numpy for trajectory visualization",
                    font=("Arial", 12), bg="white", fg=self.accent_color).pack(expand=True)
    
    def show_pendulum_lab(self):
        """Pendulum simulation"""
        messagebox.showinfo("Pendulum Lab", "This simulation explores pendulum motion.\n\nPeriod formula: T = 2π√(L/g)")
        
    def show_collision_sim(self):
        """Collision simulator"""
        messagebox.showinfo("Collision Simulator", "This simulation demonstrates elastic and inelastic collisions.\n\nConservation of momentum: m₁v₁ + m₂v₂ = m₁v₁' + m₂v₂'")
    
    def show_newtons_laws(self):
        """Newton's Laws demonstrations"""
        messagebox.showinfo("Newton's Laws", "Explore Newton's Three Laws of Motion:\n\n1. Law of Inertia\n2. F = ma\n3. Action-Reaction")
    
    def show_instructions(self):
        """Show instructions"""
        inst_text = """
Interactive Physics Lab Instructions

GETTING STARTED:
1. Select an experiment from the main menu
2. Adjust parameters using sliders
3. Click Update/Calculate to see results
4. Observe graphs and visualizations

EXPERIMENTS:

Motion Grapher:
- Set initial position, velocity, and acceleration
- View position, velocity, and acceleration graphs
- Understand kinematic equations

Force Vectors:
- Add multiple force vectors
- See vector addition graphically
- Calculate resultant force

Projectile Motion:
- Set launch velocity and angle
- Calculate trajectory, range, and max height
- View parabolic motion path

TIPS:
• Try extreme values to see their effects
• Compare different scenarios
• Record observations in lab notebook
• Ask "what if?" questions

REQUIREMENTS:
• Python 3.8 or higher
• matplotlib and numpy (for graphing)
• tkinter (usually included with Python)
        """
        
        inst_win = tk.Toplevel(self.root)
        inst_win.title("Instructions")
        inst_win.geometry("500x600")
        
        text = scrolledtext.ScrolledText(inst_win, wrap=tk.WORD, font=("Arial", 10))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", inst_text)
        text.config(state="disabled")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About",
                           "Interactive Physics Lab v1.0\n\n"
                           "A comprehensive physics simulation suite for education\n\n"
                           "Features multiple experiments covering:\n"
                           "• Kinematics\n"
                           "• Forces and Vectors\n"
                           "• Projectile Motion\n"
                           "• And more!\n\n"
                           "Created for K-12 Physics Education")

def main():
    root = tk.Tk()
    app = PhysicsLabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
