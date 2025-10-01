#!/usr/bin/env python3
"""
Financial Literacy Calculator Suite
==================================
Interactive financial planning and education tools for K-12 students.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FinancialCalculators:
    """Comprehensive financial literacy calculator suite."""
    
    def __init__(self):
        """Initialize the financial calculators application."""
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main calculator interface."""
        self.root = tk.Tk()
        self.root.title("💰 Financial Literacy Calculator Suite")
        self.root.geometry("1000x700")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup calculator tabs
        self.setup_budgeting_tab()
        self.setup_savings_tab()
        self.setup_loan_tab()
        self.setup_investment_tab()
        self.setup_comparison_tab()
        self.setup_learning_tab()
        
    def setup_budgeting_tab(self):
        """Setup the budgeting calculator tab."""
        budget_frame = ttk.Frame(self.notebook)
        self.notebook.add(budget_frame, text="📊 Budget Planner")
        
        # Income section
        income_frame = ttk.LabelFrame(budget_frame, text="Monthly Income")
        income_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(income_frame, text="Salary/Allowance:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.salary_entry = ttk.Entry(income_frame, width=15)
        self.salary_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(income_frame, text="Other Income:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.other_income_entry = ttk.Entry(income_frame, width=15)
        self.other_income_entry.grid(row=0, column=3, padx=5, pady=2)
        
        # Expenses section
        expenses_frame = ttk.LabelFrame(budget_frame, text="Monthly Expenses")
        expenses_frame.pack(fill='x', padx=5, pady=5)
        
        # Essential expenses
        ttk.Label(expenses_frame, text="Housing/Rent:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.housing_entry = ttk.Entry(expenses_frame, width=12)
        self.housing_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(expenses_frame, text="Food:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.food_entry = ttk.Entry(expenses_frame, width=12)
        self.food_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(expenses_frame, text="Transportation:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.transport_entry = ttk.Entry(expenses_frame, width=12)
        self.transport_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(expenses_frame, text="Utilities:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.utilities_entry = ttk.Entry(expenses_frame, width=12)
        self.utilities_entry.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(expenses_frame, text="Entertainment:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.entertainment_entry = ttk.Entry(expenses_frame, width=12)
        self.entertainment_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(expenses_frame, text="Shopping:").grid(row=2, column=2, sticky='w', padx=5, pady=2)
        self.shopping_entry = ttk.Entry(expenses_frame, width=12)
        self.shopping_entry.grid(row=2, column=3, padx=5, pady=2)
        
        # Calculate button
        ttk.Button(budget_frame, text="📊 Calculate Budget", 
                  command=self.calculate_budget).pack(pady=10)
        
        # Results display
        self.budget_results = tk.Text(budget_frame, height=10)
        self.budget_results.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_savings_tab(self):
        """Setup the savings calculator tab."""
        savings_frame = ttk.Frame(self.notebook)
        self.notebook.add(savings_frame, text="🏦 Savings Goals")
        
        # Savings goal input
        goal_frame = ttk.LabelFrame(savings_frame, text="Savings Goal Calculator")
        goal_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(goal_frame, text="Savings Goal ($):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.goal_amount = ttk.Entry(goal_frame, width=15)
        self.goal_amount.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(goal_frame, text="Monthly Savings ($):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.monthly_savings = ttk.Entry(goal_frame, width=15)
        self.monthly_savings.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(goal_frame, text="Interest Rate (%/year):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.interest_rate = ttk.Entry(goal_frame, width=15)
        self.interest_rate.grid(row=1, column=1, padx=5, pady=2)
        self.interest_rate.insert(0, "2.5")
        
        ttk.Button(goal_frame, text="📈 Calculate Timeline", 
                  command=self.calculate_savings_goal).grid(row=1, column=2, columnspan=2, pady=10)
        
        # Compound interest calculator
        compound_frame = ttk.LabelFrame(savings_frame, text="Compound Interest Calculator")
        compound_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(compound_frame, text="Initial Amount ($):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.initial_amount = ttk.Entry(compound_frame, width=15)
        self.initial_amount.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(compound_frame, text="Years to Save:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.years_save = ttk.Entry(compound_frame, width=15)
        self.years_save.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(compound_frame, text="💎 Calculate Growth", 
                  command=self.calculate_compound_interest).pack(pady=10)
        
        # Results display
        self.savings_results = tk.Text(savings_frame, height=12)
        self.savings_results.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_loan_tab(self):
        """Setup the loan calculator tab."""
        loan_frame = ttk.Frame(self.notebook)
        self.notebook.add(loan_frame, text="🏠 Loan Calculator")
        
        # Loan input section
        input_frame = ttk.LabelFrame(loan_frame, text="Loan Details")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Loan Amount ($):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.loan_amount = ttk.Entry(input_frame, width=15)
        self.loan_amount.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Interest Rate (%/year):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.loan_rate = ttk.Entry(input_frame, width=15)
        self.loan_rate.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Loan Term (years):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.loan_term = ttk.Entry(input_frame, width=15)
        self.loan_term.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="💳 Calculate Loan", 
                  command=self.calculate_loan).grid(row=1, column=2, columnspan=2, pady=10)
        
        # Loan comparison
        comparison_frame = ttk.LabelFrame(loan_frame, text="Loan Comparison")
        comparison_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(comparison_frame, text="Compare different loan terms and rates").pack(pady=5)
        
        # Quick comparison buttons
        button_frame = ttk.Frame(comparison_frame)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="🚗 Auto Loan (5% for 5 years)", 
                  command=lambda: self.quick_loan_calc(20000, 5.0, 5)).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🏠 Mortgage (3.5% for 30 years)", 
                  command=lambda: self.quick_loan_calc(300000, 3.5, 30)).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎓 Student Loan (4.5% for 10 years)", 
                  command=lambda: self.quick_loan_calc(50000, 4.5, 10)).pack(side='left', padx=5)
        
        # Results display
        self.loan_results = tk.Text(loan_frame, height=12)
        self.loan_results.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_investment_tab(self):
        """Setup the investment calculator tab."""
        investment_frame = ttk.Frame(self.notebook)
        self.notebook.add(investment_frame, text="📈 Investment Planner")
        
        # Investment input
        input_frame = ttk.LabelFrame(investment_frame, text="Investment Parameters")
        input_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Initial Investment ($):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.invest_initial = ttk.Entry(input_frame, width=15)
        self.invest_initial.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Monthly Contribution ($):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.invest_monthly = ttk.Entry(input_frame, width=15)
        self.invest_monthly.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Expected Return (%/year):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.invest_return = ttk.Entry(input_frame, width=15)
        self.invest_return.grid(row=1, column=1, padx=5, pady=2)
        self.invest_return.insert(0, "7")
        
        ttk.Label(input_frame, text="Investment Period (years):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.invest_years = ttk.Entry(input_frame, width=15)
        self.invest_years.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Button(input_frame, text="📊 Calculate Investment Growth", 
                  command=self.calculate_investment).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Risk education
        risk_frame = ttk.LabelFrame(investment_frame, text="Investment Education")
        risk_frame.pack(fill='x', padx=5, pady=5)
        
        risk_buttons = ttk.Frame(risk_frame)
        risk_buttons.pack(pady=5)
        
        ttk.Button(risk_buttons, text="💰 Conservative (3% return)", 
                  command=lambda: self.show_investment_type("conservative")).pack(side='left', padx=5)
        ttk.Button(risk_buttons, text="📊 Moderate (7% return)", 
                  command=lambda: self.show_investment_type("moderate")).pack(side='left', padx=5)
        ttk.Button(risk_buttons, text="🚀 Aggressive (10% return)", 
                  command=lambda: self.show_investment_type("aggressive")).pack(side='left', padx=5)
        
        # Results display
        self.investment_results = tk.Text(investment_frame, height=10)
        self.investment_results.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_comparison_tab(self):
        """Setup the financial comparison tab."""
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="⚖️ Compare Options")
        
        # Rent vs Buy calculator
        housing_frame = ttk.LabelFrame(comparison_frame, text="Rent vs. Buy Analysis")
        housing_frame.pack(fill='x', padx=5, pady=5)
        
        # Rent side
        rent_frame = ttk.Frame(housing_frame)
        rent_frame.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Label(rent_frame, text="RENTING", font=('Arial', 10, 'bold')).pack()
        ttk.Label(rent_frame, text="Monthly Rent:").pack()
        self.rent_monthly = ttk.Entry(rent_frame, width=15)
        self.rent_monthly.pack(pady=2)
        
        # Buy side
        buy_frame = ttk.Frame(housing_frame)
        buy_frame.pack(side='right', fill='x', expand=True, padx=5)
        
        ttk.Label(buy_frame, text="BUYING", font=('Arial', 10, 'bold')).pack()
        ttk.Label(buy_frame, text="Home Price:").pack()
        self.home_price = ttk.Entry(buy_frame, width=15)
        self.home_price.pack(pady=2)
        
        ttk.Label(buy_frame, text="Down Payment (%):").pack()
        self.down_payment = ttk.Entry(buy_frame, width=15)
        self.down_payment.pack(pady=2)
        self.down_payment.insert(0, "20")
        
        ttk.Button(housing_frame, text="🏠 Compare Housing Options", 
                  command=self.compare_rent_buy).pack(pady=10)
        
        # Results display
        self.comparison_results = tk.Text(comparison_frame, height=15)
        self.comparison_results.pack(fill='both', expand=True, padx=5, pady=5)
        
    def setup_learning_tab(self):
        """Setup the financial education tab."""
        learning_frame = ttk.Frame(self.notebook)
        self.notebook.add(learning_frame, text="🎓 Financial Education")
        
        # Educational content
        content_frame = ttk.LabelFrame(learning_frame, text="Financial Literacy Concepts")
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.education_text = tk.Text(content_frame, wrap=tk.WORD)
        edu_scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=self.education_text.yview)
        self.education_text.configure(yscrollcommand=edu_scrollbar.set)
        
        self.education_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        edu_scrollbar.pack(side='right', fill='y')
        
        # Load educational content
        self.load_financial_education()
        
        # Topic buttons
        topic_frame = ttk.Frame(learning_frame)
        topic_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(topic_frame, text="💳 Credit & Debt", 
                  command=lambda: self.show_topic("credit")).pack(side='left', padx=5)
        ttk.Button(topic_frame, text="💰 Budgeting Basics", 
                  command=lambda: self.show_topic("budgeting")).pack(side='left', padx=5)
        ttk.Button(topic_frame, text="📊 Investment Fundamentals", 
                  command=lambda: self.show_topic("investing")).pack(side='left', padx=5)
        ttk.Button(topic_frame, text="🏦 Banking & Savings", 
                  command=lambda: self.show_topic("banking")).pack(side='left', padx=5)
    
    # Calculator Methods
    def calculate_budget(self):
        """Calculate and display budget analysis."""
        try:
            # Get income
            salary = float(self.salary_entry.get() or 0)
            other_income = float(self.other_income_entry.get() or 0)
            total_income = salary + other_income
            
            # Get expenses
            housing = float(self.housing_entry.get() or 0)
            food = float(self.food_entry.get() or 0)
            transport = float(self.transport_entry.get() or 0)
            utilities = float(self.utilities_entry.get() or 0)
            entertainment = float(self.entertainment_entry.get() or 0)
            shopping = float(self.shopping_entry.get() or 0)
            
            total_expenses = housing + food + transport + utilities + entertainment + shopping
            remaining = total_income - total_expenses
            
            # Calculate percentages
            if total_income > 0:
                housing_pct = (housing / total_income) * 100
                food_pct = (food / total_income) * 100
                savings_pct = (remaining / total_income) * 100 if remaining > 0 else 0
            else:
                housing_pct = food_pct = savings_pct = 0
            
            # Generate report
            report = f"""
📊 BUDGET ANALYSIS REPORT
{'='*40}

💰 INCOME SUMMARY:
   Salary/Allowance: ${salary:,.2f}
   Other Income: ${other_income:,.2f}
   Total Monthly Income: ${total_income:,.2f}

💸 EXPENSE BREAKDOWN:
   Housing/Rent: ${housing:,.2f} ({housing_pct:.1f}% of income)
   Food: ${food:,.2f} ({food_pct:.1f}% of income)
   Transportation: ${transport:,.2f}
   Utilities: ${utilities:,.2f}
   Entertainment: ${entertainment:,.2f}
   Shopping: ${shopping:,.2f}
   Total Expenses: ${total_expenses:,.2f}

📈 FINANCIAL HEALTH:
   Money Left Over: ${remaining:,.2f}
   Savings Rate: {savings_pct:.1f}%

💡 BUDGET RECOMMENDATIONS:
"""
            
            # Add recommendations
            if housing_pct > 30:
                report += "   ⚠️  Housing costs are high (>30% of income)\n"
            if savings_pct < 20:
                report += "   💰 Try to save at least 20% of your income\n"
            if remaining < 0:
                report += "   🚨 You're spending more than you earn! Cut expenses.\n"
            else:
                report += "   ✅ Good job! You have money left to save.\n"
            
            if food_pct > 15:
                report += "   🍽️  Consider meal planning to reduce food costs\n"
            
            report += f"\n🎯 SUGGESTED 50/30/20 BUDGET:\n"
            report += f"   Needs (50%): ${total_income * 0.5:,.2f}\n"
            report += f"   Wants (30%): ${total_income * 0.3:,.2f}\n"
            report += f"   Savings (20%): ${total_income * 0.2:,.2f}\n"
            
            self.budget_results.delete(1.0, tk.END)
            self.budget_results.insert(tk.END, report)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
    
    def calculate_savings_goal(self):
        """Calculate time to reach savings goal."""
        try:
            goal = float(self.goal_amount.get())
            monthly = float(self.monthly_savings.get())
            rate = float(self.interest_rate.get()) / 100 / 12  # Monthly rate
            
            if monthly <= 0:
                messagebox.showerror("Input Error", "Monthly savings must be greater than 0.")
                return
            
            # Calculate months to goal with compound interest
            if rate > 0:
                months = math.log(1 + (goal * rate) / monthly) / math.log(1 + rate)
            else:
                months = goal / monthly
            
            years = months / 12
            
            # Calculate total contributions and interest earned
            total_contributed = monthly * months
            interest_earned = goal - total_contributed
            
            report = f"""
🎯 SAVINGS GOAL ANALYSIS
{'='*30}

💰 Goal Amount: ${goal:,.2f}
💳 Monthly Savings: ${monthly:,.2f}
📈 Interest Rate: {float(self.interest_rate.get()):.2f}% per year

⏰ TIME TO GOAL:
   {months:.0f} months ({years:.1f} years)

💵 CONTRIBUTION SUMMARY:
   Total You'll Save: ${total_contributed:,.2f}
   Interest Earned: ${interest_earned:,.2f}
   Total Goal Amount: ${goal:,.2f}

💡 TIPS TO REACH YOUR GOAL FASTER:
   • Increase monthly savings by $50 → Save {(months - goal/(monthly + 50)):.0f} months
   • Find higher interest rate (3.5%) → Save approximately {months - (math.log(1 + (goal * 0.035/12) / monthly) / math.log(1 + 0.035/12) if 0.035/12 > 0 else goal/monthly):.0f} months
   • Make one-time deposit of $500 → Reduce time by {((goal-500)/monthly - goal/monthly):.0f} months

🌟 MILESTONE TRACKER:
   25% of goal (${goal*0.25:,.2f}): {months*0.25:.0f} months
   50% of goal (${goal*0.5:,.2f}): {months*0.5:.0f} months  
   75% of goal (${goal*0.75:,.2f}): {months*0.75:.0f} months
   100% of goal (${goal:,.2f}): {months:.0f} months
"""
            
            self.savings_results.delete(1.0, tk.END)
            self.savings_results.insert(tk.END, report)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error in calculation: {e}")
    
    def calculate_compound_interest(self):
        """Calculate compound interest growth."""
        try:
            principal = float(self.initial_amount.get())
            monthly = float(self.monthly_savings.get() or 0)
            rate = float(self.interest_rate.get()) / 100
            years = float(self.years_save.get())
            
            # Calculate with monthly compounding
            monthly_rate = rate / 12
            months = years * 12
            
            # Future value with regular contributions
            if monthly > 0:
                fv = principal * (1 + monthly_rate)**months + monthly * (((1 + monthly_rate)**months - 1) / monthly_rate)
            else:
                fv = principal * (1 + monthly_rate)**months
            
            total_contributed = principal + (monthly * months)
            interest_earned = fv - total_contributed
            
            report = f"""
💎 COMPOUND INTEREST CALCULATOR
{'='*35}

📊 INVESTMENT DETAILS:
   Initial Amount: ${principal:,.2f}
   Monthly Addition: ${monthly:,.2f}
   Interest Rate: {rate:.2f}% per year
   Time Period: {years:.0f} years

📈 GROWTH PROJECTION:
   Total Contributed: ${total_contributed:,.2f}
   Interest Earned: ${interest_earned:,.2f}
   Final Amount: ${fv:,.2f}

🚀 GROWTH FACTOR: {fv/total_contributed:.2f}x your money!

💰 YEAR-BY-YEAR BREAKDOWN:
"""
            
            # Show year-by-year growth
            for year in range(1, min(int(years) + 1, 11)):  # Show up to 10 years
                year_months = year * 12
                if monthly > 0:
                    year_value = principal * (1 + monthly_rate)**year_months + monthly * (((1 + monthly_rate)**year_months - 1) / monthly_rate)
                else:
                    year_value = principal * (1 + monthly_rate)**year_months
                report += f"   Year {year}: ${year_value:,.2f}\n"
            
            if years > 10:
                report += f"   ...\n   Year {years:.0f}: ${fv:,.2f}\n"
            
            self.savings_results.delete(1.0, tk.END)
            self.savings_results.insert(tk.END, report)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
    
    def load_financial_education(self):
        """Load comprehensive financial education content."""
        content = """
💰 FINANCIAL LITERACY EDUCATION CENTER

📚 FUNDAMENTAL CONCEPTS:

1. BUDGETING - THE FOUNDATION OF FINANCIAL SUCCESS
   • Track where your money comes from and where it goes
   • Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings
   • Review and adjust your budget monthly
   • Emergency fund should cover 3-6 months of expenses

2. COMPOUND INTEREST - THE EIGHTH WONDER OF THE WORLD
   • Money grows faster when earnings also earn money
   • Start early - time is your biggest advantage
   • Einstein called it "the most powerful force in the universe"
   • Example: $100/month for 40 years at 7% = $262,481!

3. DEBT MANAGEMENT - GOOD DEBT vs BAD DEBT
   • Good debt: Mortgages, student loans (invest in your future)
   • Bad debt: Credit cards, payday loans (high interest, no benefit)
   • Pay off high-interest debt first
   • Avoid borrowing for things that lose value

4. INVESTING BASICS - GROWING YOUR WEALTH
   • Diversification reduces risk
   • Higher potential returns usually mean higher risk
   • Start with index funds for beginners
   • Dollar-cost averaging smooths out market volatility

5. CREDIT SCORES - YOUR FINANCIAL REPUTATION
   • Range from 300-850 (excellent is 750+)
   • Factors: Payment history (35%), credit utilization (30%)
   • Check your credit report annually for free
   • Good credit saves money on loans and insurance

6. INSURANCE - PROTECTING YOUR FINANCIAL FUTURE
   • Health insurance is essential - medical bills can be devastating
   • Auto insurance is legally required in most places
   • Life insurance protects your family's financial security
   • Don't over-insure or under-insure

7. RETIREMENT PLANNING - IT'S NEVER TOO EARLY
   • Take advantage of employer 401(k) matching (free money!)
   • Roth IRA vs Traditional IRA - understand the differences
   • Social Security won't be enough for most people
   • The earlier you start, the less you need to save monthly

🎯 FINANCIAL GOALS BY AGE:
   Teens: Learn budgeting, start saving, understand compound interest
   20s: Build emergency fund, start investing, avoid debt
   30s: Increase income, buy home, max retirement contributions
   40s: Peak earning years, catch-up retirement savings
   50s+: Preserve wealth, plan for retirement

💡 TOP 10 FINANCIAL TIPS:
   1. Pay yourself first - automate your savings
   2. Live below your means, not at your means
   3. Invest in yourself - education and skills pay dividends
   4. Avoid lifestyle inflation when income increases
   5. Use credit cards responsibly - pay full balance monthly
   6. Shop around for better rates on loans and insurance
   7. Don't try to time the market - consistent investing wins
   8. Have multiple income streams when possible
   9. Review and rebalance investments annually
   10. Seek financial education - it's the best investment

🚨 COMMON FINANCIAL MISTAKES TO AVOID:
   • Not having an emergency fund
   • Carrying high-interest credit card debt
   • Not investing early enough
   • Buying too much house or car
   • Not having adequate insurance
   • Falling for get-rich-quick schemes
   • Not diversifying investments
   • Emotional investing (buying high, selling low)
   • Not planning for taxes
   • Ignoring inflation in long-term planning

Remember: Personal finance is more personal than finance. 
What works for others may not work for you. Start small, 
stay consistent, and keep learning!
        """
        
        self.education_text.delete(1.0, tk.END)
        self.education_text.insert(tk.END, content)
    
    def run(self):
        """Start the financial calculator application."""
        self.root.mainloop()

def main():
    """Main function to run the financial calculators."""
    print("💰 Financial Literacy Calculator Suite")
    print("=" * 40)
    print("📊 Interactive Financial Planning Tools")
    print("🎓 Learn money management through calculation")
    print()
    print("Starting Financial Calculators...")
    
    calculators = FinancialCalculators()
    calculators.run()

if __name__ == "__main__":
    main()