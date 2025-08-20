#!/usr/bin/env python3

"""
Enhanced Chad runner with Tor integration
Combines Chad Google Dorking with Tor IP rotation and advanced user agent cycling
"""

import os
import sys
import subprocess
import argparse

# Add the source path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    try:
        import nagooglesearch
    except ImportError:
        missing_deps.append("nagooglesearch")
    
    try:
        import alive_progress
    except ImportError:
        missing_deps.append("alive-progress")
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        return False
    
    return True

def check_tor_availability():
    """Check if Tor is available on the system"""
    try:
        result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print("[!] Tor is not installed on this system")
            print("[!] Install Tor using your package manager:")
            print("    Ubuntu/Debian: sudo apt install tor")
            print("    Fedora/RHEL:   sudo dnf install tor")
            print("    Arch:          sudo pacman -S tor")
            return False
    except Exception:
        return False

def show_banner():
    """Display enhanced Chad banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                       🚀 ENHANCED CHAD 🚀                        ║
║              Google Dorking Tool with Tor Integration             ║
║                                                                   ║
║  Features:                                                        ║
║  • Advanced Google Dorking capabilities                          ║
║  • Tor IP rotation for enhanced anonymity                        ║
║  • Comprehensive user agent rotation (900+ agents)               ║
║  • Intelligent rate limiting protection                          ║
║  • 640+ Google Dorks in 8 specialized categories                 ║
║                                                                   ║
║  Enhanced by: AI Assistant                                        ║
║  Original by: github.com/ivan-sincek/chad                        ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

def list_dork_files():
    """List available Google Dork files"""
    dork_dir = os.path.join(os.path.dirname(__file__), 'src', 'dorks')
    if os.path.exists(dork_dir):
        print("\n📁 Available Google Dork Collections:")
        for file in sorted(os.listdir(dork_dir)):
            if file.endswith('.txt'):
                file_path = os.path.join(dork_dir, file)
                try:
                    with open(file_path, 'r') as f:
                        line_count = sum(1 for line in f if line.strip())
                    print(f"   • {file:<30} ({line_count:>3} dorks)")
                except:
                    print(f"   • {file}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Chad Google Dorking Tool with Tor Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--check-deps', action='store_true', 
                       help='Check if all dependencies are installed')
    parser.add_argument('--check-tor', action='store_true', 
                       help='Check if Tor is available and working')
    parser.add_argument('--list-dorks', action='store_true', 
                       help='List available Google Dork collections')
    parser.add_argument('--test-tor', action='store_true',
                       help='Test Tor Manager functionality')
    
    # Standard Chad arguments
    parser.add_argument('chad_args', nargs='*', 
                       help='Arguments to pass to Chad (use -- to separate)')
    
    args = parser.parse_args()
    
    show_banner()
    
    if args.check_deps:
        if check_dependencies():
            print("✅ All dependencies are installed")
        else:
            sys.exit(1)
        return
    
    if args.check_tor:
        if check_tor_availability():
            print("✅ Tor is available")
            # Test Tor functionality
            try:
                from src.chad.utils.tor_manager import TorManager
                tor_manager = TorManager()
                if tor_manager.check_tor_status():
                    print("✅ Tor is working correctly")
                    print(f"📍 Current Tor IP: {tor_manager.current_ip}")
                else:
                    print("❌ Tor is installed but not working correctly")
            except Exception as e:
                print(f"❌ Error testing Tor: {e}")
        else:
            sys.exit(1)
        return
    
    if args.list_dorks:
        list_dork_files()
        return
    
    if args.test_tor:
        try:
            from src.chad.utils.tor_manager import TorManager
            print("🧅 Testing Tor Manager...")
            tor_manager = TorManager()
            print("✅ Tor Manager initialized successfully")
            print(f"📍 Current IP: {tor_manager.current_ip}")
            print("🔄 Testing IP rotation...")
            tor_manager.rotate_ip()
            print(f"📍 New IP: {tor_manager.current_ip}")
            print("🎭 Random User Agent:", tor_manager.get_random_user_agent()[:50] + "...")
        except Exception as e:
            print(f"❌ Error testing Tor Manager: {e}")
        return
    
    # Check dependencies before running Chad
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run Chad
    try:
        from src.chad.main import main as chad_main
        
        # If no arguments provided, show help
        if not args.chad_args:
            print("💡 Usage Examples:")
            print()
            print("   Basic usage:")
            print("   python run_enhanced_chad.py -- -q 'intext:password' -o results.json")
            print()
            print("   With Tor enabled:")
            print("   python run_enhanced_chad.py -- -q src/dorks/credentials_dorks.txt -tor -tr-rot 5 -o results.json")
            print()
            print("   Using dork file with site restriction:")
            print("   python run_enhanced_chad.py -- -q src/dorks/web_app_security_dorks.txt -s '*.github.com' -o github_results.json")
            print()
            print("   Show Chad help:")
            print("   python run_enhanced_chad.py -- -h")
            print()
            return
        
        # Set sys.argv to pass arguments to Chad
        sys.argv = ['chad'] + args.chad_args
        chad_main()
        
    except ImportError as e:
        print(f"❌ Error importing Chad: {e}")
        print("Make sure you're running from the correct directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running Chad: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
