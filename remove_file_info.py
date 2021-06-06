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

for workdir, dirs, files in os.walk(output_file_path):
    for name in files:
        full_input_file = join(workdir, name)
        if not full_input_file.endswith('json'):
            continue

        with open(full_input_file, 'r') as f:
            print(f'### {counter} {f.name}')
            data = json.load(f)

            if 'files' in data['datasetVersion'].keys():
                del(data['datasetVersion']['files'])
                with open(full_input_file, 'w') as jsonf:
                    counter += 1
                    json.dump(data, jsonf)

