# 🔐 Password Security Tools

This folder contains tools for password analysis, testing, and cryptographic education.

## 📁 Tools Included

### `password_analyzer.py`
- **Purpose**: Analyze password strength and security
- **Features**:
  - Comprehensive strength assessment
  - Common password detection
  - Entropy calculation
  - Security recommendations
  - Breach database checking simulation

**Usage:**
```bash
python password_analyzer.py
# Interactive mode - enter passwords to analyze
```

### `hash_cracker.py`
- **Purpose**: Educational hash cracking for learning cryptography
- **Features**:
  - Dictionary attacks with common passwords
  - Brute force capabilities (short passwords)
  - Multiple hash algorithm support (MD5, SHA1, SHA256, SHA512)
  - Multi-threaded processing
  - Educational timing and statistics

**Usage:**
```bash
# Crack MD5 hash using dictionary
python hash_cracker.py 5d41402abc4b2a76b9719d911017c592 --type md5

# Enable brute force for short passwords
python hash_cracker.py hash_here --brute-force --max-length 4

# SHA256 hash with more threads
python hash_cracker.py hash_here --type sha256 --threads 8
```

### `hash_generator.py`
- **Purpose**: Generate test hashes for educational purposes
- **Features**:
  - Multiple hash algorithm support
  - Test hash generation for learning
  - Common password hash examples
  - Educational hash comparison

**Usage:**
```bash
# Generate test hashes
python hash_generator.py --test-hashes

# Generate hash for specific text
python hash_generator.py --text "your_password" --algorithm md5
```

## 🎯 Educational Objectives

### Learn About:
1. **Password Security Principles**
   - What makes passwords strong or weak
   - Common attack patterns
   - Defense strategies

2. **Cryptographic Hashing**
   - How hash functions work
   - Different algorithm characteristics
   - Salt usage and importance

3. **Attack Methodologies**
   - Dictionary attacks vs. brute force
   - Time complexity and feasibility
   - Real-world attack scenarios

## ⚠️ Ethical Guidelines

**CRITICAL: Educational Use Only**
- Only test hashes you own or have permission to test
- Never use these tools for unauthorized access
- Understand legal implications of password cracking
- Use knowledge to improve security, not exploit it

## 🛡️ Security Best Practices

### For Password Creation:
- Use long, complex passwords (12+ characters)
- Include uppercase, lowercase, numbers, and symbols
- Avoid common words and patterns
- Use unique passwords for each account
- Consider using password managers

### For System Security:
- Implement proper password hashing (bcrypt, Argon2)
- Use strong salts for all password storage
- Implement rate limiting and account lockouts
- Monitor for suspicious authentication patterns

## 📊 Understanding Results

### Dictionary Attack Success:
- Indicates password is in common lists
- Suggests need for more unique passwords
- Shows vulnerability to basic attacks

### Brute Force Limitations:
- Demonstrates why longer passwords are secure
- Shows computational complexity of password cracking
- Illustrates importance of proper hash algorithms

## 📚 Further Learning

1. **Study cryptography fundamentals**
2. **Learn about modern password storage techniques**
3. **Understand authentication security**
4. **Practice secure coding principles**
5. **Stay updated on security best practices**

---

*These tools teach why strong passwords and proper security practices are essential for protecting digital assets.*