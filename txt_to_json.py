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
            if line != '\r\n' and registry != [] and '=' in line:
                registry[i].append(line)
    for items in registry:
        items = [item.strip() for item in items]
        hex_string = ''
        registry_keys = {}
        for regkey in items:
            if ',00' in regkey:
                hex_string += regkey
            else:
                if hex_string != '':
                    key, value = hex_string.split('=')
                    value = re.sub(r'hex\((2|7)\):|,00,|,00|00,|00|,|\\', r'', value)
                    value = decode_hex(value, 'cp1251')
                    registry_keys = dict(((key, value),))
                    hex_string = ''
                if 'HKLM:' not in regkey and regkey != '':
                    key, value = re.split('=', regkey, maxsplit=1)
                    value = re.sub(r'\\\\', r'\\', value)
                    if re.match(r'^\\', value): value = re.sub(r'^\\|\\$', '"', value)
                    if re.search(r'\s\\', value): value = re.sub(r'\\', '"', value)
                    value = value.replace('\\ ', '" ')
                    if 'dword' in value: value = dword_decode(value)
                    registry_keys[key] = value
        output[items[0]] = registry_keys
    with open(out_json, 'w') as f:
        json.dump(output, f, indent=4, separators=(',', ': '), encoding='cp1251')


input_txt_file = raw_input('Введите исходный txt файл: ')
output_json_file = raw_input('Введите имя файла для json: ')

try:
    make_json_registry(input_txt_file, output_json_file)
    print ('Файлы json созданы')
    check_json.check_keys(input_txt_file, output_json_file)
except IOError as e:
    print e
