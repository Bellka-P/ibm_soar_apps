# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for the test_echo function."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.echo_service import echo

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Component that implements the test_echo SOAR function."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("test_echo")
    def _app_function(self, fn_inputs):
        """Return the required test_text input as an echo response."""
        validate_fields(["test_text"], fn_inputs)
        yield FunctionResult(echo(fn_inputs.test_text))
