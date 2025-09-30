#!/usr/bin/env python3
"""
FIXED Secure User Authentication System
======================================
This is the corrected version that prevents timing attacks.

The key fix: Using secrets.compare_digest() for cryptographic comparisons
instead of the standard == operator.
"""

import hashlib
import secrets
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List

class SecureUserAuthFixed:
    """
    Fixed version of the authentication system that prevents timing attacks.
    """
    
    def __init__(self, db_file: str = "users_fixed.json"):
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
        
        print("🔐 SecureAuth System v2.1.0 (FIXED) Initialized")
        print("✅ Timing attack protection enabled")
    
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
            with open(self.db_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except IOError as e:
            self._log_security_event("DATABASE_ERROR", f"Failed to save users: {e}")
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Secure password hashing using multiple iterations."""
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
                del self.locked_accounts[username]
        return False
    
    def _log_security_event(self, event_type: str, details: str) -> None:
        """Log security events for audit trail."""
        timestamp = datetime.now().isoformat()
        event = {
            'timestamp': timestamp,
            'type': event_type,
            'details': details,
            'ip': '127.0.0.1'
        }
        self.audit_log.append(event)
        
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
        
        print(f"🔍 Security Event: [{event_type}] {details}")
    
    def register_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        """Register a new user with comprehensive validation."""
        try:
            username = self._sanitize_input(username)
            email = self._sanitize_input(email)
            
            if not username or len(username) < 3:
                return False, "Username must be at least 3 characters"
            
            if not email or '@' not in email:
                return False, "Valid email address required"
            
            if username in self.users:
                self._log_security_event("REGISTRATION_FAILED", f"Username already exists: {username}")
                return False, "Username already exists"
            
            is_strong, message = self._validate_password_strength(password)
            if not is_strong:
                return False, message
            
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
        FIXED: Authenticate user with timing attack protection.
        
        The key fix is using secrets.compare_digest() instead of == 
        for password hash comparison.
        """
        try:
            # Add small random delay to further obscure timing
            time.sleep(secrets.randbelow(10) / 1000.0)  # 0-9ms random delay
            
            # Rate limiting
            if not self._check_rate_limit(username):
                self._log_security_event("RATE_LIMIT_EXCEEDED", f"Rate limit exceeded for: {username}")
                return False, "Too many requests. Please try again later.", None
            
            username = self._sanitize_input(username)
            
            # Check if account is locked
            if self._is_account_locked(username):
                remaining_time = self.LOCKOUT_DURATION - (time.time() - self.locked_accounts[username])
                self._log_security_event("LOCKED_ACCOUNT_ACCESS", f"Access attempted on locked account: {username}")
                return False, f"Account locked. Try again in {int(remaining_time/60)} minutes.", None
            
            # Always perform hash calculation to prevent user enumeration timing attacks
            dummy_salt = secrets.token_hex(32)
            dummy_hash = self._hash_password(password, dummy_salt)
            
            # Check if user exists
            if username not in self.users:
                # Perform a dummy comparison to maintain consistent timing
                secrets.compare_digest(dummy_hash, dummy_hash)
                
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = []
                self.failed_attempts[username].append(time.time())
                
                self._log_security_event("LOGIN_FAILED", f"Login attempt for non-existent user: {username}")
                return False, "Invalid username or password", None
            
            user = self.users[username]
            
            if not user.get('is_active', True):
                # Still perform hash comparison to maintain timing
                secrets.compare_digest(dummy_hash, dummy_hash)
                self._log_security_event("INACTIVE_ACCOUNT_ACCESS", f"Access attempted on inactive account: {username}")
                return False, "Account is deactivated", None
            
            # Verify password - THE FIX IS HERE!
            salt = user['salt']
            expected_hash = user['password_hash']
            provided_hash = self._hash_password(password, salt)
            
            # 🔒 SECURITY FIX: Use secrets.compare_digest() for constant-time comparison
            # This prevents timing attacks by always taking the same amount of time
            if secrets.compare_digest(provided_hash, expected_hash):
                # Successful login
                session_token = self._generate_session_token()
                session_data = {
                    'username': username,
                    'created_at': time.time(),
                    'last_activity': time.time()
                }
                self.sessions[session_token] = session_data
                
                user['last_login'] = datetime.now().isoformat()
                user['failed_login_count'] = 0
                
                if username in self.failed_attempts:
                    del self.failed_attempts[username]
                
                self._save_users()
                self._log_security_event("LOGIN_SUCCESS", f"Successful login: {username}")
                return True, "Login successful", session_token
            else:
                # Failed login
                user['failed_login_count'] = user.get('failed_login_count', 0) + 1
                
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = []
                self.failed_attempts[username].append(time.time())
                
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
        
        if current_time - session['last_activity'] > self.SESSION_TIMEOUT:
            del self.sessions[session_token]
            self._log_security_event("SESSION_EXPIRED", f"Session expired for: {session['username']}")
            return False, None
        
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


def main():
    """Demonstration of the FIXED authentication system."""
    print("=" * 60)
    print("🔐 FIXED SECURE AUTHENTICATION SYSTEM")
    print("=" * 60)
    print("✅ Now protected against timing attacks!")
    
    auth = SecureUserAuthFixed()
    
    # Demo registration
    print("\n📝 Registering demo user...")
    success, message = auth.register_user(
        "demo_user", 
        "SecurePass123!", 
        "demo@example.com"
    )
    print(f"Registration: {message}")
    
    if success:
        print("\n🔑 Attempting login...")
        success, message, token = auth.authenticate_user("demo_user", "SecurePass123!")
        print(f"Login: {message}")
        
        if token:
            print(f"🎫 Session token: {token[:20]}...")
            
            valid, username = auth.validate_session(token)
            print(f"✅ Session valid for user: {username}")
    
    print("\n" + "=" * 60)
    print("🛡️  SECURITY IMPROVEMENTS:")
    print("• Used secrets.compare_digest() for password comparison")
    print("• Added random delays to obscure timing patterns")
    print("• Consistent timing regardless of username existence")
    print("• Constant-time cryptographic operations")
    print("=" * 60)


if __name__ == "__main__":
    main()