{
  "actions": [],
  "apps": [],
  "automatic_tasks": [],
  "export_date": 1789723200000,
  "export_format_version": 2,
  "fields": [
    {
      "allow_default_value": false,
      "blank_option": false,
      "calculated": false,
      "changeable": true,
      "chosen": false,
      "default_chosen_by_server": false,
      "deprecated": false,
      "export_key": "__function/test_text",
      "hide_notification": false,
      "id": 1001,
      "input_type": "text",
      "internal": false,
      "is_tracked": false,
      "name": "test_text",
      "operation_perms": {},
      "operations": [],
      "placeholder": "",
      "prefix": null,
      "read_only": false,
      "required": "always",
      "rich_text": false,
      "tags": [],
      "templates": [],
      "text": "Test Text",
      "tooltip": "Text to echo",
      "type_id": 11,
      "uuid": "20b2e8e0-9ca7-4a5f-b486-c48f355a6c01",
      "values": []
    }
  ],
  "functions": [
    {
      "description": {
        "content": "Return the supplied text in a simple echo response.",
        "format": "text"
      },
      "destination_handle": "fn_test_app",
      "display_name": "Test Echo",
      "export_key": "test_echo",
      "id": 1002,
      "name": "test_echo",
      "tags": [],
      "uuid": "315b45ad-aa93-4433-9dc8-e606f076d25e",
      "version": 1,
      "view_items": [
        {
          "content": "20b2e8e0-9ca7-4a5f-b486-c48f355a6c01",
          "element": "field_uuid",
          "field_type": "__function",
          "show_if": null,
          "show_link_header": false,
          "step_label": null
        }
      ],
      "workflows": []
    }
  ],
  "id": 0,
  "incident_artifact_types": [],
  "incident_types": [],
  "layouts": [],
  "locale": "en",
  "message_destinations": [
    {
      "api_keys": [],
      "destination_type": 0,
      "expect_ack": true,
      "export_key": "fn_test_app",
      "name": "fn_test_app",
      "programmatic_name": "fn_test_app",
      "tags": [],
      "users": [],
      "uuid": "40846042-411a-4b95-84d4-ab8d1142e5fc"
    }
  ],
  "overrides": null,
  "phases": [],
  "playbooks": [],
  "scripts": [],
  "server_version": {
    "build_number": 0,
    "major": 51,
    "minor": 0,
    "version": "51.0.0"
  },
  "types": [],
  "workflows": []
}
