import requests
import json
import logging
import csv

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

        with requests.Session() as session:
            response = session.post(login_url, headers=login_headers, json=login_payload, verify=self.verify)
            response.raise_for_status()

            self.token_cookie = session.cookies.get('TOKEN')
            self.csrf_token = response.headers.get('x-csrf-token')

            if not self.token_cookie or not self.csrf_token:
                raise ValueError("Error: TOKEN cookie or x-csrf-token not found in the login response")

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

    def update_license_plate(self, email_license_data):
        users = self.get_unifi_users()
        
        for user in users:
            email = user.get('email')
            if email and email in email_license_data:
                license_plate = email_license_data[email]
                update_payload = json.dumps({"license_plate": license_plate})
                
                user_url = f"{self.base_url}/proxy/access/api/v2/user/{user['id']}"
                response = requests.put(user_url, headers=unifi_headers, data=update_payload, verify=self.verify)
                
                if response.status_code == 200:
                    logging.info(f"Updated license plate for user {email}")
                else:
                    logging.error(f"Failed to update license plate for {email}: {response.text}")

    @staticmethod
    def load_license_data_from_csv(file_path):
        email_license_data = {}
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    email = row.get("email")
                    license_plate = row.get("license_plate")
                    if email and license_plate:
                        email_license_data[email] = license_plate
        except Exception as e:
            logging.error(f"Failed to read CSV file: {e}")
        
        return email_license_data

# Usage example:
# unipy_access = UnipyAccess(base_url="https://your-unifi-url", username="your-username", password="your-password", verify=False)
# license_data = unipy_access.load_license_data_from_csv("license_plates.csv")
# unipy_access.update_license_plate(license_data)
