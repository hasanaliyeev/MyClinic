import re


def phone_validator(number):
    pattern = re.compile(r'^(\+7|8)[0-9]{10}$')
    return pattern.match(number)


def slug_generator(word):
    dictionary = {
        'ё': 'yo',
        'й': 'j',
        'ц': 'c',
        'у': 'u',
        'к': 'k',
        'е': 'e',
        'н': 'n',
        'г': 'g',
        'ш': 'sh',
        'щ': 'sh',
        'з': 'z',
        'х': 'x',
        'ф': 'f',
        'ы': 'y',
        'в': 'v',
        'а': 'a',
        'п': 'p',
        'р': 'r',
        'о': 'o',
        'л': 'l',
        'д': 'd',
        'ж': 'zh',
        'э': 'e',
        'я': 'ya',
        'ч': 'ch',
        'с': 's',
        'м': 'm',
        'и': 'i',
        'т': 't',
        'ь': '',
        'б': 'b',
        'ю': 'yu',
        'ъ': ''
    }
    word = word.lower()
    translated_list = list()
    translated_word = ''
    for i in word:
        if dictionary.get(i):
            translated_list.append(dictionary.get(i))
        else:
            translated_list.append(i)
    return translated_word.join(translated_list)
