# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:12/17/2021:3:18 PM
@email:nash.xiang@comm100.com
======================
"""

import csv
import glob
import json
import os
from pathlib import Path

TEST_DATA_BASE_PATH = Path.cwd().joinpath('apiTestCases')
CONFIG_DATA_BASE_PATH = Path.cwd().joinpath('autoConfig')
Third_Tools_BASE_PATH = Path.cwd().joinpath('theThirdTools')


def get_test_data_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = TEST_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = TEST_DATA_BASE_PATH.joinpath(f'{file_name}.json')
    return path


def get_test_data_file_with_csv_extension(file_name):
    if '.csv' in file_name:
        path = TEST_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = TEST_DATA_BASE_PATH.joinpath(f'{file_name}.csv')
    return path


def get_files_list_with_ext(extension):
    os.chdir(TEST_DATA_BASE_PATH)
    file_list = glob.glob('*.{}'.format(extension))
    file_list.sort()
    return file_list


def read_config_file(file_name):
    path = get_config_file_with_json_extension(file_name)
    with path.open(mode='r') as f:
        return json.load(f)


def get_config_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = CONFIG_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = CONFIG_DATA_BASE_PATH.joinpath(f'{file_name}.json')
    return path


def get_webdriver_file_with_extension(file_name):
    if '.exe' in file_name:
        path = Third_Tools_BASE_PATH.joinpath(file_name)
    else:
        path = None
    return path


