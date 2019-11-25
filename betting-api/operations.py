from definitions import ROOT_DIR
from decorators import timer

import json
import requests


class Operations:
    """
    Encapsulates all betting operations
    """

    def __init__(self):
        """
        Initialize all static data required by Operations.
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

    @timer
    def retrieve(self, operation, payload):
        """
        Generic method hat retrieves data based on the operation and filter supplied.
        :param operation: Betting API operation, for example; listEvents/
        :param payload: Filter
        :return: Operation-type data
        """
        headers = {
            'X-Application': self.application_key,
            'X-Authentication': self.token,
            'Content-Type': 'application/json'
        }
        return requests.request('POST', self.rest_endpoint + operation, data=payload, headers=headers).json()


# todo: explore returned data from listEvents
if __name__ == '__main__':
    ops = Operations()

    op = 'listEvents/'
    pl = '{"filter":{"eventTypeIds":["1"]}}'
    dt = ops.retrieve(op, pl)
    print(len(dt))

    # working with the returned data
    count = 0
    for ev in dt:
        # retrieve event and marketCount
        mkc = ev['marketCount']
        for k, v in ev['event'].items():
            if ' v ' in v:
                count += 1

    print(count)
