from pyDataverse.api import Api
from pyDataverse.exceptions import ApiAuthorizationError
import csv
import json
import os
from pathlib import Path
from requests import put
import dvconfig

fail_counter = 0
total_counter = 0

base_url = dvconfig.base_url
api_token = dvconfig.api_token
native_api_base_url = f'{base_url}/api'

api = Api(base_url, api_token)
print('API status: ' + api.status)

error_file = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/easy-additional-metadata-error'
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


def get_full_file_name(filename, postfix='.json'):
    return Path(additional_json_path, filename).with_suffix(postfix)


def write_error_to_file(resp):
    with open(error_file, 'a+') as f:
        json.dump(resp.json(), f)
        f.writelines('\n')


def put_request(query_str, metadata=None, auth=False, params=None):
    """Make a PUT request.

    Parameters
    ----------
    query_str : string
        Query string for the request. Will be concatenated to
        `native_api_base_url`.
    metadata : string
        Metadata as a json-formatted string. Defaults to `None`.
    auth : bool
        Should an api token be sent in the request. Defaults to `False`.
    params : dict
        Dictionary of parameters to be passed with the request.
        Defaults to `None`.

    Returns
    -------
    requests.Response
        Response object of requests library.

    """
    global fail_counter, total_counter

    url = '{0}{1}'.format(native_api_base_url, query_str)

    if auth:
        if api_token:
            if not params:
                params = {}
            params['key'] = api_token
        else:
            ApiAuthorizationError(
                'ERROR: PUT - Api token not passed to '
                '`put_request` {}.'.format(url)
            )

    try:
        resp = put(
            url,
            data=open(metadata, mode='rb').read(),
            params=params
        )
        if resp.status_code < 200 or resp.status_code > 299:
            fail_counter += 1
            write_error_to_file(resp)
        return resp
    except ConnectionError:
        raise ConnectionError(
            'ERROR: PUT - Could not establish connection to api {}.'
            ''.format(url)
        )


def update_metadata(filename, pid, auth=True):
    query_str = f'/datasets/:persistentId/editMetadata/?persistentId=doi:{pid}'
    resp = put_request(query_str, filename, auth)

    if resp.status_code == 201:
        identifier = resp.json()['data']['persistentId']
        print('Dataset {} created.'.format(identifier))
    return resp


def __main__():
    mapping_dict = load_dict_from_csv(additional_file_list_in_csv)
    for f in load_filename_into_key_list():
        current_doi = get_doi_by_filename(mapping_dict, f)

        # check if this doi exists on DV installation
        if current_doi is not None and isinstance(current_doi, str):
            if ds_exists(current_doi):
                print(f'{f} has doi {current_doi}: Exists: Yes; Updating...')
                full_input_filename = get_full_file_name(f)
                resp = update_metadata(full_input_filename, current_doi)
                # TODO: try replacing update_metadata with the following api call, if it works, should stick to pyDataverse
                # resp = api.edit_dataset_metadata(current_doi, open(full_input_filename, mode='r').read())
                if 300 > resp.status_code >= 200:
                    print(f'{base_url}/dataset.xhtml?persistentId=doi:{current_doi}&version=DRAFT')
                    print(f'{f} has doi {current_doi}: Exists: Yes; Updated')
                else:
                    print(f'{f} has doi {current_doi}: Exists: Yes; Update failed')


if __name__ == '__main__':
    __main__()
