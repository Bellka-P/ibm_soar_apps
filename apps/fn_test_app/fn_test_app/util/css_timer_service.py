"""Generate a visual-only CSS timer experiment."""


WARNING = "CSS animation is visual only and is not an accurate SLA countdown"


def render_css_timer_experiment():
    """Return static markup containing CSS animations and no JavaScript."""
    test_html = """<div style="width:100%; box-sizing:border-box; padding:12px; border:1px solid #8d8d8d;">
  <style>
    @keyframes soarProgress { from { width:0%; } to { width:100%; } }
    @keyframes soarBlink { 0%,100% { opacity:0.25; } 50% { opacity:1; } }
    @keyframes soarRotate { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
  </style>
  <strong>CSS Timer Experiment</strong>
  <span style="display:inline-block; margin-left:8px; color:#24a148; animation:soarBlink 1s infinite;">●</span>
  <div style="margin-top:10px; width:100%; height:10px; background:#e0e0e0; overflow:hidden;">
    <div style="height:10px; width:0%; background:#0f62fe; animation:soarProgress 10s linear infinite;"></div>
  </div>
  <div style="display:inline-block; margin-top:10px; animation:soarRotate 2s linear infinite;">◷</div>
  <p style="margin-bottom:0;">Visual animation only; no real remaining time is calculated in the browser.</p>
</div>"""

    return {
        "success": True,
        "html": test_html,
        "length": len(test_html),
        "warning": WARNING,
        "type": "css_timer_experiment",
    }
