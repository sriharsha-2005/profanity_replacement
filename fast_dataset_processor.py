import pandas as pd
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_word(word):
    """Clean a word by removing special characters."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word.lower())
    return cleaned.strip()

def get_word_pos_fast(word):
    """Fast POS detection using simple rules."""
    # Common verb endings
    verb_endings = ['ing', 'ed', 'er', 'est', 'ize', 'ise', 'ate']
    word_lower = word.lower()
    
    for ending in verb_endings:
        if word_lower.endswith(ending):
            return 'verb'
    
    # Default to noun
    return 'noun'

def find_simple_replacement(word, pos_type):
    """Find simple replacements using a predefined mapping."""
    # Simple replacement dictionary
    replacements = {
        'fuck': 'mess',
        'shit': 'stuff', 
        'ass': 'rear',
        'bitch': 'person',
        'cock': 'rooster',
        'dick': 'person',
        'pussy': 'cat',
        'cunt': 'person',
        'bastard': 'person',
        'whore': 'person',
        'slut': 'person',
        'faggot': 'person',
        'nigger': 'person',
        'damn': 'darn',
        'hell': 'heck',
        'piss': 'urine',
        'tits': 'chest',
        'dickhead': 'person',
        'asshole': 'person',
        'motherfucker': 'person',
        'fucker': 'person',
        'crap': 'stuff',
        'bollocks': 'nonsense',
        'wanker': 'person',
        'twat': 'person',
        'arse': 'rear',
        'bugger': 'person',
        'bloody': 'very',
        'sod': 'person'
    }
    
    return replacements.get(word.lower(), '')

def process_bad_words_fast(input_file='badWords.csv', text_column='text'):
    """Fast processing of bad words dataset."""
    try:
        logger.info(f"Loading dataset from {input_file}")
        df = pd.read_csv(input_file)
        
        if text_column not in df.columns:
            available_columns = list(df.columns)
            logger.error(f"Column '{text_column}' not found. Available columns: {available_columns}")
            raise ValueError(f"Column '{text_column}' not found in the dataset")
        
        # Extract and clean words
        raw_words = df[text_column].dropna().astype(str)
        cleaned_words = [clean_word(word) for word in raw_words]
        unique_words = list(set([word for word in cleaned_words if word and len(word) > 1]))
        
        logger.info(f"Found {len(unique_words)} unique bad words")
        
        # Process words quickly
        processed_data = []
        for word in unique_words:
            pos_type = get_word_pos_fast(word)
            replacement = find_simple_replacement(word, pos_type)
            
            processed_data.append({
                'badword': word,
                'replacement_word': replacement,
                'type': pos_type
            })
        
        result_df = pd.DataFrame(processed_data)
        result_df = result_df.sort_values('badword').reset_index(drop=True)
        
        logger.info(f"Processed {len(result_df)} words in seconds")
        return result_df
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

def save_dataset(df, output_file='processed_bad_words_fast.csv'):
    """Save the dataset."""
    df.to_csv(output_file, index=False)
    logger.info(f"Saved to {output_file}")

def main():
    """Main function."""
    try:
        processed_df = process_bad_words_fast('badWords.csv', 'text')
        save_dataset(processed_df)
        
        print(f"\n=== Results ===")
        print(f"Total words: {len(processed_df)}")
        print(f"POS distribution: {processed_df['type'].value_counts().to_dict()}")
        print(f"Words with replacements: {len(processed_df[processed_df['replacement_word'] != ''])}")
        
        print(f"\n=== Sample Data ===")
        print(processed_df.head(10))
        
    except Exception as e:
        logger.error(f"Failed: {e}")

if __name__ == "__main__":
    main() 