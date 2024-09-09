# UnipyAccess API Connector

## Overview

unipyAccess is a Python class designed to interface with the Unifi Access, allowing for the management of users in the system. This connector handles authentication, retrieval of users, creation, activation, deactivation, deletion, and updating of user groups.

Disclaimer: This implementation does not use the new Unifi API. Instead, it utilizes authentication through a admin user account.

## Requirements

- Python 3.x
- `requests` library

To install the `requests` library, run:
```bash
pip install requests
```

# Class: unipyAccess
## Initialization
The **unipyAccess** class requires the following parameters upon initialization:

```python
unipy = unipyAccess(baseUrl, username, password, verify)
```
`baseUrl`: Internal URL of the Unifi controller (e.g., https://unifi-controller.local).
`username`: Username of the configuration user.
`password`: Password of the configuration user.
`verify`: Boolean (True/False) to indicate whether SSL verification should be performed on the requests. If None, verification defaults to True.

**Note**: Disabling SSL verification is not recommended in production environments as it can expose your application to security risks.

## Example
```python
from unipyAccess import unipyAccess
unipy = unipyAccess("https://unifi-controller.local", "unipy", "password123", verify=False)
```
## Methods
### 1. getUnifiUsers()
Retrieves the list of users from the Unifi Access system.

```python
unipy.getUnifiUsers()
```

Example Response:
```json
[
    {
        "id": "12345",
        "first_name": "John",
        "last_name": "Doe",
        "employee_number": "54321"
    }
]
```
### 2. createUnifiUsers(users)
Creates new users in the Unifi Access system.

`users`: List of dictionaries, where each dictionary represents a user with the following structure:
`first_name`: User's first name
`last_name`: User's last name
`PersonId`: Optional employee number (string)
`group_ids`: Optional list of group IDs to assign to the user.
```python
users = [
    {"first_name": "Alice", "last_name": "Smith", "PersonId": 123, "group_ids": [1, 2]},
    {"first_name": "Bob", "last_name": "Jones", "PersonId": 456}
]
unipy.createUnifiUsers(users)
```
### 3. deactivateUnifiUsers(users)
Deactivates the given users.

`users`: List of dictionaries with the following structure:
`id`: User's unique ID
```python
users = [{"id": "1bae4670-c853-4740-8bbc-62ff90aaad07"}]
unipy.deactivateUnifiUsers(users)
```
### 4. activateUnifiUsers(users)
Activates the given users.

`users`: List of dictionaries with the following structure:
`id`: User's unique ID

```python
users = [{"id": "1bae4670-c853-4740-8bbc-62ff90aaad07"}]
unipy.activateUnifiUsers(users)
```
### 5. deleteUnifiUsers(users)
Deletes users from the Unifi Access system.

`users`: List of dictionaries with the following structure:
`id`: User's unique ID

```python
users = [{"id": "1bae4670-c853-4740-8bbc-62ff90aaad07"}]
unipy.deleteUnifiUsers(users)
```
### 6. setUsersGroup(users)
Assigns or updates the group of the specified users.

`users`: List of dictionaries with the following structure:
`id`: User's unique ID
`group`: Group ID to assign to the user.

```python

users = [{"id": "12345", "group": 1}]
unipy.setUsersGroup(users)
```

# License
This project is licensed under the MIT License.

This README file provides an overview, usage instructions, and example code to help users understand and use the `unipyAccess` class effectively.
