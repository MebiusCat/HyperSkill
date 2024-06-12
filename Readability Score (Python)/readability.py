from nltk.tokenize import sent_tokenize

text = input()

sent_count = sent_tokenize(text)

if len(text) <= 100 and len(sent_count) <= 3:
    print(f'Difficulty: EASY')
else:
    print('Difficulty: HARD')
