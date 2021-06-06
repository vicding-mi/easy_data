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
            print(f'### {f.name}')
            metadata = json.load(f)
            fields = metadata['datasetVersion']['metadataBlocks']['citation']['fields']
            if fields:
                for field in fields:
                    if field['typeName'] == 'subject':
                        field['value'] = ['Social Sciences']
                        with open(full_input_file, 'w') as jsonf:
                            counter += 1
                            json.dump(metadata, jsonf)

