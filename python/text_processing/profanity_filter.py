from typing import List, Dict, Any
import re
import csv
import os

# Load replacements from CSV file
def load_profanity_replacements():
    """Load profanity replacements from CSV file"""
    replacements = {}
    
    # Try to load from CSV
    csv_path = 'validated_profanity_replacements.csv'
    
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    badword = row.get('badword', '').strip().lower()
                    replacement = row.get('replacement_word', '').strip()
                    if badword and replacement:
                        # Create regex pattern for word boundaries
                        pattern = r'\b' + re.escape(badword) + r'\b'
                        replacements[pattern] = replacement
            print(f"Loaded {len(replacements)} replacements from {csv_path}")
        except Exception as e:
            print(f"Error loading {csv_path}: {e}")
    
    # Always add test cases
    test_replacements = {
        r'\bjeans\b': "pants",
        r'\bshit\b': "crap",
        r'\basshole\b': "jerk",
        r'\bmother\s?fucker\b': "awesome person"
    }
    
    # Merge test replacements with CSV replacements
    for pattern, replacement in test_replacements.items():
        if pattern not in replacements:
            replacements[pattern] = replacement
    
    return replacements

# Load the profanity map
PROFANITY_MAP = load_profanity_replacements()

def filter_transcript(transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    replacements = []
    
    # Create a searchable version of the transcript with character positions
    char_pos = 0
    word_positions = []
    for word in transcript:
        word_text = word["word"]
        word_positions.append({
            "start_char": char_pos,
            "end_char": char_pos + len(word_text),
            "word": word
        })
        char_pos += len(word_text) + 1  # +1 for space
    
    full_text = " ".join(word["word"] for word in transcript)
    
    # Check for all profanity patterns
    for pattern, replacement in PROFANITY_MAP.items():
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            # Find words that overlap with this match
            match_start = match.start()
            match_end = match.end()
            
            overlapping_words = [
                wp for wp in word_positions 
                if not (wp["end_char"] <= match_start or wp["start_char"] >= match_end)
            ]
            
            if not overlapping_words:
                continue
                
            # Get timing information from first and last overlapping words
            start_time = overlapping_words[0]["word"]["start"]
            end_time = overlapping_words[-1]["word"]["end"]
            
            replacements.append({
                "start": start_time,
                "end": end_time,
                "original": match.group(),
                "replacement": replacement
            })
    
    # Sort by start time and remove overlaps (keep longer matches)
    replacements.sort(key=lambda x: x["start"])
    filtered_replacements = []
    
    for repl in replacements:
        if not filtered_replacements:
            filtered_replacements.append(repl)
        else:
            last = filtered_replacements[-1]
            if repl["start"] < last["end"]:
                # Overlapping - keep the longer match
                if (repl["end"] - repl["start"]) > (last["end"] - last["start"]):
                    filtered_replacements[-1] = repl
            else:
                filtered_replacements.append(repl)
    
    return filtered_replacements

def test_profanity_filter():
    """Test the profanity filter with sample text"""
    test_transcript = [
        {"word": "I", "start": 0.0, "end": 0.5},
        {"word": "love", "start": 0.5, "end": 1.0},
        {"word": "my", "start": 1.0, "end": 1.5},
        {"word": "jeans", "start": 1.5, "end": 2.0},
        {"word": "and", "start": 2.0, "end": 2.5},
        {"word": "shit", "start": 2.5, "end": 3.0}
    ]
    
    replacements = filter_transcript(test_transcript)
    print("Test Results:")
    for repl in replacements:
        print(f"'{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']})")
    
    return replacements

if __name__ == "__main__":
    test_profanity_filter()