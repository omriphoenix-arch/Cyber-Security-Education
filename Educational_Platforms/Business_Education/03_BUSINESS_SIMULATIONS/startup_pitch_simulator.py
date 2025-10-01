#!/usr/bin/env python3
"""
Startup Pitch Simulator
=======================
Interactive entrepreneurship training tool for developing business pitch skills.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

class StartupPitchSimulator:
    """Interactive startup pitch development and practice tool."""
    
    def __init__(self):
        """Initialize the pitch simulator."""
        self.pitch_data = {
            'business_name': '',
            'problem': '',
            'solution': '',
            'market_size': '',
            'business_model': '',
            'competition': '',
            'financial_projections': '',
            'team': '',
            'funding_request': ''
        }
        self.investor_feedback = []
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main pitch simulator interface."""
        self.root = tk.Tk()
        self.root.title("🚀 Startup Pitch Simulator - Entrepreneurship Training")
        self.root.geometry("1200x800")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_pitch_builder_tab()
        self.setup_practice_tab()
        self.setup_investor_panel_tab()
        self.setup_feedback_tab()
        self.setup_resources_tab()
        
    def setup_pitch_builder_tab(self):
        """Setup the pitch building tab."""
        builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(builder_frame, text="🔨 Build Your Pitch")
        
        # Create scrollable frame
        canvas = tk.Canvas(builder_frame)
        scrollbar = ttk.Scrollbar(builder_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Business Name
        name_frame = ttk.LabelFrame(scrollable_frame, text="1. Business Name & Tagline")
        name_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(name_frame, text="Business Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.name_entry = ttk.Entry(name_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2, columnspan=2)
        
        ttk.Label(name_frame, text="Tagline:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.tagline_entry = ttk.Entry(name_frame, width=50)
        self.tagline_entry.grid(row=1, column=1, padx=5, pady=2, columnspan=2)
        
        # Problem Statement
        problem_frame = ttk.LabelFrame(scrollable_frame, text="2. Problem Statement")
        problem_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(problem_frame, text="What problem are you solving? (Be specific and compelling)").pack(anchor='w', padx=5)
        self.problem_text = tk.Text(problem_frame, height=4, wrap=tk.WORD)
        self.problem_text.pack(fill='x', padx=5, pady=5)
        
        # Solution
        solution_frame = ttk.LabelFrame(scrollable_frame, text="3. Your Solution")
        solution_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(solution_frame, text="How does your product/service solve this problem?").pack(anchor='w', padx=5)
        self.solution_text = tk.Text(solution_frame, height=4, wrap=tk.WORD)
        self.solution_text.pack(fill='x', padx=5, pady=5)
        
        # Market Size
        market_frame = ttk.LabelFrame(scrollable_frame, text="4. Market Opportunity")
        market_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(market_frame, text="Market Size:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.market_size_entry = ttk.Entry(market_frame, width=30)
        self.market_size_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(market_frame, text="Target Customer:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.target_customer_entry = ttk.Entry(market_frame, width=30)
        self.target_customer_entry.grid(row=0, column=3, padx=5, pady=2)
        
        # Business Model
        model_frame = ttk.LabelFrame(scrollable_frame, text="5. Business Model")
        model_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(model_frame, text="How will you make money?").pack(anchor='w', padx=5)
        self.model_text = tk.Text(model_frame, height=3, wrap=tk.WORD)
        self.model_text.pack(fill='x', padx=5, pady=5)
        
        # Competition
        competition_frame = ttk.LabelFrame(scrollable_frame, text="6. Competition & Advantages")
        competition_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(competition_frame, text="Who are your competitors and what's your competitive advantage?").pack(anchor='w', padx=5)
        self.competition_text = tk.Text(competition_frame, height=3, wrap=tk.WORD)
        self.competition_text.pack(fill='x', padx=5, pady=5)
        
        # Financial Projections
        financial_frame = ttk.LabelFrame(scrollable_frame, text="7. Financial Projections")
        financial_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(financial_frame, text="Revenue Year 1:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.revenue_y1 = ttk.Entry(financial_frame, width=20)
        self.revenue_y1.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(financial_frame, text="Revenue Year 3:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.revenue_y3 = ttk.Entry(financial_frame, width=20)
        self.revenue_y3.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(financial_frame, text="Funding Needed:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.funding_entry = ttk.Entry(financial_frame, width=20)
        self.funding_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(financial_frame, text="Use of Funds:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.funds_use_entry = ttk.Entry(financial_frame, width=20)
        self.funds_use_entry.grid(row=1, column=3, padx=5, pady=2)
        
        # Team
        team_frame = ttk.LabelFrame(scrollable_frame, text="8. Team & Experience")
        team_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(team_frame, text="Who's on your team and why are you the right people to solve this?").pack(anchor='w', padx=5)
        self.team_text = tk.Text(team_frame, height=3, wrap=tk.WORD)
        self.team_text.pack(fill='x', padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(button_frame, text="💾 Save Pitch", command=self.save_pitch).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📋 Load Example", command=self.load_example_pitch).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔍 Analyze Pitch", command=self.analyze_pitch).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎯 Practice Mode", command=self.switch_to_practice).pack(side='left', padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_practice_tab(self):
        """Setup the pitch practice tab."""
        practice_frame = ttk.Frame(self.notebook)
        self.notebook.add(practice_frame, text="🎤 Practice Pitch")
        
        # Timer and controls
        control_frame = ttk.LabelFrame(practice_frame, text="Pitch Timer & Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(control_frame, text="Pitch Duration:").grid(row=0, column=0, padx=5, pady=5)
        self.duration_var = tk.StringVar(value="5 minutes")
        duration_combo = ttk.Combobox(control_frame, textvariable=self.duration_var, 
                                     values=["2 minutes", "5 minutes", "10 minutes", "15 minutes"])
        duration_combo.grid(row=0, column=1, padx=5, pady=5)
        
        self.timer_label = ttk.Label(control_frame, text="00:00", font=('Arial', 20, 'bold'))
        self.timer_label.grid(row=0, column=2, padx=20, pady=5)
        
        ttk.Button(control_frame, text="▶️ Start Timer", command=self.start_timer).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(control_frame, text="⏹️ Stop Timer", command=self.stop_timer).grid(row=0, column=4, padx=5, pady=5)
        
        # Pitch outline display
        outline_frame = ttk.LabelFrame(practice_frame, text="Your Pitch Outline")
        outline_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.outline_text = tk.Text(outline_frame, height=15, wrap=tk.WORD, font=('Arial', 12))
        outline_scrollbar = ttk.Scrollbar(outline_frame, orient='vertical', command=self.outline_text.yview)
        self.outline_text.configure(yscrollcommand=outline_scrollbar.set)
        
        self.outline_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        outline_scrollbar.pack(side='right', fill='y')
        
        # Practice tips
        tips_frame = ttk.LabelFrame(practice_frame, text="💡 Pitch Practice Tips")
        tips_frame.pack(fill='x', padx=5, pady=5)
        
        tips = [
            "🎯 Know your audience - tailor your pitch to the investor type",
            "📊 Lead with the problem - make it relatable and urgent", 
            "⭐ Practice your opening line until it's perfect",
            "🔢 Use specific numbers and metrics where possible",
            "😊 Maintain eye contact and confident body language",
            "⏰ Stay within time limits - practice with a timer"
        ]
        
        for tip in tips:
            ttk.Label(tips_frame, text=tip).pack(anchor='w', padx=5, pady=1)
        
    def setup_investor_panel_tab(self):
        """Setup the simulated investor panel tab."""
        investor_frame = ttk.Frame(self.notebook)
        self.notebook.add(investor_frame, text="👥 Investor Panel")
        
        # Investor selection
        selection_frame = ttk.LabelFrame(investor_frame, text="Select Investor Panel")
        selection_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Choose your audience:").pack(anchor='w', padx=5)
        
        self.investor_type = tk.StringVar(value="Angel Investors")
        investor_options = ["Angel Investors", "Venture Capitalists", "Bank Loan Officers", "Startup Competition Judges"]
        
        for option in investor_options:
            ttk.Radiobutton(selection_frame, text=option, variable=self.investor_type, 
                           value=option).pack(anchor='w', padx=20, pady=2)
        
        ttk.Button(selection_frame, text="🎲 Generate Random Questions", 
                  command=self.generate_investor_questions).pack(pady=10)
        
        # Investor questions display
        questions_frame = ttk.LabelFrame(investor_frame, text="Investor Questions")
        questions_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.questions_text = tk.Text(questions_frame, height=12, wrap=tk.WORD)
        questions_scrollbar = ttk.Scrollbar(questions_frame, orient='vertical', command=self.questions_text.yview)
        self.questions_text.configure(yscrollcommand=questions_scrollbar.set)
        
        self.questions_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        questions_scrollbar.pack(side='right', fill='y')
        
        # Response area
        response_frame = ttk.LabelFrame(investor_frame, text="Your Response")
        response_frame.pack(fill='x', padx=5, pady=5)
        
        self.response_text = tk.Text(response_frame, height=4, wrap=tk.WORD)
        self.response_text.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(response_frame, text="📝 Submit Response", 
                  command=self.submit_response).pack(pady=5)
        
    def setup_feedback_tab(self):
        """Setup the feedback and scoring tab."""
        feedback_frame = ttk.Frame(self.notebook)
        self.notebook.add(feedback_frame, text="📊 Feedback & Score")
        
        # Scoring criteria
        criteria_frame = ttk.LabelFrame(feedback_frame, text="Pitch Evaluation Criteria")
        criteria_frame.pack(fill='x', padx=5, pady=5)
        
        criteria = [
            ("Problem Definition", "How clearly did you define the problem?"),
            ("Solution Clarity", "Is your solution easy to understand?"),
            ("Market Opportunity", "Did you demonstrate a large enough market?"),
            ("Business Model", "Is your revenue model clear and realistic?"),
            ("Competitive Advantage", "What makes you different/better?"),
            ("Financial Projections", "Are your numbers realistic and well-researched?"),
            ("Team Strength", "Do you have the right team to execute?"),
            ("Presentation Skills", "Was your delivery confident and engaging?")
        ]
        
        self.score_vars = {}
        for i, (criterion, description) in enumerate(criteria):
            frame = ttk.Frame(criteria_frame)
            frame.pack(fill='x', padx=5, pady=2)
            
            ttk.Label(frame, text=f"{criterion}:", width=20).pack(side='left')
            
            self.score_vars[criterion] = tk.IntVar(value=5)
            scale = ttk.Scale(frame, from_=1, to=10, orient='horizontal', 
                             variable=self.score_vars[criterion])
            scale.pack(side='left', fill='x', expand=True, padx=5)
            
            score_label = ttk.Label(frame, text="5")
            score_label.pack(side='right')
            
            # Update label when scale moves
            scale.configure(command=lambda val, label=score_label: label.config(text=f"{float(val):.0f}"))
        
        ttk.Button(criteria_frame, text="📊 Calculate Score", 
                  command=self.calculate_pitch_score).pack(pady=10)
        
        # Feedback display
        feedback_display_frame = ttk.LabelFrame(feedback_frame, text="Detailed Feedback")
        feedback_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.feedback_text = tk.Text(feedback_display_frame, wrap=tk.WORD)
        feedback_scrollbar = ttk.Scrollbar(feedback_display_frame, orient='vertical', command=self.feedback_text.yview)
        self.feedback_text.configure(yscrollcommand=feedback_scrollbar.set)
        
        self.feedback_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        feedback_scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        action_frame = ttk.Frame(feedback_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="💡 Get Improvement Tips", 
                  command=self.show_improvement_tips).pack(side='left', padx=5)
        ttk.Button(action_frame, text="📈 Track Progress", 
                  command=self.track_progress).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 New Pitch", 
                  command=self.new_pitch).pack(side='left', padx=5)
        
    def setup_resources_tab(self):
        """Setup the learning resources tab."""
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="📚 Resources")
        
        # Educational content
        content_frame = ttk.LabelFrame(resources_frame, text="Entrepreneurship Learning Center")
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.resources_text = tk.Text(content_frame, wrap=tk.WORD)
        resources_scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=self.resources_text.yview)
        self.resources_text.configure(yscrollcommand=resources_scrollbar.set)
        
        self.resources_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        resources_scrollbar.pack(side='right', fill='y')
        
        # Load educational content
        self.load_entrepreneurship_resources()
        
        # Resource buttons
        button_frame = ttk.Frame(resources_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="🎯 Pitch Templates", 
                  command=lambda: self.show_resource("templates")).pack(side='left', padx=5)
        ttk.Button(button_frame, text="💡 Startup Ideas", 
                  command=lambda: self.show_resource("ideas")).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📊 Market Research", 
                  command=lambda: self.show_resource("research")).pack(side='left', padx=5)
        ttk.Button(button_frame, text="💰 Funding Options", 
                  command=lambda: self.show_resource("funding")).pack(side='left', padx=5)
    
    # Implementation methods
    def save_pitch(self):
        """Save the current pitch data."""
        self.pitch_data = {
            'business_name': self.name_entry.get(),
            'tagline': self.tagline_entry.get(),
            'problem': self.problem_text.get(1.0, tk.END).strip(),
            'solution': self.solution_text.get(1.0, tk.END).strip(),
            'market_size': self.market_size_entry.get(),
            'target_customer': self.target_customer_entry.get(),
            'business_model': self.model_text.get(1.0, tk.END).strip(),
            'competition': self.competition_text.get(1.0, tk.END).strip(),
            'revenue_y1': self.revenue_y1.get(),
            'revenue_y3': self.revenue_y3.get(),
            'funding_needed': self.funding_entry.get(),
            'funds_use': self.funds_use_entry.get(),
            'team': self.team_text.get(1.0, tk.END).strip()
        }
        
        try:
            filename = f"pitch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.pitch_data, f, indent=2)
            messagebox.showinfo("Pitch Saved", f"Your pitch has been saved as {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save pitch: {e}")
    
    def load_example_pitch(self):
        """Load an example pitch for learning."""
        examples = {
            'EcoDelivery': {
                'name': 'EcoDelivery',
                'tagline': 'Carbon-neutral delivery for a sustainable future',
                'problem': 'Last-mile delivery creates 25% of urban carbon emissions. Consumers want convenient delivery but feel guilty about environmental impact.',
                'solution': 'Electric bike and drone delivery network that reduces emissions by 80% while maintaining speed and convenience.',
                'market_size': '$150 billion delivery market',
                'target': 'Environmentally conscious urban consumers aged 25-45',
                'model': 'Subscription service + per-delivery fees. Premium pricing for guaranteed carbon-neutral delivery.',
                'competition': 'Traditional delivery services like UberEats, DoorDash lack environmental focus. We differentiate through sustainability and community impact.',
                'revenue_y1': '$500,000',
                'revenue_y3': '$5,000,000',
                'funding': '$2,000,000',
                'funds_use': '60% fleet expansion, 25% technology, 15% marketing',
                'team': 'CEO with 10 years logistics experience, CTO from Tesla, sustainability advisor from Patagonia'
            }
        }
        
        example = examples['EcoDelivery']
        
        # Fill in the form
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, example['name'])
        
        self.tagline_entry.delete(0, tk.END)
        self.tagline_entry.insert(0, example['tagline'])
        
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(1.0, example['problem'])
        
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(1.0, example['solution'])
        
        messagebox.showinfo("Example Loaded", "EcoDelivery example pitch loaded! Study this structure and adapt for your own idea.")
    
    def switch_to_practice(self):
        """Switch to practice tab and load current pitch."""
        # Generate outline from current data
        outline = self.generate_pitch_outline()
        self.outline_text.delete(1.0, tk.END)
        self.outline_text.insert(1.0, outline)
        
        # Switch to practice tab
        self.notebook.select(1)  # Index 1 is practice tab
    
    def generate_pitch_outline(self):
        """Generate a structured pitch outline."""
        outline = f"""
🚀 YOUR PITCH OUTLINE - {self.name_entry.get() or '[Business Name]'}
{'='*60}

1. HOOK & INTRODUCTION (30 seconds)
   "Hi, I'm [Your Name], and I'm here to talk about {self.name_entry.get() or '[Business Name]'}"
   Tagline: "{self.tagline_entry.get() or '[Your compelling tagline]'}"

2. THE PROBLEM (1 minute)
   {self.problem_text.get(1.0, tk.END).strip() or '[Describe the problem you\'re solving]'}

3. YOUR SOLUTION (1-2 minutes)  
   {self.solution_text.get(1.0, tk.END).strip() or '[Explain your solution]'}

4. MARKET OPPORTUNITY (30 seconds)
   Market Size: {self.market_size_entry.get() or '[Market size]'}
   Target Customer: {self.target_customer_entry.get() or '[Target customer]'}

5. BUSINESS MODEL (30 seconds)
   {self.model_text.get(1.0, tk.END).strip() or '[How you make money]'}

6. COMPETITION & ADVANTAGE (30 seconds)
   {self.competition_text.get(1.0, tk.END).strip() or '[Your competitive advantage]'}

7. FINANCIAL PROJECTIONS (30 seconds)
   Year 1 Revenue: ${self.revenue_y1.get() or '[Y1 Revenue]'}
   Year 3 Revenue: ${self.revenue_y3.get() or '[Y3 Revenue]'}

8. THE TEAM (30 seconds)
   {self.team_text.get(1.0, tk.END).strip() or '[Your team and experience]'}

9. FUNDING REQUEST & USE (30 seconds)
   Seeking: ${self.funding_entry.get() or '[Funding amount]'}
   Use: {self.funds_use_entry.get() or '[How you\'ll use the money]'}

10. CLOSING & CALL TO ACTION (15 seconds)
    "We're excited to partner with investors who share our vision. 
    Are you ready to join us in [achieving your mission]?"

💡 DELIVERY TIPS:
• Maintain eye contact with your audience
• Use confident body language
• Speak clearly and at appropriate pace  
• Show passion for your business
• Be prepared for questions
• Practice until you can deliver without notes
        """
        return outline
    
    def generate_investor_questions(self):
        """Generate realistic investor questions based on type."""
        question_sets = {
            "Angel Investors": [
                "What's your customer acquisition cost and lifetime value?",
                "How do you plan to scale this business?", 
                "What keeps you up at night about this business?",
                "Who are your first 10 customers going to be?",
                "What happens if a big company copies your idea?",
                "How much of your own money have you invested?",
                "What's your exit strategy?"
            ],
            "Venture Capitalists": [
                "What's your total addressable market (TAM)?",
                "Show me your unit economics and path to profitability",
                "What are your key metrics and how do you track them?",
                "How will you use this funding to achieve 10x growth?",
                "What's your competitive moat and how will you defend it?",
                "Who else is in this space and why will you win?",
                "What's your customer acquisition strategy?"
            ],
            "Bank Loan Officers": [
                "What collateral can you provide for this loan?",
                "Show me your cash flow projections for the next 2 years",
                "What's your credit history and personal financial situation?",
                "How will you repay this loan if the business fails?",
                "What experience do you have running a business?",
                "What's your debt-to-income ratio?",
                "Do you have a business plan and financial statements?"
            ],
            "Startup Competition Judges": [
                "What's the most innovative aspect of your solution?",
                "How does this create social or economic impact?",
                "What validation do you have that customers want this?",
                "What's your go-to-market strategy?",
                "How does this differentiate from existing solutions?",
                "What's your timeline for launching and scaling?",
                "What support do you need beyond funding?"
            ]
        }
        
        selected_questions = random.sample(question_sets[self.investor_type.get()], 4)
        
        questions_display = f"""
👥 {self.investor_type.get().upper()} PANEL QUESTIONS:
{'='*50}

"""
        for i, question in enumerate(selected_questions, 1):
            questions_display += f"{i}. {question}\n\n"
        
        questions_display += """
💡 TIPS FOR ANSWERING:
• Be specific with numbers and data
• Acknowledge challenges honestly  
• Show you've done your research
• Connect back to your core value proposition
• Ask clarifying questions if needed
"""
        
        self.questions_text.delete(1.0, tk.END)
        self.questions_text.insert(1.0, questions_display)
    
    def load_entrepreneurship_resources(self):
        """Load comprehensive entrepreneurship education content."""
        content = """
🚀 ENTREPRENEURSHIP LEARNING CENTER

📚 STARTUP FUNDAMENTALS:

1. IDEATION & VALIDATION
   • Problems are opportunities in disguise
   • Talk to 100 potential customers before building
   • Validate demand before creating supply
   • Start with a minimum viable product (MVP)
   • Iterate based on customer feedback

2. BUSINESS MODEL DESIGN
   • Revenue streams: How will you make money?
   • Cost structure: What are your main expenses?
   • Value propositions: What value do you create?
   • Customer segments: Who are you serving?
   • Channels: How will you reach customers?

3. MARKET RESEARCH & ANALYSIS
   • Total Addressable Market (TAM)
   • Serviceable Addressable Market (SAM) 
   • Serviceable Obtainable Market (SOM)
   • Competitive landscape analysis
   • Customer persona development

4. FINANCIAL PLANNING & FUNDING
   • Cash flow is king - track it religiously
   • Understand your unit economics
   • Bootstrap vs. external funding
   • Types of investors: Angels, VCs, crowdfunding
   • Valuation methods and equity considerations

5. TEAM BUILDING & LEADERSHIP
   • Hire slowly, fire quickly
   • Equity distribution among founders
   • Building company culture from day one
   • Advisory boards and mentorship
   • Delegation and scaling leadership

6. MARKETING & SALES
   • Product-market fit comes first
   • Digital marketing vs. traditional methods
   • Sales funnels and conversion optimization
   • Customer acquisition cost (CAC)
   • Customer lifetime value (CLV)

7. LEGAL & OPERATIONAL BASICS
   • Business structure: LLC, Corporation, Partnership
   • Intellectual property protection
   • Contracts and legal agreements
   • Insurance and risk management
   • Accounting and bookkeeping systems

🎯 PITCH DECK ESSENTIALS:

Slide 1: Title & Contact Info
Slide 2: Problem Statement
Slide 3: Solution Overview
Slide 4: Market Opportunity
Slide 5: Product Demo/Screenshots
Slide 6: Business Model
Slide 7: Go-to-Market Strategy
Slide 8: Competition Analysis
Slide 9: Financial Projections
Slide 10: Team Bios
Slide 11: Funding Request & Use
Slide 12: Contact & Next Steps

💡 SUCCESS TRAITS OF ENTREPRENEURS:
• Persistence in face of rejection
• Willingness to take calculated risks
• Customer obsession over product obsession
• Adaptability when plans don't work
• Strong communication and storytelling
• Financial discipline and cash management
• Network building and relationship focus
• Continuous learning and skill development

🚨 COMMON STARTUP MISTAKES:
• Building product without customer validation
• Running out of cash (poor financial planning)
• Hiring too fast or wrong people
• Focusing on competition instead of customers
• Perfectionism preventing launch
• Ignoring legal and compliance issues
• Poor pricing strategy
• Neglecting marketing and sales

📈 GROWTH STRATEGIES:
• Viral marketing and referral programs
• Content marketing and SEO
• Strategic partnerships and alliances
• Product-led growth strategies
• Community building and engagement
• Data-driven optimization
• International expansion planning
• Platform and marketplace strategies

Remember: Entrepreneurship is a marathon, not a sprint. 
Focus on solving real problems for real people!
        """
        
        self.resources_text.delete(1.0, tk.END)
        self.resources_text.insert(1.0, content)
    
    def run(self):
        """Start the startup pitch simulator application."""
        self.root.mainloop()

def main():
    """Main function to run the startup pitch simulator."""
    print("🚀 Startup Pitch Simulator")
    print("=" * 30)
    print("🎯 Learn entrepreneurship through pitch practice")
    print("💡 Develop business ideas and presentation skills")
    print()
    print("Starting Pitch Simulator...")
    
    simulator = StartupPitchSimulator()
    simulator.run()

if __name__ == "__main__":
    main()