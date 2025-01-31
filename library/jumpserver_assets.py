from ansible.module_utils.basic import AnsibleModule
import requests
import json

DOCUMENTATION = r'''
---
module: jumpserver_assets
short_description: Manage assets via REST API
version_added: "1.0.0"
description:
  - Create or delete assets in a REST API-driven asset management system.
options:
  host:
    description:
      - Hostname or IP address of the API server.
    required: true
    type: str
  api_token:
    description:
      - API token for authentication.
    required: true
    type: str
    no_log: true
  name:
    description:
      - Name of the asset.
    required: true
    type: str
  address:
    description:
      - IP address or hostname of the asset.
      - Required when state is 'present'.
    type: str
  state:
    description:
      - Desired state of the asset.
    choices: [ 'present', 'absent' ]
    default: 'present'
    type: str
requirements:
  - requests
author:
  - Your Name (@iriskins)
'''

EXAMPLES = r'''
# Create a new asset
- name: Ensure asset exists
  asset_manager:
    host: "api.example.com"
    api_token: "secret_token"
    name: "server01"
    address: "192.168.1.100"
    state: present

# Delete an asset
- name: Ensure asset is removed
  asset_manager:
    host: "api.example.com"
    api_token: "secret_token"
    name: "server01"
    state: absent
'''

RETURN = r'''
changed:
  description: Indicates if a change was made.
  type: bool
  returned: always
msg:
  description: Message describing the result.
  type: str
  returned: always
'''

def get_assets(url, api_token):
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return []
    return []

def get_id(name, assets):
    for a in assets:
        if a["name"] == name:
            return a["id"]
    return None

def asset_exists(url, api_token, name):
    assets = get_assets(url, api_token)
    for a in assets:
        if a["name"] == name:
            return True
    return False

def create_asset(url, api_token, name, address, module):
    headers = {
        "Authorization": 'Bearer ' + api_token,
        "Content-Type": 'application/json'
    }

    data = {'platform': {'pk': 1}, 'address': address, 'name': name, 'protocols': [{'name': 'ssh', 'port': '22'}]}

    if not asset_exists(url, api_token, name):
        r = requests.post(url, json=data, headers=headers, verify=False)

        if r.status_code == 201:
            try:
                response_data = r.json()
            except json.JSONDecodeError:
                response_data = r.text
            module.exit_json(changed=True, msg=str(response_data))
        else:
            try:
                error_msg = r.json()
            except json.JSONDecodeError:
                error_msg = r.text
            module.fail_json(msg=str(error_msg))
    else:
        module.exit_json(changed=False, msg="Asset already exists")

def delete_asset(url, api_token, name, module):
    headers = {
        "Authorization": 'Bearer ' + api_token,
        "Content-Type": 'application/json'
    }
    assets = get_assets(url, api_token)
    asset_id = get_id(name, assets)

    if asset_id is not None:
        r = requests.delete(url + f'{asset_id}/', headers=headers, verify=False)

        if r.status_code == 204:
            module.exit_json(changed=True, msg="Asset deleted")
        else:
            try:
                error_msg = r.json()
            except json.JSONDecodeError:
                error_msg = r.text
            module.fail_json(msg=str(error_msg))
    else:
        module.exit_json(changed=False, msg="Asset not found")

def main():
    module_args = dict(
        host=dict(type='str', required=True),
        api_token=dict(type='str', required=True, no_log=True),
        name=dict(type='str', required=True),
        address=dict(type='str', required_if=['state', 'present']),
        state=dict(type='str', default='present', choices=['present', 'absent']),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    
    host = module.params['host']
    api_token = module.params['api_token']
    name = module.params['name']
    address = module.params['address']
    state = module.params['state']

    url = f"https://{host}/api/v1/assets/hosts/"

    try:
        if state == 'present':
            create_asset(url, api_token, name, address, module)
        elif state == 'absent':
            delete_asset(url, api_token, name, module)

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
