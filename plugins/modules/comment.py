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
  - This module adds a comment to a BigPanda incident.
module: comment
options:
  environment_id:
    description: The ID of the BigPanda environment containing the incident.
    required: true
    type: str
  incident_id:
    description: The ID of the incident to add a comment to.
    required: true
    type: str
  comment:
    description: The text of the comment.
    required: true
    type: str
  api_token:
    description: The API token for authentication.
    required: true
    type: str
short_description: Add a comment to a BigPanda incident.
version_added: 1.0.0
"""

EXAMPLES = """
- name: Add a comment to an incident
  bigpanda.incident.comment:
    environment_id: "your_environment_id"
    incident_id: "12345"
    comment: "This is a test comment."
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the comment addition was successful.
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
  sample: "Comment added successfully."
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            comment=dict(type='str', required=True),
            api_token=dict(type='str', required=True, no_log=True),
        ),
        supports_check_mode=True,
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    comment = module.params['comment']
    api_token = module.params['api_token']

    url = (
        'https://api.bigpanda.io/resources/v2.0/environments/'
        f'{environment_id}/incidents/{incident_id}/comments'
    )
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    payload = {'comment': comment}

    if module.check_mode:
        module.exit_json(changed=True, msg='check mode: no API call made', url=url)

    response, info = fetch_url(
        module,
        url,
        headers=headers,
        data=json.dumps(payload),
        method='POST',
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
