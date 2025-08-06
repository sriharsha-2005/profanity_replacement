from typing import List, Dict, Any
import re
import csv
import os
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def get_word_pos(word):
    """Get the primary POS (Part of Speech) for a word."""
    try:
        synsets = wordnet.synsets(word.lower())
        
        if not synsets:
            pos_tags = pos_tag([word.lower()])
            tag = pos_tags[0][1] if pos_tags else 'NN'
            
            if tag.startswith('VB'):
                return 'verb'
            elif tag.startswith('NN'):
                return 'noun'
            else:
                return 'noun'
        
        pos_counts = {'noun': 0, 'verb': 0}
        
        for synset in synsets:
            if synset.pos() == 'n':
                pos_counts['noun'] += 1
            elif synset.pos() == 'v':
                pos_counts['verb'] += 1
        
        if pos_counts['verb'] > pos_counts['noun']:
            return 'verb'
        else:
            return 'noun'
            
    except Exception as e:
        return 'noun'

def process_bad_words_dataset(input_file, bad_word_column='badword'):
    """Process a dataset of bad words, remove duplicates, and add POS tagging."""
    try:
        df = pd.read_csv(input_file)
        
        if bad_word_column not in df.columns:
            available_columns = list(df.columns)
            raise ValueError(f"Column '{bad_word_column}' not found. Available columns: {available_columns}")
        
        bad_words = df[bad_word_column].dropna().astype(str).str.lower().unique()
        
        processed_data = []
        
        for word in bad_words:
            word = word.strip()
            if word:
                pos_type = get_word_pos(word)
                processed_data.append({
                    'badword': word,
                    'replacement_word': '',
                    'type': pos_type
                })
        
        result_df = pd.DataFrame(processed_data)
        result_df = result_df.sort_values('badword').reset_index(drop=True)
        
        return result_df
        
    except Exception as e:
        raise

def load_profanity_replacements():
    """Load profanity replacements from CSV file with POS tagging."""
    replacements = {}
    
    # Try to load from validated CSV
    csv_path = 'validated_profanity_replacements.csv'
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path, delimiter='\t')
            
            for _, row in df.iterrows():
                badword = row.get('badword', '').strip().lower()
                replacement = row.get('replacement_word', '').strip()
                badword_type = row.get('badwordtype', 'noun').strip()
                replacement_type = row.get('replacement_wordtype', 'literal').strip()
                
                if badword and replacement:
                    # Create regex pattern for word boundaries
                    pattern = r'\b' + re.escape(badword) + r'\b'
                    replacements[pattern] = {
                        'replacement': replacement,
                        'badword_type': badword_type,
                        'replacement_type': replacement_type
                    }
            
            print(f"Loaded {len(replacements)} replacements from {csv_path}")
            
        except Exception as e:
            print(f"Error loading {csv_path}: {e}")
    
    # Add fallback test cases if CSV is not available
    if not replacements:
        test_replacements = {
            r'\bjeans\b': {'replacement': "pants", 'badword_type': 'noun', 'replacement_type': 'literal'},
            r'\bshit\b': {'replacement': "crap", 'badword_type': 'noun', 'replacement_type': 'euphemism'},
            r'\basshole\b': {'replacement': "jerk", 'badword_type': 'noun', 'replacement_type': 'euphemism'},
            r'\bmother\s?fucker\b': {'replacement': "awesome person", 'badword_type': 'noun', 'replacement_type': 'euphemism'}
        }
        
        for pattern, data in test_replacements.items():
            if pattern not in replacements:
                replacements[pattern] = data
    
    return replacements

# Load the profanity map
PROFANITY_MAP = load_profanity_replacements()

def filter_transcript(transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter transcript for profanity and return replacement segments."""
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
    for pattern, replacement_data in PROFANITY_MAP.items():
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
            
            # Get POS information for better replacement
            original_word = match.group()
            word_pos = get_word_pos(original_word)
            
            # Choose replacement based on POS matching
            replacement = replacement_data['replacement']
            if replacement_data['badword_type'] == word_pos:
                # Use the replacement as is
                pass
            else:
                # Try to find a better replacement based on POS
                # For now, use the original replacement
                pass
            
            replacements.append({
                "start": start_time,
                "end": end_time,
                "original": original_word,
                "replacement": replacement,
                "pos_type": word_pos,
                "replacement_type": replacement_data['replacement_type']
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

def integrate_pos_tagger_with_workflow():
    """Integrate POS tagger with the main workflow."""
    try:
        # Process the bad words dataset if it exists
        bad_words_file = 'badWords.csv'
        if os.path.exists(bad_words_file):
            processed_df = process_bad_words_dataset(bad_words_file)
            
            # Save processed dataset
            output_file = 'processed_bad_words_with_pos.csv'
            processed_df.to_csv(output_file, index=False)
            print(f"Processed dataset saved to {output_file}")
            
            # Update the profanity map with processed data
            global PROFANITY_MAP
            for _, row in processed_df.iterrows():
                badword = row['badword']
                pos_type = row['type']
                
                # Create pattern for this word
                pattern = r'\b' + re.escape(badword) + r'\b'
                
                # Add to profanity map if not already present
                if pattern not in PROFANITY_MAP:
                    PROFANITY_MAP[pattern] = {
                        'replacement': f"clean_{pos_type}",  # Placeholder replacement
                        'badword_type': pos_type,
                        'replacement_type': 'literal'
                    }
            
            print(f"Updated profanity map with {len(processed_df)} POS-tagged words")
            
    except Exception as e:
        print(f"Error integrating POS tagger: {e}")

def test_profanity_filter():
    """Test the profanity filter with sample text."""
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
        print(f"'{repl['original']}' -> '{repl['replacement']}' (time: {repl['start']}-{repl['end']}, POS: {repl['pos_type']})")
    
    return replacements

if __name__ == "__main__":
    # Integrate POS tagger with workflow
    integrate_pos_tagger_with_workflow()
    
    # Test the filter
    test_profanity_filter()