import pandas as pd
from pos_tagger import process_bad_words_dataset, save_processed_dataset

def create_sample_dataset():
    """
    Create a sample dataset for testing.
    """
    sample_data = {
        'badword': [
            'fuck', 'shit', 'bastard', 'asshole', 'damn', 'hell',
            'bitch', 'dick', 'pussy', 'cock', 'fucker', 'motherfucker',
            'crap', 'piss', 'tits', 'whore', 'slut', 'cunt', 'faggot',
            'nigger', 'fuck', 'shit', 'damn'  # Some duplicates
        ]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_bad_words.csv', index=False)
    print("Sample dataset created: sample_bad_words.csv")
    return df

def test_pos_tagger():
    """
    Test the POS tagger with sample data.
    """
    print("=== Testing POS Tagger ===\n")
    
    # Create sample dataset
    create_sample_dataset()
    
    # Process the dataset
    print("Processing dataset...")
    processed_df = process_bad_words_dataset('sample_bad_words.csv', bad_word_column='badword')
    
    # Display results
    print("\n=== Results ===")
    print(f"Total unique words: {len(processed_df)}")
    print(f"POS distribution:")
    print(processed_df['type'].value_counts())
    
    print("\n=== Sample Results ===")
    print(processed_df.head(15))
    
    # Save results
    save_processed_dataset(processed_df, 'test_processed_bad_words.csv')
    
    print("\n=== Test completed successfully! ===")
    print("Output file: test_processed_bad_words.csv")

if __name__ == "__main__":
    test_pos_tagger() 