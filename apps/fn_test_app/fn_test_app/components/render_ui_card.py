# -*- coding: utf-8 -*-
"""IBM QRadar SOAR integration layer for render_ui_card."""

from resilient_circuits import AppFunctionComponent, FunctionResult, app_function

from fn_test_app.util.ui_card_service import render_ui_card

PACKAGE_NAME = "fn_test_app"


class FunctionComponent(AppFunctionComponent):
    """Render an escaped, compact HTML UI card."""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function("render_ui_card")
    def _app_function(self, fn_inputs):
        yield FunctionResult(render_ui_card(
            severity=getattr(fn_inputs, "ui_severity", None),
            status=getattr(fn_inputs, "ui_status", None),
            level=getattr(fn_inputs, "ui_level", None),
            sla=getattr(fn_inputs, "ui_sla", None),
            category=getattr(fn_inputs, "ui_category", None),
            technique=getattr(fn_inputs, "ui_technique", None),
            client=getattr(fn_inputs, "ui_client", None),
            host=getattr(fn_inputs, "ui_host", None),
            user=getattr(fn_inputs, "ui_user", None),
            source_ip=getattr(fn_inputs, "ui_source_ip", None),
            events=getattr(fn_inputs, "ui_events", None),
            start_time=getattr(fn_inputs, "ui_start_time", None),
            creation_date=getattr(fn_inputs, "ui_creation_date", None),
            summary=getattr(fn_inputs, "ui_summary", None),
        ))
