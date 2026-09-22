"""Generate diagnostic markup for observing IBM SOAR HTML sanitization."""

from html import escape


WARNING = "JavaScript may be removed by IBM SOAR sanitizer"


def render_javascript_test(mode=None):
    """Return capability-test markup as data; no JavaScript runs in Python."""
    safe_mode = escape(str(mode), quote=True) if mode not in (None, "") else "default"

    test_html = """<div style="width:100%; box-sizing:border-box; padding:12px; border:1px solid #8d8d8d;">
  <h2>IBM SOAR JavaScript / Sanitizer Test</h2>
  <p><strong>Mode:</strong> {mode}</p>
  <div id="js-test">Static text</div>
  <button type="button" onclick="document.getElementById('js-test').innerText='Clicked'">Test onclick</button>
  <script>
    document.getElementById('js-test').setAttribute('data-script-test', 'executed');
    setInterval(function () {{
      document.getElementById('js-test').setAttribute('data-interval-test', 'tick');
    }}, 1000);
  </script>
  <style>
    @keyframes soarPulse {{ 0% {{ opacity: 0.35; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.35; }} }}
  </style>
  <div id="css-animation-test" style="animation:soarPulse 2s infinite; padding:8px; background:#d0e2ff;">CSS animation test</div>
  <details id="details-test"><summary>Details / summary test</summary><p>Expandable static content.</p></details>
  <iframe id="iframe-test" src="about:blank" title="Safe blank iframe sanitizer test" style="width:100%; height:60px; border:1px solid #c6c6c6;"></iframe>
  <svg id="svg-test" xmlns="http://www.w3.org/2000/svg" width="180" height="48" viewBox="0 0 180 48" role="img" aria-label="SVG sanitizer test">
    <rect x="1" y="1" width="178" height="46" rx="6" fill="#edf5ff" stroke="#0f62fe"></rect>
    <text x="16" y="30" font-family="sans-serif" font-size="16" fill="#161616">SVG test</text>
  </svg>
</div>""".format(mode=safe_mode)

    return {
        "success": True,
        "html": test_html,
        "length": len(test_html),
        "warning": WARNING,
        "type": "javascript_capability_test",
    }
