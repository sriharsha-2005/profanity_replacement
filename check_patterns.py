#!/usr/bin/env python3
"""
Check if specific words are in the loaded patterns
"""

import sys
sys.path.append('.')

from python.text_processing.profanity_filter import load_profanity_replacements

# Load the replacements
replacements = load_profanity_replacements()

# Check for specific words
test_words = ['jeans', 'shit', 'asshole']
print(f"\nChecking for test words: {test_words}")

for word in test_words:
    pattern = r'\b' + word + r'\b'
    if pattern in replacements:
        print(f"✅ Found '{word}' -> '{replacements[pattern]}'")
    else:
        print(f"❌ Not found: '{word}'")
        
        # Check if it exists with different casing
        for pattern, replacement in replacements.items():
            if word.lower() in pattern.lower():
                print(f"  Similar pattern found: {pattern} -> {replacement}")

# Print all patterns that contain "jeans" or "shit"
print(f"\nAll patterns containing 'jeans' or 'shit':")
for pattern, replacement in replacements.items():
    if 'jeans' in pattern.lower() or 'shit' in pattern.lower():
        print(f"  {pattern} -> {replacement}") 