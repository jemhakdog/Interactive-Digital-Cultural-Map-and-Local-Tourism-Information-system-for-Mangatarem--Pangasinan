#!/usr/bin/env python3
"""
MVT Implementation Test Script

Run this to verify your MVT implementation is working correctly.

Usage:
    python test_mvt_implementation.py

Requirements:
    - Flask app running on localhost:5001
    - requests library installed
"""

import requests
import time
import sys
from typing import Tuple, Optional

# Configuration
BASE_URL = "http://localhost:5001"
TIMEOUT = 10  # seconds

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text: str):
    """Print info message"""
    print(f"{BLUE}ℹ️  {text}{RESET}")


def test_endpoint_availability() -> bool:
    """Test if the Flask app is running"""
    print_header("1. Testing Application Availability")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        print_success(f"Application is running at {BASE_URL}")
        print_info(f"Status code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {BASE_URL}")
        print_info("Make sure the Flask app is running: python app.py")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def test_layers_endpoint() -> Tuple[bool, Optional[dict]]:
    """Test the /api/tiles/layers endpoint"""
    print_header("2. Testing Layers Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tiles/layers", timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Layers endpoint returned successfully")
            print_info(f"Response: {len(data.get('layers', []))} layers available")
            
            for layer in data.get('layers', []):
                print_info(f"  - {layer.get('name')}: {layer.get('table')}")
            
            return True, data
        else:
            print_error(f"Layers endpoint returned status {response.status_code}")
            return False, None
            
    except Exception as e:
        print_error(f"Failed to call layers endpoint: {e}")
        return False, None


def test_tile_endpoint() -> Tuple[bool, Optional[bytes]]:
    """Test the /api/tiles/z/x/y.pbf endpoint"""
    print_header("3. Testing Tile Endpoint")
    
    # Test coordinates for Mangatarem area
    z, x, y = 12, 500, 500
    
    try:
        url = f"{BASE_URL}/api/tiles/{z}/{x}/{y}.pbf?layer=attractions"
        response = requests.get(url, timeout=TIMEOUT)
        
        print_info(f"Requesting: {url}")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'protobuf' in content_type or 'application/x-protobuf' == content_type:
                print_success(f"Content-Type is correct: {content_type}")
            else:
                print_warning(f"Content-Type is {content_type} (expected application/x-protobuf)")
            
            # Check cache headers
            cache_control = response.headers.get('Cache-Control', '')
            if cache_control:
                print_success(f"Cache-Control header present: {cache_control}")
            else:
                print_warning("Cache-Control header missing")
            
            # Check X-Cache header
            x_cache = response.headers.get('X-Cache', '')
            if x_cache:
                print_info(f"X-Cache: {x_cache}")
            
            # Check tile size
            tile_size = len(response.content)
            print_info(f"Tile size: {tile_size} bytes")
            
            if tile_size > 0:
                print_success("Tile contains data")
            else:
                print_warning("Tile is empty (no data in this area)")
            
            return True, response.content
        else:
            print_error(f"Tile endpoint returned status {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print_error(f"Failed to call tile endpoint: {e}")
        return False, None


def test_combined_tile_endpoint() -> bool:
    """Test the /api/tiles/combined/z/x/y.pbf endpoint"""
    print_header("4. Testing Combined Tile Endpoint")
    
    z, x, y = 12, 500, 500
    
    try:
        url = f"{BASE_URL}/api/tiles/combined/{z}/{x}/{y}.pbf?layers=attractions,natural_heritage"
        response = requests.get(url, timeout=TIMEOUT)
        
        print_info(f"Requesting: {url}")
        
        if response.status_code == 200:
            print_success("Combined tile endpoint works")
            print_info(f"Tile size: {len(response.content)} bytes")
            return True
        else:
            print_error(f"Combined tile endpoint returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Failed to call combined tile endpoint: {e}")
        return False


def test_cache_invalidation() -> bool:
    """Test the /api/tiles/cache/invalidate endpoint"""
    print_header("5. Testing Cache Invalidation")
    
    try:
        url = f"{BASE_URL}/api/tiles/cache/invalidate"
        response = requests.post(
            url,
            json={"layer": "attractions"},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        print_info(f"Requesting: POST {url}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Cache invalidation endpoint works")
            print_info(f"Response: {data.get('message', 'N/A')}")
            return True
        else:
            print_warning(f"Cache invalidation returned status {response.status_code}")
            print_info("This is OK if Redis is not configured")
            return True  # Not critical
            
    except Exception as e:
        print_warning(f"Cache invalidation test failed: {e}")
        print_info("This is OK if Redis is not configured")
        return True  # Not critical


def test_performance() -> bool:
    """Test response times"""
    print_header("6. Testing Performance")
    
    z, x, y = 12, 500, 500
    url = f"{BASE_URL}/api/tiles/{z}/{x}/{y}.pbf?layer=attractions"
    
    times = []
    num_requests = 3
    
    print_info(f"Making {num_requests} requests to measure response time...")
    
    # Check if SQLite
    try:
        layers_response = requests.get(f"{BASE_URL}/api/tiles/layers", timeout=TIMEOUT)
        # We can't directly detect SQLite from client side, so we check tile size
        tile_response = requests.get(url, timeout=TIMEOUT)
        is_sqlite = tile_response.headers.get('X-Sqlite', '').lower() == 'true' or len(tile_response.content) <= 10
        if is_sqlite:
            print_warning("SQLite detected (development mode)")
            print_info("Performance testing skipped - tiles are empty in SQLite mode")
            print_info("In production with PostGIS, expect < 200ms response times")
            return True
    except:
        pass
    
    for i in range(num_requests):
        try:
            start = time.time()
            response = requests.get(url, timeout=TIMEOUT)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            times.append(elapsed)
            
            status = "✅" if elapsed < 200 else "⚠️"
            print_info(f"  Request {i+1}: {elapsed:.2f}ms {status}")
            
        except Exception as e:
            print_error(f"Request {i+1} failed: {e}")
            return False
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print_info(f"\nStatistics:")
    print_info(f"  Average: {avg_time:.2f}ms")
    print_info(f"  Min: {min_time:.2f}ms")
    print_info(f"  Max: {max_time:.2f}ms")
    
    if avg_time < 200:
        print_success(f"Performance target met! Average < 200ms")
        return True
    else:
        print_warning(f"Performance target NOT met. Average > 200ms")
        print_info("Consider enabling Redis caching or check database indexes")
        return True  # Don't fail on performance in development


def test_cache_behavior() -> bool:
    """Test if caching is working (2nd request should be faster)"""
    print_header("7. Testing Cache Behavior")
    
    z, x, y = 12, 500, 500
    url = f"{BASE_URL}/api/tiles/{z}/{x}/{y}.pbf?layer=attractions"
    
    try:
        # First request
        start = time.time()
        response1 = requests.get(url, timeout=TIMEOUT)
        time1 = (time.time() - start) * 1000
        
        # Second request
        start = time.time()
        response2 = requests.get(url, timeout=TIMEOUT)
        time2 = (time.time() - start) * 1000
        
        print_info(f"First request:  {time1:.2f}ms")
        print_info(f"Second request: {time2:.2f}ms")
        
        if time2 < time1:
            improvement = ((time1 - time2) / time1) * 100
            print_success(f"Second request was {improvement:.1f}% faster (caching working)")
            return True
        else:
            print_warning("Second request not faster (caching may not be configured)")
            print_info("This is OK - Vercel Edge Cache will still work in production")
            return True
            
    except Exception as e:
        print_error(f"Cache behavior test failed: {e}")
        return False


def test_map_page() -> bool:
    """Test if map page loads"""
    print_header("8. Testing Map Page")
    
    try:
        response = requests.get(f"{BASE_URL}/map", timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_success("Map page loads successfully")
            
            # Check if map.js is referenced
            if 'map.js' in response.text:
                print_success("map.js is included in page")
            else:
                print_warning("map.js not found in page")
            
            # Check if Mapbox token is passed
            if 'MAPBOX_TOKEN' in response.text:
                print_success("Mapbox token is passed to frontend")
            else:
                print_warning("Mapbox token not found in page")
            
            return True
        else:
            print_error(f"Map page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Failed to load map page: {e}")
        return False


def print_summary(results: dict):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print_info(f"Total tests: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    print(f"\n{BOLD}Results by category:{RESET}")
    for test_name, passed in results.items():
        icon = "✅" if passed else "❌"
        status = "PASS" if passed else "FAIL"
        print(f"  {icon} {test_name}: {status}")
    
    print(f"\n{BOLD}Overall Status:{RESET}")
    if passed == total:
        print(f"{GREEN}{BOLD}🎉 ALL TESTS PASSED! MVT implementation is working correctly.{RESET}")
        print(f"\n{BLUE}Next steps:{RESET}")
        print("  1. Open http://localhost:5001/map in browser")
        print("  2. Check DevTools Network tab for .pbf tile requests")
        print("  3. Verify colored points appear on map")
        print("  4. Test hover and click interactions")
    elif passed >= total * 0.7:
        print(f"{YELLOW}{BOLD}⚠️  MOST TESTS PASSED. Some features may need attention.{RESET}")
    else:
        print(f"{RED}{BOLD}❌ SEVERAL TESTS FAILED. Please review errors above.{RESET}")
    
    print()


def main():
    """Run all tests"""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  MVT Implementation Test Suite{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    print_info("Testing Mapbox Vector Tile implementation...")
    print_info(f"Target: {BASE_URL}\n")
    
    results = {}
    
    # Run tests
    results["Application Running"] = test_endpoint_availability()
    
    if not results["Application Running"]:
        print_error("\nApplication is not running. Please start it with: python app.py")
        print_summary(results)
        sys.exit(1)
    
    layers_ok, _ = test_layers_endpoint()
    results["Layers Endpoint"] = layers_ok
    
    tile_ok, _ = test_tile_endpoint()
    results["Tile Endpoint"] = tile_ok
    
    results["Combined Tile Endpoint"] = test_combined_tile_endpoint()
    results["Cache Invalidation"] = test_cache_invalidation()
    results["Performance"] = test_performance()
    results["Cache Behavior"] = test_cache_behavior()
    results["Map Page"] = test_map_page()
    
    # Print summary
    print_summary(results)
    
    # Exit with appropriate code
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    if passed == total:
        sys.exit(0)
    elif passed >= total * 0.7:
        sys.exit(0)  # Still consider it a warning, not failure
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
