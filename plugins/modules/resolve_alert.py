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
  - This module resolves one or more BigPanda alerts via the batch-resolve API.
module: resolve_alert
options:
  environment_id:
    description: The ID of the BigPanda environment containing the alerts.
    required: true
    type: str
  alert_ids:
    description: The IDs of the alerts to resolve.
    required: true
    type: list
    elements: str
  comments:
    description: Optional comments to attach to the resolution.
    required: false
    type: list
    elements: str
  api_token:
    description: The API token for authentication.
    required: true
    type: str
short_description: Resolve one or more BigPanda alerts.
version_added: 1.0.0
"""

EXAMPLES = """
- name: Resolve alerts
  bigpanda.incident.resolve_alert:
    environment_id: "your_environment_id"
    alert_ids:
      - "54321"
    comments:
      - "Alert resolved."
    api_token: "your_api_token"
"""

RETURN = """
changed:
  description: Indicates if the alert resolution was successful.
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
  sample: "Alerts resolved successfully."
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_id=dict(type='str', required=True),
            api_token=dict(type='str', required=True, no_log=True),
            alert_ids=dict(type='list', elements='str', required=True),
            comments=dict(type='list', elements='str', required=False),
        ),
        supports_check_mode=True,
    )

    environment_id = module.params['environment_id']
    api_token = module.params['api_token']
    alert_ids = module.params['alert_ids']
    comments = module.params['comments']

    url = (
        'https://api.bigpanda.io/resources/v2.0/environments/'
        f'{environment_id}/batch-resolve/alerts'
    )
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    payload = {'ids': alert_ids}
    if comments:
        payload['comments'] = comments

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
