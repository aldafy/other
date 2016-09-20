# -*- coding: utf-8 -*-
import json
import re


def check_keys(registry_file_txt, registry_file_json):
    txt_count = 0
    with open(registry_file_json) as jfile:
        data = json.load(jfile)
        json_count = len(data)

    for line in open(registry_file_txt):
        if 'HKEY' in line:
            txt_count += 1

    if json_count != txt_count:
        print 'В файле %s отсутствуют следующие ветки реестра:' % registry_file_json
        for line in open(registry_file_txt):
            if 'HKEY' in line:
                line = line.replace('HKEY_LOCAL_MACHINE', 'HKLM:')
                line = re.sub('\[|\]', '', line)
                if line.strip() not in data.keys():
                    print line
    else:
        print 'Все ветки перенесены в файл %s успешно' % registry_file_json
