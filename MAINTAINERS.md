# Maintainers' guide — `bigpanda.incident`

Internal docs for BigPanda engineers who own this collection. Covers the
development setup, how to build the artifact, and the publishing flow for
the public registries.

> This file is intentionally **excluded from the published tarball** (see
> `build_ignore:` in `galaxy.yml`). It lives only in the GitHub repo so
> users browsing the collection on Galaxy or Red Hat's catalog never see
> it.

## Contents

1. [Development environment](#development-environment)
2. [Building the collection tarball](#building-the-collection-tarball)
3. [Releasing a new version](#releasing-a-new-version)
4. [Publishing to public registries](#publishing-to-public-registries)
5. [Current published state](#current-published-state)
6. [Credentials & owners](#credentials--owners)
7. [Post-release checklist](#post-release-checklist)

---

## Development environment

```bash
# python 3.11+ recommended (matches AAP 2.5 EE)
brew install python@3.13
python3.13 -m venv .venv
source .venv/bin/activate
pip install ansible-core ansible-lint
```

`.venv/` is `.gitignore`d and excluded from `build_ignore:` so you can keep
it inside the repo.

---

## Building the collection tarball

```bash
# from the repo root, venv active
ansible-galaxy collection build --force
# → bigpanda-incident-<version>.tar.gz
```

Important details:

- Version comes from `version:` in `galaxy.yml`.
- File inclusion is controlled by `build_ignore:` in `galaxy.yml`. It
  excludes `.venv/`, `.idea/`, `.claude/`, `.DS_Store`, `collections/`,
  `*.tar.gz`, `__pycache__`, `.pytest_cache`, `tests/output`, and
  **`MAINTAINERS.md`** (this file).
- A correctly built tarball is around ~24 KB. Multi-MB output means
  something unintended got packed (typically the `.venv/` or a previously
  installed `collections/` tree).

### Validate before publishing

```bash
rm -rf /tmp/coll && mkdir -p /tmp/coll/ansible_collections/bigpanda/incident
tar xzf bigpanda-incident-<version>.tar.gz \
  -C /tmp/coll/ansible_collections/bigpanda/incident
cd /tmp/coll/ansible_collections/bigpanda/incident
ANSIBLE_COLLECTIONS_PATH=/tmp/coll ansible-test sanity --python 3.11
```

All 24 sanity tests should pass. Re-run with `--python 3.13` for a second
opinion.

---

## Releasing a new version

1. Bump `version:` in `galaxy.yml`.
2. Add an entry under `releases:` in `changelogs/changelog.yaml`:
   - `release_summary:`
   - `breaking_changes:` (array)
   - `major_changes:` (array)
   - `bugfixes:` (array)
3. Rebuild the tarball and re-run sanity (see above).
4. Tag the release on GitHub:

   ```bash
   git tag v<version>
   git push origin v<version>
   ```

5. Publish to the registries below.

---

## Publishing to public registries

Merging to `master` only updates the source. It does **not** push a new
version anywhere. After tagging, push the tarball to each channel.

### 1. Galaxy (community)

Fastest path. Holder of a `bigpanda` namespace token publishes:

```bash
ansible-galaxy collection publish bigpanda-incident-<version>.tar.gz \
  --token <galaxy-api-key>
```

Listing updates within minutes. Galaxy is the right place for **every**
release, including patches.

### 2. Red Hat certified Automation Hub

This is the channel AAP customers see in their Controller's "Certified"
content view. Required for clearing Red Hat's deprecation warnings.

1. Log in to <https://connect.redhat.com/> with BigPanda's partner account.
2. Navigate to the Ansible Automation Platform partner section.
3. Upload `bigpanda-incident-<version>.tar.gz`.
4. Red Hat runs automated checks (`ansible-test sanity` + policy review)
   followed by a manual review.
5. On approval the collection appears at
   <https://catalog.redhat.com/en/software/collection/bigpanda/incident>.

Lead time is typically a few days to a couple of weeks the first time
after a long gap — start this step early.

### 3. Private Automation Hub (per customer)

Customers who can't wait for the certified release, or who run an
air-gapped Hub, upload the tarball into their own AAP. See
`README.md → Testing in AAP` and the companion repo
[`bigpandaio/bigpanda-ansible-test`](https://github.com/bigpandaio/bigpanda-ansible-test)
for the customer-side instructions.

---

## Current published state

As of June 2026:

| Registry | Latest published | Link |
| --- | --- | --- |
| Galaxy (community) | 1.2.0 (Nov 2023) | <https://galaxy.ansible.com/ui/repo/published/bigpanda/incident> |
| Red Hat certified Automation Hub | 1.0.0 (Nov 2023) | <https://catalog.redhat.com/en/software/collection/bigpanda/incident> |

Update this table after every public release.

---

## Credentials & owners

### Galaxy

The `bigpanda` namespace on Galaxy is owned by a small set of BigPanda
accounts. The current owner list is public at
<https://galaxy.ansible.com/api/_ui/v1/namespaces/bigpanda/> — fetch that
URL to see who currently has publish rights.

Any existing namespace owner can either:

- generate an API token at <https://galaxy.ansible.com/ui/token/> and run
  `ansible-galaxy collection publish`, **or**
- add new BigPanda engineers as namespace owners through the Galaxy UI
  (<https://galaxy.ansible.com/ui/namespaces/bigpanda/>).

### Red Hat Partner Connect

The certified Automation Hub publish flow runs through BigPanda's
**Red Hat Partner Connect** account at <https://connect.redhat.com/>.
This is a separate credential set from Galaxy and is typically owned by
the BigPanda Product / Integrations / Partnerships team rather than
engineering. The author of the most recent certified release is the best
starting point if you don't know who currently has access.

Once the owner is identified, record their handle or the shared-vault
entry in BigPanda's internal credential store (not in this repo) so the
next maintainer doesn't have to re-discover.

---

## Post-release checklist

After a release lands on the certified Hub:

- [ ] Update <https://docs.bigpanda.io/en/ansible-automation-platform>
      with the new version's notable changes (new modules, new params,
      breaking changes from `changelogs/changelog.yaml`).
- [ ] Bump the version reference in the companion repo
      [`bigpandaio/bigpanda-ansible-test`](https://github.com/bigpandaio/bigpanda-ansible-test)
      README if any new playbooks/Survey questions are needed.
- [ ] Update the [Current published state](#current-published-state) table
      above.
- [ ] Announce internally to BigPanda's customer-facing teams (Solutions,
      Support, Integrations) so they can flag the new version to customers.
