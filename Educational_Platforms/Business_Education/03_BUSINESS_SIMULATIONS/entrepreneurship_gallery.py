#!/usr/bin/env python3
"""
Entrepreneurship Project Gallery
===============================
Interactive showcase of student business projects and startup ideas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import random

class EntrepreneurshipGallery:
    """Interactive gallery for showcasing and exploring business projects."""
    
    def __init__(self):
        """Initialize the project gallery."""
        self.projects = self.load_sample_projects()
        self.current_project = None
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main gallery interface."""
        self.root = tk.Tk()
        self.root.title("🏪 Entrepreneurship Project Gallery - Student Showcase")
        self.root.geometry("1400x900")
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup tabs
        self.setup_gallery_tab()
        self.setup_project_builder_tab()
        self.setup_business_types_tab()
        self.setup_success_stories_tab()
        self.setup_resources_tab()
        
    def setup_gallery_tab(self):
        """Setup the main project gallery tab."""
        gallery_frame = ttk.Frame(self.notebook)
        self.notebook.add(gallery_frame, text="🏪 Project Gallery")
        
        # Filter controls
        filter_frame = ttk.LabelFrame(gallery_frame, text="Browse Projects")
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                     values=["All", "Technology", "Social Impact", "E-commerce", 
                                            "Food & Beverage", "Education", "Health & Fitness",
                                            "Creative Arts", "Sustainability"])
        category_combo.grid(row=0, column=1, padx=5, pady=5)
        category_combo.bind('<<ComboboxSelected>>', self.filter_projects)
        
        ttk.Label(filter_frame, text="Grade Level:").grid(row=0, column=2, padx=5, pady=5)
        self.grade_var = tk.StringVar(value="All")
        grade_combo = ttk.Combobox(filter_frame, textvariable=self.grade_var,
                                  values=["All", "Elementary (K-5)", "Middle School (6-8)", "High School (9-12)"])
        grade_combo.grid(row=0, column=3, padx=5, pady=5)
        grade_combo.bind('<<ComboboxSelected>>', self.filter_projects)
        
        ttk.Button(filter_frame, text="🎲 Random Project", 
                  command=self.show_random_project).grid(row=0, column=4, padx=10, pady=5)
        ttk.Button(filter_frame, text="⭐ Featured Projects", 
                  command=self.show_featured_projects).grid(row=0, column=5, padx=10, pady=5)
        
        # Projects display area
        display_frame = ttk.Frame(gallery_frame)
        display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Project list (left side)
        list_frame = ttk.LabelFrame(display_frame, text="Projects")
        list_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Treeview for project list
        self.project_tree = ttk.Treeview(list_frame, columns=('category', 'grade'), height=15)
        self.project_tree.heading('#0', text='Project Name')
        self.project_tree.heading('category', text='Category')
        self.project_tree.heading('grade', text='Grade')
        self.project_tree.column('#0', width=200)
        self.project_tree.column('category', width=120)
        self.project_tree.column('grade', width=100)
        
        project_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.project_tree.yview)
        self.project_tree.configure(yscrollcommand=project_scrollbar.set)
        
        self.project_tree.pack(side='left', fill='both', expand=True)
        project_scrollbar.pack(side='right', fill='y')
        
        self.project_tree.bind('<Double-1>', self.on_project_select)
        
        # Project details (right side)
        details_frame = ttk.LabelFrame(display_frame, text="Project Details")
        details_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, font=('Arial', 11))
        details_scrollbar = ttk.Scrollbar(details_frame, orient='vertical', command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        details_scrollbar.pack(side='right', fill='y')
        
        # Load initial projects
        self.populate_project_list()
        
    def setup_project_builder_tab(self):
        """Setup the project builder tab."""
        builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(builder_frame, text="🔨 Create Project")
        
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
        
        # Project basic info
        info_frame = ttk.LabelFrame(scrollable_frame, text="Project Information")
        info_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(info_frame, text="Project Name:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.project_name_entry = ttk.Entry(info_frame, width=40)
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=2, columnspan=2)
        
        ttk.Label(info_frame, text="Creator Name:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.creator_name_entry = ttk.Entry(info_frame, width=40)
        self.creator_name_entry.grid(row=1, column=1, padx=5, pady=2, columnspan=2)
        
        ttk.Label(info_frame, text="Category:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.project_category = ttk.Combobox(info_frame, width=37,
                                           values=["Technology", "Social Impact", "E-commerce", 
                                                  "Food & Beverage", "Education", "Health & Fitness",
                                                  "Creative Arts", "Sustainability"])
        self.project_category.grid(row=2, column=1, padx=5, pady=2, columnspan=2)
        
        ttk.Label(info_frame, text="Grade Level:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.project_grade = ttk.Combobox(info_frame, width=37,
                                         values=["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)"])
        self.project_grade.grid(row=3, column=1, padx=5, pady=2, columnspan=2)
        
        # Business description
        desc_frame = ttk.LabelFrame(scrollable_frame, text="Business Description")
        desc_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(desc_frame, text="What problem does your business solve?").pack(anchor='w', padx=5)
        self.problem_text = tk.Text(desc_frame, height=3, wrap=tk.WORD)
        self.problem_text.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(desc_frame, text="What is your solution?").pack(anchor='w', padx=5)
        self.solution_text = tk.Text(desc_frame, height=3, wrap=tk.WORD)
        self.solution_text.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(desc_frame, text="Who are your customers?").pack(anchor='w', padx=5)
        self.customers_text = tk.Text(desc_frame, height=2, wrap=tk.WORD)
        self.customers_text.pack(fill='x', padx=5, pady=5)
        
        # Business model
        model_frame = ttk.LabelFrame(scrollable_frame, text="Business Model")
        model_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(model_frame, text="How will you make money?").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.revenue_entry = ttk.Entry(model_frame, width=50)
        self.revenue_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(model_frame, text="What are your main costs?").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.costs_entry = ttk.Entry(model_frame, width=50)
        self.costs_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(model_frame, text="Expected monthly revenue:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.monthly_revenue_entry = ttk.Entry(model_frame, width=50)
        self.monthly_revenue_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Marketing and competition
        marketing_frame = ttk.LabelFrame(scrollable_frame, text="Marketing & Competition")
        marketing_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(marketing_frame, text="How will you reach customers?").pack(anchor='w', padx=5)
        self.marketing_text = tk.Text(marketing_frame, height=2, wrap=tk.WORD)
        self.marketing_text.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(marketing_frame, text="What makes you different from competitors?").pack(anchor='w', padx=5)
        self.advantage_text = tk.Text(marketing_frame, height=2, wrap=tk.WORD)
        self.advantage_text.pack(fill='x', padx=5, pady=5)
        
        # Implementation plan
        implementation_frame = ttk.LabelFrame(scrollable_frame, text="Implementation Plan")
        implementation_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(implementation_frame, text="What do you need to get started?").pack(anchor='w', padx=5)
        self.startup_needs_text = tk.Text(implementation_frame, height=2, wrap=tk.WORD)
        self.startup_needs_text.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(implementation_frame, text="What challenges do you expect?").pack(anchor='w', padx=5)
        self.challenges_text = tk.Text(implementation_frame, height=2, wrap=tk.WORD)
        self.challenges_text.pack(fill='x', padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(button_frame, text="💾 Save Project", 
                  command=self.save_project).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎲 Generate Idea", 
                  command=self.generate_business_idea).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📋 Load Template", 
                  command=self.load_project_template).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔍 Validate Idea", 
                  command=self.validate_business_idea).pack(side='left', padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_business_types_tab(self):
        """Setup the business types exploration tab."""
        types_frame = ttk.Frame(self.notebook)
        self.notebook.add(types_frame, text="🏢 Business Types")
        
        # Business type selector
        selector_frame = ttk.LabelFrame(types_frame, text="Explore Business Types")
        selector_frame.pack(fill='x', padx=5, pady=5)
        
        business_types = [
            "Product-Based Business", "Service-Based Business", "Digital/Online Business",
            "Subscription Business", "Marketplace Business", "Social Enterprise",
            "Franchise Business", "B2B Business", "B2C Business"
        ]
        
        self.business_type_var = tk.StringVar(value="Product-Based Business")
        type_combo = ttk.Combobox(selector_frame, textvariable=self.business_type_var,
                                 values=business_types, width=30)
        type_combo.pack(side='left', padx=5, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.show_business_type_info)
        
        ttk.Button(selector_frame, text="📊 Compare Types", 
                  command=self.compare_business_types).pack(side='left', padx=10, pady=5)
        
        # Business type information display
        info_frame = ttk.LabelFrame(types_frame, text="Business Type Information")
        info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.type_info_text = tk.Text(info_frame, wrap=tk.WORD, font=('Arial', 11))
        type_info_scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.type_info_text.yview)
        self.type_info_text.configure(yscrollcommand=type_info_scrollbar.set)
        
        self.type_info_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        type_info_scrollbar.pack(side='right', fill='y')
        
        # Load initial business type info
        self.show_business_type_info()
        
    def setup_success_stories_tab(self):
        """Setup the success stories tab."""
        stories_frame = ttk.Frame(self.notebook)
        self.notebook.add(stories_frame, text="⭐ Success Stories")
        
        # Story selector
        selector_frame = ttk.LabelFrame(stories_frame, text="Young Entrepreneur Success Stories")
        selector_frame.pack(fill='x', padx=5, pady=5)
        
        success_stories = [
            "Mikaila Ulmer (Me & the Bees Lemonade)",
            "Ryan Kaji (Ryan's World)",
            "Moziah Bridges (Mo's Bows)",
            "Rachel Roy (Rachel Roy Brand)",
            "Ben Pasternak (Flogg App)",
            "Maya Penn (Maya's Ideas)",
            "Hart Main (ManCans)",
            "Madison Robinson (Fish Flops)"
        ]
        
        self.story_var = tk.StringVar(value=success_stories[0])
        story_combo = ttk.Combobox(selector_frame, textvariable=self.story_var,
                                  values=success_stories, width=40)
        story_combo.pack(side='left', padx=5, pady=5)
        story_combo.bind('<<ComboboxSelected>>', self.show_success_story)
        
        ttk.Button(selector_frame, text="🎲 Random Story", 
                  command=self.show_random_success_story).pack(side='left', padx=10, pady=5)
        
        # Success story display
        story_display_frame = ttk.LabelFrame(stories_frame, text="Success Story")
        story_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.success_story_text = tk.Text(story_display_frame, wrap=tk.WORD, font=('Arial', 11))
        story_scrollbar = ttk.Scrollbar(story_display_frame, orient='vertical', command=self.success_story_text.yview)
        self.success_story_text.configure(yscrollcommand=story_scrollbar.set)
        
        self.success_story_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        story_scrollbar.pack(side='right', fill='y')
        
        # Load initial success story
        self.show_success_story()
        
        # Inspiration buttons
        inspiration_frame = ttk.Frame(stories_frame)
        inspiration_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(inspiration_frame, text="💡 Key Lessons", 
                  command=self.show_key_lessons).pack(side='left', padx=5)
        ttk.Button(inspiration_frame, text="🎯 Action Steps", 
                  command=self.show_action_steps).pack(side='left', padx=5)
        ttk.Button(inspiration_frame, text="📚 More Resources", 
                  command=self.show_more_resources).pack(side='left', padx=5)
        
    def setup_resources_tab(self):
        """Setup the resources and tools tab."""
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="🛠️ Tools & Resources")
        
        # Resource categories
        category_frame = ttk.LabelFrame(resources_frame, text="Resource Categories")
        category_frame.pack(fill='x', padx=5, pady=5)
        
        resource_categories = [
            "Business Planning Templates", "Market Research Tools", "Financial Planning",
            "Marketing Resources", "Legal & Compliance", "Online Tools", "Books & Learning",
            "Competitions & Programs"
        ]
        
        self.resource_category_var = tk.StringVar(value=resource_categories[0])
        resource_combo = ttk.Combobox(category_frame, textvariable=self.resource_category_var,
                                     values=resource_categories, width=30)
        resource_combo.pack(side='left', padx=5, pady=5)
        resource_combo.bind('<<ComboboxSelected>>', self.show_resource_category)
        
        # Resource display
        resource_display_frame = ttk.LabelFrame(resources_frame, text="Resources")
        resource_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.resources_display_text = tk.Text(resource_display_frame, wrap=tk.WORD, font=('Arial', 11))
        resource_display_scrollbar = ttk.Scrollbar(resource_display_frame, orient='vertical', command=self.resources_display_text.yview)
        self.resources_display_text.configure(yscrollcommand=resource_display_scrollbar.set)
        
        self.resources_display_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        resource_display_scrollbar.pack(side='right', fill='y')
        
        # Load initial resources
        self.show_resource_category()
    
    def load_sample_projects(self):
        """Load sample student projects for the gallery."""
        return [
            {
                'name': 'EcoLunch Boxes',
                'creator': 'Sarah Chen (Grade 7)',
                'category': 'Sustainability',
                'grade': 'Middle School (6-8)',
                'problem': 'Students use too many disposable lunch containers, creating waste',
                'solution': 'Reusable, compartmentalized lunch boxes made from recycled materials',
                'customers': 'Students, parents, schools concerned about environmental impact',
                'revenue_model': 'Direct sales online and through school partnerships',
                'costs': 'Materials, manufacturing, shipping, marketing',
                'monthly_revenue': '$2,500',
                'marketing': 'Social media campaigns, school presentations, parent networks',
                'advantage': 'Stylish design, perfect size for school lunches, eco-friendly message',
                'startup_needs': 'Initial inventory, website, social media presence',
                'challenges': 'Competition from existing lunch box companies, building brand awareness',
                'featured': True
            },
            {
                'name': 'CodeBuddy Tutoring',
                'creator': 'Marcus Johnson (Grade 11)',
                'category': 'Education',
                'grade': 'High School (9-12)',
                'problem': 'Many students struggle with programming but expensive tutoring is not accessible',
                'solution': 'Affordable online coding tutoring with peer mentors',
                'customers': 'Middle and high school students learning to code',
                'revenue_model': 'Hourly tutoring fees, subscription packages',
                'costs': 'Platform development, tutor payments, marketing',
                'monthly_revenue': '$3,200',
                'marketing': 'School computer science clubs, online coding communities',
                'advantage': 'Peer-to-peer learning, affordable pricing, flexible scheduling',
                'startup_needs': 'Tutoring platform, initial group of tutors, curriculum materials',
                'challenges': 'Quality control of tutors, scaling operations',
                'featured': True
            },
            {
                'name': 'Pet Care Helpers',
                'creator': 'Emma Rodriguez (Grade 5)',
                'category': 'Social Impact',
                'grade': 'Elementary (K-5)',
                'problem': 'Neighbors need help caring for pets when they travel or work long hours',
                'solution': 'Neighborhood pet sitting and dog walking service',
                'customers': 'Local pet owners who need reliable pet care',
                'revenue_model': 'Per-visit or per-hour fees for pet care services',
                'costs': 'Insurance, supplies, transportation',
                'monthly_revenue': '$800',
                'marketing': 'Neighborhood flyers, word-of-mouth, local social media groups',
                'advantage': 'Personal touch, local trust, flexible service options',
                'startup_needs': 'Insurance, basic pet care supplies, neighborhood network',
                'challenges': 'Building trust with pet owners, managing scheduling',
                'featured': False
            },
            {
                'name': 'Study Snack Delivery',
                'creator': 'Alex Kim & Jordan Smith (Grade 9)',
                'category': 'Food & Beverage',
                'grade': 'High School (9-12)',
                'problem': 'Students get hungry during late study sessions but healthy options are limited',
                'solution': 'Delivery service for healthy study snacks to students',
                'customers': 'High school and college students during exam periods',
                'revenue_model': 'Delivery fees plus markup on healthy snacks',
                'costs': 'Food inventory, delivery costs, packaging',
                'monthly_revenue': '$1,500',
                'marketing': 'Campus partnerships, study group networks, social media',
                'advantage': 'Focused on healthy options, convenient timing, student-friendly pricing',
                'startup_needs': 'Supplier relationships, delivery system, food safety permits',
                'challenges': 'Seasonal demand, food safety compliance, logistics',
                'featured': False
            },
            {
                'name': 'Virtual Art Classes',
                'creator': 'Maya Patel (Grade 10)',
                'category': 'Creative Arts',
                'grade': 'High School (9-12)',
                'problem': 'Many students want to learn art but cannot access quality instruction',
                'solution': 'Online art classes with personalized feedback and community',
                'customers': 'Students interested in developing artistic skills',
                'revenue_model': 'Monthly subscription for access to classes and community',
                'costs': 'Video production, platform hosting, instructor payments',
                'monthly_revenue': '$2,100',
                'marketing': 'Art communities online, school art programs, social media showcases',
                'advantage': 'Personalized feedback, flexible scheduling, community aspect',
                'startup_needs': 'Video equipment, online platform, initial course content',
                'challenges': 'Creating engaging online content, building instructor network',
                'featured': True
            }
        ]
    
    def populate_project_list(self):
        """Populate the project list tree view."""
        # Clear existing items
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        
        # Add projects based on current filters
        for project in self.projects:
            if (self.category_var.get() == "All" or project['category'] == self.category_var.get()) and \
               (self.grade_var.get() == "All" or project['grade'] == self.grade_var.get()):
                
                icon = "⭐" if project.get('featured', False) else "📁"
                self.project_tree.insert('', 'end', text=f"{icon} {project['name']}", 
                                       values=(project['category'], project['grade']),
                                       tags=(project['name'],))
    
    def filter_projects(self, event=None):
        """Filter projects based on selected criteria."""
        self.populate_project_list()
    
    def on_project_select(self, event=None):
        """Handle project selection in the tree view."""
        selection = self.project_tree.selection()
        if selection:
            item = self.project_tree.item(selection[0])
            project_name = item['text'].replace("⭐ ", "").replace("📁 ", "")
            
            # Find the selected project
            for project in self.projects:
                if project['name'] == project_name:
                    self.show_project_details(project)
                    break
    
    def show_project_details(self, project):
        """Display detailed information about a project."""
        details = f"""
🏪 {project['name'].upper()}
{'='*60}

👤 CREATOR: {project['creator']}
🏷️ CATEGORY: {project['category']}
🎓 GRADE LEVEL: {project['grade']}
{'⭐ FEATURED PROJECT' if project.get('featured', False) else ''}

🎯 THE PROBLEM:
{project['problem']}

💡 THE SOLUTION:
{project['solution']}

👥 TARGET CUSTOMERS:
{project['customers']}

💰 BUSINESS MODEL:
Revenue: {project['revenue_model']}
Main Costs: {project['costs']}
Expected Monthly Revenue: {project['monthly_revenue']}

📢 MARKETING STRATEGY:
{project['marketing']}

🏆 COMPETITIVE ADVANTAGE:
{project['advantage']}

🚀 STARTUP REQUIREMENTS:
{project['startup_needs']}

⚠️ EXPECTED CHALLENGES:
{project['challenges']}

💡 LESSONS FOR OTHER ENTREPRENEURS:
• Start with a problem you personally experience
• Validate your idea by talking to potential customers
• Start small and test your concept before big investments
• Build relationships in your community or school
• Don't be afraid to adapt your idea based on feedback
• Focus on providing real value to your customers

🎯 NEXT STEPS TO DEVELOP SIMILAR BUSINESS:
1. Research the market in your area
2. Create a simple business plan
3. Start with a small pilot test
4. Get feedback from potential customers
5. Refine your offering based on feedback
6. Develop a marketing strategy
7. Consider legal requirements (permits, insurance)
8. Launch and continuously improve

Remember: Every successful entrepreneur started with just an idea!
        """
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def run(self):
        """Start the entrepreneurship gallery application."""
        self.root.mainloop()

def main():
    """Main function to run the entrepreneurship gallery."""
    print("🏪 Entrepreneurship Project Gallery")
    print("=" * 35)
    print("📚 Explore student business projects and ideas")
    print("💡 Get inspired to start your own venture")
    print()
    print("Starting Project Gallery...")
    
    gallery = EntrepreneurshipGallery()
    gallery.run()

if __name__ == "__main__":
    main()