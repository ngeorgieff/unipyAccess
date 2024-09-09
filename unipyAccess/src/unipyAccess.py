import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class unipyAccess:
    def __init__(self, baseUrl, username, password, verify):
        self.baseUrl = baseUrl
        self.username = username
        self.password = password
        self.verify = True if verify is None else eval(verify) 
        self.tokenCookie = None
        self.xCsrfToken = None
        self._login()

    def _login(self):
        if self.verify == False:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        
        # API call to login
        login_url = f"{self.baseUrl}/api/auth/login"
        login_payload = {
            "username": self.username,
            "password": self.password,
            "token": "",
            "rememberMe": False
        }
        login_headers = {
            'content-type': 'application/json',
            'origin': self.baseUrl
        }

        # Using requests.Session to manage cookies and future requests
        with requests.Session() as session:
            response = session.post(login_url, headers=login_headers, json=login_payload, verify=self.verify)
            response.raise_for_status()  # Automatically raise exception for HTTP errors

            # Extract TOKEN cookie and x-csrf-token
            self.tokenCookie = session.cookies.get('TOKEN')
            self.xCsrfToken = response.headers.get('x-csrf-token')

            if not self.tokenCookie or not self.xCsrfToken:
                raise ValueError("Error: TOKEN cookie or x-csrf-token not found in the login response")

            # Global headers for future requests
            global unifiHeaders
            unifiHeaders = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'origin': self.baseUrl,
                'x-csrf-token': self.xCsrfToken,
                'Cookie': f'TOKEN={self.tokenCookie}'
            }

    def getUnifiUsers(self):
        response = requests.get(self.baseUrl + "/proxy/access/api/v2/users", headers=unifiHeaders, verify=self.verify)
        parsedData = json.loads(response.text.replace("'", '"'))
        return parsedData

    def createUnifiUsers(self, users):
        for user in users:
            payload = json.dumps({
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "employee_number": str(user["PersonId"]) if user["PersonId"] is not None else "",
                "group_ids": user["group_ids"] if "group_ids" in user else []
            })
            if user["first_name"] and user["last_name"]:
                response = requests.post(f'{self.baseUrl + ":/proxy/access/api/v2/user"}', headers=unifiHeaders, data=payload, verify=self.verify)
                logger.info(f'Trying to create user {user["first_name"]} {user["last_name"]}: {response.text}')

    def deactivateUnifiUsers(self, users):
        for user in users:
            response = requests.put(f'{self.baseUrl + ":/proxy/access/ulp-go/api/v2/user"}/{user["id"]}/deactivate?isULP=1', headers=unifiHeaders, verify=self.verify)
            logger.info(f'Deactivated user {user["id"]}: {response.text}')

    def activateUnifiUsers(self, users):
        for user in users:
            response = requests.put(f'{self.baseUrl + ":/proxy/access/ulp-go/api/v2/user"}/{user["id"]}/active?isULP=1', headers=unifiHeaders, verify=self.verify)
            logger.info(f'Activated user {user["id"]}: {response.text}')

    def deleteUnifiUsers(self, users):
        for user in users:
            response = requests.delete(f'{self.baseUrl + ":/proxy/access/ulp-go/api/v2/user"}/{user["id"]}?isULP=1', headers=unifiHeaders, verify=self.verify)
            logger.info(f'Deleted user {user["id"]}: {response.text}')

    def setUsersGroup(self, users):
        for user in users:
            try:
                user_url = f"{self.baseUrl}/proxy/access/api/v2/user/{user['id']}"
                user_payload = json.dumps({"group_ids": [user["group"]]})
                response = requests.put(user_url, headers=unifiHeaders, data=user_payload, verify=self.verify)
                if response.ok:
                    print(f"User {user['id']} group updated successfully")
                else:
                    logger.error(f"Failed to update user {user['id']} group: {response.text}")
            except Exception as e:
                logger.error(f"Error updating group for user {user['id']}: {e}")