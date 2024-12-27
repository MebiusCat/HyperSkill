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
    soup = BeautifulSoup(r.content, 'html.parser')
    tr_content = soup.find_all('div', {'id': 'translations-content'})
    words = []
    for el in tr_content:
        for chel in el.find_all():
            if chel.has_attr('data-term'):
                words.append(chel.attrs['data-term'])

    print('Translations')
    print(words)

    examples = []
    tr_example = soup.find_all('div', {'class': 'example'})
    for sent in tr_example:
        examples.append(sent.find('div', {'class': 'src ltr'}).text.strip())
        examples.append(sent.find('div', {'class': 'trg ltr'}).text.strip())
    print(examples)



if __name__ == '__main__':
    lang, word = intro()
    translations(lang, word)