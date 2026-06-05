#!/usr/bin/python
# Copyright 2023 BigPanda
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
author:
  - Juan Cardozo (@JuanDCardozo)
description:
  - This module updates a tag on a BigPanda incident.
module: add_tag
options:
  environment_id:
    description: The ID of the BigPanda environment containing the incident.
    required: true
    type: str
  incident_id:
    description: The ID of the incident to update.
    required: true
    type: str
  tag_id:
    description: The ID of the tag to update.
    required: true
    type: str
  tag_value:
    description: The new value for the tag.
    required: true
    type: str
  api_token:
    description: The API token for authentication.
    required: true
    type: str
  api_url:
    description:
      - Base URL of the BigPanda API. Override for EU
        (C(https://eu-api.bigpanda.io)) or dedicated tenant hosts.
      - May also be set via the C(BIGPANDA_API_URL) environment variable.
    required: false
    type: str
    default: https://api.bigpanda.io
short_description: Update a BigPanda incident tag.
version_added: 1.0.0
"""

EXAMPLES = """
- name: Update an incident tag
  bigpanda.incident.add_tag:
    environment_id: "your_environment_id"
    incident_id: "incident456"
    tag_id: "tag123"
    tag_value: "NewTagValue"
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the tag update was successful.
  type: bool
  returned: always
  sample: true
status:
  description: HTTP status code returned by the BigPanda API.
  type: int
  returned: always
  sample: 200
result:
  description: Response body returned by the BigPanda API.
  type: str
  returned: success
  sample: "Tag updated successfully."
"""

import json

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import fetch_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            tag_id=dict(type='str', required=True),
            tag_value=dict(type='str', required=True),
            api_token=dict(type='str', required=True, no_log=True),
            api_url=dict(
                type='str',
                required=False,
                default='https://api.bigpanda.io',
                fallback=(env_fallback, ['BIGPANDA_API_URL']),
            ),
        ),
        supports_check_mode=True,
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    tag_id = module.params['tag_id']
    tag_value = module.params['tag_value']
    api_token = module.params['api_token']
    api_url = module.params['api_url'].rstrip('/')

    url = (
        f'{api_url}/resources/v2.0/environments/'
        f'{environment_id}/incidents/{incident_id}/tags/{tag_id}'
    )
    method = 'POST'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    payload = {'tag_value': tag_value}

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg='check mode: no API call made',
            url=url,
            method=method,
            payload=payload,
        )

    response, info = fetch_url(
        module,
        url,
        headers=headers,
        data=json.dumps(payload),
        method=method,
    )

    status = info.get('status', -1)
    if status < 200 or status >= 300:
        module.fail_json(
            msg=f"BigPanda API request failed: {info.get('msg', 'unknown error')} (HTTP {status})",
            status=status,
            body=info.get('body'),
        )

    body = response.read().decode('utf-8') if response else ''
    module.exit_json(changed=True, status=status, result=body)


if __name__ == '__main__':
    main()
