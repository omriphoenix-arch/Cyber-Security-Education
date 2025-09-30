"""
Hash Generator - Educational Cryptography Tool
Generate hashes for testing the hash cracker
FOR EDUCATIONAL PURPOSES ONLY
"""

import hashlib
import argparse

class HashGenerator:
    def __init__(self):
        self.hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
    
    def generate_hash(self, text, algorithm='md5'):
        """Generate hash for given text"""
        if algorithm.lower() not in self.hash_functions:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_func = self.hash_functions[algorithm.lower()]
        return hash_func(text.encode()).hexdigest()
    
    def generate_test_hashes(self):
        """Generate common test hashes"""
        test_passwords = [
            "hello", "world", "test", "123", "password", "admin",
            "a", "aa", "aaa", "1", "12", "123", "1234", "12345"
        ]
        
        print("🔐 Test Hashes for Educational Purposes")
        print("=" * 60)
        
        for password in test_passwords:
            for algorithm in ['md5', 'sha1', 'sha256']:
                hash_value = self.generate_hash(password, algorithm)
                print(f"'{password}' ({algorithm.upper()}): {hash_value}")
            print()

def main():
    parser = argparse.ArgumentParser(description="Educational Hash Generator")
    parser.add_argument("text", nargs="?", help="Text to hash")
    parser.add_argument("--algorithm", "-a", default="md5",
                       choices=["md5", "sha1", "sha256", "sha512"],
                       help="Hash algorithm (default: md5)")
    parser.add_argument("--test-hashes", "-t", action="store_true",
                       help="Generate test hashes for common passwords")
    
    args = parser.parse_args()
    
    generator = HashGenerator()
    
    if args.test_hashes:
        generator.generate_test_hashes()
        return
    
    if not args.text:
        print("❌ Please provide text to hash or use --test-hashes")
        return
    
    try:
        hash_value = generator.generate_hash(args.text, args.algorithm)
        print(f"Text: '{args.text}'")
        print(f"Algorithm: {args.algorithm.upper()}")
        print(f"Hash: {hash_value}")
        
        print(f"\n💡 Test command:")
        print(f"python hash_cracker.py {hash_value} --type {args.algorithm}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()