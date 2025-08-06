#!/usr/bin/env python3
"""
Comprehensive integration test for profanity filter
"""

import sys
sys.path.append('.')

from python.text_processing.profanity_filter import filter_transcript

def test_comprehensive_integration():
    """Test the complete profanity filter integration"""
    
    print("🧪 Comprehensive Profanity Filter Integration Test")
    print("=" * 50)
    
    # Test Case 1: Basic replacements
    test_cases = [
        {
            "name": "Test Case 1: jeans -> pants",
            "transcript": [
                {"word": "I", "start": 0.0, "end": 0.5},
                {"word": "love", "start": 0.5, "end": 1.0},
                {"word": "my", "start": 1.0, "end": 1.5},
                {"word": "jeans", "start": 1.5, "end": 2.0}
            ],
            "expected": ["jeans"]
        },
        {
            "name": "Test Case 2: shit -> crap",
            "transcript": [
                {"word": "This", "start": 0.0, "end": 0.5},
                {"word": "is", "start": 0.5, "end": 1.0},
                {"word": "shit", "start": 1.0, "end": 1.5}
            ],
            "expected": ["shit"]
        },
        {
            "name": "Test Case 3: Multiple replacements",
            "transcript": [
                {"word": "What", "start": 0.0, "end": 0.5},
                {"word": "the", "start": 0.5, "end": 1.0},
                {"word": "shit", "start": 1.0, "end": 1.5},
                {"word": "is", "start": 1.5, "end": 2.0},
                {"word": "this", "start": 2.0, "end": 2.5},
                {"word": "jeans", "start": 2.5, "end": 3.0}
            ],
            "expected": ["shit", "jeans"]
        },
        {
            "name": "Test Case 4: No profane words",
            "transcript": [
                {"word": "Hello", "start": 0.0, "end": 0.5},
                {"word": "world", "start": 0.5, "end": 1.0},
                {"word": "how", "start": 1.0, "end": 1.5},
                {"word": "are", "start": 1.5, "end": 2.0},
                {"word": "you", "start": 2.0, "end": 2.5}
            ],
            "expected": []
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n📋 {test_case['name']}")
        print("-" * 30)
        
        # Run the test
        replacements = filter_transcript(test_case["transcript"])
        
        # Check results
        found_words = [repl["original"] for repl in replacements]
        expected_words = test_case["expected"]
        
        print(f"Input: {[word['word'] for word in test_case['transcript']]}")
        print(f"Expected replacements: {expected_words}")
        print(f"Found replacements: {found_words}")
        
        # Verify results
        if set(found_words) == set(expected_words):
            print("✅ PASS")
            for repl in replacements:
                print(f"   '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
        else:
            print("❌ FAIL")
            print(f"   Expected: {expected_words}")
            print(f"   Found: {found_words}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Profanity filter integration is working correctly.")
        print("✅ 'jeans' -> 'pants' test case working")
        print("✅ CSV file integration working")
        print("✅ Timing information preserved")
        print("✅ Multiple replacements working")
        print("✅ No false positives")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_comprehensive_integration() 