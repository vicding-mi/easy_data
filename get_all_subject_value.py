import csv
import json
import dvconfig
from os.path import join
import os

base_url = dvconfig.base_url
input_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/json_files'

value_list = list()
ss_counter = 0
for root, dirs, files in os.walk(input_path):
    for name in files:
        full_input_file = join(root, name)
        print(f'working on {full_input_file}')
        with open(full_input_file) as f:
            metadata = json.load(f)
            fields = metadata['datasetVersion']['metadataBlocks']['citation']['fields']
            if fields:
                for field in fields:
                    if field['typeName'] == 'subject':
                        value_list.extend(field['value'])
                        if field['value'][0] in ['Social sciences', 'Social Sciences']:
                            ss_counter += 1
# print(set(value_list))
print(f'{ss_counter} ss dataset in total')
with open('/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/output.csv', 'a+') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    value_set = set(value_list)
    for v in value_set:
        file_writer.writerow([v])
# tabular_file = 'data/dataverses/open-source-at-harvard/datasets/open-source-at-harvard/files/2019-02-25.tsv'
# resp = api.upload_file(dataset_pid, tabular_file)
# print(resp)
