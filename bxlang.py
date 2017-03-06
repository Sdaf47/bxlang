#!/usr/bin/python3.5

import os
import re
import sys

from gi.module import maketrans

component = sys.argv[-1]

charMap = maketrans(
    'йцукенгшщзхъфывапролджэячсмитьбюё ',
    'ICUKENGSSZHBFYWAPROLDZEYCSMITPBUE_'
)

component_map = (
    '.parameters',
    '.description',
    'class',
    'component',
)

template_map = (
    'template',
    'result_modifier',
    'component_epilog'
)


def generate_symbol_code(file_name, message):
    code = file_name.upper().replace('.', '') + '_' + message.replace(r'[^а-яА-Я0-9\s]', '').lower().translate(charMap)
    return code


def create_lang_file(directory, name, messages):
    lang_dir = directory + 'lang/ru/'
    lang_template = '$MESS["{}"] = "{}";\n'

    if not os.path.isdir(directory + 'lang'):
        if not os.path.isdir(directory + 'lang'):
            os.mkdir(directory + 'lang')
        os.mkdir(lang_dir)

    lang_file = open(lang_dir + name + '.php', 'w+')
    lang_file.write('<?php\n')
    langs = []
    for message in messages:
        lang_o = {
            'code': generate_symbol_code(name, message),
            'message': message,
        }

        lang_file.write(lang_template.format(
            lang_o['code'],
            lang_o['message']
        ))
        langs.append(lang_o)

    return langs


def find_lang(code):
    message = re.findall(r'[а-яА-Я]+[\s,().-_а-яА-Я]+[.,а-яА-Я]', code)
    print(message)
    return message


def replace_component_lang(langs, code):
    for lang in langs:
        pass
        text_template = "\Bitrix\Main\Localization\Loc::getMessage(\"{}\")"
        code = code.replace("\"" + lang['message'] + "\"",  text_template.format(lang['code']))
        code = code.replace("\'" + lang['message'] + "\'", text_template.format(lang['code']))
        code = code.replace(lang['message'], text_template.format(lang['code']))

    return code


def replace_template_lang(langs, code):
    for lang in langs:
        quote_template = "\Bitrix\Main\Localization\Loc::getMessage(\"{}\")"
        text_template = "<?= \Bitrix\Main\Localization\Loc::getMessage(\"{}\") ?>"
        code = code.replace("\"" + lang['message'] + "\"",  quote_template.format(lang['code']))
        code = code.replace("\'" + lang['message'] + "\'", quote_template.format(lang['code']))
        code = code.replace(lang['message'], text_template.format(lang['code']))

    return code

if "/" not in component:
    component_path = component + "/"
else:
    component_path = component

print('Component: ', component[:-1])

for file_name in component_map:
    try:
        file = open(component_path + file_name + '.php')
    except FileNotFoundError:
        continue

    php_code = file.read()

    text_messages = find_lang(php_code)

    lang_list = create_lang_file(component_path, file_name, text_messages)

    php_code = replace_component_lang(lang_list, php_code)

    file.close()

    file = open(component_path + file_name + '.php', 'w+')
    file.write(php_code)

    file.close()

templates = os.listdir(component_path + 'templates/')

for template in templates:
    template_path = component_path + 'templates/' + template + '/'

    if not os.path.isdir(template_path):
        continue

    for file_name in template_map:
        try:
            file = open(template_path + file_name + '.php')
        except FileNotFoundError:
            continue

        php_code = file.read()

        text_messages = find_lang(php_code)

        lang_list = create_lang_file(template_path, file_name, text_messages)

        php_code = replace_template_lang(lang_list, php_code)

        file.close()

        file = open(template_path + file_name + '.php', 'w+')
        file.write(php_code)

        file.close()
