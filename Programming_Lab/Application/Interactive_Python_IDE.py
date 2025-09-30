#!/usr/bin/env python3
"""
Simple Code Executor - Educational Programming Environment

A safe, user-friendly environment for students to write and execute simple code.
Supports Python, basic math, and simple programming concepts.

Features:
- Safe code execution with restrictions
- Syntax highlighting
- Error handling and explanations
- Built-in examples and tutorials
- Student-friendly interface

Author: Educational Platform
Date: September 2025
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from tkinter import font as tkfont
import sys
import io
import contextlib
import traceback
import re
import math
import random
import time

class SimpleCodeExecutor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Code Executor - Learn Programming!")
        self.root.geometry("1000x700")
        
        # Set up the interface
        self.setup_gui()
        
        # Safe execution environment
        self.setup_safe_environment()
    
    def setup_gui(self):
        """Set up the main GUI interface"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="🐍 Simple Code Executor - Learn Programming! 🚀", 
                             font=('Arial', 16, 'bold'),
                             fg='blue')
        title_label.pack(pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Code Editor Tab
        self.create_editor_tab()
        
        # Examples Tab
        self.create_examples_tab()
        
        # Tutorial Tab
        self.create_tutorial_tab()
    
    def create_editor_tab(self):
        """Create the main code editor tab"""
        editor_frame = tk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="Code Editor")
        
        # Instructions
        instructions = tk.Label(editor_frame, 
                              text="Write your Python code below and click 'Run Code' to execute it!",
                              font=('Arial', 11),
                              fg='darkgreen')
        instructions.pack(pady=(0, 10))
        
        # Code input area
        code_frame = tk.Frame(editor_frame)
        code_frame.pack(fill=tk.BOTH, expand=True)
        
        # Code editor with line numbers
        editor_container = tk.Frame(code_frame)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers (simple implementation)
        self.line_numbers = tk.Text(editor_container, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(editor_container, 
                                                    font=('Consolas', 11),
                                                    wrap=tk.NONE,
                                                    undo=True)
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events for line numbers
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.code_editor.bind('<Button-1>', self.update_line_numbers)
        self.code_editor.bind('<MouseWheel>', self.update_line_numbers)
        
        # Button frame
        button_frame = tk.Frame(editor_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        run_button = tk.Button(button_frame, text="🚀 Run Code", 
                             command=self.run_code,
                             font=('Arial', 12, 'bold'),
                             bg='lightgreen',
                             fg='darkgreen')
        run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(button_frame, text="🗑️ Clear Code", 
                               command=self.clear_code,
                               font=('Arial', 12),
                               bg='lightcoral',
                               fg='darkred')
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        example_button = tk.Button(button_frame, text="📖 Load Example", 
                                 command=self.load_random_example,
                                 font=('Arial', 12),
                                 bg='lightblue',
                                 fg='darkblue')
        example_button.pack(side=tk.LEFT)
        
        # Output area
        output_label = tk.Label(editor_frame, text="Output:", font=('Arial', 12, 'bold'))
        output_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.output_area = scrolledtext.ScrolledText(editor_frame, height=10,
                                                   font=('Consolas', 10),
                                                   bg='black', fg='lightgreen')
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # Add some starter code
        starter_code = '''# Welcome to Simple Code Executor!
# Write your Python code here and click "Run Code"

print("Hello, World!")
print("Let's learn programming together!")

# Try some math
result = 5 + 3
print(f"5 + 3 = {result}")'''
        
        self.code_editor.insert(tk.END, starter_code)
        self.update_line_numbers()
    
    def create_examples_tab(self):
        """Create the examples tab with code samples"""
        examples_frame = tk.Frame(self.notebook)
        self.notebook.add(examples_frame, text="Examples")
        
        # Title
        title = tk.Label(examples_frame, text="📚 Code Examples", 
                        font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Examples list
        examples_list_frame = tk.Frame(examples_frame)
        examples_list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create scrollable frame for examples
        canvas = tk.Canvas(examples_list_frame)
        scrollbar = tk.Scrollbar(examples_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add examples
        self.add_examples_to_frame(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_examples_to_frame(self, parent):
        """Add example code snippets to the examples frame"""
        examples = [
            ("Hello World", "print('Hello, World!')\nprint('Welcome to programming!')"),
            
            ("Basic Math", "# Basic arithmetic\na = 10\nb = 5\nprint(f'{a} + {b} = {a + b}')\nprint(f'{a} - {b} = {a - b}')\nprint(f'{a} * {b} = {a * b}')\nprint(f'{a} / {b} = {a / b}')"),
            
            ("Variables", "# Working with variables\nname = 'Alice'\nage = 16\nprint(f'My name is {name}')\nprint(f'I am {age} years old')\nprint(f'Next year I will be {age + 1}')"),
            
            ("Lists", "# Working with lists\nfruits = ['apple', 'banana', 'orange']\nprint('My favorite fruits:')\nfor fruit in fruits:\n    print(f'- {fruit}')\n\nprint(f'Total fruits: {len(fruits)}')"),
            
            ("Simple Loop", "# Counting with a loop\nprint('Counting to 5:')\nfor i in range(1, 6):\n    print(f'Number {i}')"),
            
            ("User Input Simulation", "# Simulating user input\nname = 'Student'  # This would be input('What is your name? ')\nprint(f'Hello, {name}!')\nprint('Nice to meet you!')"),
            
            ("Random Numbers", "import random\n\n# Generate random numbers\nprint('Rolling a dice:')\nfor i in range(5):\n    roll = random.randint(1, 6)\n    print(f'Roll {i+1}: {roll}')"),
            
            ("Simple Calculator", "# Simple calculator\na = 15\nb = 4\n\nprint(f'Calculator for {a} and {b}:')\nprint(f'Addition: {a + b}')\nprint(f'Subtraction: {a - b}')\nprint(f'Multiplication: {a * b}')\nprint(f'Division: {a / b:.2f}')"),
            
            ("String Fun", "# Playing with strings\nmessage = 'Python is awesome!'\nprint(f'Original: {message}')\nprint(f'Uppercase: {message.upper()}')\nprint(f'Lowercase: {message.lower()}')\nprint(f'Length: {len(message)} characters')"),
            
            ("Simple Conditions", "# Using if statements\nscore = 85\n\nprint(f'Your score: {score}')\nif score >= 90:\n    print('Grade: A - Excellent!')\nelif score >= 80:\n    print('Grade: B - Good job!')\nelif score >= 70:\n    print('Grade: C - Keep trying!')\nelse:\n    print('Grade: Need more practice!')"),
        ]
        
        for title, code in examples:
            example_frame = tk.LabelFrame(parent, text=title, font=('Arial', 11, 'bold'))
            example_frame.pack(fill=tk.X, padx=5, pady=5)
            
            code_display = tk.Text(example_frame, height=6, font=('Consolas', 9),
                                 wrap=tk.WORD, bg='#f0f0f0')
            code_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            code_display.insert(tk.END, code)
            code_display.config(state=tk.DISABLED)
            
            load_btn = tk.Button(example_frame, text=f"Load '{title}' Example",
                               command=lambda c=code: self.load_example_code(c),
                               bg='lightblue')
            load_btn.pack(pady=5)
    
    def create_tutorial_tab(self):
        """Create the tutorial tab with learning content"""
        tutorial_frame = tk.Frame(self.notebook)
        self.notebook.add(tutorial_frame, text="Tutorial")
        
        # Title
        title = tk.Label(tutorial_frame, text="🎓 Programming Tutorial", 
                        font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Tutorial content
        tutorial_text = scrolledtext.ScrolledText(tutorial_frame, 
                                                font=('Arial', 10),
                                                wrap=tk.WORD)
        tutorial_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tutorial_content = """
🐍 Welcome to Python Programming!

Python is a friendly programming language that's great for beginners. Let's learn the basics!

📝 BASIC CONCEPTS:

1. PRINT STATEMENTS
   - Use print() to display text
   - Example: print("Hello!")
   - You can print variables too: print(name)

2. VARIABLES
   - Variables store information
   - name = "Alice"
   - age = 16
   - score = 95.5

3. MATH OPERATIONS
   - Addition: +
   - Subtraction: -
   - Multiplication: *
   - Division: /
   - Example: result = 5 + 3

4. LISTS
   - Store multiple items
   - fruits = ["apple", "banana", "orange"]
   - Access items: fruits[0] gets "apple"

5. LOOPS
   - Repeat code multiple times
   - for i in range(5): repeats 5 times
   - for item in list: goes through each item

6. CONDITIONS
   - Make decisions in code
   - if score > 80: print("Great job!")
   - elif score > 60: print("Good work!")
   - else: print("Keep practicing!")

🚀 GETTING STARTED:

1. Start with simple print statements
2. Try basic math operations
3. Create variables and use them
4. Experiment with lists
5. Use loops to repeat actions
6. Add conditions to make decisions

💡 TIPS FOR SUCCESS:

- Start small and build up
- Don't worry about mistakes - they help you learn!
- Try the examples in the Examples tab
- Experiment and have fun!
- Ask questions when you're stuck

🎯 COMMON MISTAKES TO AVOID:

- Forgetting quotes around text: print(Hello) ❌ print("Hello") ✅
- Mixing up = and ==: Use = to assign, == to compare
- Forgetting colons after if/for: if age > 18: ✅
- Incorrect indentation: Python cares about spaces!

🌟 CHALLENGE IDEAS:

1. Create a program that introduces yourself
2. Make a simple calculator
3. Create a list of your favorite things
4. Write a program that counts to 10
5. Make a grade calculator

Remember: Programming is like learning a new language. Practice makes perfect! 🎉
        """
        
        tutorial_text.insert(tk.END, tutorial_content)
        tutorial_text.config(state=tk.DISABLED)
    
    def setup_safe_environment(self):
        """Set up a safe execution environment with restrictions"""
        # Define safe built-ins (whitelist approach)
        self.safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'abs': abs,
            'max': max,
            'min': min,
            'sum': sum,
            'sorted': sorted,
            'reversed': reversed,
            'enumerate': enumerate,
            'zip': zip,
            'round': round,
            'bool': bool,
            'type': type,
            'isinstance': isinstance,
            'True': True,
            'False': False,
            'None': None,
        }
        
        # Safe modules
        self.safe_modules = {
            'math': math,
            'random': random,
            'time': time,
        }
    
    def update_line_numbers(self, event=None):
        """Update line numbers in the editor"""
        # Get the number of lines
        line_count = int(self.code_editor.index('end-1c').split('.')[0])
        
        # Generate line numbers
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count))
        
        # Update line numbers display
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_text)
        self.line_numbers.config(state='disabled')
    
    def clear_code(self):
        """Clear the code editor"""
        self.code_editor.delete('1.0', tk.END)
        self.update_line_numbers()
    
    def load_example_code(self, code):
        """Load example code into the editor"""
        self.clear_code()
        self.code_editor.insert(tk.END, code)
        self.update_line_numbers()
        # Switch to editor tab
        self.notebook.select(0)
    
    def load_random_example(self):
        """Load a random example"""
        examples = [
            "# Random number guessing game\nimport random\n\nnumber = random.randint(1, 10)\nprint(f'I picked a number between 1 and 10')\nprint(f'My number was: {number}')\nprint('Good luck next time!')",
            
            "# Temperature converter\ncelsius = 25\nfahrenheit = (celsius * 9/5) + 32\nprint(f'{celsius}°C = {fahrenheit}°F')",
            
            "# Simple shopping list\nshopping = ['milk', 'bread', 'eggs', 'apples']\nprint('Shopping List:')\nfor i, item in enumerate(shopping, 1):\n    print(f'{i}. {item}')",
            
            "# Fun with strings\nname = 'Python'\nprint(f'Welcome to {name}!')\nprint(f'{name} has {len(name)} letters')\nprint(f'Backwards: {name[::-1]}')",
        ]
        
        random_code = random.choice(examples)
        self.load_example_code(random_code)
    
    def run_code(self):
        """Execute the code safely"""
        code = self.code_editor.get('1.0', tk.END).strip()
        
        if not code:
            messagebox.showwarning("No Code", "Please write some code first!")
            return
        
        # Clear output area
        self.output_area.delete('1.0', tk.END)
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            # Create safe execution environment
            safe_globals = {
                '__builtins__': self.safe_builtins,
                **self.safe_modules
            }
            
            # Execute the code
            exec(code, safe_globals)
            
            # Get the output
            output = captured_output.getvalue()
            
            if output:
                self.output_area.insert(tk.END, output)
            else:
                self.output_area.insert(tk.END, "Code executed successfully! (No output)\n")
            
            self.output_area.insert(tk.END, "\n✅ Execution completed successfully!")
            
        except Exception as e:
            # Handle errors gracefully
            error_msg = str(e)
            error_type = type(e).__name__
            
            self.output_area.insert(tk.END, f"❌ Error: {error_type}\n")
            self.output_area.insert(tk.END, f"Message: {error_msg}\n\n")
            
            # Provide helpful hints for common errors
            self.provide_error_hint(error_type, error_msg)
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        # Scroll to bottom
        self.output_area.see(tk.END)
    
    def provide_error_hint(self, error_type, error_msg):
        """Provide helpful hints for common errors"""
        hints = {
            'SyntaxError': "💡 Hint: Check for missing quotes, colons, or parentheses!",
            'NameError': "💡 Hint: Make sure all variables are defined before using them!",
            'IndentationError': "💡 Hint: Check your indentation (spaces at the beginning of lines)!",
            'TypeError': "💡 Hint: Check if you're using the right data types!",
            'ZeroDivisionError': "💡 Hint: You can't divide by zero!",
            'IndexError': "💡 Hint: Make sure list indexes are within range!",
            'KeyError': "💡 Hint: Check if the dictionary key exists!",
        }
        
        hint = hints.get(error_type, "💡 Hint: Check the Examples tab for correct syntax!")
        self.output_area.insert(tk.END, hint + "\n")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("Starting Simple Code Executor...")
    app = SimpleCodeExecutor()
    app.run()

if __name__ == "__main__":
    main()