#!/usr/bin/env python3

import requests
from requests import HTTPError

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            tag_id=dict(type='str', required=True),
            tag_value=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
            environment_id=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    tag_id = module.params['tag_id']
    tag_value = module.params['tag_value']
    incident_id = module.params['incident_id']
    api_token = module.params['api_token']
    environment_id = module.params['environment_id']

    try:
        module.debug("Update Incident Tag")

        # Set the request headers
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        # Prepare the JSON data to be sent with the request
        json_data = {
            "tag_value": tag_value
        }
        module.debug(json_data)
        # Send the POST request to update the incident tag
        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/tags/{tag_id}',
            headers=headers,
            json=json_data
        )

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
