import json
import logging
import os
import sys
import pytest
from autoUtils.fileReader import read_config_file
from autoUtils.requestFactory import test_api_request
from autoUtils.optionUtil import change_to_random_string, change_to_random_int
from autoUtils.optionUtil import get_public_canned_message_rootcategory, ifItemInKeysAndValueNotNone
import pdb



logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


def create(login_info, config_data_json_dict, item):
    body = config_data_json_dict[item]['body']
    body = change_to_random_string(body)
    body = change_to_random_int(body)
    # 以下代码用于publiccannedmessagecategory和publiccannedmessage,因为这两个接口需要在body中传categoryID
    if item == 'publiccannedmessagecategory':
        if ifItemInKeysAndValueNotNone('parentId', body):
            body['parentId'] = get_public_canned_message_rootcategory(login_info)
    if item == 'publiccannedmessage':
        if ifItemInKeysAndValueNotNone('categoryId', body):
            body['categoryId'] = get_public_canned_message_rootcategory(login_info)
    # 以上代码用于publiccannedmessagecategory和publiccannedmessage,因为这两个接口在body中需要传categoryID
    method = config_data_json_dict[item]['createMethod']
    url = login_info['dashUrl'] + config_data_json_dict[item]['createPath']
    return test_api_request(url, method, login_info['commonHeader'], body)

def create_api(login_info, config_data_json_dict, item):
    body = config_data_json_dict[item]['body']
    body = change_to_random_string(body)
    body = change_to_random_int(body)
    method = config_data_json_dict[item]['createMethod']
    url = login_info['apiUrl'] + config_data_json_dict[item]['createPath']
    return test_api_request(url, method, login_info['commonHeader'], body)

def delete(login_info, config_data_json_dict, id, item):
    method = config_data_json_dict[item]['deleteMethod']
    url = login_info['dashUrl'] + config_data_json_dict[item]['deletePath'].replace('$id$',id)
    return test_api_request(url, method, login_info['commonHeader'], None)

def delete_api(login_info, config_data_json_dict, id, item):
    method = config_data_json_dict[item]['deleteMethod']
    url = login_info['apiUrl'] + config_data_json_dict[item]['deletePath'].replace('$id$',id)
    return test_api_request(url, method, login_info['commonHeader'], None)


@pytest.fixture(scope='class')
def create_and_delete_contact(login):
    config_data_json_dict = read_config_file('global_test_data.json')
    create_contact_response = create_api(login, config_data_json_dict, 'contacts')
    if create_contact_response.status_code == 201:
        logger.info('contact data initial success')
    else:
        logger.info('contact data initial failed,please retry')
    create_response = json.loads(create_contact_response.content)
    yield create_response
    if not isinstance(create_response,type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete_api(login, config_data_json_dict, create_response['id'], 'contacts')
            print('-----------------contacts delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial contacts error,please manual delete it ')
                logger.error(delete_response.content)

#scope=function，for delete case use
@pytest.fixture()
def every_function_create_contact(login):
    config_data_json_dict = read_config_file('global_test_data.json')
    create_contact_response = create_api(login, config_data_json_dict, 'contacts')
    if create_contact_response.status_code == 201:
        logger.info('contacts data initial success')
        print('-----------------contacts create success--------------')
    else:
        logger.info('contacts data initial failed,please retry')
    create_response = json.loads(create_contact_response.content)
    yield create_response
    if not isinstance(create_response,type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete_api(login, config_data_json_dict, create_response['id'], 'contacts')
            print('-----------------contacts delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial contacts error,please manual delete it ')
                logger.error(delete_response.content)

@pytest.fixture(scope='class')
def initial_data(login, request):
    item = request.param
    config_data_json_dict = read_config_file('global_test_data.json')
    create_response = create(login, config_data_json_dict, item)
    if create_response.status_code == 201:
        logger.info('data initial success')
        print('-----------------create success--------------')
    else:
        logger.info(' data initial failed,please retry')
    create_response = json.loads(create_response.content)
    yield create_response
    if not isinstance(create_response, type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(login, config_data_json_dict, create_response['id'], item)
            print('-----------------delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial data error,please manual delete it ')
                logger.error(delete_response.content)

#function级别 用于delete case
@pytest.fixture()
def function_initial_data(login, request):
    item = request.param
    config_data_json_dict = read_config_file('global_test_data.json')
    create_response = create(login, config_data_json_dict, item)
    if create_response.status_code == 201:
        logger.info('data initial success')
        print('-----------------create success--------------')
    else:
        logger.info(' data initial failed,please retry')
    create_response = json.loads(create_response.content)
    yield create_response
    if not isinstance(create_response, type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(login, config_data_json_dict, create_response['id'], item)
            print('-----------------delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial data error,please manual delete it ')
                logger.error(delete_response.content)

