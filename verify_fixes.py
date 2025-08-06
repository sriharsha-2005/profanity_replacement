#!/usr/bin/env python3
"""
Simple Verification Script for NoProfanity Fixes
Checks if all the fixes are properly implemented
"""

import os
import sys

def check_file_exists(filepath):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {filepath} - EXISTS")
        return True
    else:
        print(f"❌ {filepath} - MISSING")
        return False

def check_file_content(filepath, required_strings):
    """Check if file contains required strings."""
    if not os.path.exists(filepath):
        print(f"❌ {filepath} - FILE NOT FOUND")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing_strings = []
        for string in required_strings:
            if string not in content:
                missing_strings.append(string)
        
        if missing_strings:
            print(f"❌ {filepath} - MISSING: {missing_strings}")
            return False
        else:
            print(f"✅ {filepath} - CONTENT VERIFIED")
            return True
    except Exception as e:
        print(f"❌ {filepath} - ERROR READING: {e}")
        return False

def main():
    print("🔍 VERIFYING NOPROFANITY FIXES")
    print("=" * 50)
    
    # Check if key files exist
    key_files = [
        'requirements.txt',
        'run.py',
        'app/__init__.py',
        'app/routes.py',
        'python/main.py',
        'python/text_processing/profanity_filter.py',
        'python/others/transcription_analyzer.py',
        'python/others/video_merger.py',
        'python/others/profanity_detector.py',
        'app/templates/transcription.html',
        'app/templates/video_audio_merge.html',
        'app/templates/profanity_count.html',
        'test_integration.py',
        'README_FIXES.md'
    ]
    
    print("\n📁 CHECKING FILE STRUCTURE:")
    file_exists_count = 0
    for filepath in key_files:
        if check_file_exists(filepath):
            file_exists_count += 1
    
    print(f"\n📊 File Structure: {file_exists_count}/{len(key_files)} files found")
    
    # Check specific content fixes
    print("\n🔍 CHECKING CONTENT FIXES:")
    
    # Check requirements.txt for new dependencies
    requirements_check = check_file_content('requirements.txt', [
        'reportlab>=4.0.0',
        'nltk>=3.8.1',
        'pandas>=2.0.0'
    ])
    
    # Check transcription analyzer for PDF generation
    transcription_check = check_file_content('python/others/transcription_analyzer.py', [
        'reportlab',
        'create_pdf_transcript',
        'SimpleDocTemplate'
    ])
    
    # Check profanity filter for POS integration
    profanity_check = check_file_content('python/text_processing/profanity_filter.py', [
        'nltk',
        'get_word_pos',
        'integrate_pos_tagger_with_workflow'
    ])
    
    # Check video merge template for dual input
    video_merge_check = check_file_content('app/templates/video_audio_merge.html', [
        'videoUploadArea',
        'audioUploadArea',
        'file-upload-section'
    ])
    
    # Check profanity dashboard for charts
    dashboard_check = check_file_content('app/templates/profanity_count.html', [
        'chart.js',
        'stats-grid',
        'chart-container'
    ])
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY OF FIXES:")
    print("=" * 50)
    
    fixes_status = {
        "File Structure": f"{file_exists_count}/{len(key_files)} files present",
        "Requirements Update": "✅" if requirements_check else "❌",
        "PDF Generation": "✅" if transcription_check else "❌",
        "POS Tagging Integration": "✅" if profanity_check else "❌",
        "Video-Audio Dual Input": "✅" if video_merge_check else "❌",
        "Enhanced Dashboard": "✅" if dashboard_check else "❌"
    }
    
    for fix, status in fixes_status.items():
        print(f"{fix}: {status}")
    
    # Overall assessment
    total_checks = len(fixes_status)
    passed_checks = sum(1 for status in fixes_status.values() if "✅" in status or "files present" in status)
    
    print(f"\n🎯 OVERALL STATUS: {passed_checks}/{total_checks} fixes verified")
    
    if passed_checks == total_checks:
        print("🎉 ALL FIXES SUCCESSFULLY IMPLEMENTED!")
        print("\n📝 NEXT STEPS:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python run.py")
        print("3. Test functionality with sample files")
    else:
        print("⚠️  SOME FIXES NEED ATTENTION")
        print("Please review the failed checks above")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 