"""
Economics Market Simulator
Educational tool for understanding supply, demand, and market dynamics

Features:
- Market simulation with dynamic pricing
- Supply and demand visualization
- Business management game
- Economic concepts tutorial
- Real-world scenarios

Author: Social Studies Education Platform
License: MIT with Educational Use Extensions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import json

class EconomicsSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Economics Market Simulator - Learn Supply & Demand")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f8ff")
        
        # Game difficulty settings
        self.difficulty = "normal"  # easy, normal, hard
        
        # Game state
        self.money = 1000
        self.inventory = 0
        self.production_cost = 5
        self.selling_price = 10
        self.turn = 1
        self.max_turns = 20
        
        # Market conditions
        self.market_demand = 50
        self.market_supply = 50
        self.market_price = 10
        self.consumer_preference = 1.0
        
        # History for graphing
        self.price_history = [10]
        self.demand_history = [50]
        self.supply_history = [50]
        self.profit_history = [0]
        self.sales_history = [0]
        
        # Achievements
        self.achievements = []
        
        # Colors
        self.colors = {
            'bg': '#f0f8ff',
            'primary': '#2e8b57',
            'secondary': '#4169e1',
            'accent': '#ff6347',
            'success': '#32cd32',
            'warning': '#ffa500',
            'neutral': '#708090'
        }
        
        # Random events
        self.events = [
            {"name": "Economic Boom", "demand": 1.5, "cost": 1.0, "description": "The economy is thriving! Demand increases."},
            {"name": "Recession", "demand": 0.6, "cost": 1.0, "description": "Economic downturn. Demand decreases."},
            {"name": "Raw Material Shortage", "demand": 1.0, "cost": 1.8, "description": "Supply chain issues increase production costs."},
            {"name": "New Technology", "demand": 1.0, "cost": 0.7, "description": "Innovation reduces production costs!"},
            {"name": "Competitor Enters Market", "demand": 0.8, "cost": 1.0, "description": "New competition! Demand for your product decreases."},
            {"name": "Viral Marketing Success", "demand": 1.4, "cost": 1.0, "description": "Your product goes viral! Demand spikes."},
            {"name": "Normal Market Conditions", "demand": 1.0, "cost": 1.0, "description": "Steady market conditions."}
        ]
        
        self.create_widgets()
        self.update_market()
        
    def create_difficulty_selector(self):
        """Create difficulty level selector"""
        difficulty_frame = ttk.Frame(self.root)
        difficulty_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(difficulty_frame, text="Difficulty:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulties = [
            ("Easy", "easy", "More money, stable markets, forgiving mistakes"),
            ("Normal", "normal", "Balanced challenge and learning"),
            ("Hard", "hard", "Volatile markets, limited resources, realistic economics")
        ]
        
        for name, value, desc in difficulties:
            rb = ttk.Radiobutton(difficulty_frame, text=name, variable=self.difficulty_var, 
                               value=value, command=self.change_difficulty)
            rb.pack(side=tk.LEFT, padx=10)
            
            # Add tooltip-like description
            rb.bind("<Enter>", lambda e, d=desc: self.show_tooltip(d))
            rb.bind("<Leave>", lambda e: self.hide_tooltip())
        
        self.tooltip_label = ttk.Label(difficulty_frame, text="", foreground=self.colors['neutral'])
        self.tooltip_label.pack(side=tk.LEFT, padx=20)
    
    def show_tooltip(self, text):
        """Show tooltip text"""
        self.tooltip_label.config(text=text)
    
    def hide_tooltip(self):
        """Hide tooltip text"""
        self.tooltip_label.config(text="")
    
    def change_difficulty(self):
        """Change difficulty level"""
        old_difficulty = self.difficulty
        self.difficulty = self.difficulty_var.get()
        
        if old_difficulty != self.difficulty:
            self.apply_difficulty_settings()
            messagebox.showinfo("Difficulty Changed", 
                              f"Difficulty changed to {self.difficulty.title()}!\n\n"
                              f"Starting a new game with new settings.")
            self.new_game()
    
    def apply_difficulty_settings(self):
        """Apply difficulty-specific settings"""
        if self.difficulty == "easy":
            self.money = 1500
            self.max_turns = 15
            self.event_frequency = 0.3  # Less random events
        elif self.difficulty == "normal":
            self.money = 1000
            self.max_turns = 20
            self.event_frequency = 0.5
        elif self.difficulty == "hard":
            self.money = 750
            self.max_turns = 25
            self.event_frequency = 0.7  # More random events
        
    def create_widgets(self):
        """Create all UI elements"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabs
        self.game_frame = ttk.Frame(self.notebook)
        self.tutorial_frame = ttk.Frame(self.notebook)
        self.concepts_frame = ttk.Frame(self.notebook)
        self.scenarios_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.game_frame, text="🎮 Market Game")
        self.notebook.add(self.tutorial_frame, text="📚 Tutorial")
        self.notebook.add(self.concepts_frame, text="🧠 Economic Concepts")
        self.notebook.add(self.scenarios_frame, text="🌍 Real-World Scenarios")
        
        # Difficulty selector
        self.create_difficulty_selector()
        
        self.create_game_tab()
        self.create_tutorial_tab()
        self.create_concepts_tab()
        self.create_scenarios_tab()
        
    def create_game_tab(self):
        """Create the main game simulation"""
        # Status bar
        status_frame = ttk.LabelFrame(self.game_frame, text="📊 Business Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_labels = {}
        status_info = [
            ("Turn:", "turn"),
            ("💰 Money:", "money"),
            ("📦 Inventory:", "inventory"),
            ("📈 Market Price:", "market_price"),
            ("💲 Your Selling Price:", "selling_price")
        ]
        
        for i, (label, key) in enumerate(status_info):
            ttk.Label(status_frame, text=label, font=('Arial', 10, 'bold')).grid(row=0, column=i*2, padx=5)
            self.status_labels[key] = ttk.Label(status_frame, text="", font=('Arial', 10))
            self.status_labels[key].grid(row=0, column=i*2+1, padx=5)
        
        # Market information
        market_frame = ttk.LabelFrame(self.game_frame, text="🏪 Market Information", padding=10)
        market_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Market conditions display
        conditions_frame = ttk.Frame(market_frame)
        conditions_frame.pack(fill=tk.X)
        
        ttk.Label(conditions_frame, text="📈 Market Demand:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.demand_label = ttk.Label(conditions_frame, text="", font=('Arial', 9))
        self.demand_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(conditions_frame, text="📦 Market Supply:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=5)
        self.supply_label = ttk.Label(conditions_frame, text="", font=('Arial', 9))
        self.supply_label.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        ttk.Label(conditions_frame, text="⚙️ Production Cost:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5)
        self.cost_label = ttk.Label(conditions_frame, text="", font=('Arial', 9))
        self.cost_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Event display with better styling
        event_frame = ttk.Frame(market_frame)
        event_frame.pack(fill=tk.X, pady=5)
        self.event_label = ttk.Label(event_frame, text="", font=('Arial', 10), wraplength=600, 
                                   foreground=self.colors['secondary'], background='#e6f3ff', padding=5)
        self.event_label.pack(fill=tk.X)
        
        # Save/Load buttons
        save_frame = ttk.Frame(market_frame)
        save_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(save_frame, text="💾 Save Game", command=self.save_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="📁 Load Game", command=self.load_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="🏆 Achievements", command=self.show_achievements).pack(side=tk.LEFT, padx=5)
        
        # Actions frame
        actions_frame = ttk.LabelFrame(self.game_frame, text="Your Actions", padding=10)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Production section
        production_section = ttk.Frame(actions_frame)
        production_section.pack(fill=tk.X, pady=5)
        
        ttk.Label(production_section, text="Produce Items:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.produce_var = tk.StringVar(value="10")
        produce_entry = ttk.Entry(production_section, textvariable=self.produce_var, width=10)
        produce_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(production_section, text="Produce", command=self.produce_items).pack(side=tk.LEFT, padx=5)
        
        self.produce_info = ttk.Label(production_section, text="", foreground='gray')
        self.produce_info.pack(side=tk.LEFT, padx=10)
        
        # Pricing section
        pricing_section = ttk.Frame(actions_frame)
        pricing_section.pack(fill=tk.X, pady=5)
        
        ttk.Label(pricing_section, text="Set Selling Price:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.price_var = tk.StringVar(value="10")
        price_entry = ttk.Entry(pricing_section, textvariable=self.price_var, width=10)
        price_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(pricing_section, text="Set Price", command=self.set_price).pack(side=tk.LEFT, padx=5)
        
        self.price_info = ttk.Label(pricing_section, text="Higher price = more profit per sale, but fewer customers", foreground='gray')
        self.price_info.pack(side=tk.LEFT, padx=10)
        
        # End turn button
        ttk.Button(actions_frame, text="End Turn & Sell Products", 
                  command=self.end_turn, style='Accent.TButton').pack(pady=10)
        
        # Results display
        results_frame = ttk.LabelFrame(self.game_frame, text="Turn Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(results_frame, height=8, width=80, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Graph frame with multiple charts
        graph_frame = ttk.LabelFrame(self.game_frame, text="📊 Market Trends & Analysis", padding=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Graph controls
        controls_frame = ttk.Frame(graph_frame)
        controls_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(controls_frame, text="Show:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.show_price = tk.BooleanVar(value=True)
        self.show_profit = tk.BooleanVar(value=True)
        self.show_demand = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(controls_frame, text="Price", variable=self.show_price, 
                       command=self.draw_graph).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(controls_frame, text="Profit", variable=self.show_profit, 
                       command=self.draw_graph).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(controls_frame, text="Demand", variable=self.show_demand, 
                       command=self.draw_graph).pack(side=tk.LEFT, padx=5)
        
        self.canvas = tk.Canvas(graph_frame, bg='white', height=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # New game button
        button_frame = ttk.Frame(self.game_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="🎮 New Game", command=self.new_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Economic Analysis", command=self.show_analysis).pack(side=tk.LEFT, padx=5)
        
    def save_game(self):
        """Save game state"""
        game_state = {
            'difficulty': self.difficulty,
            'money': self.money,
            'inventory': self.inventory,
            'production_cost': self.production_cost,
            'selling_price': self.selling_price,
            'turn': self.turn,
            'max_turns': self.max_turns,
            'market_demand': self.market_demand,
            'market_supply': self.market_supply,
            'market_price': self.market_price,
            'consumer_preference': self.consumer_preference,
            'price_history': self.price_history,
            'demand_history': self.demand_history,
            'supply_history': self.supply_history,
            'profit_history': self.profit_history,
            'sales_history': self.sales_history,
            'achievements': self.achievements
        }
        
        try:
            with open('economics_simulator_save.json', 'w') as f:
                json.dump(game_state, f, indent=2)
            messagebox.showinfo("Save Successful", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        """Load game state"""
        try:
            with open('economics_simulator_save.json', 'r') as f:
                game_state = json.load(f)
            
            self.difficulty = game_state.get('difficulty', 'normal')
            self.difficulty_var.set(self.difficulty)
            self.apply_difficulty_settings()
            
            self.money = game_state.get('money', 1000)
            self.inventory = game_state.get('inventory', 0)
            self.production_cost = game_state.get('production_cost', 5)
            self.selling_price = game_state.get('selling_price', 10)
            self.turn = game_state.get('turn', 1)
            self.max_turns = game_state.get('max_turns', 20)
            self.market_demand = game_state.get('market_demand', 50)
            self.market_supply = game_state.get('market_supply', 50)
            self.market_price = game_state.get('market_price', 10)
            self.consumer_preference = game_state.get('consumer_preference', 1.0)
            self.price_history = game_state.get('price_history', [10])
            self.demand_history = game_state.get('demand_history', [50])
            self.supply_history = game_state.get('supply_history', [50])
            self.profit_history = game_state.get('profit_history', [0])
            self.sales_history = game_state.get('sales_history', [0])
            self.achievements = game_state.get('achievements', [])
            
            self.update_display()
            self.draw_graph()
            
            messagebox.showinfo("Load Successful", "Game loaded successfully!")
            
        except FileNotFoundError:
            messagebox.showwarning("No Save File", "No saved game found!")
        except Exception as e:
            messagebox.showerror("Load Failed", f"Failed to load game: {str(e)}")
    
    def show_achievements(self):
        """Display achievements"""
        ach_win = tk.Toplevel(self.root)
        ach_win.title("🏆 Economic Achievements")
        ach_win.geometry("500x400")
        ach_win.configure(bg=self.colors['bg'])
        
        ttk.Label(ach_win, text="🏆 Economic Achievements", 
                 font=('Arial', 16, 'bold')).pack(pady=15)
        
        if not self.achievements:
            ttk.Label(ach_win, text="No achievements unlocked yet.\n\nKeep playing to earn achievements!",
                     font=('Arial', 11)).pack(pady=20)
        else:
            achievements_frame = ttk.Frame(ach_win)
            achievements_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for achievement in self.achievements:
                ach_frame = ttk.Frame(achievements_frame, relief='solid', borderwidth=1)
                ach_frame.pack(fill=tk.X, pady=5)
                ttk.Label(ach_frame, text=f"🏆 {achievement}", 
                         font=('Arial', 11, 'bold')).pack(pady=8, padx=15)
        
        ttk.Button(ach_win, text="Close", command=ach_win.destroy).pack(pady=15)
    
    def check_achievements(self):
        """Check and award achievements"""
        new_achievements = []
        
        # Profit achievements
        total_profit = sum(self.profit_history)
        if total_profit >= 1000 and "Profit Master" not in self.achievements:
            new_achievements.append("Profit Master")
        if total_profit >= 500 and "Business Savvy" not in self.achievements:
            new_achievements.append("Business Savvy")
        
        # Market understanding
        if len([p for p in self.profit_history if p > 0]) >= 10 and "Market Expert" not in self.achievements:
            new_achievements.append("Market Expert")
        
        # Survival achievements
        if self.turn >= self.max_turns and self.money > 1000 and "Economic Survivor" not in self.achievements:
            new_achievements.append("Economic Survivor")
        
        # Strategy achievements
        avg_price_ratio = sum(self.price_history) / len(self.price_history) / 10
        if 0.9 <= avg_price_ratio <= 1.1 and "Price Optimizer" not in self.achievements:
            new_achievements.append("Price Optimizer")
        
        if new_achievements:
            self.achievements.extend(new_achievements)
            achievement_text = "🏆 New Achievements Unlocked!\n\n" + "\n".join(f"• {ach}" for ach in new_achievements)
            messagebox.showinfo("Achievement Unlocked!", achievement_text)
    
    def show_analysis(self):
        """Show economic analysis of current game"""
        analysis_win = tk.Toplevel(self.root)
        analysis_win.title("📊 Economic Analysis")
        analysis_win.geometry("700x500")
        analysis_win.configure(bg=self.colors['bg'])
        
        ttk.Label(analysis_win, text="📊 Economic Analysis", 
                 font=('Arial', 16, 'bold')).pack(pady=15)
        
        analysis_text = tk.Text(analysis_win, wrap=tk.WORD, padx=10, pady=10, height=20)
        analysis_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Generate analysis
        total_profit = sum(self.profit_history)
        avg_profit = total_profit / max(1, len(self.profit_history))
        profitable_turns = len([p for p in self.profit_history if p > 0])
        total_sales = sum(self.sales_history)
        
        analysis = f"""
ECONOMIC ANALYSIS - TURN {self.turn}

═══════════════════════════════════════════════════════════════

PERFORMANCE METRICS:
• Total Profit: ${total_profit:.2f}
• Average Profit per Turn: ${avg_profit:.2f}
• Profitable Turns: {profitable_turns}/{len(self.profit_history)}
• Total Items Sold: {total_sales}
• Current Money: ${self.money:.2f}

MARKET ANALYSIS:
• Average Market Price: ${sum(self.price_history)/len(self.price_history):.2f}
• Average Your Price: ${sum([p for p in self.price_history if p != 10]) / max(1, len([p for p in self.price_history if p != 10])):.2f}
• Price Competitiveness: {'Good' if abs(self.selling_price - self.market_price) < 2 else 'Needs Adjustment'}

ECONOMIC LESSONS LEARNED:

1. SUPPLY & DEMAND RELATIONSHIP:
   Your sales are affected by how your price compares to market conditions.
   When you price too high, you sell fewer items. When you price competitively, you sell more.

2. PROFIT MAXIMIZATION:
   Profit = (Selling Price - Production Cost) × Items Sold
   You need to balance price per item vs. quantity sold.

3. MARKET VOLATILITY:
   Random events affect market conditions. Successful businesses adapt to change.

4. OPPORTUNITY COST:
   Money spent on production can't be used for other opportunities.
   Every business decision involves trade-offs.

STRATEGY RECOMMENDATIONS:

• {'✓ Good job staying competitive!' if abs(self.selling_price - self.market_price) < 2 else 'Consider adjusting your price to match market conditions.'}
• {'✓ Strong profit performance!' if avg_profit > 50 else 'Focus on finding the optimal price point for maximum profit.'}
• {'✓ Good market adaptation!' if profitable_turns / max(1, len(self.profit_history)) > 0.6 else 'Try to maintain profitability across more turns.'}

Keep experimenting to master market economics!
"""
        
        analysis_text.insert('1.0', analysis)
        analysis_text.config(state=tk.DISABLED)
        
        ttk.Button(analysis_win, text="Close", command=analysis_win.destroy).pack(pady=10)
        
    def create_tutorial_tab(self):
        """Create tutorial tab"""
        tutorial_text = tk.Text(self.tutorial_frame, wrap=tk.WORD, padx=10, pady=10)
        tutorial_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.tutorial_frame, orient=tk.VERTICAL, command=tutorial_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tutorial_text.config(yscrollcommand=scrollbar.set)
        
        tutorial_content = """
ECONOMICS MARKET SIMULATOR - HOW TO PLAY

OBJECTIVE:
Make as much profit as possible over 20 turns by managing production and pricing in a dynamic market.

GAME MECHANICS:

1. PRODUCTION
   - You can produce items each turn
   - Production costs money (shown as "Production Cost")
   - Items go into your inventory
   - Formula: Total Cost = Production Cost × Number of Items

2. PRICING
   - Set your selling price for items
   - Higher prices = more profit per item, but fewer customers
   - Lower prices = less profit per item, but more customers
   - Try to find the "sweet spot"!

3. SELLING
   - At the end of each turn, customers buy your products
   - Sales depend on:
     * Your price vs. market price
     * Market demand
     * Random market events

4. MARKET DYNAMICS

   Supply and Demand:
   - If demand > supply → prices tend to rise
   - If supply > demand → prices tend to fall
   
   Market Price:
   - The "equilibrium" price in the market
   - Changes based on supply and demand
   
   Your Strategy:
   - Price too high → few sales
   - Price too low → low profit
   - Watch market trends!

5. RANDOM EVENTS
   Events happen each turn that affect the market:
   - Economic booms (higher demand)
   - Recessions (lower demand)
   - Cost changes (materials, technology)
   - Competition changes
   
6. WINNING STRATEGY TIPS

   - Start conservative: Produce moderate amounts
   - Watch the market price: Try to stay competitive
   - Adapt to events: Adjust production and pricing
   - Balance inventory: Don't overproduce or underproduce
   - Calculate profit margin: Price - Cost = Profit per item
   - Think ahead: Build cash reserves for expensive production

ECONOMIC CONCEPTS DEMONSTRATED:

• Supply and Demand curves
• Price elasticity (how price affects sales)
• Market equilibrium
• Profit maximization
• Opportunity cost (money spent on production)
• Risk and uncertainty (random events)
• Competition and market structure

EXAMPLE TURN:

Turn 1:
- You have $1000
- Production cost is $5 per item
- Market price is $10
- You produce 50 items (cost: $250, leaving you $750)
- You set selling price at $11 (slightly above market)
- End turn: You sell 35 items for $385
- Profit this turn: $385 - $250 = $135
- New total: $885 (you lost money this turn!)
- Lesson: Price too high = fewer sales than expected

Better strategy: Price at $9 or $10 to sell more!

CHALLENGES TO TRY:

1. Steady Growth: Make profit every turn
2. Risk Taker: Produce maximum items and price aggressively
3. Conservative: Never go below $500 cash
4. Market Leader: Always match or beat market price
5. Adaptive: Change strategy based on events

Good luck! Remember: In economics, there's always a trade-off!
"""
        
        tutorial_text.insert('1.0', tutorial_content)
        tutorial_text.config(state=tk.DISABLED)
        
    def create_concepts_tab(self):
        """Create economic concepts reference"""
        concepts_text = tk.Text(self.concepts_frame, wrap=tk.WORD, padx=10, pady=10)
        concepts_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.concepts_frame, orient=tk.VERTICAL, command=concepts_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        concepts_text.config(yscrollcommand=scrollbar.set)
        
        concepts_content = """
ECONOMIC CONCEPTS EXPLAINED

═══════════════════════════════════════════════════════

1. SUPPLY AND DEMAND

   The fundamental principle of economics!
   
   DEMAND: How much people want to buy
   - Higher price → Lower demand (people buy less)
   - Lower price → Higher demand (people buy more)
   
   SUPPLY: How much is available to sell
   - Higher price → Higher supply (producers make more)
   - Lower price → Lower supply (producers make less)
   
   EQUILIBRIUM: Where supply meets demand
   - This determines the market price
   - Natural "balance point"

   Real Example: iPhone Pricing
   - Apple prices high → fewer people buy (but more profit per phone)
   - If priced too high → inventory builds up (too much supply)
   - If priced too low → shortages (too much demand)

═══════════════════════════════════════════════════════

2. PRICE ELASTICITY

   How sensitive is demand to price changes?
   
   ELASTIC: Demand changes a lot with price
   - Example: Restaurant meals
   - Price increase → many people cook at home instead
   
   INELASTIC: Demand doesn't change much with price
   - Example: Gasoline, medicine
   - Price increase → people still need it, buy anyway
   
   In the simulator:
   - Your products are moderately elastic
   - Price too high → lose many customers
   - Price competitive → sell well

═══════════════════════════════════════════════════════

3. PROFIT MAXIMIZATION

   The goal of businesses!
   
   Profit = Revenue - Costs
   Revenue = Price × Quantity Sold
   
   Two strategies:
   
   HIGH PRICE, LOW VOLUME:
   - Sell fewer items at high price
   - Example: Luxury goods (Rolex watches)
   - Risk: Price too high = very few sales
   
   LOW PRICE, HIGH VOLUME:
   - Sell many items at low price
   - Example: Walmart
   - Risk: Price too low = little profit per item
   
   The sweet spot:
   - Maximum total profit
   - Usually between extremes
   - Requires trial and error!

═══════════════════════════════════════════════════════

4. MARKET STRUCTURES

   Different types of markets:
   
   PERFECT COMPETITION:
   - Many sellers
   - Identical products
   - No control over price
   - Example: Agricultural products
   
   MONOPOLY:
   - One seller
   - No competition
   - Complete price control
   - Example: Local utility company
   
   OLIGOPOLY:
   - Few sellers
   - Similar products
   - Some price influence
   - Example: Cell phone carriers
   
   MONOPOLISTIC COMPETITION:
   - Many sellers
   - Differentiated products
   - Some price flexibility
   - Example: Restaurants, clothing stores
   
   The simulator represents monopolistic competition.

═══════════════════════════════════════════════════════

5. OPPORTUNITY COST

   What you give up when making a choice.
   
   In the simulator:
   - Spend $500 on production
   - Opportunity cost: You can't use that $500 for other things
   - If sales are bad, you lose that opportunity
   
   Real life:
   - Go to college: Opportunity cost = money you could have earned working
   - Buy a car: Opportunity cost = other things you could buy
   - Time at work: Opportunity cost = time with family/friends
   
   Key insight: Every economic decision involves trade-offs!

═══════════════════════════════════════════════════════

6. SCARCITY AND CHOICE

   The fundamental economic problem.
   
   SCARCITY: Not enough resources for unlimited wants
   - Limited money
   - Limited time
   - Limited materials
   
   Because of scarcity, we must CHOOSE:
   - What to produce?
   - How much to produce?
   - What price to charge?
   
   In simulator:
   - Scarcity: Limited money to produce items
   - Choice: Produce more now or save for later?
   - Trade-off: Current production vs. future flexibility

═══════════════════════════════════════════════════════

7. MARKET EQUILIBRIUM

   Where supply equals demand.
   
   If Price > Equilibrium:
   - Surplus (too much supply)
   - Sellers lower prices
   - Market moves toward equilibrium
   
   If Price < Equilibrium:
   - Shortage (too much demand)
   - Sellers raise prices
   - Market moves toward equilibrium
   
   The "invisible hand":
   - Markets naturally move toward equilibrium
   - No central planner needed
   - Prices signal information
   
   Watch this happen in the simulator's market price!

═══════════════════════════════════════════════════════

8. FIXED VS. VARIABLE COSTS

   FIXED COSTS: Don't change with production
   - Rent, equipment, salaries
   - Pay these even if you produce nothing
   
   VARIABLE COSTS: Change with production
   - Raw materials, hourly labor
   - The simulator's production cost
   
   TOTAL COST = Fixed Costs + Variable Costs
   
   Business insight:
   - Need to cover fixed costs
   - Higher production spreads fixed costs over more items
   - "Economies of scale"

═══════════════════════════════════════════════════════

9. REVENUE STREAMS

   Where money comes from.
   
   In simulator:
   - Revenue = Selling Price × Items Sold
   - Simple, single product
   
   Real businesses:
   - Multiple products
   - Different prices
   - Different profit margins
   
   Strategy:
   - Maximize total revenue
   - Balance between price and volume
   - Respond to market conditions

═══════════════════════════════════════════════════════

10. RISK AND UNCERTAINTY

    Economic decisions involve unknown outcomes.
    
    In simulator:
    - Random events affect market
    - Can't predict exact sales
    - Must adapt strategy
    
    Risk management:
    - Don't spend all your money (liquidity)
    - Diversify (in real world: multiple products)
    - Have reserves for bad turns
    - Be flexible
    
    Real world examples:
    - Farmers facing weather uncertainty
    - Businesses facing economic cycles
    - Investors managing portfolios
    
    Key lesson: Perfect information doesn't exist!

═══════════════════════════════════════════════════════

CONNECTING TO REAL WORLD:

All these concepts affect YOU:

- When you buy something: Demand
- When prices change: Supply and demand
- When you choose one thing over another: Opportunity cost
- When you save vs. spend: Time value of money
- When you compare prices: Market competition
- When you negotiate: Economic value

Understanding economics helps you:
• Make better financial decisions
• Understand news and policy
• Recognize market trends
• Plan for the future
• Be an informed citizen

Try to spot these concepts in your daily life!
"""
        
        concepts_text.insert('1.0', concepts_content)
        concepts_text.config(state=tk.DISABLED)
        
    def create_scenarios_tab(self):
        """Create real-world scenarios tab"""
        scenarios_text = tk.Text(self.scenarios_frame, wrap=tk.WORD, padx=10, pady=10)
        scenarios_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.scenarios_frame, orient=tk.VERTICAL, command=scenarios_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scenarios_text.config(yscrollcommand=scrollbar.set)
        
        scenarios_content = """
REAL-WORLD ECONOMIC SCENARIOS

═══════════════════════════════════════════════════════

SCENARIO 1: THE TOILET PAPER SHORTAGE (2020)

What Happened:
During COVID-19 pandemic start, toilet paper disappeared from stores.

Economic Analysis:
• DEMAND: Panic buying → sudden demand spike
• SUPPLY: Same production capacity, can't increase quickly
• RESULT: Shortage (demand >> supply)
• PRICE: Some retailers raised prices (surge pricing)
• HOARDING: People bought more than needed, worsening shortage

Lessons:
- Supply can't always respond quickly to demand changes
- Consumer behavior affects markets (panic buying)
- Price controls can worsen shortages
- Eventually supply caught up, market stabilized

Connection to Simulator:
- Demand shocks from random events
- Limited ability to produce instantly
- Need to balance supply and demand

═══════════════════════════════════════════════════════

SCENARIO 2: NETFLIX PRICING STRATEGY

Background:
Netflix started at $7.99/month, now $15+ for standard plan.

Economic Strategy:
• START LOW: Build customer base, low price
• INCREASE GRADUALLY: As service improves, raise prices
• TEST PRICE ELASTICITY: How many customers leave?
• DIFFERENT TIERS: Basic, Standard, Premium pricing
• CONTENT INVESTMENT: Higher prices fund better shows

Results:
- Most customers stayed despite price increases
- Some switched to competitors (elasticity)
- More revenue → better content → more value
- Sustainable business model

Lessons:
- Price elasticity varies by product value
- Can raise prices if you add value
- Gradual changes better than sudden jumps
- Competition limits pricing power

Connection to Simulator:
- Finding optimal price point
- Balancing price and customer retention
- Market competition effects

═══════════════════════════════════════════════════════

SCENARIO 3: HOUSING MARKET BUBBLE (2008)

What Happened:
House prices rose dramatically, then crashed, causing recession.

Economic Chain:
1. Low interest rates → easy to borrow money
2. More buyers → demand increases
3. Prices rise → people buy expecting more increases
4. "Flipping" houses becomes profitable
5. BUBBLE: Prices disconnected from real value
6. CRASH: Reality hits, prices plummet
7. Many people lose homes, banks fail

Key Concepts:
• SPECULATION: Buying because you expect prices to rise
• BUBBLE: Unsustainable price increases
• LEVERAGE: Borrowing to invest (risky!)
• SYSTEMIC RISK: One market affects entire economy

Lessons:
- Markets can become irrational (temporarily)
- Rapid price increases aren't always sustainable
- Debt amplifies both gains and losses
- Government regulation matters

Connection to Simulator:
- Market prices can vary from "true" value
- Economic events affect business environment
- Importance of financial reserves

═══════════════════════════════════════════════════════

SCENARIO 4: CONCERT TICKET PRICING (DYNAMIC PRICING)

Modern Approach:
Ticket prices change based on demand (like airline tickets).

Traditional Model:
• Fixed price ($50)
• First come, first served
• Scalpers buy and resell at higher prices
• Artists/venues don't capture full value

Dynamic Pricing:
• High demand shows → higher prices
• Low demand shows → lower prices
• Prices adjust in real-time
• Less scalping (official prices closer to market value)

Controversy:
- Fans feel exploited (higher prices for popular shows)
- More economically efficient
- Questions of fairness vs. efficiency

Economic Analysis:
• EFFICIENCY: Resources go to those who value them most
• CONSUMER SURPLUS: What fans would pay vs. what they do pay
• FAIRNESS: Should price = willingness to pay?

Connection to Simulator:
- Demand affects optimal pricing
- Higher demand → can charge more
- Balance profit and customer satisfaction

═══════════════════════════════════════════════════════

SCENARIO 5: FARMING AND CROP PRICES

Farmer's Challenge:
Plant crops now, sell months later. What price will you get?

Economic Uncertainty:
• WEATHER: Drought → low supply → high prices
• GLOBAL MARKETS: Other countries' harvests affect price
• FUEL COSTS: Tractor fuel is variable cost
• DEMAND SHIFTS: Biofuels, exports, consumer preferences
• NO PRICE CONTROL: "Price taker" not "price maker"

Risk Management:
• Crop insurance
• Futures contracts (lock in price ahead)
• Diversify crops
• Government support programs

Real Example - Corn:
- 2012 drought → corn prices spiked (supply shock)
- 2014 good harvest → prices dropped (supply increase)
- Farmers who locked in 2012 prices did well in 2014
- Those without contracts struggled

Lessons:
- Commodity markets are volatile
- Can't control prices, only production
- Risk management essential
- Weather and global events matter

Connection to Simulator:
- Production decisions with uncertainty
- Random events affect profitability
- Can't always control outcomes
- Need financial reserves

═══════════════════════════════════════════════════════

SCENARIO 6: MINIMUM WAGE DEBATE

The Question:
Should government set a minimum wage? How high?

Arguments FOR Higher Minimum Wage:
• Workers earn living wage
• Reduces poverty
• More consumer spending → economic growth
• Many studies show minimal job losses

Arguments AGAINST Higher Minimum Wage:
• Businesses cut jobs (can't afford workers)
• Higher labor costs → higher prices
• Hurts small businesses most
• Some workers lose jobs

Economic Concepts:
• PRICE FLOOR: Minimum wage = price floor for labor
• SUPPLY/DEMAND: Wage above equilibrium → unemployment?
• MONOPSONY: When few employers, they set low wages
• INFLATION: Higher wages → higher prices?

Real Data:
- Studies show mixed results
- Small increases: minimal job loss
- Large increases: some job loss in some markets
- Depends on local economy, industry

Complex Trade-offs:
- Help some workers vs. potentially hurt others
- Economic efficiency vs. fairness
- Short-term vs. long-term effects

Connection to Simulator:
- Price floors and ceilings affect markets
- Trade-offs in economic decisions
- No perfect solutions

═══════════════════════════════════════════════════════

SCENARIO 7: BLACK FRIDAY PRICING STRATEGY

Retail Strategy:
Deep discounts one day a year - why?

Business Logic:
• LOSS LEADERS: Sell some items below cost
• GET CUSTOMERS IN: Once in store, buy other things
• CLEAR INVENTORY: Make room for new products
• BEAT COMPETITION: Customers choose your store
• URGENCY: Limited time creates urgency
• PROFIT ON VOLUME: Lower margin, higher sales

Consumer Psychology:
- Scarcity: "Only 10 available!" drives purchases
- Anchoring: Compare sale price to "original" price
- Sunk cost: Already waited in line, might as well buy
- Social proof: Everyone else is buying

Results:
- Some stores make profit from increased sales
- Some lose money but gain customers
- E-commerce changing the game
- "Cyber Monday" now bigger than Black Friday

Economic Concepts:
• PRICE DISCRIMINATION: Different prices, different times
• CONSUMER SURPLUS: Customers get deals, feel good
• STRATEGIC PRICING: Short-term loss, long-term gain

Connection to Simulator:
- Pricing strategy matters
- Sometimes low prices make sense
- Consider long-term, not just immediate profit

═══════════════════════════════════════════════════════

SCENARIO 8: UBER SURGE PRICING

How It Works:
During high demand (New Year's Eve, rain), prices multiply (2x, 3x, 5x).

Uber's Argument:
• High prices bring more drivers online
• Matches supply to demand
• Ensures rides available
• Efficient allocation

Customer Reaction:
- Feel exploited during emergencies
- Many refuse to pay surge prices
- PR problems
- But... it works (more drivers do come online)

Economic Analysis:
• RATIONING: How to allocate scarce resources?
  - By price? (Uber's approach)
  - First come, first served? (Traditional)
  - Lottery?
  - Need-based?

• EFFICIENCY: Surge pricing is economically efficient
• FAIRNESS: But is it fair?

Alternative: Queuing
- No surge, but long wait times
- No incentive for more drivers
- Same scarcity, different allocation method

Lessons:
- Prices serve a function (rationing)
- Efficiency and fairness can conflict
- Cultural attitudes toward pricing vary
- Technology enables dynamic pricing

Connection to Simulator:
- Price responds to demand
- Higher prices during high demand
- Trade-offs in pricing strategy

═══════════════════════════════════════════════════════

DISCUSSION QUESTIONS:

1. Which scenario surprised you most? Why?

2. In each scenario, who benefits and who is hurt by price changes?

3. Should there be limits on how much prices can change? When?

4. How do these scenarios relate to your own spending decisions?

5. What role should government play in regulating prices?

6. How has technology (internet, apps) changed how markets work?

7. What economic principles apply across multiple scenarios?

8. How would you solve the tension between efficiency and fairness?

═══════════════════════════════════════════════════════

APPLY YOUR LEARNING:

Look for economic concepts in the news:
• Supply chain issues
• Inflation reports
• Stock market changes
• New product launches
• Labor market news
• International trade

Ask these questions:
- What's the supply and demand situation?
- Who has pricing power?
- What incentives do people face?
- What are the trade-offs?
- Who benefits? Who is hurt?
- Are markets working efficiently?
- What role does government play?

Economics is everywhere! Once you see it, you can't unsee it.
"""
        
        scenarios_text.insert('1.0', scenarios_content)
        scenarios_text.config(state=tk.DISABLED)
        
    def update_display(self):
        """Update all status displays"""
        self.status_labels['turn'].config(text=f"{self.turn}/{self.max_turns}")
        self.status_labels['money'].config(text=f"${self.money:.2f}")
        self.status_labels['inventory'].config(text=str(self.inventory))
        self.status_labels['market_price'].config(text=f"${self.market_price:.2f}")
        self.status_labels['selling_price'].config(text=f"${self.selling_price:.2f}")
        
        self.demand_label.config(text=f"{self.market_demand:.1f} units")
        self.supply_label.config(text=f"{self.market_supply:.1f} units")
        self.cost_label.config(text=f"${self.production_cost:.2f} per item")
        
        # Update produce info
        try:
            qty = int(self.produce_var.get())
            cost = qty * self.production_cost
            self.produce_info.config(text=f"Total cost: ${cost:.2f}")
        except:
            self.produce_info.config(text="")
        
    def produce_items(self):
        """Produce items"""
        try:
            quantity = int(self.produce_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Please enter a positive number")
                return
                
            total_cost = quantity * self.production_cost
            
            if total_cost > self.money:
                messagebox.showerror("Insufficient Funds", 
                                   f"You need ${total_cost:.2f} but only have ${self.money:.2f}")
                return
            
            self.money -= total_cost
            self.inventory += quantity
            self.update_display()
            
            messagebox.showinfo("Production Complete", 
                              f"Produced {quantity} items for ${total_cost:.2f}\n"
                              f"New inventory: {self.inventory} items\n"
                              f"Money remaining: ${self.money:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def set_price(self):
        """Set selling price"""
        try:
            price = float(self.price_var.get())
            if price <= 0:
                messagebox.showerror("Error", "Price must be positive")
                return
            
            self.selling_price = price
            self.update_display()
            
            # Give feedback on pricing
            if price < self.production_cost:
                feedback = "WARNING: Selling below cost! You'll lose money on each sale."
            elif price < self.market_price * 0.8:
                feedback = "Very low price - you'll sell many items but profit will be low."
            elif price > self.market_price * 1.5:
                feedback = "Very high price - you may not sell much."
            elif price > self.market_price * 1.2:
                feedback = "Above market price - sales may be limited."
            else:
                feedback = "Competitive pricing - good balance of profit and sales."
            
            self.price_info.config(text=feedback)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
    
    def end_turn(self):
        """End turn and calculate sales"""
        if self.inventory <= 0:
            messagebox.showwarning("No Inventory", "You have no items to sell! Produce some first.")
            return
        
        # Calculate sales based on price vs market price
        price_ratio = self.selling_price / self.market_price
        
        # Sales decrease as price increases relative to market
        # Using exponential decay function
        demand_factor = math.exp(-((price_ratio - 1) ** 2) * 2) * self.consumer_preference
        
        # Base sales on demand
        potential_sales = int(self.market_demand * demand_factor)
        
        # Can't sell more than inventory
        actual_sales = min(potential_sales, self.inventory)
        
        # Add some randomness
        actual_sales = max(0, int(actual_sales * random.uniform(0.8, 1.2)))
        actual_sales = min(actual_sales, self.inventory)
        
        # Calculate revenue and profit
        revenue = actual_sales * self.selling_price
        cost_of_goods = actual_sales * self.production_cost
        profit = revenue - cost_of_goods
        
        # Update state
        self.inventory -= actual_sales
        self.money += revenue
        
        # Record history
        self.profit_history.append(profit)
        self.sales_history.append(actual_sales)
        
        # Display results with educational feedback
        result = f"\n{'='*70}\n"
        result += f"TURN {self.turn} RESULTS - ECONOMIC ANALYSIS\n"
        result += f"{'='*70}\n"
        result += f"📊 SALES PERFORMANCE:\n"
        result += f"• Items sold: {actual_sales} out of {actual_sales + self.inventory} in inventory\n"
        result += f"• Revenue: ${revenue:.2f}\n"
        result += f"• Cost of goods sold: ${cost_of_goods:.2f}\n"
        result += f"• Profit this turn: ${profit:.2f}\n"
        result += f"• Remaining inventory: {self.inventory}\n"
        result += f"• Total money: ${self.money:.2f}\n"
        
        # Economic analysis
        result += f"\n🧠 ECONOMIC ANALYSIS:\n"
        
        # Price analysis
        price_ratio = self.selling_price / self.market_price
        if price_ratio < 0.8:
            result += f"• PRICING: Your price (${self.selling_price:.2f}) is significantly below market price (${self.market_price:.2f})\n"
            result += f"  → You sold {actual_sales} items but profit margin is low\n"
        elif price_ratio > 1.2:
            result += f"• PRICING: Your price (${self.selling_price:.2f}) is above market price (${self.market_price:.2f})\n"
            result += f"  → Fewer customers bought due to higher price\n"
        else:
            result += f"• PRICING: Your price is competitive with market conditions\n"
            result += f"  → Good balance of sales volume and profit margin\n"
        
        # Inventory analysis
        if actual_sales < self.inventory + actual_sales:
            result += f"• INVENTORY: You could have sold {self.inventory + actual_sales - actual_sales} more items\n"
            result += f"  → Consider producing more next turn or lowering price\n"
        
        # Profit analysis
        if profit > 0:
            result += f"• PROFITABILITY: ✅ Profitable turn! You earned ${profit:.2f}\n"
        else:
            result += f"• PROFITABILITY: ❌ Loss of ${-profit:.2f} this turn\n"
            result += f"  → Review your pricing and production costs\n"
        
        # Market condition feedback
        if self.market_demand > 60:
            result += f"• MARKET: High demand - good opportunity for sales!\n"
        elif self.market_demand < 40:
            result += f"• MARKET: Low demand - consider lowering price or reducing production\n"
        
        # Strategy tips
        result += f"\n💡 STRATEGY TIPS:\n"
        if self.turn < self.max_turns:
            if profit <= 0:
                result += f"• Try adjusting your price closer to market conditions\n"
                result += f"• Consider producing fewer items to reduce costs\n"
            else:
                result += f"• Great job! Try to maintain this profitable strategy\n"
                result += f"• Watch for market changes that might affect demand\n"
        
        self.results_text.insert('1.0', result)
        
        # Move to next turn
        self.turn += 1
        
        if self.turn > self.max_turns:
            self.end_game()
            return
        
        # Update market for next turn
        self.update_market()
        self.update_display()
        self.draw_graph()
        
        # Check achievements
        self.check_achievements()
        
    def update_market(self):
        """Update market conditions"""
        # Random event
        event = random.choice(self.events)
        self.event_label.config(text=f"EVENT: {event['name']} - {event['description']}")
        
        # Apply event effects
        self.market_demand = 50 * event['demand']
        self.production_cost = 5 * event['cost']
        self.consumer_preference = event['demand']
        
        # Update market supply (simulated other producers)
        self.market_supply = random.uniform(40, 60)
        
        # Calculate market price based on supply/demand
        if self.market_demand > self.market_supply:
            # High demand pushes prices up
            self.market_price = 10 * (self.market_demand / self.market_supply) ** 0.5
        else:
            # High supply pushes prices down
            self.market_price = 10 * (self.market_demand / self.market_supply) ** 0.5
        
        # Add some randomness
        self.market_price *= random.uniform(0.9, 1.1)
        
        # Keep reasonable bounds
        self.market_price = max(6, min(20, self.market_price))
        
        # Record history
        self.price_history.append(self.market_price)
        self.demand_history.append(self.market_demand)
        self.supply_history.append(self.market_supply)
        
    def draw_graph(self):
        """Draw market trends graph with multiple series"""
        self.canvas.delete('all')
        
        if len(self.price_history) < 2:
            return
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 100 or height < 100:
            return
        
        margin = 50
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin
        
        # Draw axes
        self.canvas.create_line(margin, height - margin, width - margin, height - margin, width=2)
        self.canvas.create_line(margin, margin, margin, height - margin, width=2)
        
        # Labels
        self.canvas.create_text(width // 2, height - 10, text="Turn", font=('Arial', 10))
        self.canvas.create_text(15, height // 2, text="Value", angle=90, font=('Arial', 10))
        
        # Prepare data series
        series_data = []
        
        if self.show_price.get():
            series_data.append(('Price ($)', self.price_history, 'blue', 2))
        
        if self.show_profit.get() and len(self.profit_history) > 1:
            # Normalize profit to positive values for display
            profit_data = [p + 100 for p in self.profit_history]  # Shift up by 100
            series_data.append(('Profit ($)', profit_data, 'green', 2))
        
        if self.show_demand.get():
            series_data.append(('Demand', self.demand_history, 'red', 2))
        
        # Draw each series
        for name, data, color, width_line in series_data:
            if len(data) < 2:
                continue
            
            # Find min/max for scaling
            data_min = min(data)
            data_max = max(data)
            data_range = data_max - data_min if data_max != data_min else 1
            
            points = []
            for i, value in enumerate(data):
                x = margin + (i / (len(data) - 1)) * graph_width
                y = height - margin - ((value - data_min) / data_range) * graph_height
                points.extend([x, y])
            
            if len(points) >= 4:
                self.canvas.create_line(points, fill=color, width=width_line, smooth=True)
        
        # Legend
        legend_y = 20
        for name, _, color, _ in series_data:
            self.canvas.create_line(width - 150, legend_y, width - 120, legend_y, fill=color, width=2)
            self.canvas.create_text(width - 80, legend_y, text=name, anchor=tk.W, font=('Arial', 9))
            legend_y += 20
        
    def new_game(self):
        """Start a new game"""
        # Apply difficulty settings
        self.apply_difficulty_settings()
        
        self.inventory = 0
        self.production_cost = 5
        self.selling_price = 10
        self.turn = 1
        
        self.market_demand = 50
        self.market_supply = 50
        self.market_price = 10
        self.consumer_preference = 1.0
        
        self.price_history = [10]
        self.demand_history = [50]
        self.supply_history = [50]
        self.profit_history = [0]
        self.sales_history = [0]
        
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', f"🎮 New {self.difficulty.title()} game started!\n\n"
                                       f"Starting money: ${self.money:.2f}\n"
                                       f"Goal: Complete {self.max_turns} turns profitably.\n\n"
                                       f"Produce items and set your selling price to begin!\n")
        
        self.update_market()
        self.update_display()
        self.canvas.delete('all')
        
        # Reset achievements for new game
        self.achievements = []
        
    def end_game(self):
        """End game and show results"""
        total_profit = sum(self.profit_history)
        avg_profit = total_profit / len(self.profit_history) if self.profit_history else 0
        profitable_turns = len([p for p in self.profit_history if p > 0])
        total_sales = sum(self.sales_history)
        
        result = f"\n{'='*70}\n"
        result += f"🎉 GAME OVER - FINAL ECONOMIC ANALYSIS\n"
        result += f"{'='*70}\n"
        result += f"📈 FINANCIAL SUMMARY:\n"
        result += f"• Starting money: ${1000 if self.difficulty == 'normal' else (1500 if self.difficulty == 'easy' else 750):.2f}\n"
        result += f"• Final money: ${self.money:.2f}\n"
        result += f"• Net change: ${self.money - (1000 if self.difficulty == 'normal' else (1500 if self.difficulty == 'easy' else 750)):.2f}\n"
        result += f"• Total profit over all turns: ${total_profit:.2f}\n"
        result += f"• Average profit per turn: ${avg_profit:.2f}\n"
        result += f"• Profitable turns: {profitable_turns}/{len(self.profit_history)}\n"
        result += f"• Total items sold: {total_sales}\n"
        
        # Performance rating
        if self.difficulty == "easy":
            if self.money >= 2000:
                rating = "EXCELLENT! Master economist even on easy mode!"
                score = 5
            elif self.money >= 1700:
                rating = "GREAT! Strong understanding of economics!"
                score = 4
            elif self.money >= 1500:
                rating = "GOOD! Profitable business performance!"
                score = 3
            elif self.money >= 1300:
                rating = "OKAY. Broke even with extra starting money."
                score = 2
            else:
                rating = "NEEDS IMPROVEMENT. Focus on pricing strategy."
                score = 1
        elif self.difficulty == "normal":
            if self.money >= 2000:
                rating = "EXCELLENT! Economics virtuoso!"
                score = 5
            elif self.money >= 1500:
                rating = "GREAT! Master of supply and demand!"
                score = 4
            elif self.money >= 1200:
                rating = "GOOD! Solid business acumen!"
                score = 3
            elif self.money >= 1000:
                rating = "OKAY. Broke even - room for improvement."
                score = 2
            else:
                rating = "NEEDS IMPROVEMENT. Study pricing and market dynamics."
                score = 1
        else:  # hard
            if self.money >= 1500:
                rating = "EXCELLENT! Economics genius on hard mode!"
                score = 5
            elif self.money >= 1200:
                rating = "GREAT! Thrived in challenging market conditions!"
                score = 4
            elif self.money >= 900:
                rating = "GOOD! Survived hard mode economics!"
                score = 3
            elif self.money >= 750:
                rating = "OKAY. Broke even despite tough conditions."
                score = 2
            else:
                rating = "NEEDS IMPROVEMENT. Hard mode requires better strategy."
                score = 1
        
        result += f"\n🏆 PERFORMANCE RATING: {rating}\n"
        result += f"   Difficulty: {self.difficulty.title()} | Score: {score}/5\n"
        
        # Economic lessons learned
        result += f"\n🧠 ECONOMIC LESSONS FROM THIS GAME:\n"
        result += f"• Supply & Demand: Market prices change based on availability and desire\n"
        result += f"• Profit Maximization: Balance price per item vs. quantity sold\n"
        result += f"• Opportunity Cost: Every decision has trade-offs\n"
        result += f"• Market Adaptation: Successful businesses respond to changing conditions\n"
        
        if profitable_turns / len(self.profit_history) > 0.7:
            result += f"• You maintained profitability most turns - excellent market understanding!\n"
        elif profitable_turns / len(self.profit_history) > 0.5:
            result += f"• You were profitable over half the time - good progress!\n"
        else:
            result += f"• Focus on finding the optimal price point for consistent profits.\n"
        
        result += f"\n💡 KEY TAKEAWAYS:\n"
        result += f"• Price too high → Fewer sales, more profit per item\n"
        result += f"• Price too low → More sales, less profit per item\n"
        result += f"• Market conditions change - adapt your strategy!\n"
        result += f"• Balance inventory with expected demand\n"
        result += f"• Watch for random events that affect the market\n"
        
        result += f"\n🎮 Ready for another challenge? Click 'New Game' to try a different difficulty!\n"
        
        self.results_text.insert('1.0', result)
        
        # Final achievement check
        self.check_achievements()
        
        messagebox.showinfo("Game Over", 
                          f"Final money: ${self.money:.2f}\n\n{rating}\n\n"
                          f"Check the results panel for detailed economic analysis!")

def main():
    root = tk.Tk()
    app = EconomicsSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
