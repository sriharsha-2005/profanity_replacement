import csv
from typing import Dict, Tuple

# Master replacement dictionary with CONTEXTUAL replacements
REPLACEMENT_DB = {
    # Anger/Frustration
    "damn": ("darn", "euphemism"),
    "hell": ("heck", "euphemism"),
    "shit": ("crap", "euphemism"),
    "piss off": ("annoy", "literal"),
    # Vulgarity
    "ass": ("backside", "literal"),
    "slut": ("promiscuous person", "literal"),
    "whore": ("sex worker", "literal"),
    "dick": ("jerk", "contextual"),
    "cunt": ("rude person", "contextual"),
    # Nonsense
    "bullshit": ("nonsense", "literal"),
    # Sexual terms
    "oralsex": ("intimacy", "literal"),
    "orgasm": ("climax", "literal"),
    "ejaculating": ("releasing", "literal"),
    # Insults
    "bastard": ("jerk", "literal"),
    "bitch": ("mean person", "literal"),
    "motherfucker": ("terrible person", "literal"),
    # Racial slurs (neutral replacements)
    "nigger": ("person", "neutral"),
    "chink": ("person", "neutral"),
    # ... (add all other 1483 words as needed)
}

# Spelling correction mapping (expand as needed)
CORRECT_SPELLING = {
    "0ralsex": "oralsex",
    "0rgasm": "orgasm",
    "3jaculating": "ejaculating",
    "4rse": "arse",
    "5hit": "shit",
    # ... (add all spelling corrections as needed)
}

def correct_spelling(word: str) -> str:
    return CORRECT_SPELLING.get(word.lower(), word.lower())

def get_replacement(word: str, word_type: str) -> Tuple[str, str]:
    word = correct_spelling(word)
    if word not in REPLACEMENT_DB:
        return ("", "")
    replacement, replacement_type = REPLACEMENT_DB[word]
    if replacement == "contextual":
        if word_type == "noun":
            return ("person", "neutral")
        elif word_type == "verb":
            return ("action", "neutral")
        else:
            return ("thing", "neutral")
    return (replacement, replacement_type)

def process_dataset(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['badword', 'badword_pos', 'replacement_word', 'replacement_word_type'])
        writer.writeheader()
        for row in reader:
            original_word = row['badword'].strip().lower()
            word_type = row['type'].strip().lower()
            if not original_word or word_type not in ['noun', 'verb', 'adjective']:
                continue
            corrected = correct_spelling(original_word)
            replacement, replacement_type = get_replacement(corrected, word_type)
            if replacement:
                writer.writerow({
                    'badword': corrected,
                    'badword_pos': word_type,
                    'replacement_word': replacement,
                    'replacement_word_type': replacement_type
                })

if __name__ == "__main__":
    process_dataset("processed_bad_words_fast.csv", "final_clean_replacements.csv")