# 🚀 Enhanced Chad - Advanced Google Dorking Tool

**Enhanced version of Chad with Tor integration, advanced rate limiting, and comprehensive user agent rotation**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Custom-red.svg)](LICENSE)
[![Tor](https://img.shields.io/badge/Tor-Integrated-purple.svg)](https://www.torproject.org/)
[![OSINT](https://img.shields.io/badge/OSINT-Ready-green.svg)](https://github.com/jarek-bir/chad)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [Dork Collections](#dork-collections)
- [Credits](#credits)
- [Security & Ethics](#security--ethics)

## 🎯 Overview

Enhanced Chad is a sophisticated Google Dorking tool designed for cybersecurity professionals, bug bounty hunters, and OSINT researchers. Built upon the excellent foundation of [Ivan Sincek's Chad](https://github.com/ivan-sincek/chad), this enhanced version adds:

- **🧅 Tor Integration**: Complete anonymity with automatic IP rotation
- **⚡ Advanced Rate Limiting**: Intelligent algorithms to evade Google blocks
- **🎭 User Agent Rotation**: 1000+ realistic browser signatures
- **📊 Performance Monitoring**: Comprehensive metrics and analytics
- **🗂️ Specialized Dork Collections**: 8000+ categorized Google dorks

## ✨ Features

### 🔒 **Enhanced Anonymity**
- **Tor Integration**: Automatic Tor service management and SOCKS5 proxy
- **IP Rotation**: Intelligent rotation based on error patterns
- **User Agent Cycling**: 1000+ real browser user agents
- **Header Randomization**: Realistic HTTP headers for each request

### ⚡ **Intelligent Rate Limiting**
- **Adaptive Timing**: Dynamic delays based on success/failure rates
- **Google Block Evasion**: Smart detection and response to 429 errors
- **Performance Optimization**: Automatic tuning for optimal speed
- **Metrics Export**: Detailed JSON reports for analysis

### 🔍 **Advanced Google Dorking**
- **8000+ Dorks**: Comprehensive collections across 8 categories
- **Targeted Searches**: Specialized dorks for specific platforms (X.com, etc.)
- **Result Filtering**: Blacklist and whitelist capabilities
- **Parallel Processing**: Multi-threaded search execution

## 🚀 Installation

### Prerequisites

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip tor

# Install Python dependencies
pip3 install -r requirements.txt
```

### Quick Installation

```bash
# Clone the enhanced repository
git clone https://github.com/jarek-bir/chad.git
cd chad

# Install dependencies
pip3 install requests nagooglesearch alive-progress python-dateutil

# Download user agents
wget -O user-agents.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/User-Agents/UserAgents.fuzz.txt

# Test installation
python3 run_enhanced_chad.py --check-deps
```

## ⚡ Quick Start

### 1. **Check System Status**
```bash
# Verify all dependencies
python3 run_enhanced_chad.py --check-deps

# Test Tor integration
python3 run_enhanced_chad.py --test-tor

# List available dork collections
python3 run_enhanced_chad.py --list-dorks
```

### 2. **Basic Google Dorking**
```bash
# Simple search with Tor
python3 src/chad/main.py \
    --queries "site:example.com filetype:pdf" \
    --use-tor \
    --total-results 10

# Multiple queries from file
python3 src/chad/main.py \
    --queries-from-file src/dorks/bug_bounty_dorks.txt \
    --use-tor \
    --total-results 50
```

### 3. **Advanced Search with Custom Settings**
```bash
# Enhanced search with full configuration
python3 src/chad/main.py \
    --queries "intext:\"API key\" filetype:env" \
    --use-tor \
    --tor-rotation 5 \
    --total-results 100 \
    --minimum-queries 10 \
    --maximum-queries 15 \
    --output results.json
```

## 🔧 Advanced Usage

### **Tor Configuration**
```bash
# Basic Tor usage
python3 src/chad/main.py --queries "site:target.com" --use-tor

# Custom Tor rotation (rotate IP every 3 queries)
python3 src/chad/main.py --queries "site:target.com" --use-tor --tor-rotation 3
```

### **Rate Limiting Control**
```bash
# Conservative rate limiting (slower but safer)
python3 src/chad/main.py \
    --queries "sensitive search" \
    --minimum-queries 20 \
    --maximum-queries 40 \
    --use-tor

# Aggressive search (faster but higher block risk)
python3 src/chad/main.py \
    --queries "quick search" \
    --minimum-queries 1 \
    --maximum-queries 3 \
    --use-tor
```

### **Specialized Searches**
```bash
# Bug bounty focused
python3 src/chad/main.py \
    --queries-from-file src/dorks/bug_bounty_dorks.txt \
    --use-tor \
    --total-results 200 \
    --output bug_bounty_results.json

# Social media intelligence
python3 src/chad/main.py \
    --queries-from-file src/dorks/social_media_dorks.txt \
    --use-tor \
    --total-results 100 \
    --output social_intel.json
```

## 🗂️ Dork Collections

Enhanced Chad includes 8000+ specialized Google dorks across multiple categories:

| Collection | Dorks | Purpose |
|-----------|-------|---------|
| **🔧 Bug Bounty** | 97 | Subdomain enumeration, vulnerability discovery |
| **🛡️ Web App Security** | 199 | Authentication bypass, error disclosure |
| **💳 Credentials** | 87 | API keys, tokens, exposed secrets |
| **📄 Sensitive Documents** | 83 | Configuration files, backups |
| **📱 Social Media** | 126 | Contact information, profiles |
| **🏗️ Infrastructure** | 62 | Admin panels, services |
| **🔍 Bug Hunting** | 197 | General vulnerability research |
| **🌐 Web Application** | 64 | Additional web testing vectors |

### **Using Dork Collections**
```bash
# List all collections
python3 run_enhanced_chad.py --list-dorks

# Use specific collection
python3 src/chad/main.py \
    --queries-from-file src/dorks/bug_bounty_dorks.txt \
    --site target.com \
    --use-tor
```

## 👏 Credits

### **Original Creator**
**Enhanced Chad** is built upon the excellent foundation of **Chad** by:
- **[Ivan Sincek](https://github.com/ivan-sincek)** - Original Chad creator
- **Original Repository**: [https://github.com/ivan-sincek/chad](https://github.com/ivan-sincek/chad)

### **Enhanced Version**
- **[Jarek Bir](https://github.com/jarek-bir)** - Enhanced version with Tor integration and advanced features
- **Enhanced Repository**: [https://github.com/jarek-bir/chad](https://github.com/jarek-bir/chad)

### **Special Thanks**
- Ivan Sincek for creating the robust foundation
- The Tor Project for anonymity infrastructure
- Security research community for dork collections
- Contributors and testers

## 🛡️ Security & Ethics

⚠️ **Important**: Enhanced Chad is designed for legitimate security research and OSINT purposes only.

**✅ Approved Uses:**
- Bug bounty research on authorized targets
- Penetration testing with proper authorization
- Academic research and education
- Personal cybersecurity awareness
- OSINT investigations within legal boundaries

**❌ Prohibited Uses:**
- Unauthorized access attempts
- Malicious reconnaissance
- Privacy violations
- Illegal data harvesting
- Any activity violating terms of service

## 📄 License

This project builds upon Ivan Sincek's Chad and maintains compatibility with the original licensing terms. Please refer to the [LICENSE](LICENSE) file for detailed information.

**Important**: This enhanced version adds significant new functionality while respecting the original work and licensing.

---

**⚠️ Disclaimer**: This tool is for authorized security testing and research only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for misuse of this tool.

**🛡️ Ethics First**: Always ensure you have proper authorization before conducting security research on any target.
