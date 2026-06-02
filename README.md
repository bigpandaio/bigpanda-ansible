# BigPanda Ansible Collection (`bigpanda.incident`)

Ansible Collection of action modules that automate the BigPanda Incident
Management platform. Use it from a plain `ansible-playbook` invocation, from
[Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible)
(AAP), or from an Event-Driven Ansible (EDA) rulebook to react to BigPanda
webhooks.

The collection is distributed through Red Hat **Automation Hub** as the
certified `bigpanda.incident` collection.

---

## Table of contents

1. [What's included](#whats-included)
2. [Action modules — reference](#action-modules--reference)
3. [Quick local test](#quick-local-test)
4. [Building the collection tarball](#building-the-collection-tarball)
5. [Getting an Ansible Automation Platform instance](#getting-an-ansible-automation-platform-instance)
6. [Uploading the tarball to Automation Hub](#uploading-the-tarball-to-automation-hub)
7. [Testing end-to-end from the AAP UI](#testing-end-to-end-from-the-aap-ui)
8. [EDA rulebook](#eda-rulebook)
9. [Development](#development)
10. [License](#license)

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
Every module supports `check_mode` — `--check` returns the URL that would
have been called without making any HTTP request.

---

## Action modules — reference

### `bigpanda.incident.comment`

| Parameter | Required | Description |
|---|---|---|
| `environment_id` | yes | The BigPanda environment that contains the incident |
| `incident_id` | yes | Incident to comment on |
| `comment` | yes | Comment text (≤ 1000 chars) |
| `api_token` | yes | BigPanda User API Key |

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
| `comments` | no | List of comment strings to attach to the batch resolve |
| `api_token` | yes | BigPanda User API Key |

```yaml
- bigpanda.incident.resolve_alert:
    environment_id: "{{ environment_id }}"
    alert_ids:      ["5d09d221aebaec1c43ccd448", "5cff623a21169351a82cb5e2"]
    comments:       ["Marking for regional similarity"]
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

For a fast sanity check before involving AAP:

```bash
# install ansible-core
brew install ansible

# build and install the collection from this repo
ansible-galaxy collection build --force
ansible-galaxy collection install bigpanda-incident-<VERSION>.tar.gz -p ./collections -f

# dry run (no network calls)
ANSIBLE_COLLECTIONS_PATH=./collections \
ansible-playbook ./tests/integration/bigpanda_test.yml --check \
  -e environment_id=<env-uuid> \
  -e incident_id=<inc-uuid> \
  -e api_token=<your-token> \
  -e tag_id=priority -e tag_value=P3 \
  -e assignee_id=<user-uuid> \
  -e source_incidents='["incA","incB"]' \
  -e alert_ids='["alertX","alertY"]'
```

Drop `--check` to make the real API calls. Each module supports check mode
and will return the URL it would have called.

---

## Building the collection tarball

The collection is shipped as a single `.tar.gz` artifact, produced by
`ansible-galaxy collection build`.

```bash
# from the repo root
ansible-galaxy collection build --force
# → bigpanda-incident-<version>.tar.gz
```

Important details:

- The version comes from the `version:` field in `galaxy.yml`.
- The list of files included is controlled by `build_ignore:` in
  `galaxy.yml`. It excludes `.venv/`, `.idea/`, `.claude/`, `.DS_Store`,
  `collections/`, `*.tar.gz`, `__pycache__`, `.pytest_cache`, and
  `tests/output`. A correctly built tarball is around ~20 KB; if you see a
  multi-megabyte artifact, something unintended (typically a venv or a
  previously-installed `collections/` tree) is being included.
- Validate the build with `ansible-test sanity` before uploading anywhere:

  ```bash
  rm -rf /tmp/coll && mkdir -p /tmp/coll/ansible_collections/bigpanda/incident
  tar xzf bigpanda-incident-<version>.tar.gz -C /tmp/coll/ansible_collections/bigpanda/incident
  cd /tmp/coll/ansible_collections/bigpanda/incident
  ANSIBLE_COLLECTIONS_PATH=/tmp/coll ansible-test sanity --python 3.11
  ```

  All 24 sanity tests should pass.

---

## Getting an Ansible Automation Platform instance

If you don't already have AAP, the quickest free option is the
[**Red Hat Developer Sandbox**](https://developers.redhat.com/developer-sandbox):

1. Sign in with a free Red Hat developer account.
2. Provision the **Ansible Automation Platform** sandbox. It typically
   includes:
   - Automation Controller
   - Event-Driven Ansible (EDA) Controller
   - Private Automation Hub
3. The sandbox URL looks like
   `https://sandbox-aap-<you>.apps.<cluster>.openshiftapps.com/overview`.

For longer-running needs see the
[60-day AAP trial](https://www.redhat.com/en/technologies/management/ansible/trial)
or a paid subscription.

---

## Uploading the tarball to Automation Hub

Either the public Red Hat Automation Hub or a Private Automation Hub on
your AAP instance.

### Private Automation Hub (typical for dev/test)

1. Sign in to AAP and open **Automation Content** in the left navigation.
2. Go to **Namespaces** → **Create namespace** → name it `bigpanda`.
3. Open the namespace, then **Upload collection** → select
   `bigpanda-incident-<version>.tar.gz`. Leave the target repository as
   `staging`.
4. Go to **Automation Content → Approval**, find the staged
   `bigpanda.incident <version>` row, and **Approve** it. Approval moves it
   into the `published` repository, which is what Job Templates pull from.
5. **Wire AAP up to consume from the Hub:**
   - Generate a Hub API token: **Automation Content → API Token →
     Load token**.
   - Create a Galaxy credential: **Automation Execution → Infrastructure
     → Credentials → Create credential**:
     - Credential type: **Ansible Galaxy/Automation Hub API Token**
     - Galaxy server URL: `https://<your-aap-host>/api/galaxy/`
     - API token: paste the token
   - Attach it on the org: **Access Management → Organizations → Default
     → Galaxy credentials**, add the new credential alongside the
     existing public `Ansible Galaxy`.

After this, any Project that references the collection in
`collections/requirements.yml` will install it automatically at sync time.

### Red Hat certified Automation Hub (production publishing)

Publishing to the certified Hub is gated by Red Hat's partner certification
process — see the
[Red Hat Partner Connect Ansible documentation](https://connect.redhat.com/partner-with-us/ansible-automation)
for the current workflow and credentials.

---

## Testing end-to-end from the AAP UI

To exercise every module from the AAP Controller UI (Project → Job Template
→ Survey), use the companion repository
**[bigpandaio/bigpanda-ansible-test](https://github.com/bigpandaio/bigpanda-ansible-test)**.

It contains:

- One playbook per module (`playbooks/<module>.yml`) — each playbook calls
  one module with every parameter sourced from `extra_vars`.
- A `collections/requirements.yml` that pulls `bigpanda.incident` from the
  Hub at Project-sync time.
- A README with the **full Job Template + Survey configuration** for every
  module: question labels, variable names, types, defaults, descriptions,
  and a recommended safe-to-destructive launch order.

The high-level flow on AAP is:

1. Create a Project pointing at
   `https://github.com/bigpandaio/bigpanda-ansible-test.git`
   (branch `master`, **Update revision on launch** enabled).
2. Create one Job Template per playbook, attach the Survey from the
   companion README, leave Credentials empty (the Survey provides
   `api_token` as a Password field).
3. Launch each template from the UI; the Survey collects
   `environment_id` / `incident_id` / `api_token` / module-specific inputs.

---

## EDA rulebook

`extensions/eda/rulebooks/bigpanda-webhook.yml` listens on TCP 6000 and
matches the BigPanda Share-via-Webhook payload shape:

| Rule | Condition | Default action |
|---|---|---|
| 1 | `event.payload.status == "resolved"` | Run AAP job template `BigPanda - On Incident Resolved` |
| 2 | `event.payload.status == "active"` AND `event.payload.severity in ["High", "Critical"]` | Run AAP job template `BigPanda - On High Severity Incident` |
| 3 | `event.payload is defined` | Debug-log the payload (catch-all) |

Wire your AAP-side job templates to do the actual remediation. Configure
your BigPanda share integration to POST to the EDA listener URL.

For an auth-protected listener, uncomment the `token` and `hmac_secret`
fields at the top of the rulebook.

---

## Development

```bash
# create a virtualenv outside the repo, OR use the .venv pattern below
brew install python@3.13
python3.13 -m venv .venv
source .venv/bin/activate
pip install ansible-core ansible-lint

# run sanity tests (matches what Automation Hub runs at publish time)
ansible-galaxy collection build --force
mkdir -p /tmp/coll/ansible_collections/bigpanda/incident
tar xzf bigpanda-incident-*.tar.gz -C /tmp/coll/ansible_collections/bigpanda/incident
cd /tmp/coll/ansible_collections/bigpanda/incident
ANSIBLE_COLLECTIONS_PATH=/tmp/coll ansible-test sanity --python 3.11
```

The repo's `galaxy.yml` already filters `.venv/` and friends out of the
build, so you can keep your venv inside the repo if you want.

### Releasing a new version

1. Bump `version:` in `galaxy.yml`.
2. Add an entry under `releases:` in `changelogs/changelog.yaml` describing
   breaking changes, major changes, and bugfixes.
3. Rebuild the tarball and re-run sanity (see
   [Building the collection tarball](#building-the-collection-tarball)).
4. Tag the release on GitHub:

   ```bash
   git tag v<version>
   git push origin v<version>
   ```

5. Publish to the registries below.

---

## Publishing to public registries

`bigpanda.incident` is distributed through three channels. Merging to
`master` here only updates the source — it does **not** push a new version
to any registry. After tagging a release, push the tarball to whichever
registries apply.

### Current published state (as of writing)

| Registry | Latest published version | Link |
| --- | --- | --- |
| Galaxy (community) | 1.2.0 (Nov 2023) | <https://galaxy.ansible.com/ui/repo/published/bigpanda/incident> |
| Red Hat certified Automation Hub | 1.0.0 (Nov 2023) | <https://catalog.redhat.com/en/software/collection/bigpanda/incident> |
| Private Automation Hub | per-customer | uploaded into each customer's AAP instance |

### 1. Galaxy (community)

Fastest path. Anyone with the Galaxy `bigpanda` namespace token can
publish:

```bash
ansible-galaxy collection publish bigpanda-incident-<version>.tar.gz \
  --token <galaxy-api-key>
```

Listing updates within minutes. Galaxy is the right place to publish
**every release**, including patch releases.

### 2. Red Hat certified Automation Hub

This is the channel AAP customers see in their Controller's "Certified"
content view, and the one Red Hat will deprecate if it goes stale. Requires
going through Red Hat's partner certification flow:

1. Log in to [Red Hat Partner Connect](https://connect.redhat.com/) with
   the BigPanda partner account.
2. Navigate to the Ansible Automation Platform partner section.
3. Upload `bigpanda-incident-<version>.tar.gz`.
4. Red Hat runs automated certification checks (`ansible-test sanity` plus
   policy checks) and a manual review.
5. On approval, the collection appears on
   [catalog.redhat.com](https://catalog.redhat.com/en/software/collection/bigpanda/incident)
   and AAP Controllers pulling from certified Hub see the new version.

Lead time can be a few days to a couple of weeks the first time after a
long gap — start this step early.

### 3. Private Automation Hub (per customer)

For customers who want a specific version before it lands on the certified
Hub, or who run an air-gapped Hub, the tarball can be uploaded directly
into their AAP — see
[Uploading the tarball to Automation Hub](#uploading-the-tarball-to-automation-hub)
above.

### Post-release checklist

After a release is live on the certified Hub:

- [ ] Update [docs.bigpanda.io/en/ansible-automation-platform](https://docs.bigpanda.io/en/ansible-automation-platform)
      with the new version's notable changes (new modules, new params,
      breaking changes from `changelogs/changelog.yaml`).
- [ ] Verify the example playbooks in the companion repo
      ([bigpandaio/bigpanda-ansible-test](https://github.com/bigpandaio/bigpanda-ansible-test))
      still match the latest module signatures.

---

## License

[GPL-2.0-or-later](COPYING). See `COPYING` in the repo root.
