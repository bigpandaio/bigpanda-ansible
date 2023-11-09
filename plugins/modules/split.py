#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
from requests import HTTPError
import requests
__metaclass__ = type


DOCUMENTATION = """
module: bigpanda.incident.split
author: JuanDCardozo
short_description: Split a BigPanda incident into multiple incidents.
description:
  - This module splits a BigPanda incident into multiple incidents.
options:
  incident_id:
    description: The ID of the incident to split.
    required: true
  comment:
    description: A comment describing the split.
    required: false
  api_token:
    description: The API token for authentication.
    required: true
  environment_id:
    description: The environment ID.
    required: true
  alert_ids:
    description: A list of alert IDs to split.
    required: true
"""

EXAMPLES = """
- name: Split incidents
  bigpanda.incident.split:
    incident_id: "source_incident"
    comment: "Splitting the incident."
    api_token: "your_api_token"
    environment_id: "your_environment"
    alert_ids:
      - "alert1"
      - "alert2"
"""

RETURN = """
changed:
  description: Indicates if the incident was successfully split.
  type: bool
  returned: true/false
  sample: true
result:
  description: The response from the BigPanda server.
  type: str
  returned: BigPanda's Response
  sample: "Incident split successfully."
"""


def main():

    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
            comment=dict(type='str', required=False),
            alert_ids=dict(type='list', required=True)
        ),
        supports_check_mode=True
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    api_token = module.params['api_token']
    alert_ids = module.params['alert_ids']
    comment = module.params['comment']

    try:
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }
        data = {
            'comment': comment,
            'alerts': alert_ids,
        }

        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/split',
            headers=headers,
            json=data)

        response.raise_for_status()
        module.exit_json(changed=True, result=response.text)
    except HTTPError as e:
        # Log any HTTP errors
        module.fail_json(msg=f"An HTTP error occurred: {str(e)}")


if __name__ == '__main__':
    main()
