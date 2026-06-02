#!/usr/bin/python
# Copyright 2023 BigPanda
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
  - Juan Cardozo (@JuanDCardozo)
description:
  - This module merges multiple BigPanda incidents into a single target incident.
module: merge
options:
  environment_id:
    description: The ID of the BigPanda environment containing the incidents.
    required: true
    type: str
  incident_id:
    description: The ID of the target incident to merge into.
    required: true
    type: str
  source_incidents:
    description: A list of source incident IDs to merge into the target.
    required: true
    type: list
    elements: str
  comment:
    description: A comment describing the merge.
    required: false
    type: str
  api_token:
    description: The API token for authentication.
    required: true
    type: str
short_description: Merge multiple BigPanda incidents into one.
version_added: 1.0.0
"""

EXAMPLES = """
- name: Merge incidents
  bigpanda.incident.merge:
    environment_id: "your_environment"
    incident_id: "target_incident"
    source_incidents:
      - "incident1"
      - "incident2"
    comment: "Merging multiple incidents."
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the incidents were successfully merged.
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
  sample: "Incidents merged successfully."
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            incident_id=dict(type='str', required=True),
            source_incidents=dict(type='list', elements='str', required=True),
            comment=dict(type='str', required=False),
            api_token=dict(type='str', required=True, no_log=True),
        ),
        supports_check_mode=True,
    )

    environment_id = module.params['environment_id']
    incident_id = module.params['incident_id']
    source_incidents = module.params['source_incidents']
    comment = module.params['comment']
    api_token = module.params['api_token']

    url = (
        'https://api.bigpanda.io/resources/v2.0/environments/'
        f'{environment_id}/incidents/{incident_id}/merge'
    )
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'source_incidents': source_incidents,
        'comment': comment,
    }

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
