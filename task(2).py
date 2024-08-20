import pandas as pd  # For data manipulation and saving results to CSV
import re  # For regular expression operations (not used in this snippet, but could be useful for text processing)
import nltk  # Natural Language Toolkit for text processing
from nltk.corpus import stopwords, opinion_lexicon, cmudict
from nltk.tokenize import word_tokenize, sent_tokenize
import os  # For interacting with the operating system (e.g., file handling)

# Download necessary NLTK data files
nltk.download('punkt')  # For tokenizing words and sentences
nltk.download('stopwords')  # For a list of common stopwords
nltk.download('opinion_lexicon')  # For sentiment analysis (positive and negative words)
nltk.download('cmudict')  # For pronunciation dictionary (syllable counting)

# Use NLTK's list of English stopwords
stop_words = set(stopwords.words('english'))

# Load the opinion lexicon for sentiment analysis (positive and negative words)
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# Load the CMU Pronouncing Dictionary for counting syllables in words
pronouncing_dict = cmudict.dict()

def syllable_count(word):
    """
    Counts the number of syllables in a word.
    Args:
    - word (str): The word to count syllables for.
    Returns:
    - int: The number of syllables in the word.
    """
    try:
        word = word.lower()
        vowels = 'aeiouy'
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word[-1] in ['e'] and word[-2] not in ['l', 'r']:
            count -= 1
        if count == 0:
            count += 1
        return count
    except:
        return 0  # Handle cases where the word is not found in the CMU Pronouncing Dictionary

def is_complex_word(word):
    """
    Determines if a word is complex based on its syllable count.
    Args:
    - word (str): The word to check.
    Returns:
    - bool: True if the word has more than two syllables, False otherwise.
    """
    return syllable_count(word) > 2

def analyze_text(text):
    """
    Analyzes the text and computes various readability and sentiment metrics.
    Args:
    - text (str): The text to analyze.
    Returns:
    - dict: A dictionary containing computed metrics.
    """
    words = word_tokenize(text)  # Tokenize the text into words
    words = [word.lower() for word in words if word.isalpha()]  # Convert to lowercase and remove non-alphabetic tokens
    cleaned_words = [word for word in words if word not in stop_words]  # Remove stopwords

    sentences = sent_tokenize(text)  # Tokenize the text into sentences
    avg_sentence_length = sum(len(sent.split()) for sent in sentences) / len(sentences)  # Average sentence length

    # Compute the percentage of complex words
    complex_word_count = sum(1 for word in cleaned_words if is_complex_word(word))
    percentage_complex_words = (complex_word_count / len(cleaned_words)) * 100

    # Count personal pronouns
    personal_pronouns = [
        'i', 'me', 'my', 'myself', 'we', 'us', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
        'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'
    ]
    pronoun_count = sum(1 for word in cleaned_words if word.lower() in personal_pronouns)

    # Calculate sentiment scores
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words)

    # Compute polarity and subjectivity scores
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)

    # Additional metrics
    word_count = len(cleaned_words)
    avg_word_length = sum(len(word) for word in cleaned_words) / word_count
    syllable_per_word = sum(syllable_count(word) for word in cleaned_words) / word_count
    fog_index = 0.4 * (avg_sentence_length + complex_word_count / word_count)

    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'avg_word_length': avg_word_length,
        'syllable_per_word': syllable_per_word,
        'fog_index': fog_index,
        'pronoun_count': pronoun_count
    }

def main():
    """
    Main function to process text files in a directory and save analysis results to a CSV file.
    """
    # Specify the directory where your text files are located
    directory = './'  # Adjust this if your files are in a different directory

    # Get the list of text files to process
    files = [f for f in os.listdir(directory) if f.startswith('bctech') and f.endswith('.txt')]

    results = []
    for file in files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        if text:
            print(f"Processing file: {file}")

            # Analyze the text and append results
            analysis_results = analyze_text(text)
            analysis_results['File Name'] = file
            results.append(analysis_results)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df = df[['File Name'] + list(df.columns[:-1])]  # Reorder columns with 'File Name' first
    df.to_csv('final_output.csv', index=False)

    print("Analysis completed and saved to 'final_output.csv'.")

if __name__ == "__main__":
    main()
