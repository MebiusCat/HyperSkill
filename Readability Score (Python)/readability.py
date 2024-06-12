import argparse
import math
import nltk
from nltk.tokenize import sent_tokenize

def index_description(idx):
    if idx >= 14:
        return '18-22'
    else:
        return f'{idx + 4}-{idx + 5}'


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
count_symbols = len(text
                    .replace(' ', '')
                    .replace('\n', '')
                    .replace('\t', ''))

# Count the number of word in the text
count_words = len(nltk.regexp_tokenize(text, "[0-9A-z']+"))

# Tokenize the text into sentences and count them
count_sent = len(sent_tokenize(text))

# Calculate Automated readability index
score = 4.71 * count_symbols / count_words + 0.5 * count_words / count_sent - 21.43
score = math.ceil(score)

# Determine the difficulty of the text
# difficulty = 'HARD' if average_words > 10 else 'EASY'

# Output the result
print(f'Text: {text}\n')
print(f'Characters: {count_symbols}')
print(f'Sentences: {count_sent}')
print(f'Words: {count_words}')
print(f'Automated Readability Index: {score}'
      f' (this text should be understood by {index_description(score)} year olds).')
