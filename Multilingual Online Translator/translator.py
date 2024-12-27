import requests

from bs4 import BeautifulSoup

languages = ['Arabic', 'German', 'English', 'Spanish',
             'French', 'Hebrew', 'Japanese', 'Dutch',
             'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']

def intro():
    print('Hello, welcome to the translator. Translator supports: ')
    print([f'{i + 1}. {name}' for i, name in enumerate(languages)])

    print('Type the number of your language: ')
    lang_in = int(input())
    print('Type the number of language you want to translate to:')
    lang_out = int(input())
    print('Type the word you want to translate:')
    word = input()
    # print(f'You chose "{lang}" as the language to translate "{word}" to.')
    return (lang_in - 1, lang_out - 1), word


def translations(lang=(1, 2), word='hello'):
    lang_in, lang_out = lang
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    url = (f'https://context.reverso.net/translation/{languages[lang_in].lower()}-'
           f'{languages[lang_out].lower()}/{word}')
    r = requests.get(url, headers=headers)
    print(f'{r.status_code} {r.reason}')

    content = BeautifulSoup(r.content, 'html.parser')
    words_section = content.find_all('div', {'id': 'translations-content'})[0]
    words = [el.attrs['data-term'] for el in words_section.find_all('a')]

    examples_in = [el.text.strip() for el in content.find_all('div', {"class": ['src ltr']})]
    examples_out = [el.text.strip() for el in content.find_all('div', {"class": ['trg ltr']})]

    return words, zip(examples_in, examples_out)


def print_output(lang, words, examples):
    lang_in, lang_out = lang
    print(f'\n{languages[lang_out]} Translations:')
    print('\n'.join(words[:5]))
    print(f'\n{languages[lang_out]} Examples:')
    for sent, transl in list(examples)[:5]:
        print(f'{sent}\n{transl}\n')


if __name__ == '__main__':
    lang, word = intro()

    print_output(lang, *translations(lang, word))