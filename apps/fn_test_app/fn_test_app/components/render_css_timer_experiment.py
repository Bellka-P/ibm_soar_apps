# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for render_css_timer_experiment."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function

from fn_test_app.util.css_timer_service import render_css_timer_experiment

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return visual-only CSS animation test markup."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_css_timer_experiment")
    def _app_function(self, fn_inputs):
        yield FunctionResult(render_css_timer_experiment())
