# encoding: utf-8
import json
import shutil

import lxml.objectify as objectify
import lxml.etree as et
import os
from os.path import join
import csv

output_file_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/json_files'

counter = 0
error_counter = 0


def cleanse(f, pos):
    f.seek(pos)
    size = len(f.readline())
    pos = pos + size - 1
    f.seek(pos)
    f.write(b' ')


for workdir, dirs, files in os.walk(output_file_path):
    for name in files:
        full_input_file = join(workdir, name)
        if not full_input_file.endswith('json'):
            continue

        with open(full_input_file, 'r+b') as f:
            print(f'### {counter} {f.name}')
            validated = False
            while not validated:

                try:
                    data = json.load(f)
                    validated = True
                except json.decoder.JSONDecodeError as ex:
                    error_counter += 1
                    cleanse(f, ex.pos)
            counter += 1


