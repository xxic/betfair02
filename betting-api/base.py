from definitions import ROOT_DIR

import json
import requests


class Base:

    def __init__(self):
        """
        Initialize static data required by Operations.
        """
        self.certificate = (ROOT_DIR + '/resources/client-2048.crt', ROOT_DIR + '/resources/client-2048.key')

        with open(ROOT_DIR + '/resources/setting.json', 'r+') as file:
            setting = json.load(file)

        self.username = setting['username']
        self.password = setting['password']
        self.login_url = setting['login_url']
        self.application = setting['application']
        self.application_key = setting['application_key']
        self.certificate_login = setting['certificate_login']
        self.rest_endpoint = setting['rest_endpoint']

        payload = f"username={self.username}&password={self.password}"
        headers = {
            'Accept': "application/json",
            'X-Application': self.application,
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", self.login_url, data=payload, headers=headers)
        if response.status_code == 200:
            self.token = response.json()['token']
        else:
            self.token = None

        self.mysql_credentials = {
            'username': setting['mysql_username'],
            'password': setting['mysql_password'],
            'host': setting['mysql_host'],
            'port': setting['mysql_port'],
            'database': setting['mysql_default_schema']
        }

    def retrieve(self, operation, payload):
        """
        Generic method hat retrieves data based on the operation and filter(payload) supplied.
        :param operation: Betting API operation, for example; listEvents/
        :param payload: Filter
        :return: Operation-type data
        """
        headers = {
            'X-Application': self.application_key,
            'X-Authentication': self.token,
            'Content-Type': 'application/json'
        }
        return requests.request('post', self.rest_endpoint + operation, data=payload, headers=headers).json()
