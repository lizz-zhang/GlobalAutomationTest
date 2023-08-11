# -*- coding: utf-8 -*-
"""
======================
@author:Mila
@time:04/27/2022:3:18 PM
@email:Mila.song@comm100.com
======================
"""
import json
import logging
import pdb
import pytest
import allure
import os
import logging
from autoUtils.assertFactory import commonResponseAssert
from autoUtils.requestFactory import test_api_request
from autoUtils.ymlLib import ReadFile
import uuid

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
fileName = basedir + '\\apiTestData\\global\\platform\\registerApi\\' + os.path.basename(__file__).split('.')[0] + '.yml'
readfile = ReadFile(fileName)
cases, parameters = readfile.get_businessTests_data()

logger = logging.getLogger(__name__)

class TestRegister:
    # request_url, request_type, request_header, request_body
    @pytest.mark.registerapi
    @pytest.mark.mila
    @pytest.mark.smoke
    @pytest.mark.parametrize('case, http, expect', list(parameters), ids=cases)

    def test_register(self, case, http, expect,login):
        login_info = login
        env_dash = login_info['dashUrl']
        temp = uuid.uuid4()

        http['body']['email'] = str(temp)+"@auto.com"
        get_response = test_api_request(env_dash+http['path'], http['method'], http['head'], http['body'])

        commonResponseAssert(get_response, expect)

        logger.info('----------register ----------id=%s-----response code=%s' % (json.loads(get_response.content), get_response.status_code))
