
# unipyaccess

`unipyaccess` is a Python package designed to interface with the **Unifi Access** system. This package provides a simple and efficient way to manage users in Unifi Access, including authentication, retrieval, creation, activation, deactivation, deletion, and updating of user groups.

> **Note**: This implementation uses Unifi API endpoints with admin user authentication. It does **not** utilize the latest, in my opinion half-baked Unifi API.

## Features

- Authenticate with Unifi Access using admin credentials.
- Retrieve, create, activate, deactivate, and delete user accounts.
- Update user group assignments.

## Installation

Install the package via `pip`:

```bash
pip install unipyaccess
```

## Requirements

- Python 3.x
- `requests` library

Install the requirements with:

```bash
pip install requests
```

## Environment Setup

Store your configuration details in a `.env` file:

```bash
UNIFI_CONTROLLER_ADDRESS=https://unifi-controller.local
UNIFI_LOGIN=admin
UNIFI_PASSWORD=password123
VERIFY_SSL=False
```

## Usage

Import `unipyaccess` and use it in your Python script:

```python
from unipyaccess import UnipyAccess
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the UnipyAccess API client
unifiApi = UnipyAccess(
    base_url=os.getenv('UNIFI_CONTROLLER_ADDRESS'),
    username=os.getenv('UNIFI_LOGIN'),
    password=os.getenv('UNIFI_PASSWORD'),
    verify=os.getenv('VERIFY_SSL')
)

# Example: Create a new user
users = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "PersonId": 124,
        "group_ids": ["bc1bf76d-5d2a-4a90-ae50-6aca02bccc63"]
    }
]
unifiApi.create_unifi_users(users)
```

## Methods

### 1. `get_unifi_users()`
Fetches the list of users from Unifi Access.

**Usage:**

```python
users = unifiApi.get_unifi_users()
print(users)
```

### 2. `create_unifi_users(users)`
Creates new users.

**Parameters:**
- `users` (list): List of user dictionaries containing:
  - `first_name` (str): User's first name.
  - `last_name` (str): User's last name.
  - `PersonId` (str): Optional employee number.
  - `group_ids` (list): Optional list of group IDs.

**Usage:**

```python
users = [
    {"first_name": "Jane", "last_name": "Doe", "PersonId": "789", "group_ids": ["group-123"]}
]
unifiApi.create_unifi_users(users)
```

### 3. `deactivate_unifi_users(users)`
Deactivates users.

**Usage:**

```python
users = [{"id": "user-123"}]
unifiApi.deactivate_unifi_users(users)
```

### 4. `activate_unifi_users(users)`
Activates users.

**Usage:**

```python
users = [{"id": "user-123"}]
unifiApi.activate_unifi_users(users)
```

### 5. `delete_unifi_users(users)`
Deletes users.

**Usage:**

```python
users = [{"id": "user-123"}]
unifiApi.delete_unifi_users(users)
```

### 6. `set_users_group(users)`
Updates user group assignments.

**Usage:**

```python
users = [{"id": "user-123", "group": "group-456"}]
unifiApi.set_users_group(users)
```

## Example Code

```python
from unipyaccess import UnipyAccess
from dotenv import load_dotenv
import os

load_dotenv()

unifiApi = UnipyAccess(
    base_url=os.getenv('UNIFI_CONTROLLER_ADDRESS'),
    username=os.getenv('UNIFI_LOGIN'),
    password=os.getenv('UNIFI_PASSWORD'),
    verify=os.getenv('VERIFY_SSL')
)

# Retrieve users
print(unifiApi.get_unifi_users())

# Create a user
new_user = [{"first_name": "Alice", "last_name": "Smith", "PersonId": "125"}]
unifiApi.create_unifi_users(new_user)

# Activate a user
unifiApi.activate_unifi_users([{"id": "user-123"}])

# Deactivate a user
unifiApi.deactivate_unifi_users([{"id": "user-123"}])

# Delete a user
unifiApi.delete_unifi_users([{"id": "user-123"}])

# Update user group
unifiApi.set_users_group([{"id": "user-123", "group": "group-789"}])
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
