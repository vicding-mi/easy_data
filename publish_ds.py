import os
import sys

from pyDataverse.api import Api
import csv
import dvconfig

base_url = dvconfig.base_url
api_token = dvconfig.api_token

api = Api(base_url, api_token)
print('API status: ' + api.status)

additional_file_list_in_csv = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/easy_additional_metadata_files.csv'
all_dataverse_ids = set()
all_dataset_ids = set()


def find_children(dataverse_database_id):
    query_str = '/dataverses/' + str(dataverse_database_id) + '/contents'
    params = {}
    resp = api.get_request(query_str, params=params, auth=True)
    for dvobject in resp.json()['data']:
        dvtype = dvobject['type']
        if 'dataverse' == dvtype:
            dvid = dvobject['id']
            find_children(dvid)
            all_dataverse_ids.add(dvid)
        else:
            dvid = f'{dvobject["protocol"]}:{dvobject["authority"]}/{dvobject["identifier"]}'
            all_dataset_ids.add(dvid)


def load_dict_from_csv(csv_path):
    result_list = set()
    with open(csv_path, 'r') as csvf:
        data = csv.reader(csvf, delimiter=',', quotechar='"')
        next(data)
        for r in data:
            result_list.add(f'doi:{r[2]}')
    return result_list


def ds_exists(doi, prefix='doi'):
    resp = api.get_dataset(f'{prefix}:{doi}')
    return True if resp.status_code == 200 else False


def publish_dv(dv_ids, ds_ids):
    for i in dv_ids:
        api.publish_dataverse(i, True)
    for i in ds_ids:
        print(f'Publishing {i}')
        if ds_exists(i, ''):
            api.publish_dataset(i, 'major', True)
        else:
            print(f'{i} does not exist')


def __main__(dv, action='all'):
    find_children(dv)
    ss_dois = load_dict_from_csv(additional_file_list_in_csv)
    other_dois = all_dataset_ids - ss_dois

    print(f'len of all ds {len(all_dataset_ids)}')
    print(f'len of all dv {len(all_dataverse_ids)}')
    print(f'len of ss ds {len(ss_dois)}')
    print(f'len of other ds {len(other_dois)}')
    # exit()

    if action == 'all':
        publish_dv(all_dataverse_ids, all_dataset_ids)
    elif action == 'ss':
        publish_dv(all_dataverse_ids, ss_dois)
    elif action == 'other':
        publish_dv(all_dataverse_ids, other_dois)
    else:
        print(action)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit('Please specify the dv you want to publish and whether you want to publish all/ss/other datasets!')
    else:
        __main__(sys.argv[1], sys.argv[2])
