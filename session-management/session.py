import json
import requests
import os


class Session:
    """
    Session management
    """
    def __init__(self):
        """
        Get account login information from file.
        This is for improved security by not having static sensitive data permanently in code.
        todo: Improve further by encrypting the file and/or changing permissions
        """
        with open(os.path.dirname(__file__) + '/setting.json', 'r+') as file:
            data = json.load(file)
        self.username = data['username']
        self.password = data['password']
        self.login_url = data['login_url']
        self.application = data['application']

    def token(self):
        """
        Obtain the session token.
        :return: session token
        """
        payload = f"username={self.username}&password={self.password}"
        headers = {
            'Accept': "application/json",
            'X-Application': self.application,
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", self.login_url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['token']
        else:
            print('Login failed: ', response.status_code)


# if __name__ == '__main__':
#     session = Session()
#     token = session.token()
#     print(token)
