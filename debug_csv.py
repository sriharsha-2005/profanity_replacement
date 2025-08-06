#!/usr/bin/env python3
"""
Debug script to check CSV content
"""

import csv
import re

# Check CSV content
with open('validated_profanity_replacements.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    
    print("CSV columns:", reader.fieldnames)
    print("\nFirst 10 rows:")
    
    count = 0
    for row in reader:
        if count < 10:
            print(f"Row {count}: {row}")
        count += 1
    
    print(f"\nTotal rows: {count}")

# Test specific words
test_words = ['jeans', 'shit', 'asshole']
print(f"\nTesting specific words: {test_words}")

with open('validated_profanity_replacements.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    
    for row in reader:
        badword = row.get('badword', '').strip().lower()
        replacement = row.get('replacement_word', '').strip()
        
        if badword in test_words:
            print(f"Found '{badword}' -> '{replacement}'")
            
        # Also check if any of our test words are in the badword
        for test_word in test_words:
            if test_word in badword or badword in test_word:
                print(f"Partial match: '{badword}' contains '{test_word}' -> '{replacement}'") 