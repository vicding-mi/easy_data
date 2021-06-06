import argparse
import sys
from pyDataverse.api import Api
import dvconfig
import requests

base_url = dvconfig.base_url
api_token = dvconfig.api_token

api = Api(base_url, api_token)
print('API status: ' + api.status)


def ds_exists(doi, prefix='doi'):
    resp = api.get_dataset(f'{prefix}:{doi}')
    return True if resp.status_code == 200 else False


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def __main__(pid, prefix='doi'):
    if ds_exists(pid, prefix):
        api.delete_dataset(f'{prefix}:{pid}')
        print(f'{pid} removed')
    else:
        print(f'cannot find {pid}')


if __name__ == '__main__':
    pid = sys.argv[1]
    __main__(pid)
