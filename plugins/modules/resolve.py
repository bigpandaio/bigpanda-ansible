#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from requests import HTTPError
import requests

__metaclass__ = type

DOCUMENTATION = """
module: bigpanda.incident.resolve
author: JuanDCardozo
short_description: Resolve a BigPanda incident.
description:
  - This module resolves a BigPanda incident by providing the incident ID and an optional resolution message.
options:
  incident_id:
    description: The ID of the incident to resolve.
    required: true
  resolution_comment:
    description: The resolution message for the incident.
    required: false
  api_token:
    description: The API token for authentication.
    required: true
"""

EXAMPLES = """
- name: Resolve an incident
  bigpanda.incident.resolve:
    incident_id: "12345"
    resolution_comment: "Incident resolved."
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the incident resolution was successful.
  type: bool
  returned: true/false
  sample: true
result:
  description: The response from the BigPanda server.
  type: str
  returned: BigPanda's Response
  sample: "Incident resolved successfully."
"""


def main():
    module = AnsibleModule(
        argument_spec=dict(
            resolution_comment=dict(type='str', required=False),
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    resolution_comment = module.params['resolution_comment']
    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    api_token = module.params['api_token']

    module.debug("Resolve Incident")

    # Set the request headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    # Prepare the JSON data to be sent with the request
    json_data = {
        'comments': resolution_comment
    }

    try:
        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/resolve',
            headers=headers,
            json=json_data)

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
