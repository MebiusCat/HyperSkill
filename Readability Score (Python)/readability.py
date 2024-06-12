import argparse
import nltk
from nltk.tokenize import sent_tokenize

#  Download the necessary NLTK models for sentence tokenization
nltk.download('punkt')

# Set up parameters for reading file
parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

# Read the text from user file
with open(args.file) as f:
    text = f.read()

# Count the number of symbols in the text
count_symbols = len(text)

# Count the number of word in the text
count_words = len(nltk.regexp_tokenize(text, "[0-9A-z']+"))

# Tokenize the text into sentences and count them
count_sent = len(sent_tokenize(text))

# Calculate the average number of words
average_words = count_words / count_sent

# Determine the difficulty of the text
difficulty = 'HARD' if average_words > 10 else 'EASY'

# Output the result
print(f'Text: {text}')
print(f'Difficulty: {difficulty}')
