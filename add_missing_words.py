#!/usr/bin/env python3
"""
Add missing test words to the CSV file
"""

import csv

# Read existing CSV
existing_data = []
with open('validated_profanity_replacements.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        existing_data.append(row)

# Check if test words exist
test_words = {
    'jeans': 'pants',
    'shit': 'crap'
}

existing_badwords = [row['badword'].strip().lower() for row in existing_data]

print("Checking for test words...")
for word, replacement in test_words.items():
    if word in existing_badwords:
        print(f"✅ {word} already exists")
    else:
        print(f"❌ {word} not found, adding...")
        # Add the missing word
        new_row = {
            'badword': word,
            'badwordtype': 'noun',
            'replacement_word': replacement,
            'replacement_wordtype': 'literal'
        }
        existing_data.append(new_row)

# Write back to CSV
with open('validated_profanity_replacements.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['badword', 'badwordtype', 'replacement_word', 'replacement_wordtype'], delimiter='\t')
    writer.writeheader()
    for row in existing_data:
        writer.writerow(row)

print(f"Updated CSV with {len(existing_data)} rows")
print("✅ Test words added successfully!") 