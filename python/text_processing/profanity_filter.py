from typing import List, Dict, Any
import re

PROFANITY_MAP = {
    # Single words
    r'\basshole\b': "jerk",
    r'\bshit\b': "crap",
    r'\bjeans\b': "hello",
    # Multi-word phrases
    r'\bmother\s?fucker\b': "awesome person",
    r'\bt\s?shirt\b': "shirt"
}

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