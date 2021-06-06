# import lxml.etree as et
import os
from os.path import join
from pyDataverse.exceptions import ApiAuthorizationError
from requests import post
import json
import dvconfig

base_url = dvconfig.base_url
native_api_base_url = f'{base_url}/api'
api_token = dvconfig.api_token
dataverse_id = dvconfig.dataverse_name
release = 'no'
fail_counter = 0
total_counter = 0

input_path = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/json_files'
error_file = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/easy-data-error'


def import_dataset(dataverse, metadata, pid=None, release='no', auth=True):
    query_str = f'/dataverses/{dataverse}/datasets/:import?pid={pid}&release={release}'
    resp = post_request(query_str, metadata, auth)

    if resp.status_code == 201:
        identifier = resp.json()['data']['persistentId']
        print('Dataset {} created.'.format(identifier))
    return resp


def write_error_to_file(resp):
    with open(error_file, 'a+') as f:
        json.dump(resp.json(), f)
        f.writelines('\n')


def post_request(query_str, metadata=None, auth=False, params=None):
    """Make a POST request.

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
                'ERROR: POST - Api token not passed to '
                '`post_request` {}.'.format(url)
            )

    try:
        resp = post(
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
            'ERROR: POST - Could not establish connection to api {}.'
            ''.format(url)
        )


def get_pid(full_input_file):
    with open(full_input_file, 'r')as f:
        json_content = json.load(f)
        if json_content:
            return json_content['datasetVersion']['identifier']
    return None


def __main__():
    global total_counter, fail_counter
    for root, dirs, files in os.walk(input_path):
        for name in files:
            full_input_file = join(root, name)
            # full_input_file = '/Users/vic/Documents/DANS/projects/ODISSEI/easy-data/easy-xml/json_files/easy-dataset:33263.json'
            pid = get_pid(full_input_file)
            print(f'### {total_counter} importing {full_input_file}')
            resp = import_dataset(dataverse_id, full_input_file, pid=pid, release=release, auth=True)
            print(resp.status_code)
            print(resp.json())
            print(f'### {total_counter} done with {full_input_file}')
            total_counter += 1
            # exit()
    print(f'In total {total_counter} files processed, and {fail_counter} failed; Please see the log {error_file} for errors')


if __name__ == '__main__':
    __main__()
