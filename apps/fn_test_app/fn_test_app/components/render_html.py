# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for the render_html function."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.html_service import render_html

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Component that implements the render_html SOAR function."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_html")
    def _app_function(self, fn_inputs):
        """Return the required html_content input without modifying it."""
        validate_fields(["html_content"], fn_inputs)
        yield FunctionResult(render_html(fn_inputs.html_content))
