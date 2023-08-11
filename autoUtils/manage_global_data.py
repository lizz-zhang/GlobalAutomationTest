import json

from autoUtils.fileReader import read_config_file
from pathlib import Path


class ManageGlobalData:
    _environment = None

    def set_global_value(self, environment):
        ManageGlobalData._environment = environment

    def get_global_value(self):
        return ManageGlobalData._environment

    def get_site_id(self):
        config_data_json_dict = read_config_file('environments.json')
        site_id = config_data_json_dict[self._environment]['agent']['siteId']
        return site_id

    # def get_env(self, environment):
    #     en_path = Path.cwd().parent.parent.parent.joinpath('autoConfig')
    #     file_name = 'environments.json'
    #     if '.json' in file_name:
    #         path = en_path.joinpath(file_name)
    #     else:
    #         path = en_path.joinpath(f'{file_name}.json')
    #     with path.open(mode='r') as f:
    #         return json.load(f)


    def get_partner_id(self):
        config_data_json_dict = read_config_file('environments.json')
        partner_id = config_data_json_dict[self._environment]['partnerUser']['partnerId']
        return partner_id

    def get_partner_paidsiteid(self):
        config_data_json_dict = read_config_file('environments.json')
        partner_paidsiteid = config_data_json_dict[self._environment]['paidSite']
        return partner_paidsiteid

    def get_partner_trialsiteid(self):
        config_data_json_dict = read_config_file('environments.json')
        partner_trialsiteid = config_data_json_dict[self._environment]['trialSite']
        return partner_trialsiteid

    def get_agent_email(self):
        config_data_json_dict = read_config_file('environments.json')
        agent_email = config_data_json_dict[self._environment]['agent']['email']
        return agent_email

    def get_file_url(self):
        config_data_json_dict = read_config_file('environments.json')
        FileService = config_data_json_dict[self._environment]['partnerFileService']
        return FileService
