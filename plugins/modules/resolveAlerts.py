#!/usr/bin/env python3

import requests
from requests import HTTPError

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
            alert_ids=dict(type='list', required=True),
            comments=dict(type='list', required=False),
        ),
        supports_check_mode=True
    )

    environment_id = module.params['environment_id']
    api_token = module.params['api_token']
    alert_ids = module.params['alert_ids']
    comments = module.params['comments']

    try:
        module.debug("Batch Resolve Alerts")

        # Prepare the JSON data
        data = {
            "ids": alert_ids, 
        }

        if comments:
            data['comments'] = comments

        # Set the request headers
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        # Send the POST request using the requests library
        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/batch-resolve/alerts',
            headers=headers,
            json=data
        )

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
