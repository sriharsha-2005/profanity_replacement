#!/usr/bin/env python3
"""
Simple test script to verify Flask app can start
Run this to check if there are any import or initialization issues
"""

import sys
import os

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    
    try:
        # Test basic Flask app import
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test main processing module
        from python.main import process_video
        print("✅ Main processing module imported successfully")
        
        # Test audio processing modules
        from python.audio_processing.whisper_handler import transcriber
        print("✅ Whisper handler imported successfully")
        
        from python.audio_processing.edge_tts_handler import generate_speech
        print("✅ Edge TTS handler imported successfully")
        
        # Test text processing
        from python.text_processing.profanity_filter import filter_transcript
        print("✅ Profanity filter imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_startup():
    """Test if the Flask app can start"""
    print("\nTesting Flask app startup...")
    
    try:
        from app import app
        
        # Test if app has routes
        routes = list(app.url_map.iter_rules())
        print(f"✅ App has {len(routes)} routes")
        
        # Test if we can access the home route
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home route responds correctly")
            else:
                print(f"⚠️  Home route returned status {response.status_code}")
            
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint responds correctly")
            else:
                print(f"⚠️  Health endpoint returned status {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ App startup error: {e}")
        return False

def test_ffmpeg():
    """Test if FFmpeg is available"""
    print("\nTesting FFmpeg availability...")
    
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            return True
        else:
            print("❌ FFmpeg command failed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

if __name__ == "__main__":
    print("Flask App Test")
    print("=" * 40)
    
    import_success = test_imports()
    app_success = test_app_startup()
    ffmpeg_success = test_ffmpeg()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"App Startup: {'✅ PASS' if app_success else '❌ FAIL'}")
    print(f"FFmpeg: {'✅ PASS' if ffmpeg_success else '❌ FAIL'}")
    
    if import_success and app_success:
        print("\n✅ App should work correctly!")
    else:
        print("\n❌ There are issues that need to be fixed.")
        sys.exit(1) 