#!/usr/bin/env python3
"""
Direct CSV check for specific words
"""

import csv

# Check CSV directly
with open('validated_profanity_replacements.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    
    jeans_found = False
    shit_found = False
    
    for row in reader:
        badword = row.get('badword', '').strip().lower()
        replacement = row.get('replacement_word', '').strip()
        
        if badword == 'jeans':
            print(f"✅ Found jeans -> {replacement}")
            jeans_found = True
        elif badword == 'shit':
            print(f"✅ Found shit -> {replacement}")
            shit_found = True
    
    if not jeans_found:
        print("❌ jeans not found in CSV")
    if not shit_found:
        print("❌ shit not found in CSV")

print("CSV check completed.") 