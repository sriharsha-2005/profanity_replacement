#!/usr/bin/env python3
"""
Simple test with hardcoded replacements
"""

import re

# Simple test with hardcoded replacements
PROFANITY_MAP = {
    r'\bjeans\b': "pants",
    r'\bshit\b': "crap",
    r'\basshole\b': "jerk"
}

def filter_text(text):
    """Simple text filtering"""
    for pattern, replacement in PROFANITY_MAP.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Test
test_text = "I love my jeans and shit"
print(f"Original: {test_text}")
filtered_text = filter_text(test_text)
print(f"Filtered: {filtered_text}")

# Test with transcript format
test_transcript = [
    {"word": "I", "start": 0.0, "end": 0.5},
    {"word": "love", "start": 0.5, "end": 1.0},
    {"word": "my", "start": 1.0, "end": 1.5},
    {"word": "jeans", "start": 1.5, "end": 2.0},
    {"word": "and", "start": 2.0, "end": 2.5},
    {"word": "shit", "start": 2.5, "end": 3.0}
]

print(f"\nTranscript test:")
print(f"Original words: {[word['word'] for word in test_transcript]}")

# Simple replacement
for word in test_transcript:
    original = word['word']
    if original.lower() in ['jeans', 'shit', 'asshole']:
        if original.lower() == 'jeans':
            word['word'] = 'pants'
        elif original.lower() == 'shit':
            word['word'] = 'crap'
        elif original.lower() == 'asshole':
            word['word'] = 'jerk'

print(f"Filtered words: {[word['word'] for word in test_transcript]}")

print("✅ Simple test completed successfully!") 