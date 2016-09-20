# -*- coding: utf-8 -*-
import json
import re
import check_json


replaceables = {
    '[': '',
    ']': '',
    'HKEY_LOCAL_MACHINE': 'HKLM:',
    '"': '',
    '@=': '(default)='}


def dword_decode(dword):
    return int(dword[6:], 16)


def decode_hex(word, encoding):
    return bytearray.fromhex(word).decode(encoding)


def make_json_registry(in_txt, out_json):
    output = {}
    registry = []
    i = 0
    for line in open(in_txt):
        if line.count('=') > 1:
            pass
        else:
            for k, v in replaceables.items():
                line = line.replace(k, v)
        if 'HKLM:' in line:
            i = 0 if registry == [] else i + 1
            registry.insert(i, [])
            registry[i].append(line)
        else:
<<<<<<< HEAD
            if line != '\r\n' and registry != []:
=======
            if line != '\r\n':
>>>>>>> 5fc7586db550407e4614c5cfdbe895214d965d51
                registry[i].append(line)
    for items in registry:
        items = [item.strip() for item in items]
        hex_string = ''
        registry_keys = {}
        for w in items:
            if ',00' in w:
                hex_string += w
            else:
                if hex_string != '':
                    block = hex_string.split('=')
                    value = re.sub(r'hex\((2|7)\):|,00,|,00|00,|00|,|\\', r'', block[1])
                    value = decode_hex(value, 'cp1251')
                    registry_keys = dict(((block[0], value),))
                    hex_string = ''
                if 'HKLM:' not in w and w != '':
                    block = re.split('=', w, maxsplit=1)
                    value = re.sub(r'\\\\', r'\\', block[1])
                    value = re.sub(r'^\\|\\$', '"', value) if re.match(r'^\\', value) else value
                    value = re.sub(r'\\', '"', value) if re.search(r'\s\\', value) else value
                    value = value.replace('\\ ', '" ')
                    value = dword_decode(value) if 'dword' in value else value
                    registry_keys[block[0]] = value
        output[items[0]] = registry_keys
    with open(out_json, 'w') as f:
        json.dump(output, f, indent=4, separators=(',', ': '), encoding='cp1251')

make_json_registry('TLS.txt', 'ttest.json')
# make_json_registry('Пакет драйверов.txt', 'Драйверы.json')
# make_json_registry('CSP.txt', 'CSP.json')
print ('Файлы json созданы')
# check_json.check_keys('Пакет драйверов.txt', 'Драйверы.json')
check_json.check_keys('TLS.txt', 'ttest.json')
# check_json.check_keys('CSP.txt', 'CSP.json')
# input('Нажмите Enter для выхода...')
