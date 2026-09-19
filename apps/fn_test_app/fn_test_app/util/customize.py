# -*- coding: utf-8 -*-
# <<PUT YOUR COPYRIGHT TEXT HERE>>
# Generated with resilient-sdk v51.0.7.2.16540

"""Generate the SOAR customizations required for fn_test_app"""

import base64
import os
import io
try:
    from resilient import ImportDefinition
except ImportError:
    # Support Apps running on resilient-circuits < v35.0.195
    from resilient_circuits.util import ImportDefinition

RES_FILE = "data/export.res"


def codegen_reload_data():
    """
    Parameters required reload codegen for the fn_test_app package
    """
    return {
        "package": u"fn_test_app",
        "message_destinations": [
            u"fn_test_app"
        ],
        "functions": [
            u"test_echo",
            u"render_html"
        ],
        "workflows": [],
        "actions": [],
        "incident_fields": [
            u"html_report"
        ],
        "incident_artifact_types": [],
        "incident_types": [],
        "datatables": [],
        "automatic_tasks": [],
        "scripts": [],
        "playbooks": [],
    }


def customization_data(client=None):
    """
    Returns a Generator of ImportDefinitions (Customizations).
    Install them using `resilient-circuits customize`

    IBM SOAR Platform Version: 

    Contents:
    - Message Destinations:
        - fn_test_app
    - Functions:
        - test_echo
        - render_html
    - Incident Fields:
        - html_report
    """

    res_file = os.path.join(os.path.dirname(__file__), RES_FILE)
    if not os.path.isfile(res_file):
        raise FileNotFoundError("{} not found".format(RES_FILE))

    with io.open(res_file, mode='rt') as f:
        b64_data = base64.b64encode(f.read().encode('utf-8'))
        yield ImportDefinition(b64_data)
