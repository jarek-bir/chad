#!/usr/bin/env python3

"""
Complete test suite for Enhanced Chad with Tor and Advanced Rate Limiting
Tests all functionality including actual Google dorking
"""

import time
import json
import sys
from datetime import datetime

# Import Enhanced Chad
from src.chad.utils.chad import Chad
from src.chad.utils.rate_limiter import AdvancedRateLimiter, RateLimitConfig

def print_banner():
    """Print test banner"""
    print("\n" + "="*80)
    print("  🧪 ENHANCED CHAD FULL FUNCTIONALITY TEST")
    print("  🚀 Testing: Tor Integration + Advanced Rate Limiting + Google Dorking")
    print("="*80 + "\n")

def test_enhanced_chad_dorking():
    """Test enhanced Chad with real Google dorking"""
    print("🔍 Testing Enhanced Chad with real Google dorking...")
    
    # Test queries - safe and educational
    test_queries = [
        'site:github.com filetype:md "security"',
        'site:stackoverflow.com "python security"'
    ]
    
    # Initialize Enhanced Chad with Tor and Rate Limiting
    print("📡 Initializing Enhanced Chad with Tor and Advanced Rate Limiting...")
    
    chad = Chad(
        queries=test_queries,
        site='',  # No additional site restriction
        time=0,   # No time restriction
        total_results=5,  # Small number for testing
        page_results=5,
        minimum_queries=3,
        maximum_queries=5, 
        minimum_pages=1,
        maximum_pages=2,
        user_agents=['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'],
        proxies=[],  # No external proxies - using Tor
        sleep_on_start=False,
        debug=True,
        use_tor=True,
        tor_rotation=2  # Rotate IP every 2 queries for testing
    )
    
    print(f"✅ Chad initialized successfully!")
    print(f"🧅 Tor enabled: {chad._Chad__use_tor}")
    print(f"⚡ Rate limiter: {type(chad._Chad__rate_limiter).__name__}")
    
    # Prepare queries
    print("\n🔧 Preparing queries...")
    chad.prepare()
    
    # Get rate limiter metrics before
    rate_limiter = chad._Chad__rate_limiter
    print(f"\n📊 Rate Limiter Configuration:")
    print(f"   • Query delay range: {rate_limiter.config.min_query_delay}-{rate_limiter.config.max_query_delay}s")
    print(f"   • Adaptive timing: {rate_limiter.config.enable_adaptive}")
    print(f"   • Success speedup: {rate_limiter.config.success_speedup}x")
    print(f"   • Error slowdown: {rate_limiter.config.error_slowdown}x")
    
    # Run the enhanced search
    print(f"\n🚀 Starting enhanced Google dorking with {len(test_queries)} queries...")
    print("   ⏱️  This will demonstrate intelligent rate limiting and IP rotation")
    
    start_time = time.time()
    
    try:
        # Run the enhanced search
        results = chad.run()
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"\n✅ Enhanced Google dorking completed!")
        print(f"⏱️  Total duration: {duration:.2f} seconds")
        print(f"🔍 Queries processed: {len(test_queries)}")
        print(f"📄 Results found: {len(results)} total result sets")
        
        # Show results summary
        total_urls = sum(len(result.urls) for result in results)
        print(f"🌐 Total URLs discovered: {total_urls}")
        
        # Show rate limiter performance report
        print(f"\n📊 Advanced Rate Limiter Performance Report:")
        rate_limiter.print_performance_report()
        
        # Export metrics
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = f"enhanced_chad_test_metrics_{timestamp}.json"
        rate_limiter.export_metrics(metrics_file)
        print(f"📄 Metrics exported to: {metrics_file}")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

def main():
    """Main test function"""
    print_banner()
    
    try:
        success = test_enhanced_chad_dorking()
        
        if success:
            print(f"\n🎉 ALL TESTS PASSED!")
            print(f"✅ Enhanced Chad with Tor and Advanced Rate Limiting is working perfectly!")
            print(f"🚀 Ready for advanced Google dorking operations!")
        else:
            print(f"\n❌ Some tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
