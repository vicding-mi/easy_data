# encoding: utf-8
import lxml.objectify as objectify
import lxml.etree as et
import os
from os.path import join
import csv

xml_path = '/Users/vic/Downloads/metadata-export-2020-02-13'
output_file_path = '/Users/vic/Documents/DANS/projects/ODISSEI/list_easy_additional_metadata_file/output.csv'
# sample_file_path = '/Users/vic/Downloads/metadata-export-2020-02-13/easy-dataset:33287.xml'
ns_dc = '{http://purl.org/dc/elements/1.1/}'
namespaces = {'dc': 'http://purl.org/dc/elements/1.1/',
              'eas': 'http://easy.dans.knaw.nl/easy/easymetadata/eas/',
              'emd': 'http://easy.dans.knaw.nl/easy/easymetadata/',
              'dct': 'http://purl.org/dc/terms/'}

counter = 0

with open(output_file_path, 'a+') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

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
                identifiers = root.xpath('//dc:identifier[@eas:scheme="DOI"]', namespaces=namespaces)
                files = root.xpath('//file[contains(@name, "additional-metadata-P")]', namespaces=None)

                if identifiers and len(identifiers) > 0:
                    identifier = identifiers[0].text
                    if files and len(files) > 0:
                        for i in files:
                            counter += 1
                            dataset_id = i.xpath('./datasetId')[0].text
                            filename = i.xpath('./completePath')[0].text

                            filewriter.writerow([counter, dataset_id, identifier, filename])
                            print(f'{counter}, {dataset_id}, {identifier}, {filename}')

