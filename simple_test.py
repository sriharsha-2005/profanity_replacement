#!/usr/bin/env python3
"""
Simple test for profanity filter
"""

import sys
sys.path.append('.')

from python.text_processing.profanity_filter import filter_transcript

# Simple test
test_transcript = [
    {"word": "I", "start": 0.0, "end": 0.5},
    {"word": "love", "start": 0.5, "end": 1.0},
    {"word": "my", "start": 1.0, "end": 1.5},
    {"word": "jeans", "start": 1.5, "end": 2.0},
    {"word": "and", "start": 2.0, "end": 2.5},
    {"word": "shit", "start": 2.5, "end": 3.0}
]

print("Testing profanity filter...")
print("Input transcript:", [word["word"] for word in test_transcript])

replacements = filter_transcript(test_transcript)

print(f"Found {len(replacements)} replacements:")
for repl in replacements:
    print(f"  '{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")

if len(replacements) > 0:
    print("✅ Profanity filter is working!")
else:
    print("❌ No replacements found - check if CSV file is loaded correctly") 