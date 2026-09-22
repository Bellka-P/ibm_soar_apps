# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for render_javascript_test."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function

from fn_test_app.util.javascript_test_service import render_javascript_test

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return diagnostic markup without executing browser code on the backend."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_javascript_test")
    def _app_function(self, fn_inputs):
        yield FunctionResult(render_javascript_test(
            getattr(fn_inputs, "javascript_test_mode", None)
        ))
