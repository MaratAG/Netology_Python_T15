"""Решение задачи №14 к курсу Нетология Пайтон."""

import os

import chardet

import requests


class Textfile(object):
    """Класс - текстовый файл."""

    name = None
    language = None
    encoding = None
    original_text = None
    translate_text = None

    def __init__(self, filename):
        """Объявление класса и чтение файла в аттрибуты экземпляра класса."""
        with open(filename, 'rb') as f:
            file_for_translate = f.read()
            attribs_file = chardet.detect(file_for_translate)

            self.name = filename
            self.language = self.name[-6:-4].lower()
            self.encoding = attribs_file['encoding']
            self.original_text = file_for_translate.decode(self.encoding)

    def translate_text(self, result_language, url, key_api):
        """Перевод текста с одного яызка на другой с помощью Яндедкс."""
        language_to_language = self.language + '-' + result_language
        params = {'key': key_api,
                  'lang': language_to_language,
                  'text': self.original_text,
                  }
        response = requests.get(url, params=params).json()
        self.translate_text = ' '.join(response.get('text', []))

    def write_translate_text_to_file(self, result_file):
        """Запись переведенного текста в файл."""
        with open(result_file, 'w', encoding=self.encoding) as f:
            f.write(self.translate_text)


def locate_and_make_result_dir(name_result_dir):
    """Проверка наличия директории (при необходимости - создания)."""
    result_dir = os.path.join(os.path.dirname(__file__), name_result_dir)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    return result_dir


def main():
    """Модуль инициализации программы."""
    result_dir = locate_and_make_result_dir('Result')
    source_dir = os.path.join(os.getcwd(), 'Source')
    files = os.listdir(source_dir)

    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key_api = \
        'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.' \
        'a95fd4bfde5c1794fa433453956bd261eae80152'

    result_language = input('На какой язык перевести пакет файлов? '
                            '(по умолчанию - ru)').strip()[:2]
    if len(result_language) == 0:
        result_language = 'ru'

    for file in files:
        source_file = os.path.join(source_dir, file)
        result_file = os.path.join(result_dir, file)

        file_for_translate = Textfile(source_file)
        file_for_translate.translate_text(result_language, url, key_api)
        file_for_translate.write_translate_text_to_file(result_file)

    print("Перевод пакета файлов закончен!")


main()
