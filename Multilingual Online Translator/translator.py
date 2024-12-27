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
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    lang_out = int(input())
    print('Type the word you want to translate:')
    word = input()
    # print(f'You chose "{lang}" as the language to translate "{word}" to.')
    return (lang_in - 1, lang_out - 1), word, lang_out == 0


def translations(lang=(1, 2), word='hello', show_status=False):
    lang_in, lang_out = lang
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    url = (f'https://context.reverso.net/translation/{languages[lang_in].lower()}-'
           f'{languages[lang_out].lower()}/{word}')
    r = requests.get(url, headers=headers)
    if show_status:
        print(f'{r.status_code} {r.reason}')

    content = BeautifulSoup(r.content, 'html.parser')

    words_section = content.find_all('div', {'id': 'translations-content'})
    if len(words_section) == 0:
        return [], zip([''], [])
        # return [], []
    words_section = words_section[0]
    words = [el.attrs['data-term'] for el in words_section.find_all('a')]

    examples_in = [el.text.strip() for el in content.find_all('div', {"class": ['src ltr']})]
    examples_out = [el.text.strip() for el in content.find_all('div', {"class": ['trg ltr', 'trg rtl arabic', 'trg rtl']})]

    return words, zip(examples_in, examples_out)


def output(lang, words, examples, limit=5):
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        lang_in, lang_out = lang
        print(f'\n{languages[lang_out]} Translations:')
        print(f'\n{languages[lang_out]} Translations:', file=f)
        print('\n'.join(words[:limit]))
        print('\n'.join(words[:limit]), file=f)
        print(f'\n{languages[lang_out]} Examples:')
        print(f'\n{languages[lang_out]} Examples:', file=f)
        for sent, transl in list(examples)[:limit]:
            print(f'{sent}\n{transl}\n')
            print(f'{sent}\n{transl}\n', file=f)


def output_to_all(lang, word, limit=1):
    lang_in, lang_out = lang
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        for i in range(len(languages)):
            if lang_in == i:
                continue
            words, examples = translations((lang_in, i), word)

            print(f'\n{languages[i]} Translations:')
            print(f'\n{languages[i]} Translations:', file=f)
            print('\n'.join(words[:limit]))
            print('\n'.join(words[:limit]), file=f)
            print(f'\n{languages[i]} Examples:')
            print(f'\n{languages[i]} Examples:', file=f)
            for sent, transl in list(examples)[:limit]:
                print(f'{sent}\n{transl}\n')
                print(f'{sent}\n{transl}\n', file=f)


if __name__ == '__main__':
    # get_results(12, 0, 'глаза')
    lang, word, to_all = intro()

    if not to_all:
        output(lang, *translations(lang, word, True))
    else:
        output_to_all(lang, word)
