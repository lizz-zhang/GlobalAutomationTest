# -*- coding: utf-8 -*-
from datetime import timedelta
import json
import os
import pdb
import re
import sys
import time
from socket import socket
from time import sleep
import uuid
import pytest
import logging

import requests.auth
from filelock import FileLock
from autoUtils.datetime_util import get_next_weekday
from datetime import datetime, timedelta

from autoUtils.fileReader import read_config_file, get_webdriver_file_with_extension
from autoUtils.requestFactory import send_request
from autoUtils.optionUtil import (
    replace_dict_value_multi,
    searchAndChangeDict,
    ifItemInKeysAndValueNotNone,
)
from faker import Faker

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

fake = Faker()


# create a fixture to refresh gpttranslation cache for one site
@pytest.fixture(scope="function")
def refresh_gpttranslation_cache(login):
    """this will refresh the gpttranslation cache for one site"""

    request_url = login["api_url"] + "/gpttranslationservice/gpttranslation/clearcache"
    res = send_request(request_url, None, "DELETE", None, login["common_headers"], None)

    assert res.status_code == 204
    logger.info("\n ======= gpttranslation cache has been refreshed =======")
    yield res
