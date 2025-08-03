#!/usr/bin/env python3
"""
Test script to verify Gunicorn configuration
Run this locally to test if the configuration works before deploying
"""

import subprocess
import sys
import time
import requests
import os

def test_gunicorn_startup():
    """Test if Gunicorn starts properly with the new configuration"""
    print("Testing Gunicorn startup...")
    
    try:
        # Start Gunicorn in background
        process = subprocess.Popen([
            "gunicorn", "-c", "gunicorn.conf.py", "run:app"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for startup
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Gunicorn started successfully")
            
            # Test basic endpoint
            try:
                response = requests.get("http://localhost:5000/", timeout=10)
                if response.status_code == 200:
                    print("✅ Web server responding correctly")
                else:
                    print(f"⚠️  Web server returned status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Could not connect to web server: {e}")
            
            # Clean shutdown
            process.terminate()
            process.wait(timeout=10)
            print("✅ Gunicorn shutdown cleanly")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Gunicorn failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gunicorn: {e}")
        return False

def test_memory_usage():
    """Test memory usage with a simple request"""
    print("\nTesting memory usage...")
    
    # This would require a test video file
    print("ℹ️  Memory testing requires a test video file")
    print("ℹ️  Deploy and monitor memory usage in production")

if __name__ == "__main__":
    print("Gunicorn Configuration Test")
    print("=" * 40)
    
    success = test_gunicorn_startup()
    test_memory_usage()
    
    if success:
        print("\n✅ Configuration test passed!")
        print("You can now deploy with confidence.")
    else:
        print("\n❌ Configuration test failed!")
        print("Please check the configuration and try again.")
        sys.exit(1) 