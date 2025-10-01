#!/usr/bin/env python3
"""
Business Simulation Platform
===========================
Interactive business management and entrepreneurship simulation for K-12 education.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

class BusinessSimulation:
    """Complete business management simulation for educational purposes."""
    
    def __init__(self):
        """Initialize the business simulation."""
        self.business_data = {
            'name': 'My Business',
            'cash': 10000,
            'inventory': 0,
            'employees': 0,
            'customers': 0,
            'reputation': 50,
            'month': 1,
            'year': 1,
            'products': [],
            'expenses': [],
            'revenue': []
        }
        self.game_running = False
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main simulation interface."""
        self.root = tk.Tk()
        self.root.title("🏢 Business Simulation Platform - Educational Edition")
        self.root.geometry("1200x800")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup different tabs
        self.setup_dashboard_tab()
        self.setup_operations_tab()
        self.setup_finance_tab()
        self.setup_marketing_tab()
        self.setup_reports_tab()
        self.setup_learning_tab()
        
    def setup_dashboard_tab(self):
        """Setup the main dashboard tab."""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Business overview
        overview_frame = ttk.LabelFrame(dashboard_frame, text="Business Overview")
        overview_frame.pack(fill='x', padx=5, pady=5)
        
        # Key metrics display
        self.cash_label = ttk.Label(overview_frame, text="💰 Cash: $10,000", font=('Arial', 12))
        self.cash_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.inventory_label = ttk.Label(overview_frame, text="📦 Inventory: 0 units", font=('Arial', 12))
        self.inventory_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        self.employees_label = ttk.Label(overview_frame, text="👥 Employees: 0", font=('Arial', 12))
        self.employees_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        
        self.customers_label = ttk.Label(overview_frame, text="🛍️ Customers: 0", font=('Arial', 12))
        self.customers_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        self.reputation_label = ttk.Label(overview_frame, text="⭐ Reputation: 50/100", font=('Arial', 12))
        self.reputation_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        
        self.month_label = ttk.Label(overview_frame, text="📅 Month: 1, Year: 1", font=('Arial', 12))
        self.month_label.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Control buttons
        control_frame = ttk.LabelFrame(dashboard_frame, text="Game Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="🚀 Start Business", command=self.start_simulation).pack(side='left', padx=5, pady=5)
        ttk.Button(control_frame, text="⏸️ Pause", command=self.pause_simulation).pack(side='left', padx=5, pady=5)
        ttk.Button(control_frame, text="💾 Save Progress", command=self.save_game).pack(side='left', padx=5, pady=5)
        ttk.Button(control_frame, text="📂 Load Game", command=self.load_game).pack(side='left', padx=5, pady=5)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(dashboard_frame, text="Quick Actions")
        actions_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Button(actions_frame, text="🛒 Buy Inventory (100 units - $500)", 
                  command=lambda: self.buy_inventory(100, 500)).pack(pady=2, fill='x')
        ttk.Button(actions_frame, text="👷 Hire Employee ($2000/month)", 
                  command=lambda: self.hire_employee(2000)).pack(pady=2, fill='x')
        ttk.Button(actions_frame, text="📢 Marketing Campaign ($1000)", 
                  command=lambda: self.marketing_campaign(1000)).pack(pady=2, fill='x')
        ttk.Button(actions_frame, text="🔄 Process Month", command=self.process_month).pack(pady=2, fill='x')
        
    def setup_operations_tab(self):
        """Setup the business operations tab."""
        operations_frame = ttk.Frame(self.notebook)
        self.notebook.add(operations_frame, text="🏭 Operations")
        
        # Inventory management
        inventory_frame = ttk.LabelFrame(operations_frame, text="Inventory Management")
        inventory_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(inventory_frame, text="Purchase Quantity:").grid(row=0, column=0, padx=5, pady=2)
        self.purchase_qty = ttk.Entry(inventory_frame, width=10)
        self.purchase_qty.grid(row=0, column=1, padx=5, pady=2)
        self.purchase_qty.insert(0, "100")
        
        ttk.Label(inventory_frame, text="Unit Cost:").grid(row=0, column=2, padx=5, pady=2)
        self.unit_cost = ttk.Entry(inventory_frame, width=10)
        self.unit_cost.grid(row=0, column=3, padx=5, pady=2)
        self.unit_cost.insert(0, "5")
        
        ttk.Button(inventory_frame, text="Purchase Inventory", 
                  command=self.custom_purchase).grid(row=0, column=4, padx=5, pady=2)
        
        # Employee management
        employee_frame = ttk.LabelFrame(operations_frame, text="Employee Management")
        employee_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(employee_frame, text="Monthly Salary:").grid(row=0, column=0, padx=5, pady=2)
        self.salary_entry = ttk.Entry(employee_frame, width=10)
        self.salary_entry.grid(row=0, column=1, padx=5, pady=2)
        self.salary_entry.insert(0, "2000")
        
        ttk.Button(employee_frame, text="Hire Employee", 
                  command=self.custom_hire).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(employee_frame, text="Fire Employee", 
                  command=self.fire_employee).grid(row=0, column=3, padx=5, pady=2)
        
        # Production settings
        production_frame = ttk.LabelFrame(operations_frame, text="Production & Pricing")
        production_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(production_frame, text="Selling Price per Unit:").grid(row=0, column=0, padx=5, pady=2)
        self.selling_price = ttk.Entry(production_frame, width=10)
        self.selling_price.grid(row=0, column=1, padx=5, pady=2)
        self.selling_price.insert(0, "10")
        
        ttk.Label(production_frame, text="Quality Level (1-10):").grid(row=0, column=2, padx=5, pady=2)
        self.quality_level = ttk.Scale(production_frame, from_=1, to=10, orient='horizontal')
        self.quality_level.grid(row=0, column=3, padx=5, pady=2)
        self.quality_level.set(5)
        
    def setup_finance_tab(self):
        """Setup the financial management tab."""
        finance_frame = ttk.Frame(self.notebook)
        self.notebook.add(finance_frame, text="💰 Finance")
        
        # Financial overview
        overview_frame = ttk.LabelFrame(finance_frame, text="Financial Summary")
        overview_frame.pack(fill='x', padx=5, pady=5)
        
        # Create financial display
        self.financial_text = tk.Text(overview_frame, height=10, width=60)
        self.financial_text.pack(padx=5, pady=5)
        
        # Loan management
        loan_frame = ttk.LabelFrame(finance_frame, text="Loan Management")
        loan_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(loan_frame, text="Loan Amount:").grid(row=0, column=0, padx=5, pady=2)
        self.loan_amount = ttk.Entry(loan_frame, width=15)
        self.loan_amount.grid(row=0, column=1, padx=5, pady=2)
        self.loan_amount.insert(0, "5000")
        
        ttk.Button(loan_frame, text="Apply for Loan (10% interest)", 
                  command=self.apply_loan).grid(row=0, column=2, padx=5, pady=2)
        
        # Investment options
        investment_frame = ttk.LabelFrame(finance_frame, text="Investment Opportunities")
        investment_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(investment_frame, text="🏪 Expand Store Location ($10,000)", 
                  command=lambda: self.make_investment("store", 10000)).pack(pady=2)
        ttk.Button(investment_frame, text="🤖 Upgrade Technology ($5,000)", 
                  command=lambda: self.make_investment("technology", 5000)).pack(pady=2)
        ttk.Button(investment_frame, text="📈 Market Research ($2,000)", 
                  command=lambda: self.make_investment("research", 2000)).pack(pady=2)
        
    def setup_marketing_tab(self):
        """Setup the marketing and sales tab."""
        marketing_frame = ttk.Frame(self.notebook)
        self.notebook.add(marketing_frame, text="📢 Marketing")
        
        # Marketing campaigns
        campaign_frame = ttk.LabelFrame(marketing_frame, text="Marketing Campaigns")
        campaign_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(campaign_frame, text="Campaign Budget:").grid(row=0, column=0, padx=5, pady=2)
        self.campaign_budget = ttk.Entry(campaign_frame, width=15)
        self.campaign_budget.grid(row=0, column=1, padx=5, pady=2)
        self.campaign_budget.insert(0, "1000")
        
        ttk.Label(campaign_frame, text="Campaign Type:").grid(row=0, column=2, padx=5, pady=2)
        self.campaign_type = ttk.Combobox(campaign_frame, values=["Social Media", "TV/Radio", "Print", "Online Ads"])
        self.campaign_type.grid(row=0, column=3, padx=5, pady=2)
        self.campaign_type.set("Social Media")
        
        ttk.Button(campaign_frame, text="Launch Campaign", 
                  command=self.launch_marketing_campaign).grid(row=0, column=4, padx=5, pady=2)
        
        # Customer service
        service_frame = ttk.LabelFrame(marketing_frame, text="Customer Service")
        service_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(service_frame, text="🎁 Customer Loyalty Program ($2,000)", 
                  command=lambda: self.customer_service("loyalty", 2000)).pack(pady=2)
        ttk.Button(service_frame, text="📞 Customer Support Training ($1,500)", 
                  command=lambda: self.customer_service("training", 1500)).pack(pady=2)
        ttk.Button(service_frame, text="🎉 Special Promotion ($800)", 
                  command=lambda: self.customer_service("promotion", 800)).pack(pady=2)
        
    def setup_reports_tab(self):
        """Setup the reports and analytics tab."""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(reports_frame, text="Performance Metrics")
        metrics_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.metrics_text = tk.Text(metrics_frame, height=15)
        metrics_scrollbar = ttk.Scrollbar(metrics_frame, orient='vertical', command=self.metrics_text.yview)
        self.metrics_text.configure(yscrollcommand=metrics_scrollbar.set)
        
        self.metrics_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        metrics_scrollbar.pack(side='right', fill='y')
        
        # Report generation buttons
        buttons_frame = ttk.Frame(reports_frame)
        buttons_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="📈 Generate Monthly Report", 
                  command=self.generate_monthly_report).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="💹 Financial Analysis", 
                  command=self.financial_analysis).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="🎯 Market Analysis", 
                  command=self.market_analysis).pack(side='left', padx=5)
        
    def setup_learning_tab(self):
        """Setup the educational content and tips tab."""
        learning_frame = ttk.Frame(self.notebook)
        self.notebook.add(learning_frame, text="🎓 Learning")
        
        # Business concepts
        concepts_frame = ttk.LabelFrame(learning_frame, text="Business Concepts")
        concepts_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.learning_text = tk.Text(concepts_frame, height=20, wrap=tk.WORD)
        learning_scrollbar = ttk.Scrollbar(concepts_frame, orient='vertical', command=self.learning_text.yview)
        self.learning_text.configure(yscrollcommand=learning_scrollbar.set)
        
        self.learning_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        learning_scrollbar.pack(side='right', fill='y')
        
        # Load educational content
        self.load_learning_content()
        
        # Challenge buttons
        challenge_frame = ttk.Frame(learning_frame)
        challenge_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(challenge_frame, text="🏆 Daily Challenge", 
                  command=self.daily_challenge).pack(side='left', padx=5)
        ttk.Button(challenge_frame, text="💡 Business Tips", 
                  command=self.show_tips).pack(side='left', padx=5)
        ttk.Button(challenge_frame, text="📚 Glossary", 
                  command=self.show_glossary).pack(side='left', padx=5)
    
    # Business Logic Methods
    def start_simulation(self):
        """Start the business simulation."""
        self.game_running = True
        messagebox.showinfo("Business Started!", "Your business journey begins! Make smart decisions to grow your company.")
        self.update_display()
    
    def pause_simulation(self):
        """Pause the business simulation."""
        self.game_running = False
        messagebox.showinfo("Game Paused", "Business operations paused. Click Start to continue.")
    
    def buy_inventory(self, quantity, total_cost):
        """Purchase inventory for the business."""
        if self.business_data['cash'] >= total_cost:
            self.business_data['cash'] -= total_cost
            self.business_data['inventory'] += quantity
            self.business_data['expenses'].append({
                'type': 'Inventory Purchase',
                'amount': total_cost,
                'month': self.business_data['month'],
                'year': self.business_data['year']
            })
            messagebox.showinfo("Purchase Successful", f"Bought {quantity} units for ${total_cost}")
        else:
            messagebox.showerror("Insufficient Funds", f"Need ${total_cost}, but only have ${self.business_data['cash']}")
        self.update_display()
    
    def custom_purchase(self):
        """Handle custom inventory purchase."""
        try:
            qty = int(self.purchase_qty.get())
            cost = float(self.unit_cost.get())
            total = qty * cost
            self.buy_inventory(qty, total)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for quantity and cost.")
    
    def hire_employee(self, salary):
        """Hire a new employee."""
        if self.business_data['cash'] >= salary:
            self.business_data['employees'] += 1
            self.business_data['cash'] -= salary
            messagebox.showinfo("Employee Hired", f"New employee hired! Monthly salary: ${salary}")
        else:
            messagebox.showerror("Insufficient Funds", f"Cannot afford salary of ${salary}")
        self.update_display()
    
    def custom_hire(self):
        """Handle custom employee hiring."""
        try:
            salary = float(self.salary_entry.get())
            self.hire_employee(salary)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid salary amount.")
    
    def fire_employee(self):
        """Fire an employee."""
        if self.business_data['employees'] > 0:
            self.business_data['employees'] -= 1
            messagebox.showinfo("Employee Fired", "Employee has been let go. Severance pay: $500")
            self.business_data['cash'] -= 500
        else:
            messagebox.showinfo("No Employees", "You have no employees to fire.")
        self.update_display()
    
    def marketing_campaign(self, cost):
        """Run a marketing campaign."""
        if self.business_data['cash'] >= cost:
            self.business_data['cash'] -= cost
            new_customers = random.randint(10, 50)
            reputation_boost = random.randint(5, 15)
            
            self.business_data['customers'] += new_customers
            self.business_data['reputation'] = min(100, self.business_data['reputation'] + reputation_boost)
            
            messagebox.showinfo("Campaign Success!", 
                              f"Marketing campaign brought {new_customers} new customers!\n"
                              f"Reputation increased by {reputation_boost} points.")
        else:
            messagebox.showerror("Insufficient Funds", f"Marketing campaign costs ${cost}")
        self.update_display()
    
    def process_month(self):
        """Process a month of business operations."""
        if not self.game_running:
            messagebox.showwarning("Game Paused", "Start the simulation first!")
            return
            
        # Calculate sales
        if self.business_data['inventory'] > 0 and self.business_data['customers'] > 0:
            try:
                selling_price = float(self.selling_price.get())
                quality = self.quality_level.get()
                
                # Sales calculation based on customers, inventory, and quality
                max_sales = min(self.business_data['inventory'], self.business_data['customers'])
                quality_multiplier = quality / 10
                actual_sales = int(max_sales * quality_multiplier * random.uniform(0.5, 1.0))
                
                revenue = actual_sales * selling_price
                self.business_data['cash'] += revenue
                self.business_data['inventory'] -= actual_sales
                
                self.business_data['revenue'].append({
                    'month': self.business_data['month'],
                    'year': self.business_data['year'],
                    'sales': actual_sales,
                    'revenue': revenue
                })
                
            except ValueError:
                selling_price = 10  # Default price
                revenue = 0
        
        # Pay employee salaries
        try:
            salary = float(self.salary_entry.get())
            total_salaries = self.business_data['employees'] * salary
            self.business_data['cash'] -= total_salaries
        except ValueError:
            total_salaries = self.business_data['employees'] * 2000
            self.business_data['cash'] -= total_salaries
        
        # Random events
        self.random_event()
        
        # Advance time
        self.business_data['month'] += 1
        if self.business_data['month'] > 12:
            self.business_data['month'] = 1
            self.business_data['year'] += 1
        
        self.update_display()
        messagebox.showinfo("Month Processed", f"Month {self.business_data['month']} results processed!")
    
    def random_event(self):
        """Generate random business events."""
        events = [
            ("Economic boom increases customer demand!", 20, 0),
            ("New competitor enters market.", -10, -15),
            ("Supply chain disruption increases costs.", 0, -500),
            ("Positive customer review goes viral!", 30, 100),
            ("Government regulation increases compliance costs.", 0, -1000),
            ("Partnership opportunity increases efficiency.", 15, 200)
        ]
        
        if random.random() < 0.3:  # 30% chance of event
            event, customer_change, cash_change = random.choice(events)
            
            self.business_data['customers'] = max(0, self.business_data['customers'] + customer_change)
            self.business_data['cash'] += cash_change
            
            messagebox.showinfo("Business Event", event)
    
    def update_display(self):
        """Update all display elements."""
        self.cash_label.config(text=f"💰 Cash: ${self.business_data['cash']:,.2f}")
        self.inventory_label.config(text=f"📦 Inventory: {self.business_data['inventory']} units")
        self.employees_label.config(text=f"👥 Employees: {self.business_data['employees']}")
        self.customers_label.config(text=f"🛍️ Customers: {self.business_data['customers']}")
        self.reputation_label.config(text=f"⭐ Reputation: {self.business_data['reputation']}/100")
        self.month_label.config(text=f"📅 Month: {self.business_data['month']}, Year: {self.business_data['year']}")
    
    def generate_monthly_report(self):
        """Generate a monthly business report."""
        report = f"""
📊 MONTHLY BUSINESS REPORT - Month {self.business_data['month']}, Year {self.business_data['year']}
{'='*60}

💰 FINANCIAL SUMMARY:
   Current Cash: ${self.business_data['cash']:,.2f}
   Total Employees: {self.business_data['employees']}
   Current Inventory: {self.business_data['inventory']} units

👥 CUSTOMER METRICS:
   Total Customers: {self.business_data['customers']}
   Reputation Score: {self.business_data['reputation']}/100

📈 RECENT PERFORMANCE:
"""
        
        if self.business_data['revenue']:
            recent_revenue = self.business_data['revenue'][-3:]  # Last 3 months
            total_recent = sum(r['revenue'] for r in recent_revenue)
            report += f"   Last 3 Months Revenue: ${total_recent:,.2f}\n"
        
        if self.business_data['expenses']:
            recent_expenses = self.business_data['expenses'][-5:]  # Last 5 expenses
            total_expenses = sum(e['amount'] for e in recent_expenses)
            report += f"   Recent Expenses: ${total_expenses:,.2f}\n"
        
        report += "\n💡 RECOMMENDATIONS:\n"
        if self.business_data['cash'] < 5000:
            report += "   ⚠️  Cash flow is low - consider cost reduction or loans\n"
        if self.business_data['inventory'] < 50:
            report += "   📦 Inventory is low - restock to meet demand\n"
        if self.business_data['reputation'] < 70:
            report += "   ⭐ Focus on customer service to improve reputation\n"
        
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(tk.END, report)
    
    def load_learning_content(self):
        """Load educational business content."""
        content = """
🎓 BUSINESS EDUCATION CONTENT

📊 KEY BUSINESS CONCEPTS:

1. CASH FLOW MANAGEMENT
   • Cash flow is the lifeblood of any business
   • Track money coming in (revenue) and going out (expenses)
   • Maintain adequate cash reserves for unexpected costs
   • Tip: Aim to keep 3-6 months of expenses in reserve

2. INVENTORY MANAGEMENT
   • Balance having enough stock without tying up too much cash
   • Consider storage costs and product shelf life
   • Use data to predict demand patterns
   • Just-in-time inventory can reduce costs but increases risk

3. CUSTOMER RELATIONSHIP MANAGEMENT
   • Acquiring new customers costs 5-25x more than retaining existing ones
   • Focus on customer satisfaction and loyalty programs
   • Word-of-mouth marketing is powerful and cost-effective
   • Listen to customer feedback and adapt accordingly

4. MARKETING AND SALES
   • Identify your target market and their needs
   • Different marketing channels have different costs and effectiveness
   • Track return on investment (ROI) for marketing campaigns
   • Quality products and service are the best marketing

5. FINANCIAL PLANNING
   • Create budgets and financial forecasts
   • Understand the difference between profit and cash flow
   • Monitor key performance indicators (KPIs)
   • Plan for seasonal variations in business

6. HUMAN RESOURCES
   • Employees are your most valuable asset
   • Invest in training and development
   • Fair compensation reduces turnover costs
   • Good management increases productivity

7. RISK MANAGEMENT
   • Identify potential risks to your business
   • Diversify revenue streams when possible
   • Consider insurance for major risks
   • Have contingency plans for various scenarios

💡 SUCCESS TIPS:
   • Start small and grow gradually
   • Focus on one thing and do it well
   • Learn from failures - they're learning opportunities
   • Network with other business owners
   • Stay informed about your industry and market trends
   • Always prioritize customer satisfaction
   • Keep accurate financial records

🏆 ENTREPRENEURSHIP SKILLS:
   • Problem-solving and creative thinking
   • Leadership and communication
   • Financial literacy and planning
   • Risk assessment and decision-making
   • Adaptability and resilience
   • Time management and organization
        """
        
        self.learning_text.delete(1.0, tk.END)
        self.learning_text.insert(tk.END, content)
    
    def save_game(self):
        """Save the current game state."""
        try:
            filename = f"business_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.business_data, f, indent=2)
            messagebox.showinfo("Game Saved", f"Progress saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save game: {e}")
    
    def load_game(self):
        """Load a saved game state."""
        # This would typically open a file dialog
        messagebox.showinfo("Load Game", "Load game feature - select a saved .json file")
    
    def run(self):
        """Start the business simulation application."""
        self.root.mainloop()

def main():
    """Main function to run the business simulation."""
    print("🏢 Business Simulation Platform")
    print("=" * 40)
    print("📚 Educational Business Management Game")
    print("🎯 Learn entrepreneurship through interactive simulation")
    print()
    print("Starting Business Simulation...")
    
    simulation = BusinessSimulation()
    simulation.run()

if __name__ == "__main__":
    main()