# Enhanced Chad - Google Dorking Tool with Tor Integration

Enhanced version of the Chad Google Dorking tool with integrated Tor support for improved anonymity and comprehensive user agent rotation.

## 🚀 New Features

### 🧅 Tor Integration
- **Automatic IP Rotation**: Rotate Tor IP addresses every N queries
- **Enhanced Anonymity**: Route all traffic through Tor network
- **Intelligent Rate Limiting**: Better handling of Google rate limits
- **Automatic Tor Management**: Install and configure Tor automatically

### 🎭 Advanced User Agent Rotation
- **900+ User Agents**: Comprehensive collection from real browsers
- **Smart Rotation**: Automatic cycling through different user agents
- **Realistic Headers**: Additional HTTP headers for better camouflage

### 📚 Enhanced Google Dorks Collections
- **8 Specialized Categories**: 643 total Google Dorks
- **Categorized by Purpose**: Credentials, vulnerabilities, files, etc.
- **Bug Bounty Focused**: Dorks specifically for security research

## 📋 Requirements

### Dependencies
```bash
pip install requests nagooglesearch alive-progress python-dateutil
```

### System Requirements (for Tor)
- Linux/Unix system
- sudo access (for Tor installation/management)
- Tor package (auto-installed if missing)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd chad
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tor** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt install tor
   
   # Fedora/RHEL
   sudo dnf install tor
   
   # Arch Linux
   sudo pacman -S tor
   ```

## 🚀 Usage

### Basic Usage (Original Chad)
```bash
python run_enhanced_chad.py -- -q 'intext:password' -o results.json
```

### With Tor Integration
```bash
python run_enhanced_chad.py -- -q 'intext:password' -tor -tr-rot 5 -o results.json
```

### Using Dork Collections
```bash
python run_enhanced_chad.py -- -q src/dorks/credentials_dorks.txt -tor -o results.json
```

### Advanced Example
```bash
python run_enhanced_chad.py -- \
  -q src/dorks/web_app_security_dorks.txt \
  -s '*.github.com' \
  -tor \
  -tr-rot 3 \
  -tr 100 \
  -o github_security_results.json
```

## 📖 Command Line Options

### New Tor Options
- `-tor, --use-tor`: Enable Tor for enhanced anonymity
- `-tr-rot, --tor-rotation`: Number of queries after which to rotate Tor IP (default: 10)

### Original Chad Options
- `-q, --queries`: File containing Google Dorks or single query
- `-s, --site`: Domain(s) to search
- `-t, --time`: Get results not older than specified months
- `-tr, --total-results`: Total number of unique results (default: 100)
- `-pr, --page-results`: Number of results per page
- `-o, --out`: Output file
- `-x, --proxies`: File containing web proxies
- `-a, --user-agents`: User agents to use
- `-nsos, --no-sleep-on-start`: Disable safety sleep
- `-dbg, --debug`: Enable debug output

## 🗂️ Google Dorks Collections

### Available Collections (643 Total Dorks)
1. **credentials_dorks.txt** (64 dorks) - Login credentials and auth files
2. **social_media_dorks.txt** (101 dorks) - Social media and profiles
3. **web_app_security_dorks.txt** (89 dorks) - Web application vulnerabilities
4. **infrastructure_dorks.txt** (76 dorks) - Network infrastructure
5. **bug_bounty_dorks.txt** (70 dorks) - Bug bounty specific searches
6. **sensitive_files_dorks.txt** (85 dorks) - Configuration and sensitive files
7. **database_dorks.txt** (58 dorks) - Database exposures
8. **government_dorks.txt** (100 dorks) - Government and official sites

### List Available Collections
```bash
python run_enhanced_chad.py --list-dorks
```

## 🧪 Testing & Diagnostics

### Check Dependencies
```bash
python run_enhanced_chad.py --check-deps
```

### Test Tor Functionality
```bash
python run_enhanced_chad.py --check-tor
python run_enhanced_chad.py --test-tor
```

## 🛡️ Security & Privacy Features

### Tor Integration Benefits
- **IP Anonymization**: Hide your real IP address
- **Traffic Encryption**: All traffic routed through Tor network
- **Location Masking**: Appear to be browsing from different countries
- **Rate Limit Evasion**: Rotate IPs when hitting Google limits

### User Agent Rotation
- **Browser Diversity**: Mimic different browsers and operating systems
- **Realistic Headers**: Include accept-language, encoding, and other headers
- **Random Selection**: Pick different user agents for each request

### Rate Limiting Protection
- **Intelligent Delays**: Configurable sleep times between requests
- **Error Handling**: Automatic retry with IP rotation on rate limits
- **Proxy Failover**: Switch between different connection methods

## 🔧 Configuration

### Tor Configuration
The tool automatically manages Tor configuration, but you can customize:

```python
# In tor_manager.py
tor_manager = TorManager(
    user_agents_file="user-agents.txt",  # Custom user agents file
    tor_port=9050,                       # Tor SOCKS port
    control_port=9051                    # Tor control port
)
```

### Custom User Agents
Add your own user agents to `user-agents.txt` or use the comprehensive built-in collection.

## 📊 Output Format

Results are saved in JSON format with enhanced metadata:

```json
[
  {
    "query": "intext:password",
    "proxy": "socks5://127.0.0.1:9050",
    "urls": [
      "https://example.com/page1",
      "https://example.com/page2"
    ]
  }
]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📜 Legal Notice

This tool is for educational and authorized security testing purposes only. Users are responsible for complying with applicable laws and regulations. Do not use this tool for unauthorized access or malicious activities.

## 🙏 Credits

- **Original Chad**: [github.com/ivan-sincek/chad](https://github.com/ivan-sincek/chad)
- **Tor Project**: [torproject.org](https://www.torproject.org/)
- **Enhanced by**: AI Assistant with user input

## 📞 Support

For issues specific to the enhanced features, please check:
1. Tor installation and configuration
2. Python dependencies
3. Network connectivity
4. System permissions for Tor management

For original Chad functionality, refer to the original repository.
