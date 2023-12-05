import re
from collections import Counter

def determine_most_used_words(text, top_n=10):
    """
    Determine the most frequently used words in a given text.

    Parameters:
    - text (str): The input text from which to extract word frequencies.
    - top_n (int, optional): The number of top words to retrieve. Default is 10.

    Returns:
    list: A list of tuples containing the most used words and their frequencies.
          Each tuple has the format (word, frequency), sorted by frequency in descending order.
    """
    # Remove punctuation and numbers from the text
    text = re.sub(r'[^\w\s]', '', text)
    
    # Convert the text to lowercase and split it into words
    words = text.lower().split()

    # Count the frequencies of words
    word_frequencies = Counter(words)

    # Determine the most used words
    most_used_words = word_frequencies.most_common(top_n)

    return most_used_words
