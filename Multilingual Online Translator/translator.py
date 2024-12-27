import requests

from bs4 import BeautifulSoup

def intro():
    GREETING = 'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:'

    print(GREETING)
    lang = input()
    print('Type the word you want to translate:')
    word = input()
    print(f'You chose "{lang}" as the language to translate "{word}" to.')
    return lang, word


def translations(lang='fr', word='hello'):
    lang_map = {'fr': 'english-french', 'en': 'french-english'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    url = f'https://context.reverso.net/translation/{lang_map[lang]}/{word}'
    r = requests.get(url, headers=headers)
    print(f'{r.status_code} {r.reason}')

    content = BeautifulSoup(r.content, 'html.parser')
    words_section = content.find_all('div', {'id': 'translations-content'})[0]
    words = [el.attrs['data-term'] for el in words_section.find_all('a')]

    examples_in = [el.text.strip() for el in content.find_all('div', {"class": ['src ltr']})]
    examples_out = [el.text.strip() for el in content.find_all('div', {"class": ['trg ltr']})]

    return words, zip(examples_in, examples_out)


def print_output(lang, words, examples):
    lang_map = {'fr': 'French', 'en': 'English'}
    print(f'\n{lang_map[lang]} Translations:')
    print('\n'.join(words[:5]))
    print(f'\n{lang_map[lang]} Examples:')
    for sent, transl in list(examples)[:5]:
        print(f'{sent}\n{transl}\n')


if __name__ == '__main__':
    lang, word = intro()

    print_output(lang, *translations(lang, word))