"""
Network Discovery Tool - Educational Network Security
Discover hosts and services on a network for learning purposes
USE ONLY ON YOUR OWN NETWORKS OR WITH EXPLICIT PERMISSION
"""

import socket
import subprocess
import threading
import ipaddress
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

class NetworkDiscovery:
    def __init__(self, network, threads=50, timeout=3):
        self.network = network
        self.threads = threads
        self.timeout = timeout
        self.alive_hosts = []
        self.host_info = {}
        
    def ping_host(self, ip):
        """Ping a single host to check if it's alive"""
        try:
            # Windows ping command
            if sys.platform.startswith('win'):
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '1000', str(ip)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
            else:
                # Linux/Mac ping command
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '1', str(ip)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
            
            if result.returncode == 0:
                return str(ip)
            return None
                
        except (subprocess.TimeoutExpired, Exception):
            return None
    
    def get_hostname(self, ip):
        """Try to get hostname for IP"""
        try:
            hostname = socket.gethostbyaddr(str(ip))[0]
            return hostname
        except:
            return "Unknown"
    
    def check_common_ports(self, ip):
        """Check common ports on a host"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 3389]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        return open_ports
    
    def scan_network(self):
        """Main network scanning function"""
        try:
            network = ipaddress.IPv4Network(self.network, strict=False)
        except ValueError as e:
            print(f"❌ Invalid network: {e}")
            return
        
        print(f"🌐 Scanning network: {network}")
        print(f"📊 Host range: {network.network_address} - {network.broadcast_address}")
        print(f"⚡ Threads: {self.threads}, Timeout: {self.timeout}s")
        print(f"🎯 Checking {network.num_addresses} addresses...")
        print("-" * 60)
        
        # Ping sweep
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.ping_host, ip): ip for ip in network.hosts()}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.alive_hosts.append(result)
                    print(f"✅ Host alive: {result}")
        
        if not self.alive_hosts:
            print("🚫 No alive hosts found")
            return
        
        print(f"\n🔍 Found {len(self.alive_hosts)} alive hosts. Gathering details...")
        print("-" * 60)
        
        # Get detailed info for alive hosts
        for ip in self.alive_hosts:
            print(f"📋 Analyzing {ip}...")
            
            # Get hostname
            hostname = self.get_hostname(ip)
            
            # Check common ports
            ports = self.check_common_ports(ip)
            
            self.host_info[ip] = {
                'hostname': hostname,
                'open_ports': ports
            }
            
            print(f"   Hostname: {hostname}")
            if ports:
                print(f"   Open ports: {', '.join(map(str, ports))}")
            else:
                print(f"   Open ports: None found")
            print()
    
    def print_summary(self):
        """Print discovery summary"""
        print("=" * 60)
        print("🎯 NETWORK DISCOVERY SUMMARY")
        print("=" * 60)
        
        if not self.alive_hosts:
            print("🚫 No hosts discovered")
            return
        
        print(f"📊 Total hosts found: {len(self.alive_hosts)}\n")
        
        for ip, info in self.host_info.items():
            print(f"🖥️  Host: {ip}")
            print(f"   Hostname: {info['hostname']}")
            
            if info['open_ports']:
                print(f"   Services: {len(info['open_ports'])} ports open")
                port_services = []
                for port in info['open_ports']:
                    service = self.get_service_name(port)
                    port_services.append(f"{port}({service})")
                print(f"   Ports: {', '.join(port_services)}")
            else:
                print(f"   Services: No common ports open")
            print()
    
    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 3389: "RDP"
        }
        return services.get(port, "Unknown")

def main():
    parser = argparse.ArgumentParser(
        description="Educational Network Discovery Tool - Use only on authorized networks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python network_discovery.py 192.168.1.0/24
  python network_discovery.py 10.0.0.0/8 --threads 100
  python network_discovery.py 172.16.0.0/12 --timeout 5

⚠️  WARNING: Only use on networks you own or have explicit permission to scan!
        """
    )
    
    parser.add_argument("network", help="Network to scan (CIDR notation, e.g., 192.168.1.0/24)")
    parser.add_argument("--threads", "-t", type=int, default=50, help="Number of threads (default: 50)")
    parser.add_argument("--timeout", type=int, default=3, help="Timeout in seconds (default: 3)")
    
    args = parser.parse_args()
    
    # Basic validation for private networks
    try:
        network = ipaddress.IPv4Network(args.network, strict=False)
        if not network.is_private:
            response = input(f"⚠️  You are about to scan public network {network}. Do you have permission? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("🛑 Scan cancelled. Only scan networks you own or have permission to test.")
                sys.exit(1)
    except ValueError as e:
        print(f"❌ Invalid network format: {e}")
        sys.exit(1)
    
    print("🔒 Educational Network Discovery Tool v1.0")
    print("⚠️  For educational and authorized testing purposes only!\n")
    
    # Create and run scanner
    discovery = NetworkDiscovery(
        network=args.network,
        threads=args.threads,
        timeout=args.timeout
    )
    
    try:
        start_time = time.time()
        discovery.scan_network()
        discovery.print_summary()
        
        elapsed = time.time() - start_time
        print(f"⏰ Scan completed in {elapsed:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()