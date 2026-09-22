# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for render_sla_timer."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function
from resilient_lib import validate_fields

from fn_test_app.util.sla_timer_service import render_sla_timer

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Return a static SLA countdown snapshot to an IBM SOAR Playbook."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_sla_timer")
    def _app_function(self, fn_inputs):
        validate_fields(
            ["sla_deadline", "sla_label", "sla_show_seconds"], fn_inputs
        )

        try:
            result = render_sla_timer(
                fn_inputs.sla_deadline,
                fn_inputs.sla_label,
                fn_inputs.sla_show_seconds,
            )
        except ValueError as error:
            message = str(error)
            yield FunctionResult(
                {
                    "success": False,
                    "error": message,
                    "type": "sla_timer",
                },
                success=False,
                reason=message,
            )
            return

        yield FunctionResult(result)
