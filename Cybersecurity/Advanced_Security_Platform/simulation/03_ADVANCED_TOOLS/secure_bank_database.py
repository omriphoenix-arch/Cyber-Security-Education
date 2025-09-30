#!/usr/bin/env python3
"""
SecureBank Database System
=========================
A realistic banking website database with comprehensive security features
and one critical vulnerability for educational purposes.

Features:
- User accounts with encrypted data
- Transaction logging
- Admin panel with authentication
- Session management
- Input validation
- SQL injection protection (mostly...)
- Audit trails
- Rate limiting

THE FLAW: SQL injection vulnerability in the search function
"""

import sqlite3
import hashlib
import secrets
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
import os

class SecureBankDatabase:
    """
    A comprehensive banking database system with advanced security features.
    
    Security Features:
    ✅ Password hashing with salt
    ✅ Session management
    ✅ Input validation (mostly)
    ✅ Rate limiting
    ✅ Transaction logging
    ✅ Audit trails
    ❌ SQL injection vulnerability in search function
    """
    
    def __init__(self, db_file: str = "securebank.db"):
        self.db_file = db_file
        self.sessions = {}
        self.failed_attempts = {}
        self.audit_log = []
        self.rate_limits = {}
        self.lock = threading.Lock()
        
        # Security configuration
        self.MAX_LOGIN_ATTEMPTS = 5
        self.SESSION_TIMEOUT = 1800  # 30 minutes
        self.RATE_LIMIT_WINDOW = 300  # 5 minutes
        self.MAX_REQUESTS_PER_WINDOW = 50
        
        self._initialize_database()
        self._populate_sample_data()
        
        print("🏦 SecureBank Database System v2.0 Initialized")
        print("🔒 Advanced security features enabled")
        print(f"📊 Database: {db_file}")
    
    def _initialize_database(self):
        """Initialize the database with secure schema."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Users table with encrypted sensitive data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(256) NOT NULL,
                salt VARCHAR(64) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                account_number VARCHAR(20) UNIQUE NOT NULL,
                balance DECIMAL(15,2) DEFAULT 0.00,
                account_type VARCHAR(20) DEFAULT 'checking',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                failed_login_count INTEGER DEFAULT 0,
                locked_until TIMESTAMP
            )
        """)
        
        # Transactions table for financial records
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account VARCHAR(20),
                to_account VARCHAR(20),
                amount DECIMAL(15,2) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'completed',
                reference_number VARCHAR(50) UNIQUE,
                ip_address VARCHAR(45),
                user_agent TEXT
            )
        """)
        
        # Admin logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_user VARCHAR(50),
                action VARCHAR(100),
                target_user VARCHAR(50),
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45)
            )
        """)
        
        # Security events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type VARCHAR(50),
                username VARCHAR(50),
                ip_address VARCHAR(45),
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                severity VARCHAR(20) DEFAULT 'info'
            )
        """)
        
        # Customer support tickets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject VARCHAR(200),
                message TEXT,
                status VARCHAR(20) DEFAULT 'open',
                priority VARCHAR(20) DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assigned_to VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _populate_sample_data(self):
        """Populate database with realistic sample data."""
        # Check if data already exists
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample users with various account types and balances
        sample_users = [
            {
                'username': 'john_doe',
                'email': 'john.doe@email.com',
                'password': 'SecurePass123!',
                'full_name': 'John Doe',
                'phone': '555-0101',
                'address': '123 Main St, Anytown, USA',
                'balance': 15420.50,
                'account_type': 'checking'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@email.com',
                'password': 'MyPassword456!',
                'full_name': 'Jane Smith',
                'phone': '555-0102',
                'address': '456 Oak Ave, Somewhere, USA',
                'balance': 8734.25,
                'account_type': 'savings'
            },
            {
                'username': 'mike_wilson',
                'email': 'mike.wilson@email.com',
                'password': 'BankingSecure789!',
                'full_name': 'Michael Wilson',
                'phone': '555-0103',
                'address': '789 Pine Dr, Elsewhere, USA',
                'balance': 125000.00,
                'account_type': 'premium'
            },
            {
                'username': 'admin',
                'email': 'admin@securebank.com',
                'password': 'AdminSecure2024!',
                'full_name': 'System Administrator',
                'phone': '555-0000',
                'address': 'SecureBank HQ',
                'balance': 0.00,
                'account_type': 'admin',
                'is_admin': True
            },
            {
                'username': 'sarah_davis',
                'email': 'sarah.davis@email.com',
                'password': 'Financial2024!',
                'full_name': 'Sarah Davis',
                'phone': '555-0104',
                'address': '321 Elm St, Newtown, USA',
                'balance': 45600.75,
                'account_type': 'business'
            }
        ]
        
        for user_data in sample_users:
            self.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                initial_balance=user_data['balance'],
                account_type=user_data['account_type'],
                is_admin=user_data.get('is_admin', False)
            )
        
        # Add sample transactions
        sample_transactions = [
            ('ACC001', 'ACC002', 500.00, 'transfer', 'Rent payment'),
            ('ACC002', 'ACC003', 1200.00, 'transfer', 'Business payment'),
            ('ACC001', None, 200.00, 'withdrawal', 'ATM withdrawal'),
            (None, 'ACC001', 1500.00, 'deposit', 'Salary deposit'),
            ('ACC003', 'ACC001', 300.00, 'transfer', 'Refund payment'),
        ]
        
        for transaction in sample_transactions:
            self._add_transaction(*transaction)
        
        conn.close()
        print("✅ Sample data populated successfully")
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Secure password hashing with salt."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _generate_salt(self) -> str:
        """Generate cryptographically secure salt."""
        return secrets.token_hex(32)
    
    def _generate_account_number(self) -> str:
        """Generate unique account number."""
        return f"ACC{secrets.randbelow(999999):06d}"
    
    def _generate_reference_number(self) -> str:
        """Generate unique transaction reference."""
        return f"TXN{secrets.randbelow(9999999999):010d}"
    
    def _log_security_event(self, event_type: str, username: str = None, 
                          details: str = "", severity: str = "info", ip: str = "127.0.0.1"):
        """Log security events for monitoring."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO security_events (event_type, username, ip_address, details, severity)
            VALUES (?, ?, ?, ?, ?)
        """, (event_type, username, ip, details, severity))
        
        conn.commit()
        conn.close()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔍 [{timestamp}] {event_type}: {details}")
    
    def _check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limits."""
        current_time = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Clean old requests
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if current_time - req_time < self.RATE_LIMIT_WINDOW
        ]
        
        if len(self.rate_limits[identifier]) >= self.MAX_REQUESTS_PER_WINDOW:
            return False
        
        self.rate_limits[identifier].append(current_time)
        return True
    
    def _validate_input(self, input_str: str, input_type: str = "general") -> bool:
        """Validate input to prevent injection attacks."""
        if not isinstance(input_str, str):
            return False
        
        # General dangerous patterns
        dangerous_patterns = [
            r"[<>\"'&;(){}]",  # HTML/Script injection
            r"\\x[0-9a-fA-F]{2}",  # Hex encoding
            r"(union|select|insert|update|delete|drop|create|alter)",  # SQL keywords (some protection)
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                return False
        
        # Type-specific validation
        if input_type == "username":
            return bool(re.match(r"^[a-zA-Z0-9_-]{3,50}$", input_str))
        elif input_type == "email":
            return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", input_str))
        elif input_type == "account":
            return bool(re.match(r"^ACC[0-9]{6}$", input_str))
        
        return True
    
    def create_user(self, username: str, email: str, password: str, full_name: str,
                   phone: str = "", address: str = "", initial_balance: float = 0.0,
                   account_type: str = "checking", is_admin: bool = False) -> Tuple[bool, str]:
        """Create a new user account with validation."""
        try:
            # Input validation
            if not self._validate_input(username, "username"):
                return False, "Invalid username format"
            
            if not self._validate_input(email, "email"):
                return False, "Invalid email format"
            
            if len(password) < 8:
                return False, "Password must be at least 8 characters"
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if username or email exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists"
            
            # Generate secure credentials
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)
            account_number = self._generate_account_number()
            
            # Insert user
            cursor.execute("""
                INSERT INTO users 
                (username, email, password_hash, salt, full_name, phone, address, 
                 account_number, balance, account_type, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, salt, full_name, phone, address,
                  account_number, initial_balance, account_type, is_admin))
            
            conn.commit()
            conn.close()
            
            self._log_security_event("USER_CREATED", username, f"New user account created: {account_number}")
            return True, f"Account created successfully. Account number: {account_number}"
            
        except Exception as e:
            self._log_security_event("USER_CREATION_ERROR", username, f"Error: {e}", "error")
            return False, f"Account creation failed: {e}"
    
    def authenticate_user(self, username: str, password: str, ip: str = "127.0.0.1") -> Tuple[bool, str, Optional[str]]:
        """Authenticate user with comprehensive security checks."""
        try:
            # Rate limiting
            if not self._check_rate_limit(f"login_{ip}"):
                self._log_security_event("RATE_LIMIT_EXCEEDED", username, f"Rate limit exceeded from {ip}", "warning", ip)
                return False, "Too many login attempts. Please try again later.", None
            
            # Input validation
            if not self._validate_input(username, "username"):
                self._log_security_event("INVALID_LOGIN_INPUT", username, f"Invalid username format from {ip}", "warning", ip)
                return False, "Invalid credentials", None
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get user data
            cursor.execute("""
                SELECT id, username, password_hash, salt, is_active, locked_until, failed_login_count
                FROM users WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            if not user:
                self._log_security_event("LOGIN_FAILED", username, f"User not found from {ip}", "warning", ip)
                conn.close()
                return False, "Invalid credentials", None
            
            user_id, db_username, stored_hash, salt, is_active, locked_until, failed_count = user
            
            # Check if account is locked
            if locked_until and datetime.fromisoformat(locked_until) > datetime.now():
                self._log_security_event("LOCKED_ACCOUNT_ACCESS", username, f"Access to locked account from {ip}", "warning", ip)
                conn.close()
                return False, "Account is temporarily locked", None
            
            # Check if account is active
            if not is_active:
                self._log_security_event("INACTIVE_ACCOUNT_ACCESS", username, f"Access to inactive account from {ip}", "warning", ip)
                conn.close()
                return False, "Account is deactivated", None
            
            # Verify password
            provided_hash = self._hash_password(password, salt)
            if secrets.compare_digest(provided_hash, stored_hash):
                # Successful login
                session_token = secrets.token_urlsafe(64)
                self.sessions[session_token] = {
                    'user_id': user_id,
                    'username': username,
                    'created_at': time.time(),
                    'last_activity': time.time(),
                    'ip_address': ip
                }
                
                # Update user login info
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP, failed_login_count = 0, locked_until = NULL
                    WHERE username = ?
                """, (username,))
                
                conn.commit()
                conn.close()
                
                self._log_security_event("LOGIN_SUCCESS", username, f"Successful login from {ip}", "info", ip)
                return True, "Login successful", session_token
            else:
                # Failed login
                failed_count += 1
                locked_until = None
                
                if failed_count >= self.MAX_LOGIN_ATTEMPTS:
                    locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
                    self._log_security_event("ACCOUNT_LOCKED", username, f"Account locked after {failed_count} failed attempts from {ip}", "error", ip)
                
                cursor.execute("""
                    UPDATE users SET failed_login_count = ?, locked_until = ?
                    WHERE username = ?
                """, (failed_count, locked_until, username))
                
                conn.commit()
                conn.close()
                
                self._log_security_event("LOGIN_FAILED", username, f"Failed login attempt #{failed_count} from {ip}", "warning", ip)
                return False, "Invalid credentials", None
                
        except Exception as e:
            self._log_security_event("LOGIN_ERROR", username, f"Login error: {e}", "error", ip)
            return False, "Login system error", None
    
    def validate_session(self, session_token: str) -> Tuple[bool, Optional[Dict]]:
        """Validate session token and return user info."""
        if not session_token or session_token not in self.sessions:
            return False, None
        
        session = self.sessions[session_token]
        current_time = time.time()
        
        # Check timeout
        if current_time - session['last_activity'] > self.SESSION_TIMEOUT:
            del self.sessions[session_token]
            self._log_security_event("SESSION_EXPIRED", session['username'], "Session expired")
            return False, None
        
        # Update activity
        session['last_activity'] = current_time
        return True, session
    
    def search_transactions(self, session_token: str, search_term: str) -> Tuple[bool, str, List]:
        """
        Search transactions - THIS CONTAINS THE SQL INJECTION VULNERABILITY!
        
        The vulnerability is here: Direct string concatenation instead of parameterized queries
        """
        # Validate session
        valid, session = self.validate_session(session_token)
        if not valid:
            return False, "Invalid session", []
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get user's account number
            cursor.execute("SELECT account_number FROM users WHERE id = ?", (session['user_id'],))
            account = cursor.fetchone()
            if not account:
                conn.close()
                return False, "User account not found", []
            
            account_number = account[0]
            
            # THE VULNERABILITY IS HERE! 
            # Using string concatenation instead of parameterized queries
            # This allows SQL injection attacks!
            query = f"""
                SELECT id, from_account, to_account, amount, transaction_type, 
                       description, timestamp, reference_number
                FROM transactions 
                WHERE (from_account = '{account_number}' OR to_account = '{account_number}')
                AND (description LIKE '%{search_term}%' OR reference_number LIKE '%{search_term}%')
                ORDER BY timestamp DESC
                LIMIT 50
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            conn.close()
            
            self._log_security_event("TRANSACTION_SEARCH", session['username'], 
                                   f"Searched transactions with term: {search_term}")
            
            return True, "Search completed", results
            
        except Exception as e:
            self._log_security_event("SEARCH_ERROR", session.get('username', 'unknown'), 
                                   f"Transaction search error: {e}", "error")
            return False, f"Search error: {e}", []
    
    def get_user_profile(self, session_token: str) -> Tuple[bool, str, Optional[Dict]]:
        """Get user profile information."""
        valid, session = self.validate_session(session_token)
        if not valid:
            return False, "Invalid session", None
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, email, full_name, phone, address, account_number, 
                       balance, account_type, created_at, last_login
                FROM users WHERE id = ?
            """, (session['user_id'],))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                profile = {
                    'username': user[0],
                    'email': user[1],
                    'full_name': user[2],
                    'phone': user[3],
                    'address': user[4],
                    'account_number': user[5],
                    'balance': user[6],
                    'account_type': user[7],
                    'created_at': user[8],
                    'last_login': user[9]
                }
                return True, "Profile retrieved", profile
            else:
                return False, "User not found", None
                
        except Exception as e:
            self._log_security_event("PROFILE_ERROR", session.get('username', 'unknown'), 
                                   f"Profile retrieval error: {e}", "error")
            return False, f"Profile error: {e}", None
    
    def _add_transaction(self, from_account: str, to_account: str, amount: float, 
                       transaction_type: str, description: str, ip: str = "127.0.0.1"):
        """Add a transaction record."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        reference = self._generate_reference_number()
        
        cursor.execute("""
            INSERT INTO transactions 
            (from_account, to_account, amount, transaction_type, description, reference_number, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (from_account, to_account, amount, transaction_type, description, reference, ip))
        
        conn.commit()
        conn.close()
    
    def get_all_users_admin(self, session_token: str) -> Tuple[bool, str, List]:
        """Admin function to get all users - requires admin privileges."""
        valid, session = self.validate_session(session_token)
        if not valid:
            return False, "Invalid session", []
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Check if user is admin
            cursor.execute("SELECT is_admin FROM users WHERE id = ?", (session['user_id'],))
            admin_check = cursor.fetchone()
            
            if not admin_check or not admin_check[0]:
                self._log_security_event("UNAUTHORIZED_ADMIN_ACCESS", session['username'], 
                                       "Attempted admin function without privileges", "warning")
                conn.close()
                return False, "Insufficient privileges", []
            
            # Get all users
            cursor.execute("""
                SELECT id, username, email, full_name, account_number, balance, 
                       account_type, created_at, last_login, is_active
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = cursor.fetchall()
            conn.close()
            
            self._log_security_event("ADMIN_USER_LIST", session['username'], "Admin accessed user list")
            return True, "Users retrieved", users
            
        except Exception as e:
            self._log_security_event("ADMIN_ERROR", session.get('username', 'unknown'), 
                                   f"Admin function error: {e}", "error")
            return False, f"Admin error: {e}", []
    
    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session."""
        if session_token in self.sessions:
            username = self.sessions[session_token]['username']
            del self.sessions[session_token]
            self._log_security_event("LOGOUT", username, "User logged out")
            return True
        return False
    
    def get_security_report(self) -> Dict:
        """Generate security monitoring report."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Recent security events
            cursor.execute("""
                SELECT event_type, COUNT(*) as count
                FROM security_events 
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY event_type
            """)
            recent_events = dict(cursor.fetchall())
            
            # Failed login attempts
            cursor.execute("""
                SELECT COUNT(*) FROM security_events 
                WHERE event_type = 'LOGIN_FAILED' 
                AND timestamp > datetime('now', '-1 hour')
            """)
            recent_failed_logins = cursor.fetchone()[0]
            
            # Active sessions
            active_sessions = len(self.sessions)
            
            # Locked accounts
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE locked_until > datetime('now')
            """)
            locked_accounts = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'recent_events': recent_events,
                'recent_failed_logins': recent_failed_logins,
                'active_sessions': active_sessions,
                'locked_accounts': locked_accounts,
                'system_status': 'ALERT' if recent_failed_logins > 10 else 'NORMAL'
            }
            
        except Exception as e:
            return {'error': f"Report generation failed: {e}"}


def main():
    """Interactive demo of the SecureBank database system."""
    print("=" * 70)
    print("🏦 SECUREBANK DATABASE SYSTEM - INTERACTIVE DEMO")
    print("=" * 70)
    print("⚠️  This system contains a SQL injection vulnerability for educational purposes!")
    print("=" * 70)
    
    # Initialize database
    db = SecureBankDatabase("demo_bank.db")
    
    print("\n🎯 Available Demo Accounts:")
    print("   Username: john_doe     | Password: SecurePass123!")
    print("   Username: jane_smith   | Password: MyPassword456!")
    print("   Username: admin        | Password: AdminSecure2024!")
    
    while True:
        print("\n" + "="*50)
        print("🏦 SECUREBANK MAIN MENU")
        print("="*50)
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. View Security Report")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            user_interface(db)
        elif choice == "2":
            admin_interface(db)
        elif choice == "3":
            show_security_report(db)
        elif choice == "4":
            print("👋 Thank you for using SecureBank!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def user_interface(db):
    """User interface for banking operations."""
    print("\n🔐 USER LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    success, message, token = db.authenticate_user(username, password)
    print(f"🔑 {message}")
    
    if not success or not token:
        return
    
    while True:
        print("\n" + "="*40)
        print("👤 USER DASHBOARD")
        print("="*40)
        print("1. View Profile")
        print("2. Search Transactions")
        print("3. Logout")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            success, message, profile = db.get_user_profile(token)
            if success and profile:
                print(f"\n👤 Profile Information:")
                print(f"   Name: {profile['full_name']}")
                print(f"   Account: {profile['account_number']}")
                print(f"   Balance: ${profile['balance']:,.2f}")
                print(f"   Type: {profile['account_type']}")
            else:
                print(f"❌ {message}")
                
        elif choice == "2":
            search_term = input("Enter search term for transactions: ").strip()
            success, message, results = db.search_transactions(token, search_term)
            
            if success:
                print(f"\n📊 Transaction Results ({len(results)} found):")
                for result in results:
                    print(f"   {result[6]} | {result[4]} | ${result[3]:.2f} | {result[5]}")
            else:
                print(f"❌ {message}")
                
        elif choice == "3":
            db.logout(token)
            print("👋 Logged out successfully!")
            break
        else:
            print("❌ Invalid choice.")

def admin_interface(db):
    """Admin interface with enhanced privileges."""
    print("\n🔐 ADMIN LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    success, message, token = db.authenticate_user(username, password)
    print(f"🔑 {message}")
    
    if not success or not token:
        return
    
    while True:
        print("\n" + "="*40)
        print("⚙️  ADMIN DASHBOARD")
        print("="*40)
        print("1. View All Users")
        print("2. Security Report")
        print("3. Logout")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            success, message, users = db.get_all_users_admin(token)
            if success:
                print(f"\n👥 All Users ({len(users)} found):")
                for user in users:
                    status = "🟢 Active" if user[9] else "🔴 Inactive"
                    print(f"   {user[1]} | {user[2]} | {user[4]} | ${user[5]:,.2f} | {status}")
            else:
                print(f"❌ {message}")
                
        elif choice == "2":
            show_security_report(db)
            
        elif choice == "3":
            db.logout(token)
            print("👋 Logged out successfully!")
            break
        else:
            print("❌ Invalid choice.")

def show_security_report(db):
    """Display security monitoring report."""
    report = db.get_security_report()
    
    print("\n🛡️  SECURITY REPORT")
    print("="*40)
    print(f"System Status: {report.get('system_status', 'UNKNOWN')}")
    print(f"Active Sessions: {report.get('active_sessions', 0)}")
    print(f"Locked Accounts: {report.get('locked_accounts', 0)}")
    print(f"Recent Failed Logins: {report.get('recent_failed_logins', 0)}")
    
    print("\nRecent Events (24h):")
    events = report.get('recent_events', {})
    for event_type, count in events.items():
        print(f"   {event_type}: {count}")

if __name__ == "__main__":
    main()