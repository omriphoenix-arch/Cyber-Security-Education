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
        self.bills_passed = 0
        self.bills_failed = 0
        self.vetoes_issued = 0
        self.executive_orders = 0
        self.cases_decided = 0
        self.achievements = []
        
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
            ("🗳️ Election Simulator", "Run a Presidential Campaign", self.start_election, "#f59e0b"),
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
        
        # Save/Load buttons
        save_frame = tk.Frame(menu_frame, bg=self.bg_color)
        save_frame.pack(pady=10)
        
        tk.Button(save_frame, text="💾 Save Game", command=self.save_game,
                 font=("Arial", 11), bg="#10b981", fg="white",
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(save_frame, text="📁 Load Game", command=self.load_game,
                 font=("Arial", 11), bg="#3b82f6", fg="white",
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(save_frame, text="🏆 Achievements", command=self.show_achievements,
                 font=("Arial", 11), bg="#f59e0b", fg="white",
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
    
    def save_game(self):
        """Save game state to file"""
        game_state = {
            'player_role': self.player_role,
            'bills': self.bills,
            'laws': self.laws,
            'court_cases': self.court_cases,
            'public_approval': self.public_approval,
            'budget': self.budget,
            'turn': self.turn,
            'bills_passed': self.bills_passed,
            'bills_failed': self.bills_failed,
            'vetoes_issued': self.vetoes_issued,
            'executive_orders': self.executive_orders,
            'cases_decided': self.cases_decided,
            'achievements': self.achievements
        }
        
        try:
            with open('government_simulator_save.json', 'w') as f:
                json.dump(game_state, f, indent=2)
            messagebox.showinfo("Save Successful", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        """Load game state from file"""
        try:
            with open('government_simulator_save.json', 'r') as f:
                game_state = json.load(f)
            
            self.player_role = game_state.get('player_role')
            self.bills = game_state.get('bills', [])
            self.laws = game_state.get('laws', [])
            self.court_cases = game_state.get('court_cases', [])
            self.public_approval = game_state.get('public_approval', 50)
            self.budget = game_state.get('budget', 1000000000)
            self.turn = game_state.get('turn', 1)
            self.bills_passed = game_state.get('bills_passed', 0)
            self.bills_failed = game_state.get('bills_failed', 0)
            self.vetoes_issued = game_state.get('vetoes_issued', 0)
            self.executive_orders = game_state.get('executive_orders', 0)
            self.cases_decided = game_state.get('cases_decided', 0)
            self.achievements = game_state.get('achievements', [])
            
            messagebox.showinfo("Load Successful", "Game loaded successfully!")
            
            # Return to appropriate interface
            if self.player_role == "Congress":
                self.create_legislative_interface()
            elif self.player_role == "Supreme Court":
                self.create_judicial_interface()
            elif self.player_role == "President":
                self.create_executive_interface()
            else:
                self.create_main_menu()
                
        except FileNotFoundError:
            messagebox.showwarning("No Save File", "No saved game found!")
        except Exception as e:
            messagebox.showerror("Load Failed", f"Failed to load game: {str(e)}")
    
    def check_achievements(self):
        """Check and award achievements"""
        new_achievements = []
        
        # Legislative achievements
        if len(self.laws) >= 5 and "Lawmaker" not in self.achievements:
            new_achievements.append("Lawmaker")
        if len(self.laws) >= 10 and "Legislative Leader" not in self.achievements:
            new_achievements.append("Legislative Leader")
        if self.public_approval >= 80 and "Popular Politician" not in self.achievements:
            new_achievements.append("Popular Politician")
        
        # Judicial achievements
        if self.cases_decided >= 3 and "Justice" not in self.achievements:
            new_achievements.append("Justice")
        if self.cases_decided >= 8 and "Chief Justice" not in self.achievements:
            new_achievements.append("Chief Justice")
        
        # Executive achievements
        if self.vetoes_issued >= 3 and "Veto Power" not in self.achievements:
            new_achievements.append("Veto Power")
        if self.executive_orders >= 5 and "Executive Authority" not in self.achievements:
            new_achievements.append("Executive Authority")
        
        # General achievements
        if self.turn >= 20 and "Experienced Leader" not in self.achievements:
            new_achievements.append("Experienced Leader")
        if self.budget >= 2000000000 and "Economic Genius" not in self.achievements:
            new_achievements.append("Economic Genius")
        
        if new_achievements:
            self.achievements.extend(new_achievements)
            achievement_text = "🏆 New Achievements Unlocked!\n\n" + "\n".join(f"• {ach}" for ach in new_achievements)
            messagebox.showinfo("Achievement Unlocked!", achievement_text)
    
    def show_achievements(self):
        """Display achievements"""
        ach_win = tk.Toplevel(self.root)
        ach_win.title("Achievements")
        ach_win.geometry("500x400")
        ach_win.configure(bg="white")
        
        tk.Label(ach_win, text="🏆 Achievements", font=("Arial", 18, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        if not self.achievements:
            tk.Label(ach_win, text="No achievements unlocked yet.\n\nKeep playing to earn achievements!",
                    font=("Arial", 12), bg="white").pack(pady=20)
        else:
            achievements_frame = tk.Frame(ach_win, bg="white")
            achievements_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            for achievement in self.achievements:
                ach_frame = tk.Frame(achievements_frame, bg="#fef3c7", relief="solid", bd=1)
                ach_frame.pack(fill="x", pady=5)
                tk.Label(ach_frame, text=f"🏆 {achievement}", font=("Arial", 12, "bold"),
                        bg="#fef3c7").pack(pady=8, padx=15)
        
        tk.Button(ach_win, text="Close", command=ach_win.destroy,
                 font=("Arial", 12, "bold"), bg=self.primary_color, fg="white",
                 cursor="hand2", padx=20, pady=8).pack(pady=15)
    
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
        
        def update_details(*args):
            bill = pending[selected_bill.get()]
            details_text.delete("1.0", tk.END)
            details_text.insert("1.0", bill['description'])
        
        # Update details when selection changes
        selected_bill.trace_add('write', update_details)
        
        update_details()
        
        def cast_vote(vote_type):
            bill = pending[selected_bill.get()]
            
            # Simulate congressional vote with player influence
            base_votes_for = random.randint(180, 250)
            base_votes_against = 435 - base_votes_for
            
            # Player's vote influences the outcome
            if vote_type == "yes":
                votes_for = base_votes_for + random.randint(10, 30)  # Player support boosts the bill
                votes_against = 435 - votes_for
            else:
                votes_for = base_votes_for - random.randint(10, 30)  # Player opposition hurts the bill
                votes_against = 435 - votes_for
            
            # Ensure reasonable bounds
            votes_for = max(150, min(285, votes_for))
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
            self.check_achievements()
        
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
            self.budget -= 100000000000  # 100 billion for war
            messagebox.showwarning("War Declared",
                                  "War has been declared. Public approval decreased by 20%.\n"
                                  f"War funding: $100 billion deducted from budget.")
            self.update_congress_info()
    
    def override_veto(self):
        """Override presidential veto"""
        vetoed_bills = [b for b in self.bills if b.get('status') == 'vetoed']
        
        if not vetoed_bills:
            messagebox.showinfo("No Vetoes", "There are no vetoed bills to override.")
            return
        
        override_win = tk.Toplevel(self.root)
        override_win.title("Override Presidential Veto")
        override_win.geometry("600x400")
        override_win.configure(bg="white")
        
        tk.Label(override_win, text="Override Presidential Veto", font=("Arial", 16, "bold"),
                bg="white", fg=self.primary_color).pack(pady=15)
        
        bill = vetoed_bills[0]
        
        tk.Label(override_win, text=f"Vetoed Bill: {bill['title']}", font=("Arial", 13, "bold"),
                bg="white").pack(pady=10)
        
        info_frame = tk.Frame(override_win, bg="#f3f4f6", relief="solid", bd=1)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_text = f"Category: {bill['category']}\n"
        info_text += f"Funding: ${bill['funding']:,.0f}\n"
        info_text += f"Description: {bill['description'][:200]}..."
        
        tk.Label(info_frame, text=info_text, font=("Arial", 11),
                bg="#f3f4f6", justify="left", wraplength=500).pack(padx=15, pady=15)
        
        tk.Label(override_win, text="Congress needs 2/3 majority to override veto.",
                font=("Arial", 11), bg="white").pack(pady=10)
        
        def attempt_override():
            # Simulate congressional override vote
            votes_for = random.randint(250, 400)
            votes_against = 435 - votes_for
            
            if votes_for >= 290:  # 2/3 of 435 ≈ 290
                bill['status'] = 'passed'
                self.laws.append(bill)
                self.bills.remove(bill)
                self.budget -= bill['funding']
                self.public_approval += random.randint(-5, 5)
                messagebox.showinfo("Veto Overridden!", 
                                  f"Congress successfully overrode the veto!\n\n"
                                  f"Vote: {votes_for} for, {votes_against} against\n\n"
                                  f"'{bill['title']}' is now law!")
            else:
                messagebox.showinfo("Veto Sustained",
                                  f"Veto sustained. Not enough votes to override.\n\n"
                                  f"Vote: {votes_for} for, {votes_against} against")
            
            self.turn += 1
            self.update_congress_info()
            override_win.destroy()
            self.show_bills_tab("passed")
        
        tk.Button(override_win, text="Attempt Override Vote", command=attempt_override,
                 font=("Arial", 13, "bold"), bg=self.primary_color, fg="white",
                 cursor="hand2", pady=12, padx=30).pack(pady=20)
    
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
            },
            {
                'name': 'Gideon v. Wainwright',
                'year': 1963,
                'question': 'Does the Constitution require states to provide attorneys to defendants who cannot afford them?',
                'background': 'Clarence Gideon was charged with breaking and entering but could not afford a lawyer. He represented himself and was convicted.',
                'arguments_for': '6th Amendment guarantees right to counsel. Fair trial impossible without legal representation.',
                'arguments_against': 'States should have flexibility. Not all cases require attorney. Too expensive.',
                'ruling': 'States must provide attorneys to defendants who cannot afford them in criminal cases.'
            },
            {
                'name': 'Marbury v. Madison',
                'year': 1803,
                'question': 'Can the Supreme Court declare laws unconstitutional?',
                'background': 'William Marbury sued to receive his commission as a justice of the peace. The Court had to decide if it could order the executive branch to act.',
                'arguments_for': 'Constitution is supreme law. Courts must interpret law. Judicial independence is essential.',
                'arguments_against': 'Constitution doesn\'t explicitly grant this power. Unelected judges shouldn\'t overrule elected officials.',
                'ruling': 'Established judicial review: Supreme Court can declare laws unconstitutional. Foundational case for judicial power.'
            },
            {
                'name': 'Roe v. Wade',
                'year': 1973,
                'question': 'Does the Constitution protect a woman\'s right to choose to have an abortion?',
                'background': 'Norma McCorvey (Jane Roe) challenged Texas law criminalizing abortion except to save mother\'s life.',
                'arguments_for': '14th Amendment protects privacy and personal liberty. Government intrusion on personal medical decisions.',
                'arguments_against': 'State interest in protecting potential life. Not explicitly mentioned in Constitution.',
                'ruling': 'Constitution protects right to abortion, but states can regulate after certain point. (Note: Overturned in 2022)'
            },
            {
                'name': 'New Jersey v. T.L.O.',
                'year': 1985,
                'question': 'Do school officials need a warrant to search students?',
                'background': 'A student was caught smoking and her purse was searched, revealing drug paraphernalia. She argued it violated 4th Amendment.',
                'arguments_for': 'Students have constitutional rights. Searches require probable cause and warrant.',
                'arguments_against': 'Schools need maintain order and safety. Lower standard appropriate in school setting.',
                'ruling': 'School officials can search without warrant if there are reasonable grounds. Lower standard than police searches.'
            },
            {
                'name': 'United States v. Nixon',
                'year': 1974,
                'question': 'Must the President comply with a court order to turn over evidence?',
                'background': 'President Nixon refused to release Watergate tape recordings, claiming executive privilege.',
                'arguments_for': 'No one is above the law. Courts need evidence for fair trials. Limited executive privilege.',
                'arguments_against': 'Presidential communications must be confidential. Executive privilege protects separation of powers.',
                'ruling': 'President must comply with court orders. Executive privilege exists but is not absolute. Nixon resigned shortly after.'
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
        self.player_role = "President"
        self.create_executive_interface()
    
    def create_executive_interface(self):
        """Create Presidential simulation interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.root, bg=self.secondary_color, height=70)
        header.pack(fill="x")
        
        tk.Label(header, text="🏢 Office of the President - Executive Branch",
                font=("Arial", 20, "bold"), bg=self.secondary_color, fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="← Main Menu", command=self.create_main_menu,
                 bg="white", fg=self.secondary_color, font=("Arial", 11, "bold"),
                 cursor="hand2", padx=15, pady=5).pack(side="right", padx=20)
        
        # Main content
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Presidential Actions
        left_panel = tk.Frame(content, bg="white", relief="solid", bd=2, width=400)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="Presidential Powers", font=("Arial", 16, "bold"),
                bg="white", fg=self.secondary_color).pack(pady=15)
        
        # Action buttons
        actions = [
            ("✍️ Sign/Veto Legislation", self.sign_or_veto),
            ("📋 Issue Executive Order", self.issue_executive_order),
            ("👥 Appoint Cabinet Member", self.appoint_cabinet),
            ("⚖️ Nominate Supreme Court Justice", self.nominate_justice),
            ("🌍 Conduct Foreign Policy", self.foreign_policy),
            ("🎖️ Military Command", self.military_action),
            ("🗳️ Campaign for Re-election", self.campaign),
            ("📺 Press Conference", self.press_conference),
        ]
        
        for action_text, command in actions:
            tk.Button(left_panel, text=action_text, command=command,
                     font=("Arial", 11, "bold"), bg=self.secondary_color, fg="white",
                     cursor="hand2", relief="flat", pady=10).pack(fill="x", padx=15, pady=3)
        
        # Info display
        info_frame = tk.Frame(left_panel, bg="#fee2e2", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=15, pady=15)
        
        if not hasattr(self, 'president_info'):
            self.president_info = tk.StringVar()
        self.update_president_info()
        tk.Label(info_frame, textvariable=self.president_info, font=("Arial", 10),
                bg="#fee2e2", justify="left", anchor="w").pack(padx=10, pady=10, fill="x")
        
        # Right panel - Actions Log
        right_panel = tk.Frame(content, bg="white", relief="solid", bd=2)
        right_panel.pack(side="right", fill="both", expand=True)
        
        tk.Label(right_panel, text="📜 Presidential Actions Log", font=("Arial", 14, "bold"),
                bg="white", fg=self.secondary_color).pack(pady=10)
        
        if not hasattr(self, 'exec_display') or not self.exec_display.winfo_exists():
            self.exec_display = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                                          font=("Arial", 11), height=25)
            self.exec_display.pack(fill="both", expand=True, padx=10, pady=10)
            self.exec_display.insert("1.0", "Welcome to the Oval Office!\n\n"
                                           "As President, you have executive powers to enforce laws, "
                                           "conduct foreign policy, and lead the nation.\n\n"
                                           "Your actions will be logged here.\n" + "="*60 + "\n\n")
        else:
            self.exec_display.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_president_info(self):
        """Update presidential info display"""
        info = f"Turn: {self.turn}\n"
        info += f"Public Approval: {self.public_approval}%\n"
        info += f"Laws to Review: {len([b for b in self.bills if b.get('status') == 'passed'])}\n"
        info += f"Federal Budget: ${self.budget:,.0f}\n"
        info += f"Days in Office: {self.turn * 30}"
        if hasattr(self, 'president_info'):
            self.president_info.set(info)
    
    def log_executive_action(self, text):
        """Safely log executive action"""
        if hasattr(self, 'exec_display') and self.exec_display.winfo_exists():
            self.exec_display.insert(tk.END, text)
    
    def sign_or_veto(self):
        """Sign or veto legislation"""
        passed_bills = [b for b in self.bills if b.get('status') == 'passed']
        
        if not passed_bills:
            messagebox.showinfo("No Legislation", "No bills have been passed by Congress for your review.")
            return
        
        veto_win = tk.Toplevel(self.root)
        veto_win.title("Sign or Veto Legislation")
        veto_win.geometry("700x500")
        veto_win.configure(bg="white")
        
        tk.Label(veto_win, text="Review Congressional Legislation", font=("Arial", 16, "bold"),
                bg="white", fg=self.secondary_color).pack(pady=15)
        
        bill = passed_bills[0]
        
        tk.Label(veto_win, text=f"Bill: {bill['title']}", font=("Arial", 13, "bold"),
                bg="white").pack(pady=10)
        
        info_frame = tk.Frame(veto_win, bg="#f3f4f6", relief="solid", bd=1)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_text = f"Category: {bill['category']}\n"
        info_text += f"Funding Required: ${bill['funding']:,.0f}\n"
        info_text += f"Congressional Vote: {bill.get('votes_for', 0)} For, {bill.get('votes_against', 0)} Against\n\n"
        info_text += f"Description:\n{bill['description']}"
        
        tk.Label(info_frame, text=info_text, font=("Arial", 11),
                bg="#f3f4f6", justify="left", wraplength=600).pack(padx=15, pady=15)
        
        def sign_bill():
            bill['status'] = 'signed'
            self.bills.remove(bill)
            self.laws.append(bill)
            self.public_approval += random.randint(-3, 8)
            log_text = f"✅ SIGNED: {bill['title']}\n"
            log_text += f"   Public approval: {self.public_approval}%\n"
            log_text += "-" * 60 + "\n\n"
            self.log_executive_action(log_text)
            messagebox.showinfo("Bill Signed", f"You have signed '{bill['title']}' into law!")
            self.turn += 1
            self.update_president_info()
            veto_win.destroy()
            self.check_achievements()
        
        def veto_bill():
            bill['status'] = 'vetoed'
            self.bills.remove(bill)
            self.public_approval += random.randint(-8, 3)
            log_text = f"❌ VETOED: {bill['title']}\n"
            log_text += f"   Congress can override with 2/3 vote\n"
            log_text += f"   Public approval: {self.public_approval}%\n"
            log_text += "-" * 60 + "\n\n"
            self.log_executive_action(log_text)
            messagebox.showinfo("Bill Vetoed", "You have vetoed this legislation. "
                              "Congress may attempt to override your veto.")
            self.turn += 1
            self.update_president_info()
            veto_win.destroy()
        
        btn_frame = tk.Frame(veto_win, bg="white")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="✍️ Sign Into Law", command=sign_bill,
                 font=("Arial", 12, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", padx=30, pady=12).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Veto Bill", command=veto_bill,
                 font=("Arial", 12, "bold"), bg=self.secondary_color, fg="white",
                 cursor="hand2", padx=30, pady=12).pack(side="left", padx=10)
    
    def issue_executive_order(self):
        """Issue executive order"""
        order_win = tk.Toplevel(self.root)
        order_win.title("Issue Executive Order")
        order_win.geometry("600x450")
        order_win.configure(bg="white")
        
        tk.Label(order_win, text="Issue Executive Order", font=("Arial", 16, "bold"),
                bg="white", fg=self.secondary_color).pack(pady=15)
        
        tk.Label(order_win, text="Executive orders are directives that manage federal operations.\n"
                                "They have the force of law but can be challenged in court.",
                font=("Arial", 10), bg="white", wraplength=500).pack(pady=10)
        
        tk.Label(order_win, text="Order Title:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(10, 5))
        title_entry = tk.Entry(order_win, font=("Arial", 11), width=50)
        title_entry.pack()
        
        tk.Label(order_win, text="Order Description:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(15, 5))
        desc_text = scrolledtext.ScrolledText(order_win, font=("Arial", 11),
                                             width=60, height=8, wrap=tk.WORD)
        desc_text.pack(padx=20)
        
        def submit_order():
            title = title_entry.get().strip()
            desc = desc_text.get("1.0", tk.END).strip()
            
            if not title or not desc:
                messagebox.showwarning("Incomplete", "Please fill in all fields!")
                return
            
            self.public_approval += random.randint(-5, 5)
            log_text = f"📋 EXECUTIVE ORDER: {title}\n"
            log_text += f"   {desc[:100]}...\n"
            log_text += f"   Public approval: {self.public_approval}%\n"
            log_text += "-" * 60 + "\n\n"
            self.log_executive_action(log_text)
            
            messagebox.showinfo("Order Issued", f"Executive Order '{title}' has been issued!")
            self.turn += 1
            self.update_president_info()
            order_win.destroy()
        
        tk.Button(order_win, text="Issue Order", command=submit_order,
                 font=("Arial", 13, "bold"), bg=self.secondary_color, fg="white",
                 cursor="hand2", pady=12, padx=30).pack(pady=20)
    
    def appoint_cabinet(self):
        """Appoint cabinet member"""
        positions = ["Secretary of State", "Secretary of Defense", "Attorney General",
                    "Secretary of Treasury", "Secretary of Education"]
        position = random.choice(positions)
        
        result = messagebox.askyesno("Cabinet Appointment",
                                     f"Appoint a new {position}?\n\n"
                                     "Cabinet appointments require Senate confirmation.")
        if result:
            approved = random.choice([True, True, True, False])  # 75% approval rate
            if approved:
                log_text = f"👥 APPOINTED: {position}\n"
                log_text += f"   Senate confirmed appointment\n"
                log_text += "-" * 60 + "\n\n"
                self.log_executive_action(log_text)
                messagebox.showinfo("Confirmed", "The Senate has confirmed your appointment!")
            else:
                messagebox.showwarning("Rejected", "The Senate rejected your appointment.")
            self.turn += 1
            self.update_president_info()
    
    def nominate_justice(self):
        """Nominate Supreme Court justice"""
        result = messagebox.askyesno("Supreme Court Nomination",
                                     "Nominate a Supreme Court Justice?\n\n"
                                     "This is a lifetime appointment requiring Senate confirmation.\n"
                                     "Justices can serve for decades and shape constitutional law.")
        if result:
            approved = random.choice([True, True, False])  # 67% approval rate
            if approved:
                self.public_approval += random.randint(-2, 5)
                log_text = f"⚖️ NOMINATED: Supreme Court Justice\n"
                log_text += f"   Senate confirmed after hearings\n"
                log_text += f"   Public approval: {self.public_approval}%\n"
                log_text += "-" * 60 + "\n\n"
                self.log_executive_action(log_text)
                messagebox.showinfo("Confirmed", "Your nominee has been confirmed to the Supreme Court!")
            else:
                self.public_approval -= 3
                messagebox.showwarning("Rejected", "The Senate rejected your nominee after contentious hearings.")
            self.turn += 1
            self.update_president_info()
    
    def foreign_policy(self):
        """Conduct foreign policy"""
        policies = [
            ("Negotiate Trade Agreement", 5, 10),
            ("Sign Peace Treaty", 10, 15),
            ("Impose Economic Sanctions", -5, 5),
            ("Host Diplomatic Summit", 3, 8),
        ]
        
        policy = random.choice(policies)
        result = messagebox.askyesno("Foreign Policy Action",
                                     f"{policy[0]}\n\n"
                                     "This will impact international relations and public opinion.\n\n"
                                     "Proceed?")
        if result:
            approval_change = random.randint(policy[1], policy[2])
            self.public_approval += approval_change
            log_text = f"🌍 FOREIGN POLICY: {policy[0]}\n"
            log_text += f"   Public approval change: {approval_change:+d}% (now {self.public_approval}%)\n"
            log_text += "-" * 60 + "\n\n"
            self.log_executive_action(log_text)
            self.turn += 1
            self.update_president_info()
    
    def military_action(self):
        """Military command decision"""
        result = messagebox.askyesno("Military Action",
                                     "⚠️ As Commander-in-Chief, authorize military action?\n\n"
                                     "Only Congress can declare war, but you can order "
                                     "military operations.\n\n"
                                     "This is a serious decision with major consequences.")
        if result:
            self.public_approval += random.randint(-15, 10)
            self.budget -= 50000000000  # 50 billion
            log_text = f"🎖️ MILITARY ACTION: Authorized operation\n"
            log_text += f"   Budget impact: -$50 billion\n"
            log_text += f"   Public approval: {self.public_approval}%\n"
            log_text += "-" * 60 + "\n\n"
            self.log_executive_action(log_text)
            messagebox.showwarning("Action Taken", 
                                  "Military operation authorized. "
                                  "Public opinion is divided.")
            self.turn += 1
            self.update_president_info()
    
    def campaign(self):
        """Campaign for re-election"""
        cost = 10000000  # 10 million
        if self.budget < cost:
            messagebox.showwarning("Insufficient Funds", "Not enough campaign funds!")
            return
        
        self.budget -= cost
        approval_gain = random.randint(3, 8)
        self.public_approval += approval_gain
        
        log_text = f"🗳️ CAMPAIGN: Rally and media appearances\n"
        log_text += f"   Cost: ${cost:,.0f}\n"
        log_text += f"   Approval gain: +{approval_gain}% (now {self.public_approval}%)\n"
        log_text += "-" * 60 + "\n\n"
        self.log_executive_action(log_text)
        
        messagebox.showinfo("Campaign Event", 
                          f"Successful campaign events! Approval increased by {approval_gain}%")
        self.turn += 1
        self.update_president_info()
    
    def press_conference(self):
        """Hold press conference"""
        performance = random.choice(["excellent", "good", "mixed", "poor"])
        
        changes = {
            "excellent": (5, 10),
            "good": (2, 5),
            "mixed": (-2, 2),
            "poor": (-8, -3)
        }
        
        approval_change = random.randint(changes[performance][0], changes[performance][1])
        self.public_approval += approval_change
        
        log_text = f"📺 PRESS CONFERENCE: {performance.title()} performance\n"
        log_text += f"   Public approval change: {approval_change:+d}% (now {self.public_approval}%)\n"
        log_text += "-" * 60 + "\n\n"
        self.log_executive_action(log_text)
        
        messagebox.showinfo("Press Conference", 
                          f"The press conference went {performance}.\n"
                          f"Approval rating: {approval_change:+d}%")
        self.turn += 1
        self.update_president_info()
    
    def start_election(self):
        """Start Election Simulator"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Election state
        self.campaign_funds = 100000000  # 100 million
        self.electoral_votes = 0
        self.states_won = []
        self.debate_score = 0
        
        # Header
        header = tk.Frame(self.root, bg="#f59e0b", height=70)
        header.pack(fill="x")
        
        tk.Label(header, text="🗳️ Presidential Election Simulator",
                font=("Arial", 20, "bold"), bg="#f59e0b", fg="white").pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="← Main Menu", command=self.create_main_menu,
                 bg="white", fg="#f59e0b", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=15, pady=5).pack(side="right", padx=20)
        
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info panel
        info_panel = tk.Frame(content, bg="white", relief="solid", bd=2)
        info_panel.pack(fill="x", pady=(0, 10))
        
        tk.Label(info_panel, text="Campaign to Win 270 Electoral Votes!",
                font=("Arial", 14, "bold"), bg="white", fg="#f59e0b").pack(pady=10)
        
        self.election_info = tk.StringVar()
        self.update_election_info()
        tk.Label(info_panel, textvariable=self.election_info, font=("Arial", 11),
                bg="white", justify="center").pack(pady=10)
        
        # Campaign actions
        action_frame = tk.Frame(content, bg="white", relief="solid", bd=2)
        action_frame.pack(fill="both", expand=True)
        
        tk.Label(action_frame, text="Campaign Actions", font=("Arial", 16, "bold"),
                bg="white", fg="#f59e0b").pack(pady=15)
        
        # State buttons
        states_frame = tk.Frame(action_frame, bg="white")
        states_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        swing_states = [
            ("Florida", 30), ("Pennsylvania", 19), ("Ohio", 17),
            ("Michigan", 15), ("Georgia", 16), ("North Carolina", 16),
            ("Arizona", 11), ("Wisconsin", 10), ("Nevada", 6)
        ]
        
        tk.Label(states_frame, text="Campaign in Swing States:",
                font=("Arial", 13, "bold"), bg="white").pack(pady=10)
        
        for state, ev in swing_states:
            state_frame = tk.Frame(states_frame, bg="#fef3c7", relief="solid", bd=1)
            state_frame.pack(fill="x", padx=50, pady=3)
            
            tk.Label(state_frame, text=f"{state} ({ev} electoral votes)",
                    font=("Arial", 11, "bold"), bg="#fef3c7", anchor="w").pack(side="left", padx=15, pady=8)
            
            tk.Button(state_frame, text="Campaign Here ($10M)",
                     command=lambda s=state, e=ev: self.campaign_in_state(s, e),
                     font=("Arial", 10, "bold"), bg="#f59e0b", fg="white",
                     cursor="hand2", padx=15, pady=5).pack(side="right", padx=10)
        
        # Other actions
        other_frame = tk.Frame(action_frame, bg="white")
        other_frame.pack(pady=15)
        
        tk.Button(other_frame, text="📺 Participate in Debate",
                 command=self.participate_in_debate,
                 font=("Arial", 12, "bold"), bg="#3b82f6", fg="white",
                 cursor="hand2", padx=20, pady=10).pack(pady=5)
        
        tk.Button(other_frame, text="📢 National Ad Campaign ($20M)",
                 command=self.national_ad_campaign,
                 font=("Arial", 12, "bold"), bg="#8b5cf6", fg="white",
                 cursor="hand2", padx=20, pady=10).pack(pady=5)
        
        tk.Button(other_frame, text="🎯 Check Election Results",
                 command=self.check_election_results,
                 font=("Arial", 12, "bold"), bg=self.success_color, fg="white",
                 cursor="hand2", padx=20, pady=10).pack(pady=5)
    
    def update_election_info(self):
        """Update election info"""
        info = f"Campaign Funds: ${self.campaign_funds:,.0f} | "
        info += f"Electoral Votes Won: {self.electoral_votes}/270 | "
        info += f"States Won: {len(self.states_won)}"
        self.election_info.set(info)
    
    def campaign_in_state(self, state, electoral_votes):
        """Campaign in a specific state"""
        cost = 10000000  # 10 million
        
        if self.campaign_funds < cost:
            messagebox.showwarning("Insufficient Funds", "Not enough campaign funds!")
            return
        
        if state in self.states_won:
            messagebox.showinfo("Already Won", f"You already won {state}!")
            return
        
        self.campaign_funds -= cost
        
        # Chance to win based on debate performance and spending
        win_chance = 0.5 + (self.debate_score * 0.1)
        
        if random.random() < win_chance:
            self.states_won.append(state)
            self.electoral_votes += electoral_votes
            messagebox.showinfo("Victory!", 
                              f"🎉 You won {state}!\n\n"
                              f"Gained {electoral_votes} electoral votes!\n"
                              f"Total: {self.electoral_votes}/270")
        else:
            messagebox.showinfo("Lost State", 
                              f"You lost {state} to your opponent.\n"
                              f"Consider more campaign events or debates.")
        
        self.update_election_info()
    
    def participate_in_debate(self):
        """Participate in presidential debate"""
        debate_win = tk.Toplevel(self.root)
        debate_win.title("Presidential Debate")
        debate_win.geometry("700x500")
        debate_win.configure(bg="white")
        
        tk.Label(debate_win, text="📺 Presidential Debate", font=("Arial", 18, "bold"),
                bg="white", fg="#f59e0b").pack(pady=15)
        
        questions = [
            "What is your plan for the economy?",
            "How will you address climate change?",
            "What is your foreign policy vision?",
            "How will you improve healthcare?",
            "What is your education policy?"
        ]
        
        question = random.choice(questions)
        
        tk.Label(debate_win, text=f"Debate Question:\n\n\"{question}\"",
                font=("Arial", 13), bg="white", wraplength=600).pack(pady=20)
        
        tk.Label(debate_win, text="Your Response:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=(20, 5))
        
        response_text = scrolledtext.ScrolledText(debate_win, font=("Arial", 11),
                                                 width=70, height=10, wrap=tk.WORD)
        response_text.pack(padx=20)
        
        def submit_response():
            response = response_text.get("1.0", tk.END).strip()
            
            if len(response) < 50:
                messagebox.showwarning("Too Short", "Your response needs to be more detailed!")
                return
            
            # Score based on length and random performance
            score = min(3, len(response) // 100 + random.randint(0, 2))
            self.debate_score += score
            
            performance = ["weak", "decent", "good", "strong", "excellent"][min(score, 4)]
            
            messagebox.showinfo("Debate Performance",
                              f"Your debate performance was {performance}!\n\n"
                              f"This will help your campaign in swing states.\n"
                              f"Debate Score: +{score}")
            
            debate_win.destroy()
        
        tk.Button(debate_win, text="Submit Response", command=submit_response,
                 font=("Arial", 13, "bold"), bg="#f59e0b", fg="white",
                 cursor="hand2", pady=12, padx=30).pack(pady=20)
    
    def national_ad_campaign(self):
        """Run national ad campaign"""
        cost = 20000000  # 20 million
        
        if self.campaign_funds < cost:
            messagebox.showwarning("Insufficient Funds", "Not enough campaign funds!")
            return
        
        self.campaign_funds -= cost
        self.debate_score += 1  # Helps overall campaign
        
        messagebox.showinfo("Ad Campaign",
                          "National ad campaign launched!\n\n"
                          "Your message is reaching millions of voters.\n"
                          "This will improve your chances in all states.")
        
        self.update_election_info()
    
    def check_election_results(self):
        """Check if player won election"""
        if self.electoral_votes >= 270:
            messagebox.showinfo("🎉 ELECTION VICTORY! 🎉",
                              f"Congratulations!\n\n"
                              f"You won the presidential election with {self.electoral_votes} electoral votes!\n\n"
                              f"You carried {len(self.states_won)} states and will be sworn in as President!")
        elif self.electoral_votes > 0:
            messagebox.showinfo("Election Status",
                              f"Current standing:\n\n"
                              f"Electoral Votes: {self.electoral_votes}/270\n"
                              f"States Won: {len(self.states_won)}\n\n"
                              f"Keep campaigning to reach 270!")
        else:
            messagebox.showinfo("Election Status",
                              "You haven't won any states yet!\n\n"
                              "Participate in debates and campaign in swing states to win electoral votes.")
    
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
        
        # Federalism tab
        federalism_frame = tk.Frame(notebook, bg="white")
        notebook.add(federalism_frame, text="Federalism")
        
        fed_text = scrolledtext.ScrolledText(federalism_frame, wrap=tk.WORD, font=("Arial", 11))
        fed_text.pack(fill="both", expand=True, padx=10, pady=10)
        fed_text.insert("1.0", """
FEDERALISM: DIVISION OF POWER

Federalism is the division of power between the national government and state governments.

NATIONAL GOVERNMENT POWERS (Enumerated/Delegated)
• Regulate interstate and foreign commerce
• Coin money and regulate currency
• Declare war and maintain military
• Conduct foreign policy
• Establish federal courts
• Tax and spend for common defense and welfare

STATE GOVERNMENT POWERS (Reserved)
• Education
• Intrastate commerce
• Local law enforcement
• Marriage and family law
• Most criminal law
• Property law

CONCURRENT POWERS (Shared)
• Tax citizens
• Establish courts
• Make and enforce laws
• Provide for public welfare

SUPREMACY CLAUSE (Article VI)
Federal law takes precedence over state law when they conflict.
However, states retain significant autonomy in many areas.

10TH AMENDMENT
"The powers not delegated to the United States by the Constitution, nor prohibited by it to the States, are reserved to the States respectively, or to the people."

MODERN FEDERALISM
• Federal grants to states (categorical and block grants)
• Federal mandates requiring state compliance
• Preemption: federal law overrides state law
• Cooperative federalism: federal and state cooperation
        """)
        fed_text.config(state="disabled")

def main():
    root = tk.Tk()
    app = GovernmentSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
