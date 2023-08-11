import json
import logging
import os
import pdb
import sys
import pytest
from autoUtils.fileReader import read_config_file
from autoUtils.requestFactory import test_api_request
from autoUtils.optionUtil import change_to_random_string, ifItemInKeysAndValueNotNone, upload_file
from autoUtils.manage_global_data import ManageGlobalData


logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


def create(login_info, config_data_json_dict, item):
    partner_id = ManageGlobalData().get_partner_id()
    body = config_data_json_dict[item]['body']
    body = change_to_random_string(body)
    # pdb.set_trace()
    role_path = login_info['partnerUrl'] + config_data_json_dict[item]['getAdminRoleIdPath']
    role_method = config_data_json_dict[item]['getAdminRoleIdMethod']
    get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
    assert get_role_response.status_code == 200
    admin_role_id = json.loads(get_role_response.content)[0]['id']

    if ifItemInKeysAndValueNotNone('confirmEmail', body):
        body['confirmEmail'] = body['email']
    if ifItemInKeysAndValueNotNone('partnerRoleIds', body):
        body['partnerRoleIds'][0] = admin_role_id

    method = config_data_json_dict[item]['createMethod']
    url = login_info['partnerUrl'] + config_data_json_dict[item]['createPath'].replace('$partnerId$', str(partner_id))
    return test_api_request(url, method, login_info['partnerCommonHeader'], body)

def delete(login_info, config_data_json_dict, id, item):
    partner_id = ManageGlobalData().get_partner_id()
    method = config_data_json_dict[item]['deleteMethod']
    url = login_info['partnerUrl'] + config_data_json_dict[item]['deletePath'].replace('$id$',str(id)).replace('$partnerId$', str(partner_id))
    return test_api_request(url, method, login_info['partnerCommonHeader'], None)

def create_sitecontract(login_info, config_data_json_dict, item):
    body = config_data_json_dict[item]['body']
    paid_siteId = ManageGlobalData().get_partner_paidsiteid()
    if ifItemInKeysAndValueNotNone('siteId', body):
        body['siteId'] = paid_siteId
    if ifItemInKeysAndValueNotNone('siteContractAttachments', body):
        file_key = upload_file('partnerFileServiceTokenPath', 'test_jpg.jpg', 'partner')
        body['siteContractAttachments'][0]['attachment'] = login_info['fileServiceUrl'] + body['siteContractAttachments'][0]['attachment'].replace('$fileKey$', file_key)

    method = config_data_json_dict[item]['createMethod']
    url = login_info['partnerUrl'] + config_data_json_dict[item]['createPath']
    return test_api_request(url, method, login_info['partnerCommonHeader'], body)

@pytest.fixture(scope='class')
def create_and_delete_site_contract(partnerLogin):
    config_data_json_dict = read_config_file('global_test_data.json')
    create_site_contract_response = create_sitecontract(partnerLogin, config_data_json_dict, 'sitecontracts')
    if create_site_contract_response.status_code == 201:
        # logger.info('agent data initial success')
        logger.info('----------------------------partner site contract create success-----------------------------id=%s' % (
        json.loads(create_site_contract_response.content)['id']
        ))
    else:
        logger.error('---------------------partner site contract initial failed,please retry,response is:%s ------------------------------'% json.loads(create_site_contract_response.content))
    create_response = json.loads(create_site_contract_response.content)
    yield create_response
    if not isinstance(create_response,type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(partnerLogin, config_data_json_dict, create_response['id'], 'sitecontracts')
            logger.info('----------------------------site contract delete ---------------------------id=%s-----response code:%s' %(json.loads(create_site_contract_response.content)['id'],delete_response.status_code))
            if delete_response.status_code > 300:
                logger.error('delete initial site contract error,please manual delete it ')
                logger.error(delete_response.content)

# function级别 主要是给delete接口使用的,仍然做删除，是因为有些异常的用例本身就是调不通的，所以数据会处理不掉，需要在这里进行删除
@pytest.fixture()
def every_function_create_and_delete_site_contract(partnerLogin):
    config_data_json_dict = read_config_file('global_test_data.json')
    create_site_contract_response = create_sitecontract(partnerLogin, config_data_json_dict, 'sitecontracts')
    if create_site_contract_response.status_code == 201:
        # logger.info('agent data initial success')
        logger.info('----------------------------partner site contract create success-----------------------------id=%s' % (
        json.loads(create_site_contract_response.content)['id']
        ))
    else:
        logger.error('---------------------partner site contract initial failed,please retry,response is:%s ------------------------------'% json.loads(create_site_contract_response.content))
    create_response = json.loads(create_site_contract_response.content)
    yield create_response
    if not isinstance(create_response,type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(partnerLogin, config_data_json_dict, create_response['id'], 'sitecontracts')
            logger.info('----------------------------site contract delete ---------------------------id=%s-----response code:%s' %(json.loads(create_site_contract_response.content)['id'],delete_response.status_code))
            if delete_response.status_code > 300:
                logger.error('delete initial site contract error,please manual delete it ')
                logger.error(delete_response.content)

def create_child_partner(login_info, config_data_json_dict, item):
    partner_id = ManageGlobalData().get_partner_id()
    body = config_data_json_dict[item]['body']
    body = change_to_random_string(body)
    # pdb.set_trace()
    role_path = login_info['partnerUrl'] + config_data_json_dict[item]['getAdminRoleIdPath']
    role_method = config_data_json_dict[item]['getAdminRoleIdMethod']
    get_role_response = test_api_request(role_path, role_method, login_info['partnerCommonHeader'], None)
    assert get_role_response.status_code == 200
    admin_role_id = json.loads(get_role_response.content)[0]['id']

    if ifItemInKeysAndValueNotNone('confirmEmail', body['partnerUsers'][0]):
        body['partnerUsers'][0]['confirmEmail'] = body['partnerUsers'][0]['email']
    if ifItemInKeysAndValueNotNone('partnerRoleIds', body):
        body['partnerRoleIds'][0] = admin_role_id

    method = config_data_json_dict[item]['createMethod']
    url = login_info['partnerUrl'] + config_data_json_dict[item]['createPath'].replace('$partnerId$', str(partner_id))
    return test_api_request(url, method, login_info['partnerCommonHeader'], body)


@pytest.fixture(scope='class')
def create_and_delete_child_partner(partnerLogin):
    config_data_json_dict = read_config_file('global_test_data.json')
    create_child_partner_response = create_child_partner(partnerLogin, config_data_json_dict, 'childpartner')
    if create_child_partner_response.status_code == 201:
        logger.info('----------------------------childpartner create success-----------------------------id=%s------' % (
        json.loads(create_child_partner_response.content)['id']))
    else:
        logger.error('---------------------childpartner data initial failed,please retry,response is:%s ------------------------------'% json.loads(create_child_partner_response.content))
    create_response = json.loads(create_child_partner_response.content)
    yield create_response
    if not isinstance(create_response,type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(partnerLogin, config_data_json_dict, create_response['id'], 'childpartner')
            logger.info('----------------------------childpartner delete ---------------------------id=%s-----response code:%s' %(json.loads(create_child_partner_response.content)['id'],delete_response.status_code))
            if delete_response.status_code > 300:
                logger.error('delete initial childpartner error,please manual delete it ')
                logger.error(delete_response.content)



@pytest.fixture(scope='class')
def initial_data(partnerLogin, request):
    item = request.param
    config_data_json_dict = read_config_file('global_test_data.json')
    create_response = create(partnerLogin, config_data_json_dict, item)
    if create_response.status_code == 201:
        logger.info('data initial success')
        print('-----------------create success--------------')
    else:
        logger.info(' data initial failed,please retry')
    create_response = json.loads(create_response.content)
    yield create_response
    if not isinstance(create_response, type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(partnerLogin, config_data_json_dict, create_response['id'], item)
            print('-----------------delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial data error,please manual delete it ')
                logger.error(delete_response.content)

#function级别 用于delete case
@pytest.fixture()
def function_initial_data(partnerLogin, request):
    item = request.param
    config_data_json_dict = read_config_file('global_test_data.json')
    create_response = create(partnerLogin, config_data_json_dict, item)
    if create_response.status_code == 201:
        logger.info('data initial success')
        print('-----------------create success--------------')
    else:
        logger.info(' data initial failed,please retry')
    create_response = json.loads(create_response.content)
    yield create_response
    if not isinstance(create_response, type(None)):
        if 'id' in create_response and not isinstance(create_response, type(None)):
            delete_response = delete(partnerLogin, config_data_json_dict, create_response['id'], item)
            print('-----------------delete success--------------')
            if delete_response.status_code > 300:
                logger.error('delete initial data error,please manual delete it ')
                logger.error(delete_response.content)
