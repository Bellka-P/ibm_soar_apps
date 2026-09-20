# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for update_html_summary."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.html_block_service import build_html_block

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return the Summary HTML block to an IBM SOAR Playbook."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("update_html_summary")
    def _app_function(self, fn_inputs):
        validate_fields(["summary_html"], fn_inputs)
        yield FunctionResult(build_html_block("summary", fn_inputs.summary_html))
