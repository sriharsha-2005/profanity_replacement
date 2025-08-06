import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import logging

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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_word_pos(word):
    """
    Get the primary POS (Part of Speech) for a word.
    Returns 'noun' or 'verb', defaults to 'noun' if unclear.
    
    Args:
        word (str): The word to analyze
        
    Returns:
        str: 'noun' or 'verb'
    """
    try:
        # Get all synsets for the word
        synsets = wordnet.synsets(word.lower())
        
        if not synsets:
            # If no synsets found, use NLTK POS tagger
            pos_tags = pos_tag([word.lower()])
            tag = pos_tags[0][1] if pos_tags else 'NN'
            
            # Map NLTK tags to our categories
            if tag.startswith('VB'):  # Verb tags
                return 'verb'
            elif tag.startswith('NN'):  # Noun tags
                return 'noun'
            else:
                return 'noun'  # Default to noun
        
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

def process_bad_words_dataset(input_file, bad_word_column='badword'):
    """
    Process a dataset of bad words, remove duplicates, and add POS tagging.
    
    Args:
        input_file (str): Path to the CSV file containing bad words
        bad_word_column (str): Name of the column containing bad words
        
    Returns:
        pd.DataFrame: Processed dataset with columns: badword, replacement_word, type
    """
    try:
        # Load the dataset
        logger.info(f"Loading dataset from {input_file}")
        df = pd.read_csv(input_file)
        
        # Check if the bad word column exists
        if bad_word_column not in df.columns:
            available_columns = list(df.columns)
            logger.error(f"Column '{bad_word_column}' not found. Available columns: {available_columns}")
            raise ValueError(f"Column '{bad_word_column}' not found in the dataset")
        
        # Extract bad words and remove duplicates
        bad_words = df[bad_word_column].dropna().astype(str).str.lower().unique()
        logger.info(f"Found {len(bad_words)} unique bad words")
        
        # Create new dataset
        processed_data = []
        
        for word in bad_words:
            word = word.strip()
            if word:  # Skip empty strings
                pos_type = get_word_pos(word)
                processed_data.append({
                    'badword': word,
                    'replacement_word': '',  # Will be filled later
                    'type': pos_type
                })
        
        # Create DataFrame
        result_df = pd.DataFrame(processed_data)
        
        # Sort by word for better organization
        result_df = result_df.sort_values('badword').reset_index(drop=True)
        
        logger.info(f"Processed dataset created with {len(result_df)} unique words")
        logger.info(f"POS distribution: {result_df['type'].value_counts().to_dict()}")
        
        return result_df
        
    except Exception as e:
        logger.error(f"Error processing dataset: {e}")
        raise

def save_processed_dataset(df, output_file='processed_bad_words.csv'):
    """
    Save the processed dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): The processed dataset
        output_file (str): Output file path
    """
    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Processed dataset saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving dataset: {e}")
        raise

def main():
    """
    Main function to demonstrate usage.
    """
    # Example usage
    try:
        # Replace 'your_bad_words.csv' with your actual file path
        input_file = 'your_bad_words.csv'
        
        # Process the dataset
        processed_df = process_bad_words_dataset(input_file, bad_word_column='badword')
        
        # Save the result
        save_processed_dataset(processed_df, 'processed_bad_words_with_pos.csv')
        
        # Display sample results
        print("\nSample processed data:")
        print(processed_df.head(10))
        
        print(f"\nPOS distribution:")
        print(processed_df['type'].value_counts())
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main() 