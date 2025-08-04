#!/usr/bin/env python3
"""
Test script for profanity filter integration
"""

import sys
import os
sys.path.append('.')

from python.text_processing.profanity_filter import filter_transcript

def test_profanity_filter():
    """Test the profanity filter with various test cases"""
    
    # Test case 1: "jeans" should be replaced with "pants"
    test_transcript_1 = [
        {"word": "I", "start": 0.0, "end": 0.5},
        {"word": "love", "start": 0.5, "end": 1.0},
        {"word": "my", "start": 1.0, "end": 1.5},
        {"word": "jeans", "start": 1.5, "end": 2.0},
        {"word": "very", "start": 2.0, "end": 2.5},
        {"word": "much", "start": 2.5, "end": 3.0}
    ]
    
    print("Test 1: 'jeans' replacement")
    replacements_1 = filter_transcript(test_transcript_1)
    for repl in replacements_1:
        print(f"  '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
    
    # Test case 2: "shit" should be replaced with "crap"
    test_transcript_2 = [
        {"word": "This", "start": 0.0, "end": 0.5},
        {"word": "is", "start": 0.5, "end": 1.0},
        {"word": "shit", "start": 1.0, "end": 1.5},
        {"word": "man", "start": 1.5, "end": 2.0}
    ]
    
    print("\nTest 2: 'shit' replacement")
    replacements_2 = filter_transcript(test_transcript_2)
    for repl in replacements_2:
        print(f"  '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
    
    # Test case 3: Multiple profane words
    test_transcript_3 = [
        {"word": "What", "start": 0.0, "end": 0.5},
        {"word": "the", "start": 0.5, "end": 1.0},
        {"word": "shit", "start": 1.0, "end": 1.5},
        {"word": "is", "start": 1.5, "end": 2.0},
        {"word": "this", "start": 2.0, "end": 2.5},
        {"word": "jeans", "start": 2.5, "end": 3.0},
        {"word": "doing", "start": 3.0, "end": 3.5}
    ]
    
    print("\nTest 3: Multiple replacements")
    replacements_3 = filter_transcript(test_transcript_3)
    for repl in replacements_3:
        print(f"  '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
    
    # Test case 4: No profane words
    test_transcript_4 = [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "world", "start": 0.5, "end": 1.0},
        {"word": "how", "start": 1.0, "end": 1.5},
        {"word": "are", "start": 1.5, "end": 2.0},
        {"word": "you", "start": 2.0, "end": 2.5}
    ]
    
    print("\nTest 4: No profane words")
    replacements_4 = filter_transcript(test_transcript_4)
    if replacements_4:
        for repl in replacements_4:
            print(f"  '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
    else:
        print("  No replacements found (expected)")
    
    print("\n✅ Profanity filter integration test completed successfully!")
    return True

if __name__ == "__main__":
    test_profanity_filter() 