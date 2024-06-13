import sys
import math
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize

def index_description(idx):
    if idx >= 14:
        return '18-22', 18, 22
    else:
        return f'{idx + 4}-{idx + 5}', idx + 4, idx + 5

def counting_syllables(letters, words):
    result = re.findall('[aeiouy]+', letters, flags=re.I)
    count = sum(1 if len(elem) == 1 else len(elem) - 1 for elem in result)

    silent = re.findall('e[ ,\s.?!]', letters)
    count -= len(silent)

    double_silent = re.findall('ee[,\s.?!]', letters)
    count += len(double_silent)

    # silent_d = 0
    for word in words:
        count += 1 if len(word) == 2 and word.endswith('e') else 0

    return count

def counting_words_difficulty(longman, text_words):
    count = 0
    for word in text_words:
        count += 1 if word not in longman else 0
    return count

#  Download the necessary NLTK models for sentence tokenization
nltk.download('punkt')

# Set up parameters for reading file
# Read the text from user file
with open(sys.argv[1], 'r') as f:
    text = f.read()

with open(sys.argv[2], 'r' , encoding='utf-8-sig') as f:
    longman_3000 = f.readlines()

longman_3000 = [word.strip() for word in longman_3000]

# Count the number of symbols in the text
count_symbols = len(text
                    .replace(' ', '')
                    .replace('\n', '')
                    .replace('\t', ''))

# Count the number of word in the text
word_tokens = nltk.regexp_tokenize(text, "[0-9A-z']+")
count_words = len(word_tokens)

# Tokenize the text into sentences and count them
count_sent = len(sent_tokenize(text))

# Counting syllables
count_syllables = counting_syllables(text, word_tokens)

# Calculate Automated readability index
score = 4.71 * count_symbols / count_words + 0.5 * count_words / count_sent - 21.43
score = math.ceil(score)
idx_AR, a, b = index_description(score)

# Calculate Flesch-Kincaid readability index
scoreFK = (0.39 * count_words / count_sent
           + 11.8 * count_syllables / count_words - 15.59)
scoreFK = math.ceil(scoreFK)
idx_FK, c, d = index_description(scoreFK)

# Calculate word difficulty
word_difficulty = counting_words_difficulty(longman_3000, word_tokens)

# Calculate Dale-Chall Readability Index
scoreDC = 0.1579 * word_difficulty / count_words * 100 + 0.0496 * count_words / count_sent
scoreDC += 3.6365 if scoreDC < 5 else 0
scoreDC = math.ceil(scoreDC)
idx_DC, e, f = index_description(scoreDC)

# Calculate average age
average_age = round((a + b + c + d + e + f) / 6, 1)

# Output the result
print(f'Text: {text}\n')
print(f'Characters: {count_symbols}')
print(f'Sentences: {count_sent}')
print(f'Words: {count_words}')
print(f'Difficult words: {word_difficulty}')
print(f'Syllables: {count_syllables}')
print(f'Automated Readability Index: {score}.'
      f' The text can be understood by  {idx_AR} year olds.')
print(f'Flesch–Kincaid Readability Test: {scoreFK}.'
      f' The text can be understood by {idx_FK} year olds.')
print(f'Dale-Chall Readability Index: {scoreDC}.'
      f' The text can be understood by {idx_DC} year olds.')
print(f'This text should be understood in average by {average_age} year olds.')
