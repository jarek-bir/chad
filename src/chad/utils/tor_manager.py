#!/usr/bin/env python3

"""
Tor IP Manager for Chad Google Dorking Tool
Enhanced with automatic IP rotation and user agent cycling
"""

import os
import sys
import time
import random
import subprocess
import requests
from typing import List, Optional, Dict, Any

class TorManager:
    """Manages Tor service and IP rotation for enhanced anonymity"""
    
    def __init__(self, user_agents_file: str = "user-agents.txt", 
                 tor_port: int = 9050, control_port: int = 9051):
        self.tor_port = tor_port
        self.control_port = control_port
        self.user_agents_file = user_agents_file
        self.user_agents: List[str] = []
        self.current_ip: Optional[str] = None
        self.tor_proxy = {
            'http': f'socks5://127.0.0.1:{self.tor_port}',
            'https': f'socks5://127.0.0.1:{self.tor_port}'
        }
        
        # Load user agents
        self._load_user_agents()
        
        # Initialize Tor
        self._setup_tor()
    
    def _load_user_agents(self) -> None:
        """Load user agents from file"""
        try:
            # Try multiple possible paths for user-agents.txt
            possible_paths = [
                self.user_agents_file,
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'user-agents.txt'),
                os.path.join(os.getcwd(), 'user-agents.txt'),
                '/home/jarek/Tools/chad/user-agents.txt'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        self.user_agents = [line.strip() for line in f.readlines() if line.strip()]
                    print(f"[+] Loaded {len(self.user_agents)} user agents from {path}")
                    return
            
            # Fallback user agents if file not found
            self.user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]
            print(f"[!] User agents file not found, using {len(self.user_agents)} fallback user agents")
            
        except Exception as e:
            print(f"[!] Error loading user agents: {e}")
            self.user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36']
    
    def _setup_tor(self) -> None:
        """Setup and start Tor service"""
        try:
            print("[*] Setting up Tor service...")
            
            # Check if Tor is installed
            tor_check = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if tor_check.returncode != 0:
                print("[!] Tor is not installed. Installing...")
                self._install_tor()
            
            # Start Tor service
            self._start_tor_service()
            
            # Wait for Tor to initialize
            print("[*] Waiting for Tor to initialize...")
            time.sleep(5)
            
            # Get initial IP
            self.current_ip = self._get_current_ip()
            if self.current_ip:
                print(f"[+] Tor initialized successfully. Current IP: {self.current_ip}")
            else:
                print("[!] Warning: Could not verify Tor IP")
                
        except Exception as e:
            print(f"[!] Error setting up Tor: {e}")
    
    def _install_tor(self) -> None:
        """Install Tor package"""
        try:
            distro_check = subprocess.run(['lsb_release', '-si'], capture_output=True, text=True)
            distro = distro_check.stdout.strip().lower()
            
            if 'ubuntu' in distro or 'debian' in distro:
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], check=True)
            elif 'fedora' in distro or 'rhel' in distro or 'centos' in distro:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'tor'], check=True)
            elif 'arch' in distro:
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'tor'], check=True)
            else:
                print("[!] Unknown distribution. Please install Tor manually.")
                
        except subprocess.CalledProcessError as e:
            print(f"[!] Error installing Tor: {e}")
            raise
    
    def _start_tor_service(self) -> None:
        """Start Tor service"""
        try:
            # Stop any existing Tor service
            subprocess.run(['sudo', 'systemctl', 'stop', 'tor'], 
                         capture_output=True, text=True)
            
            # Start Tor service
            result = subprocess.run(['sudo', 'systemctl', 'start', 'tor'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[+] Tor service started successfully")
            else:
                print(f"[!] Error starting Tor service: {result.stderr}")
                # Try alternative method
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
        except Exception as e:
            print(f"[!] Error managing Tor service: {e}")
    
    def _get_current_ip(self) -> Optional[str]:
        """Get current IP address through Tor"""
        try:
            response = requests.get('http://httpbin.org/ip', 
                                  proxies=self.tor_proxy, 
                                  timeout=10)
            if response.status_code == 200:
                return response.json().get('origin', 'Unknown')
        except requests.RequestException:
            try:
                # Fallback to different IP checking service
                response = requests.get('https://api.ipify.org?format=json', 
                                      proxies=self.tor_proxy, 
                                      timeout=10)
                if response.status_code == 200:
                    return response.json().get('ip', 'Unknown')
            except:
                pass
        return None
    
    def rotate_ip(self) -> bool:
        """Rotate Tor IP address"""
        try:
            print("[*] Rotating Tor IP address...")
            old_ip = self.current_ip
            
            # Restart Tor service to get new IP
            subprocess.run(['sudo', 'systemctl', 'restart', 'tor'], 
                         capture_output=True, text=True)
            
            # Wait for service to restart
            time.sleep(5)
            
            # Get new IP
            new_ip = self._get_current_ip()
            
            if new_ip and new_ip != old_ip:
                self.current_ip = new_ip
                print(f"[+] IP rotated successfully: {old_ip} -> {new_ip}")
                return True
            else:
                print(f"[!] IP rotation may have failed. Current IP: {new_ip}")
                return False
                
        except Exception as e:
            print(f"[!] Error rotating IP: {e}")
            return False
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        if self.user_agents:
            return random.choice(self.user_agents)
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def get_proxy_config(self) -> Dict[str, str]:
        """Get proxy configuration for requests"""
        return self.tor_proxy.copy()
    
    def get_session_config(self) -> Dict[str, Any]:
        """Get complete session configuration with proxy and user agent"""
        return {
            'proxies': self.get_proxy_config(),
            'headers': {
                'User-Agent': self.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            },
            'timeout': 30
        }
    
    def check_tor_status(self) -> bool:
        """Check if Tor is working properly"""
        try:
            ip = self._get_current_ip()
            return ip is not None
        except:
            return False
    
    def stop_tor(self) -> None:
        """Stop Tor service"""
        try:
            subprocess.run(['sudo', 'systemctl', 'stop', 'tor'], 
                         capture_output=True, text=True)
            print("[+] Tor service stopped")
        except Exception as e:
            print(f"[!] Error stopping Tor: {e}")

# Convenience functions for Chad integration
def create_tor_manager() -> TorManager:
    """Create and initialize Tor manager"""
    return TorManager()

def get_enhanced_session_config() -> Dict[str, Any]:
    """Get enhanced session configuration with Tor + User Agent rotation"""
    tor_manager = create_tor_manager()
    return tor_manager.get_session_config()

if __name__ == "__main__":
    # Test the Tor manager
    print("Testing Tor Manager...")
    
    tor_manager = TorManager()
    
    if tor_manager.check_tor_status():
        print("✓ Tor is working correctly")
        
        # Test IP rotation
        print("\nTesting IP rotation...")
        tor_manager.rotate_ip()
        
        # Test user agent rotation
        print(f"\nRandom User Agent: {tor_manager.get_random_user_agent()}")
        
        # Show session config
        config = tor_manager.get_session_config()
        print(f"\nProxy Config: {config['proxies']}")
        print(f"User Agent: {config['headers']['User-Agent']}")
        
    else:
        print("✗ Tor is not working properly")
