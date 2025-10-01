#!/usr/bin/env python3
"""
Animation Studio
================
Interactive animation creation tool for K-12 digital arts education.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime
import math
import time
import threading

class AnimationStudio:
    """Interactive animation creation and learning platform."""
    
    def __init__(self):
        """Initialize the animation studio."""
        self.setup_animation_variables()
        self.setup_gui()
        
    def setup_animation_variables(self):
        """Initialize animation state variables."""
        self.frames = []
        self.current_frame = 0
        self.total_frames = 24  # Default 1 second at 24fps
        self.fps = 12
        self.is_playing = False
        self.timeline_objects = {}
        self.selected_object = None
        self.canvas_width = 800
        self.canvas_height = 600
        self.onion_skin = True
        self.loop_animation = True
        
    def setup_gui(self):
        """Create the main animation studio interface."""
        self.root = tk.Tk()
        self.root.title("🎬 Animation Studio - Digital Arts Platform")
        self.root.geometry("1400x900")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_animator_tab()
        self.setup_timeline_tab()
        self.setup_character_designer_tab()
        self.setup_effects_tab()
        self.setup_tutorial_tab()
        
    def setup_animator_tab(self):
        """Setup the main animation workspace."""
        animator_frame = ttk.Frame(self.notebook)
        self.notebook.add(animator_frame, text="🎬 Animator")
        
        # Top toolbar
        toolbar = ttk.Frame(animator_frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        # Playback controls
        playback_frame = ttk.LabelFrame(toolbar, text="▶️ Playback")
        playback_frame.pack(side='left', padx=5)
        
        ttk.Button(playback_frame, text="⏮️", command=self.first_frame, width=4).pack(side='left', padx=1)
        ttk.Button(playback_frame, text="⏪", command=self.prev_frame, width=4).pack(side='left', padx=1)
        self.play_button = ttk.Button(playback_frame, text="▶️", command=self.play_pause, width=4)
        self.play_button.pack(side='left', padx=1)
        ttk.Button(playback_frame, text="⏩", command=self.next_frame, width=4).pack(side='left', padx=1)
        ttk.Button(playback_frame, text="⏭️", command=self.last_frame, width=4).pack(side='left', padx=1)
        
        # Frame info
        frame_info = ttk.LabelFrame(toolbar, text="📹 Frame Info")
        frame_info.pack(side='left', padx=5)
        
        ttk.Label(frame_info, text="Frame:").pack(side='left', padx=2)
        self.frame_label = ttk.Label(frame_info, text="1 / 24")
        self.frame_label.pack(side='left', padx=2)
        
        ttk.Label(frame_info, text="FPS:").pack(side='left', padx=5)
        self.fps_var = tk.IntVar(value=12)
        fps_spinbox = ttk.Spinbox(frame_info, from_=1, to=60, width=5, textvariable=self.fps_var,
                                 command=self.update_fps)
        fps_spinbox.pack(side='left', padx=2)
        
        # Animation settings
        settings_frame = ttk.LabelFrame(toolbar, text="⚙️ Settings")
        settings_frame.pack(side='left', padx=5)
        
        self.onion_skin_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="👻 Onion Skin", 
                       variable=self.onion_skin_var).pack(side='left', padx=2)
        
        self.loop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="🔄 Loop", 
                       variable=self.loop_var).pack(side='left', padx=2)
        
        # Main workspace
        workspace = ttk.Frame(animator_frame)
        workspace.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tools panel
        tools_panel = ttk.LabelFrame(workspace, text="🛠️ Animation Tools")
        tools_panel.pack(side='left', fill='y', padx=5)
        
        # Animation tools
        anim_tools = [
            ("✏️ Draw", "draw"),
            ("🎭 Transform", "transform"),
            ("📦 Add Object", "add_object"),
            ("🎯 Select", "select"),
            ("⚡ Tween", "tween"),
            ("🔄 Rotate", "rotate"),
            ("↔️ Scale", "scale"),
            ("📍 Keyframe", "keyframe"),
            ("🗑️ Delete", "delete")
        ]
        
        self.anim_tool_var = tk.StringVar(value="draw")
        
        for name, tool in anim_tools:
            ttk.Radiobutton(tools_panel, text=name, variable=self.anim_tool_var, 
                           value=tool, command=lambda t=tool: self.select_anim_tool(t)).pack(anchor='w', padx=5, pady=2)
        
        # Object library
        object_lib_frame = ttk.LabelFrame(tools_panel, text="📚 Object Library")
        object_lib_frame.pack(fill='x', padx=5, pady=5)
        
        objects = ["⭕ Circle", "⬜ Square", "⭐ Star", "❤️ Heart", "🎭 Character"]
        for obj in objects:
            ttk.Button(object_lib_frame, text=obj, command=lambda o=obj: self.add_object(o)).pack(fill='x', pady=1)
        
        # Canvas area
        canvas_frame = ttk.LabelFrame(workspace, text="🖼️ Animation Canvas")
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height,
                               bg='white')
        self.canvas.pack(padx=10, pady=10)
        
        # Bind canvas events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_release)
        
        # Properties panel
        props_panel = ttk.LabelFrame(workspace, text="⚙️ Properties")
        props_panel.pack(side='right', fill='y', padx=5)
        
        # Object properties
        ttk.Label(props_panel, text="Selected Object:").pack(anchor='w', padx=5, pady=2)
        self.selected_obj_label = ttk.Label(props_panel, text="None")
        self.selected_obj_label.pack(anchor='w', padx=5)
        
        # Position controls
        pos_frame = ttk.LabelFrame(props_panel, text="📍 Position")
        pos_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(pos_frame, text="X:").grid(row=0, column=0, padx=2)
        self.x_pos_var = tk.StringVar()
        ttk.Entry(pos_frame, textvariable=self.x_pos_var, width=8).grid(row=0, column=1, padx=2)
        
        ttk.Label(pos_frame, text="Y:").grid(row=1, column=0, padx=2)
        self.y_pos_var = tk.StringVar()
        ttk.Entry(pos_frame, textvariable=self.y_pos_var, width=8).grid(row=1, column=1, padx=2)
        
        # Animation properties
        anim_props_frame = ttk.LabelFrame(props_panel, text="🎬 Animation")
        anim_props_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(anim_props_frame, text="Ease In/Out:").pack(anchor='w', padx=5)
        self.ease_var = tk.StringVar(value="Linear")
        ease_combo = ttk.Combobox(anim_props_frame, textvariable=self.ease_var,
                                 values=["Linear", "Ease In", "Ease Out", "Ease In-Out", "Bounce"])
        ease_combo.pack(fill='x', padx=5, pady=2)
        
        ttk.Button(anim_props_frame, text="🔑 Set Keyframe", 
                  command=self.set_keyframe).pack(fill='x', padx=5, pady=2)
        ttk.Button(anim_props_frame, text="↔️ Create Tween", 
                  command=self.create_tween).pack(fill='x', padx=5, pady=2)
        
    def setup_timeline_tab(self):
        """Setup the timeline and frame management tab."""
        timeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(timeline_frame, text="⏰ Timeline")
        
        # Timeline controls
        timeline_controls = ttk.Frame(timeline_frame)
        timeline_controls.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(timeline_controls, text="➕ Add Frame", 
                  command=self.add_frame).pack(side='left', padx=5)
        ttk.Button(timeline_controls, text="➖ Delete Frame", 
                  command=self.delete_frame).pack(side='left', padx=5)
        ttk.Button(timeline_controls, text="📋 Copy Frame", 
                  command=self.copy_frame).pack(side='left', padx=5)
        ttk.Button(timeline_controls, text="📄 Paste Frame", 
                  command=self.paste_frame).pack(side='left', padx=5)
        
        # Timeline display
        timeline_display = ttk.LabelFrame(timeline_frame, text="📊 Timeline")
        timeline_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Timeline canvas
        self.timeline_canvas = tk.Canvas(timeline_display, height=200, bg='lightgray')
        self.timeline_canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Draw initial timeline
        self.draw_timeline()
        
        # Frame details
        frame_details = ttk.LabelFrame(timeline_frame, text="🖼️ Frame Details")
        frame_details.pack(fill='x', padx=5, pady=5)
        
        # Frame operations
        frame_ops = ttk.Frame(frame_details)
        frame_ops.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_ops, text="Frame Duration:").pack(side='left', padx=5)
        self.frame_duration_var = tk.IntVar(value=1)
        ttk.Spinbox(frame_ops, from_=1, to=10, width=5, 
                   textvariable=self.frame_duration_var).pack(side='left', padx=5)
        
        ttk.Label(frame_ops, text="frames").pack(side='left', padx=2)
        
        ttk.Button(frame_ops, text="🎬 Preview Animation", 
                  command=self.preview_animation).pack(side='right', padx=5)
        
    def setup_character_designer_tab(self):
        """Setup the character design and rigging tab."""
        character_frame = ttk.Frame(self.notebook)
        self.notebook.add(character_frame, text="🎭 Character Designer")
        
        # Character tools
        char_tools = ttk.LabelFrame(character_frame, text="🛠️ Character Tools")
        char_tools.pack(fill='x', padx=5, pady=5)
        
        # Body parts
        body_frame = ttk.Frame(char_tools)
        body_frame.pack(side='left', padx=5)
        
        ttk.Label(body_frame, text="Body Parts:").pack()
        body_parts = ["👤 Head", "👕 Torso", "🦵 Left Leg", "🦵 Right Leg", "💪 Left Arm", "💪 Right Arm"]
        
        for part in body_parts:
            ttk.Button(body_frame, text=part, 
                      command=lambda p=part: self.add_body_part(p)).pack(fill='x', pady=1)
        
        # Facial features
        face_frame = ttk.Frame(char_tools)
        face_frame.pack(side='left', padx=5)
        
        ttk.Label(face_frame, text="Facial Features:").pack()
        features = ["👁️ Eyes", "👃 Nose", "👄 Mouth", "👂 Ears", "😊 Expression"]
        
        for feature in features:
            ttk.Button(face_frame, text=feature,
                      command=lambda f=feature: self.add_facial_feature(f)).pack(fill='x', pady=1)
        
        # Rigging tools
        rigging_frame = ttk.Frame(char_tools)
        rigging_frame.pack(side='left', padx=5)
        
        ttk.Label(rigging_frame, text="Rigging:").pack()
        rigging_tools = ["🦴 Add Bone", "🔗 Connect Joints", "⚖️ Set Weights", "🎛️ IK Chain"]
        
        for tool in rigging_tools:
            ttk.Button(rigging_frame, text=tool,
                      command=lambda t=tool: self.use_rigging_tool(t)).pack(fill='x', pady=1)
        
        # Character canvas
        char_canvas_frame = ttk.LabelFrame(character_frame, text="🎨 Character Canvas")
        char_canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.char_canvas = tk.Canvas(char_canvas_frame, width=600, height=400, bg='white')
        self.char_canvas.pack(padx=10, pady=10)
        
        # Character library
        char_lib_frame = ttk.LabelFrame(character_frame, text="📚 Character Library")
        char_lib_frame.pack(fill='x', padx=5, pady=5)
        
        lib_controls = ttk.Frame(char_lib_frame)
        lib_controls.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(lib_controls, text="💾 Save Character", 
                  command=self.save_character).pack(side='left', padx=5)
        ttk.Button(lib_controls, text="📁 Load Character", 
                  command=self.load_character).pack(side='left', padx=5)
        ttk.Button(lib_controls, text="🎲 Random Character", 
                  command=self.generate_random_character).pack(side='left', padx=5)
        
    def setup_effects_tab(self):
        """Setup the effects and transitions tab."""
        effects_frame = ttk.Frame(self.notebook)
        self.notebook.add(effects_frame, text="✨ Effects")
        
        # Effect categories
        effect_categories = ttk.Frame(effects_frame)
        effect_categories.pack(fill='x', padx=5, pady=5)
        
        # Motion effects
        motion_frame = ttk.LabelFrame(effect_categories, text="🌪️ Motion Effects")
        motion_frame.pack(side='left', fill='y', padx=5)
        
        motion_effects = ["💨 Motion Blur", "👻 Ghost Trail", "💫 Sparkle Trail", "🌀 Spiral", "📈 Bounce"]
        
        for effect in motion_effects:
            ttk.Button(motion_frame, text=effect, 
                      command=lambda e=effect: self.apply_motion_effect(e)).pack(fill='x', pady=1)
        
        # Visual effects
        visual_frame = ttk.LabelFrame(effect_categories, text="🎨 Visual Effects")
        visual_frame.pack(side='left', fill='y', padx=5)
        
        visual_effects = ["🌈 Rainbow", "✨ Glitter", "🔥 Fire", "💧 Water", "⚡ Lightning"]
        
        for effect in visual_effects:
            ttk.Button(visual_frame, text=effect,
                      command=lambda e=effect: self.apply_visual_effect(e)).pack(fill='x', pady=1)
        
        # Transitions
        transition_frame = ttk.LabelFrame(effect_categories, text="🎬 Transitions")
        transition_frame.pack(side='left', fill='y', padx=5)
        
        transitions = ["🌊 Fade", "↔️ Slide", "🔄 Rotate", "📏 Wipe", "🎯 Zoom"]
        
        for transition in transitions:
            ttk.Button(transition_frame, text=transition,
                      command=lambda t=transition: self.apply_transition(t)).pack(fill='x', pady=1)
        
        # Effect preview
        preview_frame = ttk.LabelFrame(effects_frame, text="👁️ Effect Preview")
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.effect_canvas = tk.Canvas(preview_frame, width=400, height=300, bg='black')
        self.effect_canvas.pack(padx=10, pady=10)
        
        # Effect controls
        controls_frame = ttk.Frame(effects_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Effect Strength:").pack(side='left', padx=5)
        self.effect_strength_var = tk.IntVar(value=50)
        ttk.Scale(controls_frame, from_=0, to=100, orient='horizontal',
                 variable=self.effect_strength_var).pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(controls_frame, text="✨ Apply Effect", 
                  command=self.confirm_effect).pack(side='right', padx=5)
        
    def setup_tutorial_tab(self):
        """Setup the animation tutorials and learning resources."""
        tutorial_frame = ttk.Frame(self.notebook)
        self.notebook.add(tutorial_frame, text="📚 Learn Animation")
        
        # Tutorial selection
        tutorial_select = ttk.LabelFrame(tutorial_frame, text="🎓 Animation Tutorials")
        tutorial_select.pack(fill='x', padx=5, pady=5)
        
        tutorials = [
            "🎯 Animation Basics - 12 Principles",
            "🎭 Character Animation - Walk Cycle", 
            "🎨 Drawing Techniques - Clean Lines",
            "⏰ Timing and Spacing",
            "🎬 Camera Movements",
            "💫 Special Effects Animation",
            "🔄 Loop Animation Techniques",
            "📊 Storyboarding Basics"
        ]
        
        self.tutorial_var = tk.StringVar(value=tutorials[0])
        tutorial_combo = ttk.Combobox(tutorial_select, textvariable=self.tutorial_var,
                                     values=tutorials, width=50)
        tutorial_combo.pack(side='left', padx=5, pady=5)
        tutorial_combo.bind('<<ComboboxSelected>>', self.load_tutorial)
        
        ttk.Button(tutorial_select, text="▶️ Start Tutorial", 
                  command=self.start_tutorial).pack(side='left', padx=10)
        
        # Tutorial content
        content_frame = ttk.LabelFrame(tutorial_frame, text="📖 Tutorial Content")
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.tutorial_text = tk.Text(content_frame, wrap=tk.WORD, font=('Arial', 11))
        tutorial_scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=self.tutorial_text.yview)
        self.tutorial_text.configure(yscrollcommand=tutorial_scrollbar.set)
        
        self.tutorial_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        tutorial_scrollbar.pack(side='right', fill='y')
        
        # Load initial tutorial
        self.load_tutorial()
        
        # Practice exercises
        practice_frame = ttk.LabelFrame(tutorial_frame, text="💪 Practice Exercises")
        practice_frame.pack(fill='x', padx=5, pady=5)
        
        exercises = [
            ("🎾 Bouncing Ball", "Create a simple bouncing ball animation"),
            ("🚶 Walk Cycle", "Animate a character walking"),
            ("🌊 Wave Motion", "Create flowing wave animation"),
            ("⭐ Morphing Shapes", "Transform one shape into another"),
            ("🎡 Pendulum Swing", "Physics-based pendulum animation")
        ]
        
        for exercise, description in exercises:
            exercise_frame = ttk.Frame(practice_frame)
            exercise_frame.pack(fill='x', padx=5, pady=2)
            
            ttk.Label(exercise_frame, text=exercise, width=20).pack(side='left')
            ttk.Label(exercise_frame, text=description).pack(side='left', padx=10)
            ttk.Button(exercise_frame, text="Try It!", 
                      command=lambda e=exercise: self.start_exercise(e)).pack(side='right')
    
    # Animation methods
    def play_pause(self):
        """Toggle animation playback."""
        if self.is_playing:
            self.is_playing = False
            self.play_button.config(text="▶️")
        else:
            self.is_playing = True
            self.play_button.config(text="⏸️")
            self.play_animation()
            
    def play_animation(self):
        """Play the animation sequence."""
        if not self.is_playing:
            return
            
        # Update frame
        self.next_frame()
        
        # Schedule next frame
        delay = int(1000 / self.fps_var.get())  # Convert FPS to milliseconds
        self.root.after(delay, self.play_animation)
        
    def next_frame(self):
        """Move to next frame."""
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
        elif self.loop_var.get():
            self.current_frame = 0
        else:
            self.is_playing = False
            self.play_button.config(text="▶️")
            
        self.update_frame_display()
        
    def prev_frame(self):
        """Move to previous frame."""
        if self.current_frame > 0:
            self.current_frame -= 1
        self.update_frame_display()
        
    def first_frame(self):
        """Jump to first frame."""
        self.current_frame = 0
        self.update_frame_display()
        
    def last_frame(self):
        """Jump to last frame."""
        self.current_frame = self.total_frames - 1
        self.update_frame_display()
        
    def update_frame_display(self):
        """Update the frame counter display."""
        self.frame_label.config(text=f"{self.current_frame + 1} / {self.total_frames}")
        
    def load_tutorial(self, event=None):
        """Load selected tutorial content."""
        tutorial_content = {
            "🎯 Animation Basics - 12 Principles": """
🎬 THE 12 PRINCIPLES OF ANIMATION

Animation is brought to life through fundamental principles developed by Disney animators. Understanding these principles is essential for creating believable and engaging animations.

1. 🏀 SQUASH AND STRETCH
   • Most important principle
   • Gives weight and flexibility to objects
   • Ball squashes when hitting ground, stretches when bouncing up
   • Maintains volume while deforming

2. 🎯 ANTICIPATION  
   • Prepares audience for main action
   • Crouching before jumping
   • Winding up before throwing
   • Makes actions feel natural and expected

3. 🎭 STAGING
   • Presents idea clearly
   • Camera angle, lighting, character positioning
   • One main action at a time
   • Clear silhouettes and poses

4. 🎨 STRAIGHT AHEAD vs POSE TO POSE
   • Straight Ahead: Draw frame by frame in sequence
   • Pose to Pose: Draw key poses first, fill in between
   • Straight ahead = fluid, spontaneous
   • Pose to pose = controlled, planned

5. 🎪 FOLLOW THROUGH & OVERLAPPING
   • Different parts move at different rates
   • Hair continues moving after head stops
   • Clothes keep swaying after body stops
   • Creates realistic motion

6. 🐌 SLOW IN & SLOW OUT
   • Objects start slowly, speed up, then slow down
   • More frames at start and end of movement
   • Fewer frames in middle (fastest part)
   • Natural physics of acceleration/deceleration

7. 🌊 ARCS
   • Most natural movements follow curved paths
   • Arms swing in arcs, not straight lines
   • Even mechanical movements have slight curves
   • Adds fluidity and grace to motion

8. 🎭 SECONDARY ACTION
   • Supports and enhances main action
   • Facial expressions while walking
   • Tail wagging while dog runs
   • Must not compete with main action

9. ⏰ TIMING
   • Speed of action conveys emotion and meaning
   • Slow = dignified, sad, thoughtful
   • Fast = nervous, excited, frantic
   • Number of frames between key poses

10. 😂 EXAGGERATION
    • Push expressions and actions beyond reality
    • Makes animation more dynamic and appealing
    • Caricature of realistic motion
    • Emphasizes the essence of action

11. 🎨 SOLID DRAWING
    • Understanding of 3D form, weight, balance
    • Good draftsmanship and anatomy
    • Consistent proportions and volumes
    • Strong poses and clear staging

12. 🎭 APPEAL
    • Charismatic quality that draws viewers in
    • Not just "cute" - can be appealing villain
    • Clear design, interesting proportions
    • Easy to read and understand

💡 PRACTICE TIPS:
• Start with simple bouncing ball using squash/stretch
• Study real-world motion and physics
• Exaggerate movements to make them more interesting
• Always think about the emotion behind the movement
• Practice the principles individually, then combine them

🎯 ASSIGNMENT:
Create a short animation (24 frames) that demonstrates at least 3 of these principles. Start simple and focus on making the motion feel alive and believable!
            """,
        }
        
        selected = self.tutorial_var.get()
        content = tutorial_content.get(selected, "Tutorial content loading...")
        
        self.tutorial_text.delete(1.0, tk.END)
        self.tutorial_text.insert(1.0, content)
    
    def run(self):
        """Start the animation studio application."""
        self.root.mainloop()

def main():
    """Main function to run the animation studio."""
    print("🎬 Animation Studio")
    print("=" * 20)
    print("🎭 Create amazing animations")
    print("📚 Learn animation principles")
    print()
    print("Starting Animation Studio...")
    
    studio = AnimationStudio()
    studio.run()

if __name__ == "__main__":
    main()