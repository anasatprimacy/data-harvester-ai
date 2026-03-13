#!/usr/bin/env python3
"""
Test script to validate API connections and environment setup
"""

import sys
from config.env_config import config
from utils.firecrawl_client import FirecrawlClient

def test_environment_config():
    """Test environment configuration loading"""
    print("Testing Environment Configuration...")
    print("=" * 50)
    
    # Test API key validation
    validation = config.validate_required_keys()
    print("API Key Status:")
    for service, status in validation.items():
        status_icon = "✅" if status else "❌"
        print(f"  {service}: {status_icon}")
    
    missing = config.get_missing_keys()
    if missing:
        print(f"\n⚠️  Missing API keys: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All required API keys are present!")
        return True

def test_firecrawl_connection():
    """Test Firecrawl API connection"""
    print("\nTesting Firecrawl API Connection...")
    print("=" * 50)
    
    if not config.firecrawl_api_key:
        print("❌ Firecrawl API key not found")
        return False
    
    try:
        client = FirecrawlClient()
        # Test with a simple URL
        test_url = "https://httpbin.org/html"
        result = client.scrape(test_url)
        
        if result:
            print("✅ Firecrawl API connection successful!")
            print(f"   Sample content length: {len(result)} characters")
            return True
        else:
            print("❌ Firecrawl API returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ Firecrawl API connection failed: {e}")
        return False

def test_google_apis():
    """Test Google API connections"""
    print("\nTesting Google APIs...")
    print("=" * 50)
    
    success = True
    
    if not config.google_places_api_key:
        print("❌ Google Places API key not found")
        success = False
    else:
        print("✅ Google Places API key found")
    
    if not config.google_search_api_key:
        print("❌ Google Search API key not found")
        success = False
    else:
        print("✅ Google Search API key found")
    
    if not config.google_search_engine_id:
        print("❌ Google Search Engine ID not found")
        success = False
    else:
        print("✅ Google Search Engine ID found")
    
    return success

def main():
    """Run all tests"""
    print("🚀 Data Harvester - API Connection Test")
    print("=" * 60)
    
    tests = [
        ("Environment Config", test_environment_config),
        ("Firecrawl API", test_firecrawl_connection),
        ("Google APIs", test_google_apis),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! Ready for production deployment.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
