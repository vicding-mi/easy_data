import os
from pyDataverse.api import Api
import csv
import dvconfig

base_url = dvconfig.base_url
api_token = dvconfig.api_token

api = Api(base_url, api_token)
print('API status: ' + api.status)

additional_json_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/additional_files_json'
additional_file_list_in_csv = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/easy_additional_metadata_files.csv'


def load_dict_from_csv(csv_path):
    result_dict = dict()
    with open(csv_path, 'r') as csvf:
        data = csv.reader(csvf, delimiter=',', quotechar='"')
        for r in data:
            result_dict[r[3].split('.')[0]] = r[2]
    return result_dict


def load_filename_into_key_list():
    filenames_list = list()
    for root, dirs, files in os.walk(additional_json_path):
        for name in files:
            filenames_list.append(name.split('.')[0])
    return filenames_list


def get_doi_by_filename(mapping_dict, filename, prefix='original/'):
    filename = f'{prefix}{filename}'
    if filename in mapping_dict.keys():
        return mapping_dict[filename]
    return None


def ds_exists(doi, prefix='doi:'):
    resp = api.get_dataset(f'{prefix}{doi}')
    return True if resp.status_code == 200 else False


def __main__():
    mapping_dict = load_dict_from_csv(additional_file_list_in_csv)

    for f in load_filename_into_key_list():
        current_doi = get_doi_by_filename(mapping_dict, f)
        # check if this doi exists on DV installation
        if current_doi is not None and isinstance(current_doi, str):
            if not ds_exists(current_doi):
                print(f'{f} has doi {current_doi}: Exists: No')
            else:
                print(f'{f} has doi {current_doi}: Exists: Yes')
                print(f'{base_url}/dataset.xhtml?persistentId=doi:{current_doi}&version=DRAFT')


if __name__ == '__main__':
    __main__()
