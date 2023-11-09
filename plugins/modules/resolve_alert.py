#!/usr/bin/python

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from requests import HTTPError
import requests

__metaclass__ = type

DOCUMENTATION = """
module: bigpanda.incident.resolve_alert
author: JuanDCardozo
short_description: Resolve a BigPanda alert.
description:
  - This module resolves a BigPanda alert by providing the alert ID and an optional resolution message.
options:
  alert_ids:
    description: The ID of the alert to resolve.
    required: true
  resolution:
    description: The resolution message for the alert.
    required: false
  api_token:
    description: The API token for authentication.
    required: true
"""

EXAMPLES = """
- name: Resolve an alert
  bigpanda.incident.resolve_alert:
    alert_ids: "54321"
    resolution: "Alert resolved."
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the alert resolution was successful.
  type: bool
  returned: true/false
  sample: true
result:
  description: The response from the BigPanda server.
  type: str
  returned: BigPanda's Response
  sample: "Alert resolved successfully."
"""


def main():
    """
    The main function to execute the module.
    """
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
            json=data)

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
