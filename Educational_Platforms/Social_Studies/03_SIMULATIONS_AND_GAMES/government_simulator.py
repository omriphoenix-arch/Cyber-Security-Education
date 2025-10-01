"""
U.S. Government Simulator - Interactive Civics Learning
A comprehensive simulation of the U.S. government system including legislative, executive, and judicial branches

Features:
- Create and pass legislation
- Supreme Court case decisions
- Presidential powers and actions
- Constitutional principles exploration
- Checks and balances demonstrations
- Electoral process simulation

Requirements: Python 3.8+, tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
from datetime import datetime

class GovernmentSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("U.S. Government Simulator - Interactive Civics")
        self.root.geometry("1400x900")
        
        # Color scheme
        self.bg_color = "#f5f5f5"
        self.primary_color = "#1e3a8a"  # Deep blue
        self.secondary_color = "#dc2626"  # Red
        self.success_color = "#16a34a"  # Green
        self.neutral_color = "#6b7280"  # Gray
        
        self.root.configure(bg=self.bg_color)
        
        # Game state
        self.player_role = None
        self.bills = []
        self.laws = []
        self.court_cases = []
        self.public_approval = 50
        self.budget = 1000000000  # 1 billion
        self.turn = 1
        
        # Initialize UI
        self.create_main_menu()
    
    def create_main_menu(self):
        """Create the main menu"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏛️ U.S. GOVERNMENT SIMULATOR",
                        font=("Arial", 28, "bold"), bg=self.primary_color, fg="white")
        title.pack(pady=30)
        
        # Main menu frame
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(expand=True)
        
        tk.Label(menu_frame, text="Choose Your Branch of Government",
                font=("Arial", 18, "bold"), bg=self.bg_color).pack(pady=20)
        
        # Branch buttons
        branches = [
            ("🏛️ Legislative Branch", "Congress: Make Laws", self.start_legislative, "#1e3a8a"),
            ("⚖️ Judicial Branch", "Supreme Court: Interpret Laws", self.start_judicial, "#7c3aed"),
            ("🏢 Executive Branch", "President: Execute Laws", self.start_executive, "#dc2626"),
            ("📚 Learn About Government", "Educational Resources", self.show_education, "#16a34a"),
        ]
        
        for title_text, desc, command, color in branches:
            btn_frame = tk.Frame(menu_frame, bg=color, relief="raised", bd=3)
            btn_frame.pack(pady=10, padx=50, fill="x")
            
            btn = tk.Button(btn_frame, text=title_text, command=command,
                          font=("Arial", 16, "bold"), bg=color, fg="white",
                          activebackground=color, activeforeground="white",
                          cursor="hand2", relief="flat", pady=15)
            btn.pack(fill="x")
            
            desc_label = tk.Label(btn_frame, text=desc, font=("Arial", 11),
                                bg=color, fg="white")
            desc_label.pack(pady=(0, 10))
        
        # Exit button
        tk.Button(menu_frame, text="Exit", command=self.root.quit,
                 font=("Arial", 12), bg=self.neutral_color, fg="white",
                 cursor="hand2", padx=30, pady=10).pack(pady=20)
    
    def start_legislative(self):
        """Start Legislative Branch simulation"""
        self.player_role = "Congress"
        self.create_legislative_interface()
    
    def create_legislative_interface(self):
        """Create Congressional simulation interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=70)
        header.pack(fill="x")
        
        tk.Label(header, text="🏛️ U.S. Congress - Legislative Branch",
                font=("Arial", 20, "bold"), bg=self.primary_color, fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="← Main Menu", command=self.create_main_menu,
                 bg="white", fg=self.primary_color, font=("Arial", 11, "bold"),
                 cursor="hand2", padx=15, pady=5).pack(side="right", padx=20)
        
        # Main content
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Actions
        left_panel = tk.Frame(content, bg="white", relief="solid", bd=2, width=400)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="Congressional Actions", font=("Arial", 16, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        # Action buttons
        actions = [
            ("📝 Draft New Bill", self.draft_bill),
            ("🗳️ Vote on Bill", self.vote_on_bill),
            ("💰 Approve Budget", self.approve_budget),
            ("🔍 Oversight Hearing", self.conduct_oversight),
            ("🌍 Declare War", self.declare_war),
            ("✅ Override Veto", self.override_veto),
        ]
        
        for action_text, command in actions:
            tk.Button(left_panel, text=action_text, command=command,
                     font=("Arial", 12, "bold"), bg=self.primary_color, fg="white",
                     cursor="hand2", relief="flat", pady=12).pack(fill="x", padx=15, pady=5)
        
        # Info display
        info_frame = tk.Frame(left_panel, bg="#e5e7eb", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=15, pady=15)
        
        self.congress_info = tk.StringVar()
        self.update_congress_info()
        tk.Label(info_frame, textvariable=self.congress_info, font=("Arial", 10),
                bg="#e5e7eb", justify="left", anchor="w").pack(padx=10, pady=10, fill="x")
        
        # Right panel - Bills and Laws
        right_panel = tk.Frame(content, bg="white", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Tabs
        tab_frame = tk.Frame(right_panel, bg="white")
        tab_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(tab_frame, text="📋 Pending Bills", command=lambda: self.show_bills_tab("pending"),
                 font=("Arial", 11, "bold"), bg=self.primary_color, fg="white",
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=2)
        
        tk.Button(tab_frame, text="✅ Passed Laws", command=lambda: self.show_bills_tab("passed"),
                 font=("Arial", 11, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=2)
        
        # Display area
        self.bills_display = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                                       font=("Arial", 11), height=25)
        self.bills_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.show_bills_tab("pending")
    
    def update_congress_info(self):
        """Update congressional info display"""
        info = f"Turn: {self.turn}\n"
        info += f"Bills Pending: {len([b for b in self.bills if b['status'] == 'pending'])}\n"
        info += f"Laws Passed: {len(self.laws)}\n"
        info += f"Public Approval: {self.public_approval}%\n"
        info += f"Federal Budget: ${self.budget:,.0f}"
        self.congress_info.set(info)
    
    def draft_bill(self):
        """Draft a new bill"""
        draft_win = tk.Toplevel(self.root)
        draft_win.title("Draft New Bill")
        draft_win.geometry("600x500")
        draft_win.configure(bg="white")
        
        tk.Label(draft_win, text="Draft New Legislation", font=("Arial", 16, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        # Bill categories
        tk.Label(draft_win, text="Bill Category:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(10, 5))
        
        category_var = tk.StringVar(value="Healthcare")
        categories = ["Healthcare", "Education", "Environment", "Economy", "Defense",
                     "Infrastructure", "Civil Rights", "Technology", "Agriculture"]
        
        category_menu = ttk.Combobox(draft_win, textvariable=category_var, values=categories,
                                     font=("Arial", 11), state="readonly", width=30)
        category_menu.pack()
        
        # Bill title
        tk.Label(draft_win, text="Bill Title:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(15, 5))
        title_entry = tk.Entry(draft_win, font=("Arial", 11), width=50)
        title_entry.pack()
        
        # Bill description
        tk.Label(draft_win, text="Bill Description:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(15, 5))
        desc_text = scrolledtext.ScrolledText(draft_win, font=("Arial", 11),
                                             width=60, height=8, wrap=tk.WORD)
        desc_text.pack(padx=20)
        
        # Funding required
        tk.Label(draft_win, text="Funding Required ($millions):", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(15, 5))
        funding_var = tk.IntVar(value=100)
        tk.Scale(draft_win, from_=0, to=10000, resolution=100, orient="horizontal",
                variable=funding_var, length=400, font=("Arial", 10)).pack()
        
        def submit_bill():
            title = title_entry.get().strip()
            desc = desc_text.get("1.0", tk.END).strip()
            
            if not title or not desc:
                messagebox.showwarning("Incomplete", "Please fill in all fields!")
                return
            
            bill = {
                'id': len(self.bills) + 1,
                'category': category_var.get(),
                'title': title,
                'description': desc,
                'funding': funding_var.get() * 1000000,
                'status': 'pending',
                'votes_for': 0,
                'votes_against': 0,
                'turn_created': self.turn
            }
            
            self.bills.append(bill)
            messagebox.showinfo("Success", f"Bill '{title}' has been drafted and added to the docket!")
            draft_win.destroy()
            self.show_bills_tab("pending")
            self.update_congress_info()
        
        tk.Button(draft_win, text="Submit Bill to Congress", command=submit_bill,
                 font=("Arial", 13, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", pady=12, padx=30).pack(pady=20)
    
    def vote_on_bill(self):
        """Vote on pending bills"""
        pending = [b for b in self.bills if b['status'] == 'pending']
        
        if not pending:
            messagebox.showinfo("No Bills", "There are no pending bills to vote on!")
            return
        
        vote_win = tk.Toplevel(self.root)
        vote_win.title("Vote on Bill")
        vote_win.geometry("700x600")
        vote_win.configure(bg="white")
        
        tk.Label(vote_win, text="Vote on Pending Legislation", font=("Arial", 16, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        # Select bill
        tk.Label(vote_win, text="Select Bill:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        
        selected_bill = tk.IntVar(value=0)
        
        for i, bill in enumerate(pending):
            rb_frame = tk.Frame(vote_win, bg="#f3f4f6", relief="solid", bd=1)
            rb_frame.pack(fill="x", padx=20, pady=5)
            
            tk.Radiobutton(rb_frame, text=f"Bill #{bill['id']}: {bill['title']}",
                          variable=selected_bill, value=i, font=("Arial", 11, "bold"),
                          bg="#f3f4f6", anchor="w").pack(fill="x", padx=10, pady=5)
            
            tk.Label(rb_frame, text=f"Category: {bill['category']} | Funding: ${bill['funding']:,.0f}",
                    font=("Arial", 9), bg="#f3f4f6", fg="#6b7280").pack(anchor="w", padx=30)
        
        # Bill details
        details_frame = tk.Frame(vote_win, bg="#e5e7eb", relief="solid", bd=1)
        details_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        tk.Label(details_frame, text="Bill Details:", font=("Arial", 11, "bold"),
                bg="#e5e7eb").pack(pady=5)
        
        details_text = scrolledtext.ScrolledText(details_frame, font=("Arial", 10),
                                                height=6, wrap=tk.WORD)
        details_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        def update_details():
            bill = pending[selected_bill.get()]
            details_text.delete("1.0", tk.END)
            details_text.insert("1.0", bill['description'])
        
        # Update details when selection changes
        for i in range(len(pending)):
            vote_win.nametowidget(f".!frame{i+2}.!radiobutton").configure(command=update_details)
        
        update_details()
        
        def cast_vote(vote_type):
            bill = pending[selected_bill.get()]
            
            # Simulate congressional vote
            votes_for = random.randint(200, 300)
            votes_against = 435 - votes_for
            
            bill['votes_for'] = votes_for
            bill['votes_against'] = votes_against
            
            if votes_for > 218:  # Majority in House
                bill['status'] = 'passed'
                self.laws.append(bill)
                self.bills.remove(bill)
                self.budget -= bill['funding']
                self.public_approval += random.randint(-5, 10)
                messagebox.showinfo("Bill Passed!", 
                                  f"The bill passed with {votes_for} votes for and {votes_against} against!\n\n"
                                  f"It is now law and will be sent to the President for signature.")
            else:
                bill['status'] = 'failed'
                self.bills.remove(bill)
                messagebox.showinfo("Bill Failed",
                                  f"The bill failed with only {votes_for} votes for and {votes_against} against.")
            
            self.turn += 1
            self.update_congress_info()
            vote_win.destroy()
            self.show_bills_tab("pending")
        
        # Vote buttons
        btn_frame = tk.Frame(vote_win, bg="white")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="✅ Vote YES (Pass Bill)", command=lambda: cast_vote("yes"),
                 font=("Arial", 12, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", padx=20, pady=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Vote NO (Reject Bill)", command=lambda: cast_vote("no"),
                 font=("Arial", 12, "bold"), bg=self.secondary_color, fg="white",
                 cursor="hand2", padx=20, pady=12).pack(side="left", padx=10)
    
    def show_bills_tab(self, tab_type):
        """Display bills based on tab selection"""
        self.bills_display.delete("1.0", tk.END)
        
        if tab_type == "pending":
            pending = [b for b in self.bills if b['status'] == 'pending']
            if not pending:
                self.bills_display.insert("1.0", "No pending bills.\n\nDraft a new bill to get started!")
            else:
                self.bills_display.insert("1.0", "PENDING BILLS\n" + "="*60 + "\n\n")
                for bill in pending:
                    text = f"Bill #{bill['id']}: {bill['title']}\n"
                    text += f"Category: {bill['category']}\n"
                    text += f"Funding: ${bill['funding']:,.0f}\n"
                    text += f"Description: {bill['description']}\n"
                    text += "-" * 60 + "\n\n"
                    self.bills_display.insert(tk.END, text)
        
        elif tab_type == "passed":
            if not self.laws:
                self.bills_display.insert("1.0", "No laws have been passed yet.\n\nVote on pending bills to create laws!")
            else:
                self.bills_display.insert("1.0", "PASSED LAWS\n" + "="*60 + "\n\n")
                for law in self.laws:
                    text = f"Law #{law['id']}: {law['title']}\n"
                    text += f"Category: {law['category']}\n"
                    text += f"Votes: {law['votes_for']} For, {law['votes_against']} Against\n"
                    text += f"Funding: ${law['funding']:,.0f}\n"
                    text += f"Description: {law['description']}\n"
                    text += "-" * 60 + "\n\n"
                    self.bills_display.insert(tk.END, text)
        
        self.bills_display.config(state="disabled")
    
    def approve_budget(self):
        """Budget approval process"""
        messagebox.showinfo("Budget Approval",
                          f"Current Federal Budget: ${self.budget:,.0f}\n\n"
                          f"Congress has the power of the purse!\n"
                          f"Bills require funding allocations.")
    
    def conduct_oversight(self):
        """Congressional oversight"""
        messagebox.showinfo("Oversight Hearing",
                          "Congress conducts oversight hearings to check on executive branch actions.\n\n"
                          "This ensures accountability and proper use of taxpayer funds.")
    
    def declare_war(self):
        """War declaration (requires congressional approval)"""
        result = messagebox.askyesno("Declare War",
                                     "Only Congress has the power to declare war.\n\n"
                                     "This is a serious decision with major consequences.\n\n"
                                     "Declare war?")
        if result:
            self.public_approval -= 20
            messagebox.showwarning("War Declared",
                                  "War has been declared. Public approval decreased by 20%.")
            self.update_congress_info()
    
    def override_veto(self):
        """Override presidential veto"""
        messagebox.showinfo("Veto Override",
                          "Congress can override a presidential veto with a 2/3 majority vote in both chambers.\n\n"
                          "This demonstrates the system of checks and balances!")
    
    def start_judicial(self):
        """Start Judicial Branch simulation"""
        self.player_role = "Supreme Court"
        self.create_judicial_interface()
    
    def create_judicial_interface(self):
        """Create Supreme Court simulation"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg="#7c3aed", height=70)
        header.pack(fill="x")
        
        tk.Label(header, text="⚖️ Supreme Court - Judicial Branch",
                font=("Arial", 20, "bold"), bg="#7c3aed", fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="← Main Menu", command=self.create_main_menu,
                 bg="white", fg="#7c3aed", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=15, pady=5).pack(side="right", padx=20)
        
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Court cases
        cases = [
            {
                'name': 'Miranda v. Arizona',
                'year': 1966,
                'question': 'Must police inform suspects of their rights?',
                'background': 'Ernesto Miranda was arrested and confessed to crimes without being informed of his right to an attorney or against self-incrimination.',
                'arguments_for': '5th Amendment protects against self-incrimination. 6th Amendment guarantees right to counsel.',
                'arguments_against': 'No specific requirement in Constitution. Law enforcement needs flexibility.',
                'ruling': 'Suspects must be informed of rights before interrogation (Miranda Rights).'
            },
            {
                'name': 'Brown v. Board of Education',
                'year': 1954,
                'question': 'Is racial segregation in schools constitutional?',
                'background': 'Linda Brown was denied admission to white school, forced to travel long distance to segregated black school.',
                'arguments_for': '14th Amendment guarantees equal protection. Separate is inherently unequal.',
                'arguments_against': 'Plessy v. Ferguson established "separate but equal" doctrine.',
                'ruling': 'Segregation in public schools is unconstitutional. Overturned Plessy v. Ferguson.'
            },
            {
                'name': 'Tinker v. Des Moines',
                'year': 1969,
                'question': 'Do students have free speech rights in school?',
                'background': 'Students wore black armbands to protest Vietnam War and were suspended.',
                'arguments_for': '1st Amendment protects symbolic speech. Students don\'t lose rights at school gate.',
                'arguments_against': 'Schools need maintain order. Protest could disrupt education.',
                'ruling': 'Students have free speech rights unless it substantially disrupts school.'
            }
        ]
        
        tk.Label(content, text="Select a Supreme Court Case to Review:",
                font=("Arial", 14, "bold"), bg=self.bg_color).pack(pady=15)
        
        for case in cases:
            self.create_case_card(content, case)
    
    def create_case_card(self, parent, case):
        """Create a case card"""
        card = tk.Frame(parent, bg="white", relief="solid", bd=2)
        card.pack(fill="x", padx=50, pady=10)
        
        tk.Label(card, text=f"{case['name']} ({case['year']})",
                font=("Arial", 13, "bold"), bg="white", fg="#7c3aed").pack(anchor="w", padx=15, pady=10)
        
        tk.Label(card, text=f"Constitutional Question: {case['question']}",
                font=("Arial", 11), bg="white", wraplength=800, justify="left").pack(anchor="w", padx=15, pady=5)
        
        tk.Button(card, text="Hear This Case", command=lambda: self.hear_case(case),
                 font=("Arial", 11, "bold"), bg="#7c3aed", fg="white",
                 cursor="hand2", padx=20, pady=8).pack(anchor="e", padx=15, pady=10)
    
    def hear_case(self, case):
        """Hear a Supreme Court case"""
        case_win = tk.Toplevel(self.root)
        case_win.title(f"Supreme Court - {case['name']}")
        case_win.geometry("900x700")
        case_win.configure(bg="white")
        
        # Case title
        tk.Label(case_win, text=case['name'], font=("Arial", 18, "bold"),
                bg="white", fg="#7c3aed").pack(pady=15)
        
        tk.Label(case_win, text=f"Year: {case['year']}", font=("Arial", 12),
                bg="white", fg="#6b7280").pack()
        
        # Constitutional question
        question_frame = tk.Frame(case_win, bg="#fef3c7", relief="solid", bd=1)
        question_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(question_frame, text="Constitutional Question:",
                font=("Arial", 12, "bold"), bg="#fef3c7").pack(anchor="w", padx=10, pady=5)
        tk.Label(question_frame, text=case['question'], font=("Arial", 11),
                bg="#fef3c7", wraplength=800).pack(anchor="w", padx=10, pady=5)
        
        # Background
        bg_frame = tk.Frame(case_win, bg="#e0e7ff", relief="solid", bd=1)
        bg_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(bg_frame, text="Case Background:", font=("Arial", 12, "bold"),
                bg="#e0e7ff").pack(anchor="w", padx=10, pady=5)
        tk.Label(bg_frame, text=case['background'], font=("Arial", 10),
                bg="#e0e7ff", wraplength=800, justify="left").pack(anchor="w", padx=10, pady=5)
        
        # Arguments
        args_frame = tk.Frame(case_win, bg="white")
        args_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Arguments for
        for_frame = tk.Frame(args_frame, bg="#dcfce7", relief="solid", bd=1)
        for_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(for_frame, text="Arguments FOR:", font=("Arial", 11, "bold"),
                bg="#dcfce7", fg="#16a34a").pack(pady=5)
        tk.Label(for_frame, text=case['arguments_for'], font=("Arial", 10),
                bg="#dcfce7", wraplength=380, justify="left").pack(padx=10, pady=5)
        
        # Arguments against
        against_frame = tk.Frame(args_frame, bg="#fee2e2", relief="solid", bd=1)
        against_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(against_frame, text="Arguments AGAINST:", font=("Arial", 11, "bold"),
                bg="#fee2e2", fg="#dc2626").pack(pady=5)
        tk.Label(against_frame, text=case['arguments_against'], font=("Arial", 10),
                bg="#fee2e2", wraplength=380, justify="left").pack(padx=10, pady=5)
        
        # Your decision
        tk.Label(case_win, text="How do you rule?", font=("Arial", 13, "bold"),
                bg="white").pack(pady=10)
        
        def make_ruling(choice):
            result_text = f"Historical Ruling:\n\n{case['ruling']}\n\n"
            if choice == "for":
                result_text += "You ruled in favor of the petitioner."
            else:
                result_text += "You ruled in favor of the respondent."
            
            messagebox.showinfo("Court Decision", result_text)
            case_win.destroy()
        
        btn_frame = tk.Frame(case_win, bg="white")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Rule FOR Petitioner", command=lambda: make_ruling("for"),
                 font=("Arial", 12, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", padx=20, pady=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Rule AGAINST Petitioner", command=lambda: make_ruling("against"),
                 font=("Arial", 12, "bold"), bg=self.secondary_color, fg="white",
                 cursor="hand2", padx=20, pady=12).pack(side="left", padx=10)
    
    def start_executive(self):
        """Start Executive Branch simulation"""
        messagebox.showinfo("Executive Branch",
                          "⚖️ As President, you:\n\n"
                          "• Enforce laws passed by Congress\n"
                          "• Command the armed forces\n"
                          "• Conduct foreign policy\n"
                          "• Appoint federal judges and cabinet members\n"
                          "• Veto or sign legislation\n"
                          "• Issue executive orders\n\n"
                          "This simulation is coming soon!")
    
    def show_education(self):
        """Show educational content"""
        edu_win = tk.Toplevel(self.root)
        edu_win.title("Learn About U.S. Government")
        edu_win.geometry("800x600")
        edu_win.configure(bg="white")
        
        tk.Label(edu_win, text="🏛️ U.S. Government Education",
                font=("Arial", 18, "bold"), bg="white", fg=self.primary_color).pack(pady=15)
        
        notebook = ttk.Notebook(edu_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Three Branches tab
        branches_frame = tk.Frame(notebook, bg="white")
        notebook.add(branches_frame, text="Three Branches")
        
        branches_text = scrolledtext.ScrolledText(branches_frame, wrap=tk.WORD, font=("Arial", 11))
        branches_text.pack(fill="both", expand=True, padx=10, pady=10)
        branches_text.insert("1.0", """
THREE BRANCHES OF GOVERNMENT

The U.S. government is divided into three branches to prevent any one branch from becoming too powerful. This is called "separation of powers."

🏛️ LEGISLATIVE BRANCH (Congress)
• Makes laws
• Two houses: Senate and House of Representatives
• Senate: 100 members (2 per state), 6-year terms
• House: 435 members (based on state population), 2-year terms
• Powers: Pass laws, approve budget, declare war, override vetoes
• Checks on other branches: Can impeach President and judges, approve appointments

⚖️ JUDICIAL BRANCH (Supreme Court and Federal Courts)
• Interprets laws and Constitution
• Supreme Court: 9 justices, lifetime appointments
• Powers: Judicial review, resolve disputes, protect rights
• Checks on other branches: Can declare laws unconstitutional

🏢 EXECUTIVE BRANCH (President)
• Enforces laws
• President, Vice President, Cabinet, federal agencies
• President: 4-year terms, maximum 2 terms
• Powers: Sign or veto bills, command military, conduct foreign policy, appoint judges
• Checks on other branches: Veto legislation, appoint judges, pardon power

CHECKS AND BALANCES
Each branch can limit the powers of the other branches:
• Congress can override presidential vetoes
• President appoints judges, but Senate must confirm
• Courts can declare laws unconstitutional
• President can veto laws
• Congress controls budget, including judiciary funding
        """)
        branches_text.config(state="disabled")
        
        # Constitution tab
        constitution_frame = tk.Frame(notebook, bg="white")
        notebook.add(constitution_frame, text="Constitution")
        
        const_text = scrolledtext.ScrolledText(constitution_frame, wrap=tk.WORD, font=("Arial", 11))
        const_text.pack(fill="both", expand=True, padx=10, pady=10)
        const_text.insert("1.0", """
THE U.S. CONSTITUTION

Written in 1787, ratified in 1788, the Constitution is the supreme law of the United States.

PREAMBLE
"We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defense, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."

SEVEN ARTICLES
Article I: Legislative Branch
Article II: Executive Branch
Article III: Judicial Branch
Article IV: Relations among states
Article V: Amendment process
Article VI: Federal power (Supremacy Clause)
Article VII: Ratification

BILL OF RIGHTS (First 10 Amendments)
1. Freedom of religion, speech, press, assembly, petition
2. Right to bear arms
3. No quartering of soldiers
4. Protection from unreasonable search and seizure
5. Rights of accused (due process, no self-incrimination)
6. Right to speedy and public trial
7. Right to jury trial in civil cases
8. No cruel and unusual punishment
9. Rights not listed still protected
10. Powers not given to federal government belong to states/people

IMPORTANT LATER AMENDMENTS
13th: Abolished slavery (1865)
14th: Equal protection, due process (1868)
15th: Voting rights regardless of race (1870)
19th: Women's right to vote (1920)
26th: Voting age lowered to 18 (1971)

The Constitution can be amended, but it's difficult: requires 2/3 of Congress and 3/4 of states.
        """)
        const_text.config(state="disabled")

def main():
    root = tk.Tk()
    app = GovernmentSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
