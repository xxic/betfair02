from definitions import ROOT_DIR

import json
import requests


class Operations:

    def __init__(self):
        self.certificate = (ROOT_DIR + '/resources/client-2048.crt', ROOT_DIR + '/resources/client-2048.key')

        with open(ROOT_DIR + '/resources/setting.json', 'r+') as file:
            data = json.load(file)
        self.username = data['username']
        self.password = data['password']
        self.login_url = data['login_url']
        self.application = data['application']
        self.certificate_login = data['certificate_login']
        self.rest_endpoint = data['rest_endpoint']

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

    def query(self, operation, payload):
        headers = {
            'X-Application': self.application,
            'X-Authentication': self.token,
            'Content-Type': 'application/json'
        }
        return requests.request('POST', self.rest_endpoint + operation, data=payload, headers=headers).json()


if __name__ == '__main__':
    ops = Operations()
    print(ops.token)
