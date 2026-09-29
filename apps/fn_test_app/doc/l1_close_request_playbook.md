# L1 Close Request playbook

QRadar SOAR stores a Playbook as a platform-generated graph. Create this graph
in Playbook Designer; do not paste a hand-written BPMN object into `export.res`.

## Settings

- Name: `L1 Close Request`
- API name: `l1_close_request`
- Object type: `Incident`
- Activation type: `Automatic`
- Status after review: `Enabled`
- Conditions, using `All`:
  - `incident.properties.l1_submit_close equals True`
  - incident status is open (`incident.plan_status equals A`)

Add one Python 3 local-script node immediately after activation. Name it
`Validate and accept L1 close request` and paste the script below. Replace the
three `REPLACE_WITH_EXISTING_*` values with API names of fields that already
exist in the target organization. Do not recreate those fields in this app.

```python
CLOSE_TYPE_FIELD_API_NAME = "REPLACE_WITH_EXISTING_CLOSE_TYPE_API_NAME"
REQUIRED_FIELD_API_NAMES = (
    "REPLACE_WITH_EXISTING_TRIAGE_API_NAME",
    "REPLACE_WITH_EXISTING_ANALYSIS_API_NAME",
)
ALLOWED_CLOSE_TYPES = ("FP", "TP", "TP Benign")


def read_property(api_name):
    return getattr(incident.properties, api_name, None)


def has_value(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return True


def display_value(value):
    label = getattr(value, "name", None) or getattr(value, "label", None)
    return str(label if label is not None else value).strip()


# Claim the request. A second instance or later incident update sees False and
# has no effect. Validation failures also require a deliberate retry.
if incident.properties.l1_submit_close is True:
    incident.properties.l1_submit_close = False

    close_type_raw = read_property(CLOSE_TYPE_FIELD_API_NAME)
    close_type = display_value(close_type_raw) if has_value(close_type_raw) else ""
    missing_fields = [
        api_name for api_name in REQUIRED_FIELD_API_NAMES
        if not has_value(read_property(api_name))
    ]

    errors = []
    if close_type not in ALLOWED_CLOSE_TYPES:
        errors.append("close type must be FP, TP, or TP Benign")
    if missing_fields:
        errors.append("required fields are empty: {}".format(", ".join(missing_fields)))

    if errors:
        incident.addNote(helper.createRichText(
            "L1 Close Request rejected: {}. Correct the data, select "
            "Close Incident again, and save the incident.".format("; ".join(errors))
        ))
    else:
        from datetime import datetime
        started_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        incident.addNote(helper.createRichText(
            "L1 Close Request accepted. Close type: {}. Started: {}. "
            "The incident and QRadar offense were not closed.".format(
                close_type, started_at
            )
        ))

        if close_type == "FP":
            # TODO(L1-CLOSE-FP): add approved FP actions here.
            pass
        elif close_type == "TP":
            # TODO(L1-CLOSE-TP): add approved TP actions here.
            pass
        elif close_type == "TP Benign":
            # TODO(L1-CLOSE-TP-BENIGN): add approved TP Benign actions here.
            pass
```

On validation failure the flag is already reset and the note explains how to
retry. On success the note contains the selected type and UTC time. No incident
or QRadar offense is closed.

To package the Playbook later, create it on the target SOAR 51.x development
organization and use the project's normal `resilient-sdk codegen`/`extract`
workflow to refresh `export.res` with API name `l1_close_request`. Preserve the
existing `l1_submit_close` field definition and review the resulting diff so no
unrelated organization objects or layouts are included.
