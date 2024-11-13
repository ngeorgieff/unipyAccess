import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
unifi_headers = {}
class UnipyAccess:
    def __init__(self, base_url, username, password, verify):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify = True if verify is None else eval(verify)
        self.token_cookie = None
        self.csrf_token = None
        self._login()

    def _login(self):
        if not self.verify:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

        # API call to login
        login_url = f"{self.base_url}/api/auth/login"
        login_payload = {
            "username": self.username,
            "password": self.password,
            "token": "",
            "rememberMe": False
        }
        login_headers = {
            'content-type': 'application/json',
            'origin': self.base_url
        }

        # Using requests.Session to manage cookies and future requests
        with requests.Session() as session:
            response = session.post(login_url, headers=login_headers, json=login_payload, verify=self.verify)
            response.raise_for_status()  # Automatically raise exception for HTTP errors

            # Extract TOKEN cookie and x-csrf-token
            self.token_cookie = session.cookies.get('TOKEN')
            self.csrf_token = response.headers.get('x-csrf-token')

            if not self.token_cookie or not self.csrf_token:
                raise ValueError("Error: TOKEN cookie or x-csrf-token not found in the login response")

            # Global headers for future requests
            global unifi_headers
            unifi_headers = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': self.base_url,
                'x-csrf-token': self.csrf_token,
                'Cookie': f'TOKEN={self.token_cookie}'
            }

    def get_unifi_users(self):
        response = requests.get(f"{self.base_url}/proxy/access/api/v2/users", headers=unifi_headers, verify=self.verify)
        parsed_data = json.loads(response.text.replace("'", '"'))
        return parsed_data

    def create_unifi_users(self, users):
        for user in users:
            payload = json.dumps({
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "employee_number": str(user["PersonId"]) if user["PersonId"] is not None else "",
                "group_ids": user.get("group_ids", [])
            })
            if user["first_name"] and user["last_name"]:
                response = requests.post(f'{self.base_url}/proxy/access/api/v2/user', headers=unifi_headers, data=payload, verify=self.verify)
                logging.info(f'Trying to create user {user["first_name"]} {user["last_name"]}: {response.text}')

    def deactivate_unifi_users(self, users):
        for user in users:
            response = requests.put(f'{self.base_url}/proxy/access/ulp-go/api/v2/user/{user["id"]}/deactivate?isULP=1', headers=unifi_headers, verify=self.verify)
            logging.info(f'Deactivated user {user["id"]}: {response.text}')

    def activate_unifi_users(self, users):
        for user in users:
            response = requests.put(f'{self.base_url}/proxy/access/ulp-go/api/v2/user/{user["id"]}/active?isULP=1',
                                    headers=unifi_headers, verify=self.verify)
            logging.info(f'Activated user {user["id"]}: {response.text}')

    def delete_unifi_users(self, users):
        for user in users:
            response = requests.delete(f'{self.base_url}/proxy/access/ulp-go/api/v2/user/{user["id"]}?isULP=1',headers=unifi_headers, verify=self.verify)
            logging.info(f'Deleted user {user["id"]}: {response.text}')

    def set_users_group(self, users):
        # API call to update user group
        for user in users:
            try:
                user_url = f"{self.base_url}/proxy/access/api/v2/user/{user['id']}"
                user_payload = json.dumps({
                    "group_ids": [user["group"]]
                })
                response = requests.put(user_url, headers=unifi_headers, data=user_payload, verify=self.verify)
                if response.status_code == 200:
                    logging.info(f"Updated user group for {user['id']}")
                else:
                    raise Exception(f"Failed to update user group with status code {response.status_code}: {response.text}")
            except Exception as e:
                logging.error(f"Error updating group for user {user['id']}: {e}")
