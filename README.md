# Jumpserver Assets Ansible Module

An Ansible module for managing assets (hosts) in JumpServer using its REST API. This module allows you to create or delete assets in your JumpServer instance seamlessly within Ansible playbooks.

## Features

- **Create Assets**: Add new assets to JumpServer with specified parameters (name, address, protocols).
- **Delete Assets**: Remove existing assets by name.
- **Idempotent Operations**: Ensures no duplicate assets are created and handles absent assets gracefully.
- **REST API Integration**: Directly interacts with JumpServer's API for efficient asset management.

## Prerequisites

- Ansible installed on the control machine.
- `requests` library installed on the target machine (if not using a module running locally).
- Access to the JumpServer API with a valid API token.
- Proper network connectivity to the JumpServer host.

## Installation

1. Place the `jumpserver_assets.py` file in your Ansible project's `library/` directory.
2. Ensure the `requests` library is installed where the module will execute:
   ```bash
   pip install requests
   ```

## Usage

### Module Parameters

| Parameter  | Description                                                                 | Required | Default | Choices         |
|------------|-----------------------------------------------------------------------------|----------|---------|-----------------|
| `host`     | Hostname/IP of the JumpServer API.                                          | Yes      | -       | -               |
| `api_token`| API token for authentication.                                               | Yes      | -       | -               |
| `name`     | Name of the asset.                                                          | Yes      | -       | -               |
| `address`  | IP address/hostname of the asset (required when `state=present`).           | Yes*     | -       | -               |
| `state`    | Desired state of the asset.                                                 | No       | present | `present`, `absent` |

*Required when `state=present`.

### Example Playbooks

**Create an Asset**:
```yaml
- name: Ensure asset 'server01' exists
  jumpserver_assets:
    host: "jumpserver.example.com"
    api_token: "your_api_token_here"
    name: "server01"
    address: "192.168.1.100"
    state: present
```

**Delete an Asset**:
```yaml
- name: Ensure asset 'server01' is removed
  jumpserver_assets:
    host: "jumpserver.example.com"
    api_token: "your_api_token_here"
    name: "server01"
    state: absent
```

## Return Values

| Key       | Description                          | Type   | Example Output                          |
|-----------|--------------------------------------|--------|------------------------------------------|
| `changed` | Indicates if a change was made.      | bool   | `true`                                   |
| `msg`     | Result message from the operation.   | str    | "Asset created" or "Asset already exists" |

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Author

@iriskins

---
**Notes**: 
- Replace `your_api_token_here` and `jumpserver.example.com` with your actual JumpServer details.
- The module disables SSL verification (`verify=False`). For production, consider enabling SSL and providing a valid certificate.
