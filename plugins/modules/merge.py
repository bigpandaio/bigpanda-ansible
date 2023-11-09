#!/usr/bin/python

from __future__ import absolute_import, division, print_function

import requests
from requests import HTTPError
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = """
module: bigpanda.incident.merge
author: JuanDCardozo
short_description: Merge multiple BigPanda incidents into one.
description:
  - This module merges multiple BigPanda incidents into a single incident.
options:
  incident_id:
    description: The ID of the incident to merge into.
    required: true
  comment:
    description: A comment describing the merge.
    required: false
  api_token:
    description: The API token for authentication.
    required: true
  environment_id:
    description: The environment ID.
    required: true
  source_incidents:
    description: A list of incident IDs to merge.
    required: true
"""

EXAMPLES = """
- name: Merge incidents
  bigpanda.incident.merge:
    incident_id: "target_incident"
    comment: "Merging multiple incidents."
    api_token: "your_api_token"
    environment_id: "your_environment"
    source_incidents:
      - "incident1"
      - "incident2"
"""

RETURN = """
changed:
  description: Indicates if the incidents were successfully merged.
  type: bool
  sample: true
  returned: true/false
result:
  description: The response from the BigPanda server.
  type: str
  returned: BigPanda's Response
  sample: "Incidents merged successfully."
"""


def main():
    """
    The main function to execute the module.
    """
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True),
            source_incidents=dict(type='list', required=True),
            comment=dict(type='str', required=False)
        ),
        supports_check_mode=True
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    api_token = module.params['api_token']
    source_incidents = module.params['source_incidents']
    comment = module.params['comment']

    # Set the request headers
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    json_data = {
        'source_incidents': source_incidents,
        'comment': comment
    }

    try:
        response = requests.post(
            f'https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/merge',
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
