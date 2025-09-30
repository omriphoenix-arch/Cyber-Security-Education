#!/usr/bin/env python3
"""
Secure User Authentication System
==================================
A robust authentication system with password hashing, session management,
and comprehensive security features.

Author: Security Team
Version: 2.1.0
"""

import hashlib
import secrets
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List

class SecureUserAuth:
    """
    A comprehensive user authentication system with advanced security features.
    
    Features:
    - Bcrypt-style password hashing with salt
    - Session management with secure tokens
    - Rate limiting for brute force protection
    - Account lockout mechanisms
    - Audit logging for security events
    - Input validation and sanitization
    """
    
    def __init__(self, db_file: str = "users.json"):
        self.db_file = db_file
        self.users: Dict = self._load_users()
        self.sessions: Dict = {}
        self.failed_attempts: Dict = {}
        self.locked_accounts: Dict = {}
        self.audit_log: List = []
        
        # Security configuration
        self.MAX_FAILED_ATTEMPTS = 5
        self.LOCKOUT_DURATION = 1800  # 30 minutes
        self.SESSION_TIMEOUT = 3600   # 1 hour
        self.MIN_PASSWORD_LENGTH = 8
        self.RATE_LIMIT_WINDOW = 60   # 1 minute
        self.MAX_REQUESTS_PER_MINUTE = 10
        
        print("🔐 SecureAuth System v2.1.0 Initialized")
        print("✅ Advanced security features enabled")
    
    def _load_users(self) -> Dict:
        """Load user database with error handling."""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            self._log_security_event("DATABASE_ERROR", f"Failed to load users: {e}")
            return {}
    
    def _save_users(self) -> None:
        """Securely save user database."""
        try:
            # Create backup before saving
            if os.path.exists(self.db_file):
                backup_file = f"{self.db_file}.backup"
                with open(self.db_file, 'r') as src, open(backup_file, 'w') as dst:
                    dst.write(src.read())
            
            with open(self.db_file, 'w') as f:
                json.dump(self.users, f, indent=2)
                
        except IOError as e:
            self._log_security_event("DATABASE_ERROR", f"Failed to save users: {e}")
    
    def _hash_password(self, password: str, salt: str) -> str:
        """
        Secure password hashing using multiple iterations.
        Uses industry-standard PBKDF2 with SHA-256.
        """
        # Multiple rounds for security
        iterations = 100000
        hash_obj = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'), 
                                       salt.encode('utf-8'), 
                                       iterations)
        return hash_obj.hex()
    
    def _generate_salt(self) -> str:
        """Generate cryptographically secure salt."""
        return secrets.token_hex(32)
    
    def _generate_session_token(self) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(64)
    
    def _validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Comprehensive password strength validation."""
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
            return False, "Password must contain at least one special character"
        
        # Check against common passwords
        common_passwords = [
            "password", "123456", "password123", "admin", "qwerty",
            "letmein", "welcome", "monkey", "dragon", "password1"
        ]
        if password.lower() in common_passwords:
            return False, "Password is too common. Choose a more unique password"
        
        return True, "Password meets security requirements"
    
    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        if not isinstance(input_str, str):
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        sanitized = input_str
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()
    
    def _check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limits."""
        current_time = time.time()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        # Clean old attempts
        self.failed_attempts[identifier] = [
            attempt_time for attempt_time in self.failed_attempts[identifier]
            if current_time - attempt_time < self.RATE_LIMIT_WINDOW
        ]
        
        return len(self.failed_attempts[identifier]) < self.MAX_REQUESTS_PER_MINUTE
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is currently locked."""
        if username in self.locked_accounts:
            lock_time = self.locked_accounts[username]
            if time.time() - lock_time < self.LOCKOUT_DURATION:
                return True
            else:
                # Unlock account
                del self.locked_accounts[username]
        return False
    
    def _log_security_event(self, event_type: str, details: str) -> None:
        """Log security events for audit trail."""
        timestamp = datetime.now().isoformat()
        event = {
            'timestamp': timestamp,
            'type': event_type,
            'details': details,
            'ip': '127.0.0.1'  # In real app, get actual IP
        }
        self.audit_log.append(event)
        
        # Keep only last 1000 events
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
        
        print(f"🔍 Security Event: [{event_type}] {details}")
    
    def register_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        """
        Register a new user with comprehensive validation.
        
        Args:
            username: User's chosen username
            password: User's chosen password
            email: User's email address
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Input sanitization
            username = self._sanitize_input(username)
            email = self._sanitize_input(email)
            
            # Validation
            if not username or len(username) < 3:
                return False, "Username must be at least 3 characters"
            
            if not email or '@' not in email:
                return False, "Valid email address required"
            
            if username in self.users:
                self._log_security_event("REGISTRATION_FAILED", f"Username already exists: {username}")
                return False, "Username already exists"
            
            # Password strength validation
            is_strong, message = self._validate_password_strength(password)
            if not is_strong:
                return False, message
            
            # Create user account
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)
            
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'salt': salt,
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'is_active': True,
                'failed_login_count': 0
            }
            
            self.users[username] = user_data
            self._save_users()
            
            self._log_security_event("USER_REGISTERED", f"New user registered: {username}")
            return True, "User registered successfully"
            
        except Exception as e:
            self._log_security_event("REGISTRATION_ERROR", f"Registration failed: {e}")
            return False, "Registration failed due to system error"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """
        Authenticate user with comprehensive security checks.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            Tuple of (success, message, session_token)
        """
        try:
            # Rate limiting
            if not self._check_rate_limit(username):
                self._log_security_event("RATE_LIMIT_EXCEEDED", f"Rate limit exceeded for: {username}")
                return False, "Too many requests. Please try again later.", None
            
            # Input sanitization
            username = self._sanitize_input(username)
            
            # Check if account is locked
            if self._is_account_locked(username):
                remaining_time = self.LOCKOUT_DURATION - (time.time() - self.locked_accounts[username])
                self._log_security_event("LOCKED_ACCOUNT_ACCESS", f"Access attempted on locked account: {username}")
                return False, f"Account locked. Try again in {int(remaining_time/60)} minutes.", None
            
            # Check if user exists
            if username not in self.users:
                # Record failed attempt even for non-existent users (prevent user enumeration)
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = []
                self.failed_attempts[username].append(time.time())
                
                self._log_security_event("LOGIN_FAILED", f"Login attempt for non-existent user: {username}")
                return False, "Invalid username or password", None
            
            user = self.users[username]
            
            # Check if account is active
            if not user.get('is_active', True):
                self._log_security_event("INACTIVE_ACCOUNT_ACCESS", f"Access attempted on inactive account: {username}")
                return False, "Account is deactivated", None
            
            # Verify password
            salt = user['salt']
            expected_hash = user['password_hash']
            
            # THE SECURITY FLAW IS HERE! 
            # Using == for string comparison instead of secrets.compare_digest()
            # This makes the system vulnerable to timing attacks!
            provided_hash = self._hash_password(password, salt)
            if provided_hash == expected_hash:
                # Successful login
                session_token = self._generate_session_token()
                session_data = {
                    'username': username,
                    'created_at': time.time(),
                    'last_activity': time.time()
                }
                self.sessions[session_token] = session_data
                
                # Update user data
                user['last_login'] = datetime.now().isoformat()
                user['failed_login_count'] = 0
                
                # Clear failed attempts
                if username in self.failed_attempts:
                    del self.failed_attempts[username]
                
                self._save_users()
                self._log_security_event("LOGIN_SUCCESS", f"Successful login: {username}")
                return True, "Login successful", session_token
            else:
                # Failed login
                user['failed_login_count'] = user.get('failed_login_count', 0) + 1
                
                # Track failed attempts
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = []
                self.failed_attempts[username].append(time.time())
                
                # Lock account if too many failures
                if user['failed_login_count'] >= self.MAX_FAILED_ATTEMPTS:
                    self.locked_accounts[username] = time.time()
                    self._log_security_event("ACCOUNT_LOCKED", f"Account locked due to failed attempts: {username}")
                
                self._save_users()
                self._log_security_event("LOGIN_FAILED", f"Failed login attempt: {username}")
                return False, "Invalid username or password", None
                
        except Exception as e:
            self._log_security_event("AUTHENTICATION_ERROR", f"Authentication error: {e}")
            return False, "Authentication failed due to system error", None
    
    def validate_session(self, session_token: str) -> Tuple[bool, Optional[str]]:
        """Validate session token and check for timeout."""
        if not session_token or session_token not in self.sessions:
            return False, None
        
        session = self.sessions[session_token]
        current_time = time.time()
        
        # Check session timeout
        if current_time - session['last_activity'] > self.SESSION_TIMEOUT:
            del self.sessions[session_token]
            self._log_security_event("SESSION_EXPIRED", f"Session expired for: {session['username']}")
            return False, None
        
        # Update last activity
        session['last_activity'] = current_time
        return True, session['username']
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user and invalidate session."""
        if session_token in self.sessions:
            username = self.sessions[session_token]['username']
            del self.sessions[session_token]
            self._log_security_event("USER_LOGOUT", f"User logged out: {username}")
            return True
        return False
    
    def get_security_report(self) -> Dict:
        """Generate comprehensive security report."""
        current_time = time.time()
        
        # Count active sessions
        active_sessions = sum(1 for session in self.sessions.values() 
                            if current_time - session['last_activity'] < self.SESSION_TIMEOUT)
        
        # Count locked accounts
        locked_count = sum(1 for lock_time in self.locked_accounts.values()
                          if current_time - lock_time < self.LOCKOUT_DURATION)
        
        # Recent security events
        recent_events = [event for event in self.audit_log
                        if (datetime.now() - datetime.fromisoformat(event['timestamp'])).seconds < 3600]
        
        return {
            'total_users': len(self.users),
            'active_sessions': active_sessions,
            'locked_accounts': locked_count,
            'recent_security_events': len(recent_events),
            'security_events_last_hour': recent_events[-10:],  # Last 10 events
            'system_status': 'SECURE' if locked_count == 0 else 'ALERT'
        }


def main():
    """Demonstration of the authentication system."""
    print("=" * 60)
    print("🔐 SECURE AUTHENTICATION SYSTEM DEMO")
    print("=" * 60)
    
    auth = SecureUserAuth()
    
    # Demo registration
    print("\n📝 Registering demo user...")
    success, message = auth.register_user(
        "demo_user", 
        "SecurePass123!", 
        "demo@example.com"
    )
    print(f"Registration: {message}")
    
    if success:
        # Demo login
        print("\n🔑 Attempting login...")
        success, message, token = auth.authenticate_user("demo_user", "SecurePass123!")
        print(f"Login: {message}")
        
        if token:
            print(f"🎫 Session token: {token[:20]}...")
            
            # Validate session
            valid, username = auth.validate_session(token)
            print(f"✅ Session valid for user: {username}")
            
            # Security report
            report = auth.get_security_report()
            print(f"\n📊 Security Report:")
            print(f"   Total Users: {report['total_users']}")
            print(f"   Active Sessions: {report['active_sessions']}")
            print(f"   System Status: {report['system_status']}")
    
    print("\n" + "=" * 60)
    print("⚠️  SECURITY NOTE:")
    print("This system contains a subtle timing attack vulnerability!")
    print("Can you find the security flaw? Hint: Look at password comparison...")
    print("=" * 60)


if __name__ == "__main__":
    main()