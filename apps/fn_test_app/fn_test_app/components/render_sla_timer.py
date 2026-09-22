# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for render_sla_timer."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.sla_timer_service import render_sla_timer

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return a static SLA timer snapshot."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_sla_timer")
    def _app_function(self, fn_inputs):
        validate_fields(["sla_deadline"], fn_inputs)
        result = render_sla_timer(
            deadline=fn_inputs.sla_deadline,
            label=getattr(fn_inputs, "sla_label", None),
            show_seconds=getattr(fn_inputs, "sla_show_seconds", None),
        )
        yield FunctionResult(
            result,
            success=result["success"],
            reason=result.get("error"),
        )
