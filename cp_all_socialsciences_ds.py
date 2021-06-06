# encoding: utf-8
import json.decoder
import shutil

import lxml.etree as et
import os
from os.path import join

xml_path = '/Users/vic/Downloads/metadata-export-2020-02-13'
copy_from_path_json = '/Users/vic/Documents/DANS/projects/ODISSEI/saxon-in-docker/output_path'
output_file_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/json_files'

namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'eas': 'http://easy.dans.knaw.nl/easy/easymetadata/eas/',
              'emd': 'http://easy.dans.knaw.nl/easy/easymetadata/',
              'dct': 'http://purl.org/dc/terms/'}

counter = 0
ss_ds_no = [23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51,
            52, 53, 55, 156, 203, 204, 205, 218]

for workdir, dirs, files in os.walk(xml_path):
    for name in files:
        full_input_file = join(workdir, name)
        if not full_input_file.endswith('xml'):
            continue

        # print(f'### {counter} reading {full_input_file}')
        with open(full_input_file, 'r') as f:
            tree = et.parse(f)
            root = tree.getroot()

            # get DOI
            audiences = root.xpath('//dct:audience', namespaces=namespaces)
            if audiences and len(audiences) > 0:
                for a in audiences:
                    if a is not None and a.text:
                        try:
                            a_no = int(a.text.split(':')[1])
                        except Exception as ex:
                            print(f'### Error processing file: {f.name}')
                            exit()
                        if a_no in ss_ds_no:
                            local_name = f.name.split('/')[-1].replace('xml', 'json')
                            full_output_file = join(output_file_path, local_name)
                            full_copy_from_file = join(copy_from_path_json, local_name)
                            if os.path.isfile(full_copy_from_file):
                                print(f'### {counter} # copy from {full_copy_from_file}')
                                print(f'### {counter} # copy to {full_output_file}')
                                shutil.copyfile(full_copy_from_file, full_output_file)
                            counter += 1
                            break
