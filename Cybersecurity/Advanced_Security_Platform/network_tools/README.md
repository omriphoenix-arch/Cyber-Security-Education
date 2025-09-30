# 🌐 Network Security Tools

This folder contains tools for network reconnaissance and security analysis.

## 📁 Tools Included

### `network_discovery.py`
- **Purpose**: Discover active devices on a network
- **Features**:
  - Ping sweep across network ranges
  - Multi-threaded scanning for speed
  - Host discovery and basic OS detection
  - Network mapping capabilities

**Usage:**
```bash
python network_discovery.py 192.168.1.0/24
python network_discovery.py 10.0.0.0/8 --threads 50
```

### `port_scanner.py`
- **Purpose**: Scan for open ports on target systems
- **Features**:
  - TCP port scanning
  - Service detection and banner grabbing
  - Multi-threaded scanning
  - Common port identification
  - Stealth scanning options

**Usage:**
```bash
python port_scanner.py 192.168.1.1 --ports 1-1000
python port_scanner.py scanme.nmap.org --common-ports
python port_scanner.py 127.0.0.1 --ports 22,80,443,3389
```

## ⚠️ Ethical Use Guidelines

**These tools are for authorized testing only:**
- Only scan networks and systems you own
- Obtain explicit permission before testing
- Use responsibly for security improvement
- Follow all applicable laws and regulations

## 🛡️ Security Best Practices

1. **Test in isolated environments** when learning
2. **Document your testing** for professional use
3. **Respect rate limits** to avoid disruption
4. **Report findings responsibly** if vulnerabilities are found

## 📚 Learning Resources

- Study network protocols (TCP/IP, UDP, ICMP)
- Learn about network security fundamentals
- Practice in dedicated lab environments
- Understand legal and ethical implications

---

*Use these tools to strengthen security, never to cause harm.*