# BigPanda Ansible Collection (`bigpanda.incident`)

Ansible Collection of action modules that automate the BigPanda Incident
Management platform. Use it from a plain `ansible-playbook` invocation,
from [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible)
(AAP), or from an Event-Driven Ansible (EDA) rulebook to react to BigPanda
webhooks.

The collection is distributed through Red Hat **Automation Hub** as the
certified `bigpanda.incident` collection, and through community Galaxy.

---

## Table of contents

1. [What's included](#whats-included)
2. [Action modules — reference](#action-modules--reference)
3. [Quick local test](#quick-local-test)
4. [Targeting EU / dedicated tenants](#targeting-eu--dedicated-tenants)
5. [Testing in Ansible Automation Platform](#testing-in-ansible-automation-platform)
6. [EDA rulebook](#eda-rulebook)
7. [License](#license)

---

## What's included

| Type | Name | Purpose |
|---|---|---|
| Module | `bigpanda.incident.comment` | Post a comment on an incident |
| Module | `bigpanda.incident.add_tag` | Add/update a tag on an incident |
| Module | `bigpanda.incident.assign` | Assign a user to an incident |
| Module | `bigpanda.incident.resolve` | Resolve (close) an incident |
| Module | `bigpanda.incident.resolve_alert` | Resolve one or more alerts |
| Module | `bigpanda.incident.merge` | Merge incidents into a target |
| Module | `bigpanda.incident.split` | Split alerts off into a new incident |
| Rulebook | `extensions/eda/rulebooks/bigpanda-webhook.yml` | Receive BigPanda Share-via-Webhook events in EDA |

All modules call the v2.0 BigPanda public REST API. Authentication is a
BigPanda **User API Key** (Settings → API Keys), passed via `api_token`.
The API host defaults to `https://api.bigpanda.io` and can be overridden
per task with `api_url`, or once per play via `module_defaults` (see
[Targeting EU / dedicated tenants](#targeting-eu--dedicated-tenants)).
Every module supports `check_mode` — `--check` returns the `url`,
`method`, and `payload` that would have been sent without making any
HTTP request.

---

## Action modules — reference

### `bigpanda.incident.comment`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | The BigPanda environment that contains the incident |
| `incident_id` | yes | Incident to comment on |
| `comment` | yes | Comment text (≤ 1000 chars) |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.comment:
    environment_id: "{{ environment_id }}"
    incident_id:    "{{ incident_id }}"
    comment:        "Investigating; ETA 10 min"
    api_token:      "{{ api_token }}"
```

### `bigpanda.incident.add_tag`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the incident |
| `incident_id` | yes | Incident to tag |
| `tag_id` | yes | The tag name (must already exist in the env) |
| `tag_value` | yes | Value to set |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.add_tag:
    environment_id: "{{ environment_id }}"
    incident_id:    "{{ incident_id }}"
    tag_id:         "priority"
    tag_value:      "P2"
    api_token:      "{{ api_token }}"
```

### `bigpanda.incident.assign`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the incident |
| `incident_id` | yes | Incident to assign |
| `assignee_id` | yes | BigPanda user UUID |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.assign:
    environment_id: "{{ environment_id }}"
    incident_id:    "{{ incident_id }}"
    assignee_id:    "{{ assignee_id }}"
    api_token:      "{{ api_token }}"
```

### `bigpanda.incident.resolve`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the incident |
| `incident_id` | yes | Incident to resolve |
| `resolution_comment` | no | Posted to the timeline before close |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.resolve:
    environment_id:     "{{ environment_id }}"
    incident_id:        "{{ incident_id }}"
    resolution_comment: "Fixed via automated runbook"
    api_token:          "{{ api_token }}"
```

### `bigpanda.incident.resolve_alert`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the alerts |
| `alert_ids` | yes | List of alert UUIDs (≤ 500 per call) |
| `comments` | no | Resolution comment attached to the batch |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.resolve_alert:
    environment_id: "{{ environment_id }}"
    alert_ids:      ["5d09d221aebaec1c43ccd448", "5cff623a21169351a82cb5e2"]
    comments:       "Marking for regional similarity"
    api_token:      "{{ api_token }}"
```

### `bigpanda.incident.merge`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the incidents |
| `incident_id` | yes | **Target** incident (absorbs the others) |
| `source_incidents` | yes | List of incident UUIDs to merge into the target |
| `comment` | no | Posted to the timeline |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.merge:
    environment_id:   "{{ environment_id }}"
    incident_id:      "{{ incident_id }}"
    source_incidents: ["incA", "incB"]
    comment:          "Same root cause"
    api_token:        "{{ api_token }}"
```

### `bigpanda.incident.split`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | Env containing the incident |
| `incident_id` | yes | Source incident to split alerts out of |
| `alert_ids` | yes | Alert UUIDs to move into a new incident |
| `comment` | no | Posted to the timeline |
| `api_token` | yes | BigPanda User API Key |
| `api_url` | no | BigPanda API base URL (default `https://api.bigpanda.io`; env fallback `BIGPANDA_API_URL`) |

```yaml
- bigpanda.incident.split:
    environment_id: "{{ environment_id }}"
    incident_id:    "{{ incident_id }}"
    alert_ids:      ["alertX", "alertY"]
    comment:        "Different host class"
    api_token:      "{{ api_token }}"
```

---

## Quick local test

For a fast sanity check from a laptop:

```bash
# install ansible-core
brew install ansible

# install the collection from Galaxy (or Automation Hub)
ansible-galaxy collection install bigpanda.incident

# dry run (no network calls)
ansible-playbook -i 'localhost,' -c local --check \
  -e environment_id=<env-uuid> \
  -e incident_id=<inc-uuid> \
  -e api_token=<your-token> \
  -e msg="Hello from Ansible" \
  /dev/stdin <<'YAML'
- hosts: localhost
  tasks:
    - bigpanda.incident.comment:
        environment_id: "{{ environment_id }}"
        incident_id:    "{{ incident_id }}"
        comment:        "{{ msg }}"
        api_token:      "{{ api_token }}"
YAML
```

Drop `--check` to make the real API call. Each module supports check
mode and will return the `url`, `method`, and `payload` it would have
sent — useful for previewing a destructive operation before running it.

---

## Targeting EU / dedicated tenants

BigPanda is hosted at multiple endpoints. Set `api_url` on each module,
or once per play via `module_defaults`:

```yaml
- hosts: localhost
  module_defaults:
    group/bigpanda.incident.all:
      api_url:   "{{ bigpanda_api_url | default('https://api.bigpanda.io') }}"
      api_token: "{{ bigpanda_api_token }}"
  tasks:
    - bigpanda.incident.comment:
        environment_id: "{{ environment_id }}"
        incident_id:    "{{ incident_id }}"
        comment:        "Investigating"
```

Common values:

| Tenant | `api_url` |
|---|---|
| US (default) | `https://api.bigpanda.io` |
| EU (`prod-eu-central-1`) | `https://api.eu.bigpanda.io` |
| Dedicated | provided by your BigPanda CSM |

`api_url` also reads from the `BIGPANDA_API_URL` environment variable,
which is handy for execution-environment image overrides.

---

## Testing in Ansible Automation Platform

To exercise every module from the AAP Controller UI (Project → Job
Template → Survey), use the companion repository
**[bigpandaio/bigpanda-ansible-test](https://github.com/bigpandaio/bigpanda-ansible-test)**.

It contains one playbook per module, a `collections/requirements.yml` that
pulls `bigpanda.incident` from Automation Hub at Project-sync time, and a
README with the full Job Template + Survey configuration for every
module — variable names, types, defaults, descriptions, and a recommended
safe-to-destructive launch order.

If you don't already have an AAP instance, the fastest free option is the
[Red Hat Developer Sandbox](https://developers.redhat.com/developer-sandbox),
which provisions AAP 2.5 with Automation Controller, EDA Controller, and
Private Automation Hub in a single click.

---

## EDA rulebook

`extensions/eda/rulebooks/bigpanda-webhook.yml` listens on TCP 6000 and
matches the [BigPanda Notifications Webhook v2](https://docs.bigpanda.io/en/notifications-webhook)
payload shape:

| Rule | Condition | Default action |
|---|---|---|
| 1 | `event.payload.incident.resolved == true` | Run AAP job template `BigPanda - On Incident Resolved` |
| 2 | `event.payload.incident.active == true` AND `event.payload.incident.status == "critical"` | Run AAP job template `BigPanda - On Critical Incident` |

Both rules extract `incident_id` from `event.payload.incident.id` and
`environment_id` from `event.payload.metadata.environment_id` and pass them
as `extra_vars` to the downstream job template.

Wire your AAP-side job templates to do the actual remediation. Configure
your BigPanda share integration to POST to the EDA listener URL.

For an auth-protected listener, uncomment the `token` and `hmac_secret`
fields at the top of the rulebook.

---

## License

[GPL-2.0-or-later](COPYING). See `COPYING` in the repo root.
