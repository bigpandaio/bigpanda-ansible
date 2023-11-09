# BigPanda Ansible Collection

## Action Modules

The BigPanda Ansible Collections provides various action modules to interact with the BigPanda resource management system. These modules allow you to perform operations such as resolving incidents, resolving alerts, adding comments to incidents, updating incident tags, merging incidents, and splitting incidents.

To use these action modules, include them in your Ansible playbook and provide the required parameters for the specific function you want to execute.

### Resolve Incident

Use the `bigpanda.incident.resolve` action module to resolve an incident by providing the incident ID and a resolution message.

Parameters:
- `incident_id` (required): The ID of the incident to resolve.
- `resolution_comment` (optional): The resolution message for the incident.
- `api_token` (required): The API token for authentication.

**Example:**

```yaml
- name: Resolve Incident
  bigpanda.incident.resolve:
    incident_id: <incident_id>
    resolution_comment: <resolution_comment>
    api_token: <api_token>
```

### Resolve Alerts

The `bigpanda.incident.resolve_alerts` module allows you to resolve an alert by providing the alert ID and resolution message.

Parameters:
- `alert_ids` (required): The ID of the alert to resolve.
- `resolution` (optional): The resolution message for the alert.
- `api_token` (required): The API token for authentication.

**Example:**

```yaml
- name: Resolve Alert
  bigpanda.incident.resolve_alert:
    alert_ids: <alert_id>
    resolution: <resolution>
    api_token: <api_token>
```

### Add Comment to Incident

You can add a comment to an incident using the `bigpanda.incident.comment` module. Provide the incident ID and the comment text.

Parameters:
- `incident_id` (required): The ID of the incident to add a comment to.
- `comment` (required): The text of the comment.
- `api_token` (required): The API token for authentication.

**Example:**

```yaml
- name: Add Comment to Incident
  bigpanda.incident.comment:
    incident_id: <incident_id>
    comment: <comment>
    api_token: <api_token>
```

### Update Incident Tag

Use the `bigpanda.incident.add_tag` module to update an incident tag. Provide the tag ID, tag value, incident ID, and API token.

Parameters:
- `tag_id` (required): The ID of the tag to update.
- `tag_value` (required): The new value for the tag.
- `incident_id` (required): The ID of the incident to update.
- `api_token` (required): The API token for authentication.

**Example:**

```yaml
- name: Update Incident Tag
  bigpanda.incident.add_tag:
    tag_id: <tag_id>
    tag_value: <tag_value>
    incident_id: <incident_id>
    api_token: <api_token>
```

### Merge Incidents

The `bigpanda.incident.merge` module allows you to merge multiple incidents into a single incident in BigPanda.

**Example:**

```yaml
- name: Merge Incidents
  tasks:
    - name: Merge Incidents
      bigpanda.incident.merge:
        incident_id: "{{ incident_id }}"
        comment: "This is a test from the Ansible collection"
        api_token: "{{ api_token }}"
        environment_id: "{{ environment_id }}"
        source_incidents: "{{ source_incidents }}"
```

### Split Incidents

The `bigpanda.incident.split` module allows you to split a single incident into multiple incidents in BigPanda.

**Example:**

```yaml
- name: Split Incidents
  hosts: localhost
  connection: local
  tasks:
    - name: Split Incidents
      bigpanda.incident.split:
        incident_id: "{{ incident_id }}"
        comment: "This is a test from the Ansible collection"
        api_token: "{{ api_token }}"
        environment_id: "{{ environment_id }}"
        alert_ids: "{{ alert_ids }}"
```

These action modules provide a flexible way to manage incidents and alerts in the BigPanda platform. Use the provided examples in your Ansible playbooks to streamline your incident and alert management processes.

## Using and Developing with the Ansible Collection

### Running Ansible Playbook Locally and Testing Functionality

To use and develop with the BigPanda Ansible Collection, follow these steps:

1. Build and install the BigPanda collection. Run the following commands to build and install the collection in the "./collections" folder. You need to perform this step whenever you make changes:

   ```bash
   ansible-galaxy collection build --force
   ansible-galaxy collection install bigpanda-incident-<VERSION>.tar.gz -p ./collections -f
   ```

2. Run the Ansible playbook for testing. Replace the placeholders with your specific information:

   ```bash
   ansible-playbook ./tests/integration/bigpanda_test.yml --extra-vars='{"environment_id": "YOUR-ENV-ID","api_token": "YOUR-API-TOKEN", "incident_id":"YOUR-INCIDENT-ID", "tag_id": "test", "tag_value": "success"}'
   ```

### Running in an Instance

To run in an instance, you'll need to create a decision environment for EDA (Event-Driven Automation) and/or an execution environment for AAP (Ansible Automation Platform). Follow these guides:

- [Decision Environment Guide](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/html/event-driven_ansible_controller_user_guide/eda-decision-environments)
- [Execution Environment Guide](https://docs.ansible.com/automation-controller/4.0.0/html/userguide/execution_environments.html)

These guides will help you set up the necessary environments for BigPanda Ansible Collection.