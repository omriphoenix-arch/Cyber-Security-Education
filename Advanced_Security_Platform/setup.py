#!/usr/bin/env python3
"""
Ethical Hacking Toolkit - Setup and Quick Start
==============================================
This script helps users get started with the toolkit quickly and safely.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("🔒 ETHICAL HACKING TOOLKIT - QUICK START 🛡️")
    print("=" * 70)
    print("Educational cybersecurity tools for authorized testing only!")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor} detected - Compatible!")
    return True

def install_requirements():
    """Install required packages."""
    req_file = Path("documentation/requirements.txt")
    if not req_file.exists():
        print("❌ Requirements file not found!")
        return False
    
    print("\n📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)], 
                      check=True, capture_output=True)
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def show_toolkit_overview():
    """Display toolkit categories and tools."""
    print("\n📁 TOOLKIT STRUCTURE:")
    print("=" * 50)
    
    categories = {
        "🌐 Network Tools": {
            "folder": "network_tools",
            "tools": [
                "network_discovery.py - Network device discovery",
                "port_scanner.py - Port scanning and service detection"
            ]
        },
        "🔐 Password Tools": {
            "folder": "password_tools", 
            "tools": [
                "password_analyzer.py - Password strength analysis",
                "hash_cracker.py - Educational hash cracking",
                "hash_generator.py - Test hash generation"
            ]
        },
        "🕐 Advanced Research": {
            "folder": "timing_attack_demo",
            "tools": [
                "timing_attack_demo.py - Timing attack demonstration",
                "vulnerable_auth.py - Authentication with security flaw",
                "secure_auth_fixed.py - Secure implementation example"
            ]
        }
    }
    
    for category, info in categories.items():
        print(f"\n{category} ({info['folder']}/)")
        for tool in info['tools']:
            print(f"   • {tool}")

def show_usage_examples():
    """Show basic usage examples."""
    print("\n🚀 QUICK START EXAMPLES:")
    print("=" * 50)
    
    examples = [
        ("Network Discovery", "cd network_tools && python network_discovery.py 192.168.1.0/24"),
        ("Port Scanning", "cd network_tools && python port_scanner.py 127.0.0.1 --common-ports"),
        ("Password Analysis", "cd password_tools && python password_analyzer.py"),
        ("Hash Cracking Demo", "cd password_tools && python hash_cracker.py 5d41402abc4b2a76b9719d911017c592 --type md5"),
        ("Timing Attack Demo", "cd timing_attack_demo && python timing_attack_demo.py")
    ]
    
    for name, command in examples:
        print(f"\n📌 {name}:")
        print(f"   {command}")

def show_ethical_guidelines():
    """Display critical ethical guidelines."""
    print("\n⚠️  CRITICAL ETHICAL GUIDELINES:")
    print("=" * 50)
    guidelines = [
        "✅ Only test systems you OWN or have EXPLICIT PERMISSION to test",
        "✅ Use tools for LEARNING and IMPROVING security",
        "✅ Test in isolated LAB ENVIRONMENTS when practicing",
        "✅ Follow all applicable LAWS and REGULATIONS",
        "❌ NEVER test systems without proper authorization", 
        "❌ NEVER use tools to cause harm or gain unauthorized access",
        "❌ NEVER ignore legal and ethical implications"
    ]
    
    for guideline in guidelines:
        print(f"   {guideline}")

def interactive_tool_launcher():
    """Interactive tool selection and launching."""
    print("\n🎯 INTERACTIVE TOOL LAUNCHER:")
    print("=" * 50)
    
    tools = {
        "1": ("Network Discovery", "network_tools/network_discovery.py", "192.168.1.0/24"),
        "2": ("Port Scanner", "network_tools/port_scanner.py", "127.0.0.1 --common-ports"),
        "3": ("Password Analyzer", "password_tools/password_analyzer.py", ""),
        "4": ("Hash Generator", "password_tools/hash_generator.py", "--test-hashes"),
        "5": ("Timing Attack Demo", "timing_attack_demo/timing_attack_demo.py", ""),
        "6": ("View Documentation", "", "")
    }
    
    while True:
        print("\nSelect a tool to run:")
        for key, (name, _, _) in tools.items():
            print(f"   {key}. {name}")
        print("   q. Quit")
        
        choice = input("\nEnter choice (1-6, q): ").strip().lower()
        
        if choice == 'q':
            print("👋 Thanks for using the Ethical Hacking Toolkit!")
            break
        elif choice in tools:
            name, script, args = tools[choice]
            
            if choice == "6":
                print("\n📚 Opening documentation...")
                print("Main README: README.md")
                print("Tool folders contain individual README files")
                print("Usage guide: documentation/USAGE_GUIDE.md")
                continue
                
            print(f"\n🔧 Launching {name}...")
            
            if choice in ["1", "2"]:  # Network tools need target input
                if choice == "1":
                    network = input("Enter network to scan (e.g., 192.168.1.0/24): ").strip()
                    args = network if network else "192.168.1.0/24"
                elif choice == "2":
                    target = input("Enter target to scan (e.g., 127.0.0.1): ").strip()
                    args = f"{target} --common-ports" if target else "127.0.0.1 --common-ports"
            
            try:
                if args:
                    os.system(f"python {script} {args}")
                else:
                    os.system(f"python {script}")
            except KeyboardInterrupt:
                print("\n⏹️  Tool execution interrupted by user.")
            
            input("\nPress Enter to continue...")
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main setup and launcher function."""
    print_banner()
    
    # System checks
    if not check_python_version():
        return 1
    
    # Install dependencies
    print("\n🔧 SYSTEM SETUP:")
    print("-" * 30)
    install_result = install_requirements()
    
    # Show toolkit information
    show_toolkit_overview()
    show_usage_examples()
    show_ethical_guidelines()
    
    # Ask if user wants interactive launcher
    print("\n" + "=" * 70)
    response = input("Would you like to use the interactive tool launcher? (y/n): ").strip().lower()
    
    if response == 'y':
        interactive_tool_launcher()
    else:
        print("\n🎓 Setup complete! You can now use the tools manually.")
        print("📖 Check individual folder README files for detailed usage instructions.")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user. Goodbye!")
        sys.exit(1)