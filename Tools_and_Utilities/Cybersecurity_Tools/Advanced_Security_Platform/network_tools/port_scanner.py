"""
Port Scanner - Educational Network Security Tool
A simple port scanner for learning network security concepts
USE ONLY ON YOUR OWN SYSTEMS OR WITH EXPLICIT PERMISSION
"""

import socket
import threading
import argparse
import sys
from datetime import datetime
import time

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1000, threads=100, timeout=3):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        
        # Resolve hostname to IP
        try:
            self.target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"❌ Cannot resolve hostname: {target}")
            sys.exit(1)
    
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:
                # Try to grab banner
                banner = self.grab_banner(sock, port)
                with self.lock:
                    self.open_ports.append((port, banner))
                    print(f"✅ Port {port:5d}/tcp open    {banner}")
            
            sock.close()
            
        except Exception as e:
            pass  # Silently handle connection errors
    
    def grab_banner(self, sock, port):
        """Try to grab service banner"""
        try:
            if port == 22:
                return "SSH"
            elif port == 21:
                return "FTP"
            elif port == 80:
                return "HTTP"
            elif port == 443:
                return "HTTPS"
            elif port == 25:
                return "SMTP"
            elif port == 110:
                return "POP3"
            elif port == 143:
                return "IMAP"
            elif port == 993:
                return "IMAPS"
            elif port == 995:
                return "POP3S"
            elif port == 3389:
                return "RDP"
            elif port == 23:
                return "Telnet"
            elif port == 53:
                return "DNS"
            elif port == 135:
                return "RPC"
            elif port == 139:
                return "NetBIOS"
            elif port == 445:
                return "SMB"
            else:
                # Try to get actual banner
                sock.send(b'\r\n')
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner[:50] if banner else "Unknown"
                
        except:
            return "Unknown"
    
    def scan(self):
        """Main scanning function"""
        print(f"🎯 Target: {self.target} ({self.target_ip})")
        print(f"📊 Scanning ports {self.start_port}-{self.end_port}")
        print(f"⚡ Threads: {self.threads}, Timeout: {self.timeout}s")
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Create and start threads
        thread_list = []
        
        for port in range(self.start_port, self.end_port + 1):
            # Limit concurrent threads
            while len([t for t in thread_list if t.is_alive()]) >= self.threads:
                time.sleep(0.01)
            
            thread = threading.Thread(target=self.scan_port, args=(port,))
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
        
        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()
        
        self.print_results()
    
    def print_results(self):
        """Print scan results"""
        print("-" * 60)
        print(f"📋 Scan completed: {len(self.open_ports)} open ports found")
        
        if self.open_ports:
            print("\n🔍 Open Ports Summary:")
            print("Port     Service")
            print("-" * 20)
            for port, banner in sorted(self.open_ports):
                print(f"{port:5d}    {banner}")
        else:
            print("🚫 No open ports found in the specified range")
        
        print(f"\n⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(
        description="Educational Port Scanner - Use only on authorized systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py localhost
  python port_scanner.py 127.0.0.1 --start 1 --end 1000
  python port_scanner.py myserver.local --threads 50 --timeout 5

⚠️  WARNING: Only use on systems you own or have explicit permission to test!
        """
    )
    
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument("--start", "-s", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", "-e", type=int, default=1000, help="End port (default: 1000)")
    parser.add_argument("--threads", "-t", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=int, default=3, help="Connection timeout in seconds (default: 3)")
    
    args = parser.parse_args()
    
    # Validation
    if args.start < 1 or args.end > 65535:
        print("❌ Port range must be between 1 and 65535")
        sys.exit(1)
    
    if args.start > args.end:
        print("❌ Start port must be less than or equal to end port")
        sys.exit(1)
    
    # Warning for localhost/local IPs only
    if args.target not in ['localhost', '127.0.0.1', '::1'] and not args.target.startswith('192.168.'):
        response = input(f"⚠️  You are about to scan {args.target}. Do you have permission? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("🛑 Scan cancelled. Only scan systems you own or have permission to test.")
            sys.exit(1)
    
    print("🔒 Educational Port Scanner v1.0")
    print("⚠️  For educational and authorized testing purposes only!\n")
    
    # Create and run scanner
    scanner = PortScanner(
        target=args.target,
        start_port=args.start,
        end_port=args.end,
        threads=args.threads,
        timeout=args.timeout
    )
    
    try:
        scanner.scan()
    except KeyboardInterrupt:
        print("\n\n🛑 Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()