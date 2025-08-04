import pandas as pd
import nltk
from nltk.corpus import wordnet
import logging
import re

# Download required NLTK data
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_word(word):
    """
    Clean a word by removing special characters and normalizing.
    """
    # Remove special characters but keep letters and numbers
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
    return cleaned.strip()

def get_word_pos_simple(word):
    """
    Get the primary POS (Part of Speech) for a word using only WordNet.
    Returns 'noun' or 'verb', defaults to 'noun' if unclear.
    """
    try:
        # Get all synsets for the word
        synsets = wordnet.synsets(word.lower())
        
        if not synsets:
            return 'noun'  # Default to noun if no synsets found
        
        # Count occurrences of each POS
        pos_counts = {'noun': 0, 'verb': 0}
        
        for synset in synsets:
            if synset.pos() == 'n':
                pos_counts['noun'] += 1
            elif synset.pos() == 'v':
                pos_counts['verb'] += 1
        
        # Return the most common POS, default to noun if equal
        if pos_counts['verb'] > pos_counts['noun']:
            return 'verb'
        else:
            return 'noun'
            
    except Exception as e:
        logger.warning(f"Error processing word '{word}': {e}")
        return 'noun'  # Default to noun on error

def find_literal_synonym(word, pos_type='noun'):
    """
    Find a literal synonym for the word, preferring similar length and meaning.
    Avoids euphemisms and focuses on direct synonyms.
    """
    try:
        # Define POS mapping for WordNet
        pos_map = {'noun': 'n', 'verb': 'v'}
        wn_pos = pos_map.get(pos_type, 'n')
        
        # Get synsets for the word
        synsets = wordnet.synsets(word.lower(), pos=wn_pos)
        
        if not synsets:
            # Try without POS restriction
            synsets = wordnet.synsets(word.lower())
        
        if not synsets:
            return ""
        
        # Get the first synset (most common meaning)
        synset = synsets[0]
        
        # Get lemmas (synonyms) from this synset
        lemmas = synset.lemmas()
        
        # Filter out the original word and find good synonyms
        good_synonyms = []
        for lemma in lemmas:
            synonym = lemma.name()
            
            # Skip the original word
            if synonym.lower() == word.lower():
                continue
                
            # Skip if it's too short or too long (avoid extreme length differences)
            if len(synonym) < 2 or len(synonym) > len(word) * 2:
                continue
                
            # Skip if it contains the original word (avoid compounds)
            if word.lower() in synonym.lower():
                continue
                
            # Skip if it's still a bad word (basic check)
            if is_likely_bad_word(synonym):
                continue
                
            good_synonyms.append(synonym)
        
        # Return the first good synonym, or empty string if none found
        return good_synonyms[0] if good_synonyms else ""
        
    except Exception as e:
        logger.warning(f"Error finding synonym for '{word}': {e}")
        return ""

def is_likely_bad_word(word):
    """
    Basic check to see if a word is likely to be a bad word.
    """
    bad_indicators = [
        'fuck', 'shit', 'ass', 'bitch', 'cock', 'dick', 'pussy', 'cunt',
        'bastard', 'whore', 'slut', 'faggot', 'nigger', 'damn', 'hell',
        'whore', 'slut', 'cunt', 'faggot', 'nigger', 'damn', 'hell'
    ]
    
    word_lower = word.lower()
    for indicator in bad_indicators:
        if indicator in word_lower:
            return True
    return False

def process_bad_words_dataset(input_file='badWords.csv', text_column='text'):
    """
    Process the bad words dataset, remove duplicates, add POS tagging, and find synonyms.
    
    Args:
        input_file (str): Path to the CSV file containing bad words
        text_column (str): Name of the column containing bad words
        
    Returns:
        pd.DataFrame: Processed dataset with columns: badword, replacement_word, type
    """
    try:
        # Load the dataset
        logger.info(f"Loading dataset from {input_file}")
        df = pd.read_csv(input_file)
        
        # Check if the text column exists
        if text_column not in df.columns:
            available_columns = list(df.columns)
            logger.error(f"Column '{text_column}' not found. Available columns: {available_columns}")
            raise ValueError(f"Column '{text_column}' not found in the dataset")
        
        # Extract bad words and clean them
        raw_words = df[text_column].dropna().astype(str)
        cleaned_words = [clean_word(word) for word in raw_words]
        
        # Remove empty words and duplicates
        unique_words = list(set([word for word in cleaned_words if word and len(word) > 1]))
        
        logger.info(f"Found {len(unique_words)} unique bad words after cleaning")
        
        # Create new dataset
        processed_data = []
        
        for i, word in enumerate(unique_words):
            if i % 100 == 0:
                logger.info(f"Processing word {i+1}/{len(unique_words)}: {word}")
            
            # Get POS type
            pos_type = get_word_pos_simple(word)
            
            # Find literal synonym
            replacement = find_literal_synonym(word, pos_type)
            
            processed_data.append({
                'badword': word,
                'replacement_word': replacement,
                'type': pos_type
            })
        
        # Create DataFrame
        result_df = pd.DataFrame(processed_data)
        
        # Sort by word for better organization
        result_df = result_df.sort_values('badword').reset_index(drop=True)
        
        logger.info(f"Processed dataset created with {len(result_df)} unique words")
        logger.info(f"POS distribution: {result_df['type'].value_counts().to_dict()}")
        
        # Count words with synonyms found
        words_with_synonyms = len(result_df[result_df['replacement_word'] != ''])
        logger.info(f"Words with synonyms found: {words_with_synonyms}/{len(result_df)}")
        
        return result_df
        
    except Exception as e:
        logger.error(f"Error processing dataset: {e}")
        raise

def save_processed_dataset(df, output_file='processed_bad_words_with_synonyms.csv'):
    """
    Save the processed dataset to a CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Processed dataset saved to {output_file}")
        
        # Also save a summary
        summary = {
            'total_words': len(df),
            'nouns': len(df[df['type'] == 'noun']),
            'verbs': len(df[df['type'] == 'verb']),
            'words_with_synonyms': len(df[df['replacement_word'] != '']),
            'words_without_synonyms': len(df[df['replacement_word'] == ''])
        }
        
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv('processing_summary.csv', index=False)
        logger.info("Processing summary saved to processing_summary.csv")
        
    except Exception as e:
        logger.error(f"Error saving dataset: {e}")
        raise

def main():
    """
    Main function to process the bad words dataset.
    """
    try:
        # Process the dataset
        processed_df = process_bad_words_dataset('badWords.csv', text_column='text')
        
        # Save the result
        save_processed_dataset(processed_df, 'processed_bad_words_with_synonyms.csv')
        
        # Display sample results
        print("\n=== Sample Processed Data ===")
        print(processed_df.head(20))
        
        print(f"\n=== POS Distribution ===")
        print(processed_df['type'].value_counts())
        
        print(f"\n=== Words with Synonyms ===")
        words_with_synonyms = processed_df[processed_df['replacement_word'] != '']
        print(f"Total: {len(words_with_synonyms)}/{len(processed_df)}")
        print("\nSample synonyms:")
        for _, row in words_with_synonyms.head(10).iterrows():
            print(f"  {row['badword']} ({row['type']}) → {row['replacement_word']}")
        
        print(f"\n=== Files Created ===")
        print("1. processed_bad_words_with_synonyms.csv - Main dataset")
        print("2. processing_summary.csv - Summary statistics")
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main() 