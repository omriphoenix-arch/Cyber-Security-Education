"""
Hash Cracker - Educational Cryptography Tool
Crack simple hashes using dictionary and brute force methods
FOR EDUCATIONAL PURPOSES ONLY - Learn about hash security
"""

import hashlib
import itertools
import string
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class HashCracker:
    def __init__(self, hash_value, hash_type="md5", max_length=6, threads=4):
        self.hash_value = hash_value.lower()
        self.hash_type = hash_type.lower()
        self.max_length = max_length
        self.threads = threads
        self.found = False
        self.result = None
        self.attempts = 0
        self.lock = threading.Lock()
        
        # Hash functions
        self.hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if self.hash_type not in self.hash_functions:
            raise ValueError(f"Unsupported hash type: {hash_type}")
        
        self.hash_func = self.hash_functions[self.hash_type]
        
        # Common passwords dictionary
        self.common_passwords = [
                        # Common numeric passwords
            "123456", "password", "123456789", "12345678", "12345", "123",
            "1234567", "1234567890", "qwerty", "abc123", "111111",
            "dragon", "master", "monkey", "letmein", "login",
            "princess", "qwertyuiop", "solo", "passw0rd", "starwars",
            "password1", "password123", "admin", "welcome", "hello",
            "guest", "test", "root", "user", "default", "demo",
            "sample", "temp", "temporary", "pass", "secret",
            "love", "sex", "god", "money", "freedom", "whatever",
            "computer", "internet", "email", "website", "server"
        ]
        
        # Extended with years, names, etc.
        self.extended_dict = self.common_passwords.copy()
        
        # Add years
        for year in range(1950, 2030):
            self.extended_dict.append(str(year))
        
        # Add common names
        names = ["john", "mike", "david", "james", "robert", "mary", 
                "lisa", "jennifer", "sarah", "jessica", "admin", "user"]
        self.extended_dict.extend(names)
        
        # Add simple variations
        variations = []
        for pwd in self.common_passwords[:20]:  # Limit variations
            variations.extend([
                pwd + "123", pwd + "1", pwd + "!", pwd + "@",
                pwd.capitalize(), pwd.upper()
            ])
        self.extended_dict.extend(variations)
        
        # Add more common words and variations
        more_words = [
            "hello", "world", "test", "example", "sample", "data",
            "info", "security", "hacker", "python", "code", "hash",
            "crack", "simple", "easy", "hard", "complex", "random"
        ]
        self.extended_dict.extend(more_words)
        
        # Add single digits and letters
        for i in range(10):
            self.extended_dict.append(str(i))
        
        for letter in string.ascii_lowercase:
            self.extended_dict.append(letter)
            self.extended_dict.append(letter * 2)  # aa, bb, cc, etc.
            self.extended_dict.append(letter * 3)  # aaa, bbb, ccc, etc.
    
    def hash_string(self, text):
        """Hash a string using the specified algorithm"""
        return self.hash_func(text.encode()).hexdigest()
    
    def dictionary_attack(self):
        """Try dictionary attack with common passwords"""
        print(f"🔍 Starting dictionary attack with {len(self.extended_dict)} words...")
        
        start_time = time.time()
        
        for i, password in enumerate(self.extended_dict):
            if self.found:
                break
                
            with self.lock:
                self.attempts += 1
            
            if self.hash_string(password) == self.hash_value:
                with self.lock:
                    if not self.found:
                        self.found = True
                        self.result = password
                        elapsed = time.time() - start_time
                        print(f"✅ Password found: '{password}'")
                        print(f"⏰ Time: {elapsed:.2f} seconds")
                        print(f"🔢 Attempts: {self.attempts}")
                        return True
            
            if i % 1000 == 0 and i > 0:
                print(f"   Tried {i:,} passwords...")
        
        elapsed = time.time() - start_time
        print(f"❌ Dictionary attack failed after {elapsed:.2f} seconds")
        print(f"🔢 Total attempts: {self.attempts}")
        return False
    
    def brute_force_worker(self, passwords_chunk):
        """Worker function for brute force attack"""
        for password in passwords_chunk:
            if self.found:
                break
                
            with self.lock:
                self.attempts += 1
                if self.attempts % 100000 == 0:
                    print(f"   Attempts: {self.attempts:,}")
            
            if self.hash_string(password) == self.hash_value:
                with self.lock:
                    if not self.found:
                        self.found = True
                        self.result = password
                return password
        return None
    
    def generate_passwords(self, length):
        """Generate all possible passwords of given length"""
        # Use common characters (letters, digits, basic symbols)
        chars = string.ascii_lowercase + string.digits
        if length > 4:  # Add uppercase and symbols for longer passwords
            chars += string.ascii_uppercase + "!@#$"
        
        for password in itertools.product(chars, repeat=length):
            if self.found:
                break
            yield ''.join(password)
    
    def brute_force_attack(self):
        """Try brute force attack"""
        print(f"🔨 Starting brute force attack (max length: {self.max_length})...")
        print("⚠️  This may take a very long time for longer passwords!")
        
        start_time = time.time()
        
        for length in range(1, self.max_length + 1):
            if self.found:
                break
                
            print(f"\n🔍 Trying length {length}...")
            length_start = time.time()
            
            # Estimate combinations
            charset_size = len(string.ascii_lowercase + string.digits)
            if length > 4:
                charset_size = len(string.ascii_lowercase + string.digits + 
                                string.ascii_uppercase + "!@#$")
            
            total_combinations = charset_size ** length
            print(f"   Total combinations: {total_combinations:,}")
            
            if total_combinations > 10_000_000:
                response = input(f"   This will try {total_combinations:,} combinations. Continue? (y/n): ")
                if response.lower() != 'y':
                    print("   Skipping this length...")
                    continue
            
            # Generate passwords and split into chunks for threading
            chunk_size = max(1000, total_combinations // (self.threads * 10))
            
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                current_chunk = []
                
                for password in self.generate_passwords(length):
                    if self.found:
                        break
                    
                    current_chunk.append(password)
                    
                    if len(current_chunk) >= chunk_size:
                        future = executor.submit(self.brute_force_worker, current_chunk.copy())
                        futures.append(future)
                        current_chunk = []
                
                # Submit remaining passwords
                if current_chunk and not self.found:
                    future = executor.submit(self.brute_force_worker, current_chunk)
                    futures.append(future)
                
                # Check results
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        elapsed = time.time() - start_time
                        print(f"✅ Password found: '{result}'")
                        print(f"⏰ Time: {elapsed:.2f} seconds")
                        print(f"🔢 Total attempts: {self.attempts:,}")
                        return True
            
            length_elapsed = time.time() - length_start
            print(f"   Length {length} completed in {length_elapsed:.2f} seconds")
        
        elapsed = time.time() - start_time
        print(f"❌ Brute force attack failed after {elapsed:.2f} seconds")
        print(f"🔢 Total attempts: {self.attempts:,}")
        return False
    
    def crack(self, use_dictionary=True, use_brute_force=False):
        """Main cracking function"""
        print(f"🔐 Hash Cracker - Educational Tool")
        print(f"🎯 Target hash: {self.hash_value}")
        print(f"🔍 Hash type: {self.hash_type.upper()}")
        print(f"⚡ Threads: {self.threads}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Try dictionary attack first
        if use_dictionary and not self.found:
            if self.dictionary_attack():
                return self.result
        
        # Try brute force if dictionary failed
        if use_brute_force and not self.found:
            print(f"\n{'='*60}")
            if self.brute_force_attack():
                return self.result
        
        total_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"❌ Hash could not be cracked")
        print(f"⏰ Total time: {total_time:.2f} seconds")
        print(f"🔢 Total attempts: {self.attempts:,}")
        print("\n💡 Consider:")
        print("   • The password might be longer than the max length")
        print("   • The password might use complex characters")
        print("   • The hash might have a salt (not supported)")
        
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Educational Hash Cracker - Learn about hash security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # MD5 hash of "hello"
  python hash_cracker.py 5d41402abc4b2a76b9719d911017c592
  
  # SHA1 with brute force
  python hash_cracker.py aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d --type sha1 --brute-force
  
  # Longer max length
  python hash_cracker.py hash_here --max-length 8 --threads 8

⚠️  Educational purposes only! Only crack hashes you own or have permission to crack.
        """
    )
    
    parser.add_argument("hash", help="Hash to crack (hex format)")
    parser.add_argument("--type", "-t", default="md5", 
                       choices=["md5", "sha1", "sha256", "sha512"],
                       help="Hash algorithm (default: md5)")
    parser.add_argument("--max-length", "-l", type=int, default=6,
                       help="Maximum password length for brute force (default: 6)")
    parser.add_argument("--threads", type=int, default=4,
                       help="Number of threads (default: 4)")
    parser.add_argument("--dictionary-only", "-d", action="store_true",
                       help="Use dictionary attack only")
    parser.add_argument("--brute-force", "-b", action="store_true",
                       help="Enable brute force attack")
    
    args = parser.parse_args()
    
    # Validate hash format
    expected_lengths = {"md5": 32, "sha1": 40, "sha256": 64, "sha512": 128}
    if len(args.hash) != expected_lengths[args.type]:
        print(f"❌ Invalid hash length. {args.type.upper()} hashes should be {expected_lengths[args.type]} characters")
        return
    
    if not all(c in string.hexdigits for c in args.hash):
        print("❌ Hash should only contain hexadecimal characters")
        return
    
    print("🔒 Educational Hash Cracker v1.0")
    print("📚 Learn about password hashing and security\n")
    
    # Security warning
    print("⚠️  EDUCATIONAL USE ONLY")
    print("   Only crack hashes from your own systems or with explicit permission!")
    
    if not args.dictionary_only:
        response = input("\nContinue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("🛑 Operation cancelled")
            return
    
    try:
        cracker = HashCracker(
            hash_value=args.hash,
            hash_type=args.type,
            max_length=args.max_length,
            threads=args.threads
        )
        
        use_dictionary = not args.brute_force or not args.dictionary_only
        use_brute_force = args.brute_force
        
        if args.dictionary_only:
            use_brute_force = False
        
        result = cracker.crack(
            use_dictionary=use_dictionary,
            use_brute_force=use_brute_force
        )
        
        if result:
            print(f"\n🎉 SUCCESS! Password: '{result}'")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Cracking interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()