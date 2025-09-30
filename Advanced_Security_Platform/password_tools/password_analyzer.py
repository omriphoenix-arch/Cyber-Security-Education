"""
Password Strength Analyzer - Educational Security Tool
Analyze password strength and provide security recommendations
For educational purposes in understanding password security
"""

import re
import math
import hashlib
import string
import argparse
from collections import Counter

class PasswordAnalyzer:
    def __init__(self):
        self.common_passwords = [
            "123456", "password", "123456789", "12345678", "12345",
            "1234567", "1234567890", "qwerty", "abc123", "111111",
            "password1", "admin", "welcome", "monkey", "login",
            "dragon", "pass", "master", "hello", "charlie", "aa123456"
        ]
        
        # Common patterns
        self.keyboard_patterns = [
            "qwerty", "asdf", "zxcv", "1234", "abcd", "qwertyuiop",
            "asdfghjkl", "zxcvbnm", "!@#$%^&*()", "qwer", "asdfg"
        ]
        
        # Dictionary words (basic list)
        self.dictionary_words = [
            "password", "admin", "user", "login", "welcome", "guest",
            "test", "demo", "sample", "default", "root", "system",
            "computer", "internet", "email", "website", "server"
        ]
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def check_character_diversity(self, password):
        """Check character type diversity"""
        diversity = {
            'lowercase': any(c.islower() for c in password),
            'uppercase': any(c.isupper() for c in password),
            'digits': any(c.isdigit() for c in password),
            'special': any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        }
        
        diversity_score = sum(diversity.values())
        return diversity, diversity_score
    
    def check_common_patterns(self, password):
        """Check for common weak patterns"""
        issues = []
        password_lower = password.lower()
        
        # Check for common passwords
        if password_lower in [p.lower() for p in self.common_passwords]:
            issues.append("Uses a very common password")
        
        # Check for keyboard patterns
        for pattern in self.keyboard_patterns:
            if pattern in password_lower or pattern[::-1] in password_lower:
                issues.append(f"Contains keyboard pattern: {pattern}")
        
        # Check for dictionary words
        for word in self.dictionary_words:
            if word in password_lower:
                issues.append(f"Contains dictionary word: {word}")
        
        # Check for repeated characters
        if len(set(password)) < len(password) * 0.5:
            issues.append("Too many repeated characters")
        
        # Check for simple substitutions
        substitutions = {'@': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's'}
        desubstituted = password_lower
        for sub, orig in substitutions.items():
            desubstituted = desubstituted.replace(sub, orig)
        
        for word in self.dictionary_words:
            if word in desubstituted:
                issues.append(f"Contains word with simple substitution: {word}")
        
        return issues
    
    def check_sequences(self, password):
        """Check for sequential patterns"""
        sequences = []
        
        # Numeric sequences
        numeric_seq = []
        for i in range(len(password) - 2):
            try:
                if (int(password[i]) + 1 == int(password[i+1]) and 
                    int(password[i+1]) + 1 == int(password[i+2])):
                    numeric_seq.append(password[i:i+3])
            except ValueError:
                continue
        
        if numeric_seq:
            sequences.append(f"Numeric sequences: {', '.join(set(numeric_seq))}")
        
        # Alphabetic sequences
        alpha_seq = []
        for i in range(len(password) - 2):
            if (password[i:i+3].lower() in string.ascii_lowercase and
                ord(password[i].lower()) + 1 == ord(password[i+1].lower()) and
                ord(password[i+1].lower()) + 1 == ord(password[i+2].lower())):
                alpha_seq.append(password[i:i+3])
        
        if alpha_seq:
            sequences.append(f"Alphabetic sequences: {', '.join(set(alpha_seq))}")
        
        return sequences
    
    def calculate_crack_time(self, entropy):
        """Estimate crack time based on entropy"""
        # Assuming 1 billion guesses per second
        guesses_per_second = 1_000_000_000
        total_combinations = 2 ** entropy
        seconds_to_crack = total_combinations / (2 * guesses_per_second)  # Average case
        
        if seconds_to_crack < 1:
            return "Instantly"
        elif seconds_to_crack < 60:
            return f"{seconds_to_crack:.1f} seconds"
        elif seconds_to_crack < 3600:
            return f"{seconds_to_crack/60:.1f} minutes"
        elif seconds_to_crack < 86400:
            return f"{seconds_to_crack/3600:.1f} hours"
        elif seconds_to_crack < 31536000:
            return f"{seconds_to_crack/86400:.1f} days"
        else:
            years = seconds_to_crack / 31536000
            if years > 1000000:
                return f"{years/1000000:.1f} million years"
            elif years > 1000:
                return f"{years/1000:.1f} thousand years"
            else:
                return f"{years:.1f} years"
    
    def get_strength_rating(self, entropy, length, diversity_score, issues):
        """Get overall password strength rating"""
        if entropy < 25 or length < 6 or len(issues) > 3:
            return "Very Weak", "🔴"
        elif entropy < 35 or length < 8 or len(issues) > 1:
            return "Weak", "🟠"
        elif entropy < 50 or length < 10 or diversity_score < 3:
            return "Fair", "🟡"
        elif entropy < 60 or length < 12:
            return "Good", "🟢"
        else:
            return "Very Strong", "🟢"
    
    def generate_recommendations(self, password, diversity, issues):
        """Generate improvement recommendations"""
        recommendations = []
        
        if len(password) < 12:
            recommendations.append("Use at least 12 characters")
        
        if not diversity['lowercase']:
            recommendations.append("Add lowercase letters")
        if not diversity['uppercase']:
            recommendations.append("Add uppercase letters")
        if not diversity['digits']:
            recommendations.append("Add numbers")
        if not diversity['special']:
            recommendations.append("Add special characters (!@#$%^&*)")
        
        if issues:
            recommendations.append("Avoid common words and patterns")
            recommendations.append("Use random combination of characters")
        
        recommendations.append("Consider using a passphrase with random words")
        recommendations.append("Use a unique password for each account")
        recommendations.append("Consider using a password manager")
        
        return recommendations
    
    def analyze(self, password):
        """Main password analysis function"""
        if not password:
            return {"error": "Password cannot be empty"}
        
        # Calculate metrics
        length = len(password)
        entropy = self.calculate_entropy(password)
        diversity, diversity_score = self.check_character_diversity(password)
        issues = self.check_common_patterns(password)
        sequences = self.check_sequences(password)
        crack_time = self.calculate_crack_time(entropy)
        strength, strength_emoji = self.get_strength_rating(entropy, length, diversity_score, issues)
        recommendations = self.generate_recommendations(password, diversity, issues)
        
        # Combine all issues
        all_issues = issues + sequences
        
        return {
            "length": length,
            "entropy": entropy,
            "diversity": diversity,
            "diversity_score": diversity_score,
            "issues": all_issues,
            "crack_time": crack_time,
            "strength": strength,
            "strength_emoji": strength_emoji,
            "recommendations": recommendations
        }

def print_analysis(analysis):
    """Print formatted analysis results"""
    print("🔐 PASSWORD STRENGTH ANALYSIS")
    print("=" * 50)
    
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    # Basic metrics
    print(f"📏 Length: {analysis['length']} characters")
    print(f"🔢 Entropy: {analysis['entropy']:.1f} bits")
    print(f"⏰ Est. crack time: {analysis['crack_time']}")
    print(f"💪 Strength: {analysis['strength_emoji']} {analysis['strength']}")
    print()
    
    # Character diversity
    print("📊 CHARACTER DIVERSITY:")
    diversity = analysis['diversity']
    print(f"   Lowercase: {'✅' if diversity['lowercase'] else '❌'}")
    print(f"   Uppercase: {'✅' if diversity['uppercase'] else '❌'}")
    print(f"   Digits:    {'✅' if diversity['digits'] else '❌'}")
    print(f"   Special:   {'✅' if diversity['special'] else '❌'}")
    print(f"   Score:     {analysis['diversity_score']}/4")
    print()
    
    # Issues
    if analysis['issues']:
        print("⚠️  SECURITY ISSUES:")
        for issue in analysis['issues']:
            print(f"   • {issue}")
        print()
    
    # Recommendations
    print("💡 RECOMMENDATIONS:")
    for rec in analysis['recommendations'][:5]:  # Show top 5
        print(f"   • {rec}")

def main():
    parser = argparse.ArgumentParser(description="Educational Password Strength Analyzer")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Interactive mode (hides password input)")
    parser.add_argument("password", nargs="?", help="Password to analyze (use quotes for spaces)")
    
    args = parser.parse_args()
    
    print("🔒 Educational Password Strength Analyzer v1.0")
    print("📚 Learn about password security and best practices\n")
    
    analyzer = PasswordAnalyzer()
    
    if args.interactive or not args.password:
        # Interactive mode with hidden input
        import getpass
        try:
            password = getpass.getpass("🔐 Enter password to analyze (hidden): ")
        except KeyboardInterrupt:
            print("\n\n🛑 Analysis cancelled")
            return
    else:
        password = args.password
    
    # Analyze password
    analysis = analyzer.analyze(password)
    
    # Print results
    print_analysis(analysis)
    
    print("\n" + "=" * 50)
    print("📚 Educational Note: This tool helps you understand password")
    print("   security. Always use strong, unique passwords for your accounts!")

if __name__ == "__main__":
    main()