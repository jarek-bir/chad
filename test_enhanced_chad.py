#!/usr/bin/env python3

"""
Test script for Enhanced Chad with Tor integration
"""

import os
import sys
import time

# Add source path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_functionality():
    """Test basic Chad functionality without Tor"""
    print("🧪 Testing Basic Chad Functionality...")
    
    try:
        from src.chad.utils import chad, config, validate
        print("✅ Chad modules imported successfully")
        
        # Test argument validation
        sys.argv = ['chad', '-q', 'intext:test', '-tr', '5']
        validator = validate.Validate()
        success, args = validator.validate_args()
        
        if success:
            print("✅ Argument validation passed")
            print(f"   Query: {args.queries[0]}")
            print(f"   Total results: {args.total_results}")
        else:
            print("❌ Argument validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing basic functionality: {e}")
        return False
    
    return True

def test_tor_manager():
    """Test Tor Manager functionality"""
    print("\n🧅 Testing Tor Manager...")
    
    try:
        from src.chad.utils.tor_manager import TorManager
        
        # Test initialization
        print("   Initializing Tor Manager...")
        tor_manager = TorManager()
        print("✅ Tor Manager initialized")
        
        # Test user agent rotation
        print("   Testing user agent rotation...")
        ua1 = tor_manager.get_random_user_agent()
        ua2 = tor_manager.get_random_user_agent()
        print(f"   UA1: {ua1[:50]}...")
        print(f"   UA2: {ua2[:50]}...")
        
        if ua1 != ua2:
            print("✅ User agent rotation working")
        else:
            print("⚠️  User agent rotation may not be working (could be random)")
        
        # Test proxy config
        proxy_config = tor_manager.get_proxy_config()
        print(f"   Proxy config: {proxy_config}")
        
        # Test session config
        session_config = tor_manager.get_session_config()
        print("✅ Session configuration generated")
        
        # Test Tor status
        if tor_manager.check_tor_status():
            print("✅ Tor is working")
            print(f"   Current IP: {tor_manager.current_ip}")
        else:
            print("⚠️  Tor status check failed (may not be properly configured)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Tor Manager: {e}")
        return False

def test_google_dorks():
    """Test Google Dorks collections"""
    print("\n📚 Testing Google Dorks Collections...")
    
    dorks_dir = os.path.join('src', 'dorks')
    if not os.path.exists(dorks_dir):
        print("❌ Dorks directory not found")
        return False
    
    total_dorks = 0
    collections = []
    
    for file in os.listdir(dorks_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(dorks_dir, file)
            try:
                with open(file_path, 'r') as f:
                    dorks = [line.strip() for line in f if line.strip()]
                    collections.append((file, len(dorks)))
                    total_dorks += len(dorks)
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
                return False
    
    print(f"✅ Found {len(collections)} dork collections with {total_dorks} total dorks")
    for name, count in sorted(collections):
        print(f"   • {name:<35} {count:>3} dorks")
    
    return True

def test_enhanced_chad_integration():
    """Test Enhanced Chad with Tor integration"""
    print("\n🚀 Testing Enhanced Chad Integration...")
    
    try:
        # Test import of enhanced Chad
        from src.chad.utils.chad import Chad
        from src.chad.utils.tor_manager import TorManager
        
        print("✅ Enhanced Chad imports successful")
        
        # Test Chad with Tor parameters
        test_queries = ['intext:test']
        chad_instance = Chad(
            queries=test_queries,
            site="",
            time=0,
            total_results=5,
            page_results=10,
            minimum_queries=1,
            maximum_queries=2,
            minimum_pages=1,
            maximum_pages=2,
            user_agents=['Mozilla/5.0 (Test)'],
            proxies=[],
            sleep_on_start=False,
            debug=True,
            use_tor=False,  # Don't actually use Tor in test
            tor_rotation=5
        )
        
        print("✅ Enhanced Chad instance created successfully")
        
        # Test query validation
        if chad_instance.prepare():
            print("✅ Query preparation successful")
        else:
            print("❌ Query preparation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Enhanced Chad integration: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Enhanced Chad Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Tor Manager", test_tor_manager),
        ("Google Dorks", test_google_dorks),
        ("Enhanced Integration", test_enhanced_chad_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced Chad is ready to use.")
        print("\n💡 Next steps:")
        print("1. Install Tor: sudo apt install tor")
        print("2. Test Tor: python run_enhanced_chad.py --test-tor")
        print("3. Run with Tor: python run_enhanced_chad.py -- -q 'intext:test' -tor")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
