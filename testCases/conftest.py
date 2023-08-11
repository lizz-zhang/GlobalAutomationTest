# -*- coding: utf-8 -*-
"""
======================
@author:nash
@time:01/17/2022:3:18 PM
@email:nash.xiang@comm100.com
======================
"""

import json
import os
import re
import sys
from socket import socket
from time import sleep

import pyodbc
import pytest
import logging

from filelock import FileLock
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autoUtils.manage_global_data import ManageGlobalData
from autoUtils.fileReader import read_config_file, get_webdriver_file_with_extension
from autoUtils.requestFactory import test_api_request
from autoUtils.optionUtil import ifItemInKeysAndValueNotNone

# from uiPages.login_page import LoginPage

logger = logging.getLogger(__name__)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)



def pytest_addoption(parser):
    parser.addoption('--environment', action="store", default="decoupling")
    parser.addoption('--ifsentemail', action="store", default="no")
    parser.addoption('--ifconnectdb', action="store", default="no")
    parser.addoption('--browser', action="store", default="chrome")


def agentLogin(request):
    environment = request.config.getoption("--environment")
    ManageGlobalData().set_global_value(environment)
    config_data_json_dict = read_config_file('environments.json')
    dashUrl = config_data_json_dict[environment]['dash']
    apiUrl = config_data_json_dict[environment]['api']
    commonServiceUrl = config_data_json_dict[environment]['commonService']
    apiV4Url = config_data_json_dict[environment]['apiv4']
    internalUrl = config_data_json_dict[environment]['internal']
    jwtTokenAPI = config_data_json_dict[environment]['getJwtTokenByAgent']
    jwtTokenUrl = dashUrl + jwtTokenAPI + str(config_data_json_dict[environment]['agent']['siteId'])
    user_data_json = config_data_json_dict[environment]['agent']
    commonHeader = config_data_json_dict[environment]['commonHeaders']
    routeserverUrl = config_data_json_dict[environment]['routeserver']
    centerUrl = config_data_json_dict[environment]['center']

    oauth_token_path = config_data_json_dict[environment]["oauth_token"]["path"]
    oauth_token_body = config_data_json_dict[environment]["oauth_token"]["body"]
    oauth_reponse = test_api_request(oauth_token_path, "POST", commonHeader, oauth_token_body)
    assert oauth_reponse.status_code == 200
    oauth_header = commonHeader
    oauth_header['Authorization'] = "Bearer " + json.loads(oauth_reponse.content)['access_token']

    login_response = test_api_request(jwtTokenUrl, 'POST', commonHeader, user_data_json)
    assert login_response.status_code == 200
    # login success and get the token
    login_response_dict = json.loads(login_response.content)
    jwtToken = login_response_dict['jwtToken']
    user_data_json['agentId'] = login_response_dict['agentId']
    logger.info("=======Get the api access token=======")
    # prepare the common header
    commonHeader['Authorization'] = "Bearer " + jwtToken
    preparedInformation = {'dashUrl': dashUrl, 'apiUrl': apiUrl, 'commonServiceUrl': commonServiceUrl,
                           'apiV4Url': apiV4Url, 'internalUrl': internalUrl, 'userData': user_data_json,
                           'commonHeader': commonHeader, "oauth_header": oauth_header, 'routeserverUrl': routeserverUrl, 'centerUrl': centerUrl}
    logger.info("=======Prepared the login information successfully=======")
    return preparedInformation


def connectDB(request):
    environment = request.config.getoption("--environment")
    dbconfig_data_json_dict = read_config_file('environments.json')
    sqlserverUrl = dbconfig_data_json_dict[environment]['dbConnectInfo']['sqlserver']
    sqlserverPort = dbconfig_data_json_dict[environment]['dbConnectInfo']['port']
    sqlserverUserName = dbconfig_data_json_dict[environment]['dbConnectInfo']['userName']
    sqlserverPassWord = dbconfig_data_json_dict[environment]['dbConnectInfo']['passWord']
    # db_general_name = dbconfig_data_json_dict[environment]['dbOtherInfo']['db_general_name']
    # db_general_tabels = dbconfig_data_json_dict[environment]['dbOtherInfo']['db_general_tabels']
    # db_site_name = dbconfig_data_json_dict[environment]['dbOtherInfo']['db_site_name']
    # db_site_tables = dbconfig_data_json_dict[environment]['dbOtherInfo']['db_site_tables']
    # 连接到Sqlserver服务器，返回连接句柄conn和操作光标cursor
    logger.info("=======Start to Connect MSSQL=======")
    try:
        if not re.match(r"[0-9]+(.[0-9]+){3}", sqlserverUrl):
            host0 = socket.getaddrinfo(sqlserverUrl, None)
            host = str(host0[0][4][0])
        else:
            host = sqlserverUrl
        connect_str = "DRIVER={SQL Server};SERVER=%s,%s;UID=%s;PWD=%s" % \
                      (host, sqlserverPort, sqlserverUserName, sqlserverPassWord)
        conn = pyodbc.connect(connect_str)
        logger.info("=======Succeed in Connect MSSQL=======")
    except pyodbc.OperationalError as e:
        logger.info("=======Failed in Connecting MSSQL, the error message: %s =======" % e)
    return conn


@pytest.fixture(scope='session')
def login(request, tmp_path_factory, worker_id):
    if worker_id == "master":
        # not executing in with multiple workers, just produce the data and let
        # pytest's fixture caching do its job
        data = agentLogin(request)
    else:
        # get the temp directory shared by all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent

        fn = root_tmp_dir / "loginData.json"
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                data = json.loads(fn.read_text())
            else:
                data = agentLogin(request)
                fn.write_text(json.dumps(data))
    yield data


@pytest.fixture(scope='session')
def getDBInformation(request, tmp_path_factory, worker_id, name="connectDB"):
    ifconnectdb = request.config.getoption("--ifconnectdb")
    if str(ifconnectdb).lower() == 'yes':
        if worker_id == "master":
            # not executing in with multiple workers, just produce the data and let
            # pytest's fixture caching do its job
            conn = connectDB(request)
            data = {'conn': conn}
            # dbdict['db_general_name'] = db_general_name
            # dbdict['db_general_tabels'] = db_general_tabels
            # dbdict['db_site_name'] = db_site_name
            # dbdict['db_site_tables'] = db_site_tables
        else:
            # get the temp directory shared by all workers
            root_tmp_dir = tmp_path_factory.getbasetemp().parent

            fn = root_tmp_dir/"databaseData.json"
            with FileLock(str(fn) + ".lock"):
                if fn.is_file():
                    data = json.loads(fn.read_text())
                else:
                    conn = connectDB(request)
                    # dbdict['db_general_name'] = db_general_name
                    # dbdict['db_general_tabels'] = db_general_tabels
                    # dbdict['db_site_name'] = db_site_name
                    # dbdict['db_site_tables'] = db_site_tables
                    data = {'conn': conn}
                    fn.write_text(json.dumps(data))
        yield data
        try:
            conn.close()
            logger.info("=======Succeed in Closing Connect=======")
        except pyodbc.OperationalError as e:
            logger.info("=======Failed in Closing Connect, the error message: %s=======" % e)
    else:
        logger.info("=======No Need to Connect MSSQL=======")
        # return None


@pytest.fixture(scope='session')
def createWebDriver(request):
    browser = request.config.getoption("--browser")
    environment = request.config.getoption("--environment")
    driver = None
    if browser == 'chrome':
        # 创建Chrome浏览器的一个Options实例对象
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=BDD")
        # 添加屏蔽--ignore--certificate--errors提示信息的设置参数项
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        driver = webdriver.Chrome(executable_path=get_webdriver_file_with_extension('chromedriver.exe'),
                                  options=chrome_options)
    elif browser == 'firfox':
        # 创建Firefox浏览器的一个Options实例对象
        firefox_options = Options()
        driver = webdriver.Chrome(executable_path=get_webdriver_file_with_extension('geckodriver.exe'),
                                  options=firefox_options)
    elif browser == 'edge':
        # 创建edge浏览器的一个Options实例对象
        edge_options = Options()
        driver = webdriver.Chrome(executable_path=get_webdriver_file_with_extension('edge.exe'),
                                  options=edge_options)
    if not isinstance(driver, type(None)):
        driver.maximize_window()
    logger.info("=======Create WebDriver Successfully=======")

    config_data_json_dict = read_config_file('environments.json')
    dashUrl = config_data_json_dict[environment]['dash']
    email_name = config_data_json_dict[environment]['agent']['email']
    passwd = config_data_json_dict[environment]['agent']['password']
    site_id = config_data_json_dict[environment]['agent']['siteId']
    # login_for_all_test = LoginPage(driver, dashUrl, email_name, passwd)
    login_for_all_test = None
    try:
        sleep(5)
        login_for_all_test.login()
        sleep(3)
    except Exception as e:
        logging.info("登录失败，错误信息如下：%s" % e)
    initialDict = {'loginPage': login_for_all_test, 'siteid': site_id}
    yield initialDict
    login_for_all_test.driver.quit()


@pytest.fixture(scope='session')
def creatReportAndSentEmail(request):
    ifsentemail = request.config.getoption("--ifsentemail")
    if ifsentemail == 'yes':
        cmdStr = ''
        yield "start send email"
        logger.info("=======Prepare to send email=======")



@pytest.fixture(scope='session')
def partnerLogin(request, tmp_path_factory, worker_id):
    if worker_id == "master":
        # not executing in with multiple workers, just produce the data and let
        # pytest's fixture caching do its job
        data = partnerUserLogin(request)
    else:
        # get the temp directory shared by all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent

        fn = root_tmp_dir / "partnerLoginData.json"
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                data = json.loads(fn.read_text())
            else:
                data = partnerUserLogin(request)
                fn.write_text(json.dumps(data))
    yield data


def partnerUserLogin(request):
    environment = request.config.getoption("--environment")
    ManageGlobalData().set_global_value(environment)
    config_data_json_dict = read_config_file('environments.json')
    partnerUrl = config_data_json_dict[environment]['partner']
    jwtTokenAPI = config_data_json_dict[environment]['getJwtTokenByPartnerUser']
    jwtTokenUrl = partnerUrl + jwtTokenAPI
    partnerUser_data_json = config_data_json_dict[environment]['partnerUser']
    partnerCommonHeader = config_data_json_dict[environment]['commonHeaders']
    fileServiceUrl = config_data_json_dict[environment]['partnerFileService']


    partner_oauth_token_path = config_data_json_dict[environment]["partner_oauth_token"]["path"]
    partner_oauth_token_body = config_data_json_dict[environment]["partner_oauth_token"]["body"]
    oauth_reponse = test_api_request(partner_oauth_token_path, "POST", partnerCommonHeader, partner_oauth_token_body)
    assert oauth_reponse.status_code == 200
    partner_oauth_header = partnerCommonHeader
    content = json.loads(oauth_reponse.content)
    if ifItemInKeysAndValueNotNone('access_token', content):
        partner_oauth_header['Authorization'] = "Bearer " + content['access_token']


    partnerLogin_response = test_api_request(jwtTokenUrl, 'POST', partnerCommonHeader, partnerUser_data_json)
    assert partnerLogin_response.status_code == 200
    # login success and get the token
    partnerLogin_response_dict = json.loads(partnerLogin_response.content)
    jwtToken = partnerLogin_response_dict['jwtToken']
    logger.info("=======Get the api access token=======")
    # prepare the common header
    partnerCommonHeader['Authorization'] = "Bearer " + jwtToken
    preparedPartnerInformation = {'partnerUrl': partnerUrl, 'partnerUserData': partnerUser_data_json,
                           'partnerCommonHeader': partnerCommonHeader, "partner_oauth_header": partner_oauth_header, "fileServiceUrl": fileServiceUrl}
    logger.info("=======Prepared the login information successfully=======")
    return preparedPartnerInformation


