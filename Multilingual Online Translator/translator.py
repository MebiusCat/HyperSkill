GREETING = 'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:'

print(GREETING)
language = input()
print('Type the word you want to translate:')
word = input()
print(f'You chose "{language}" as the language to translate "{word}" to.')
