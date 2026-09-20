# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for update_html_evidence."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.html_block_service import build_html_block

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return the Evidence HTML block to an IBM SOAR Playbook."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("update_html_evidence")
    def _app_function(self, fn_inputs):
        validate_fields(["evidence_html"], fn_inputs)
        yield FunctionResult(build_html_block("evidence", fn_inputs.evidence_html))
