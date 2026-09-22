# fn_test_app

Minimal IBM QRadar SOAR App Host application used to verify the complete
development cycle and Rich Text rendering. Current version: `1.2.1`.

## Functions

### `test_echo`

`test_echo` accepts one required text input, `test_text`, and returns:

```json
{
  "success": true,
  "input": "example",
  "message": "Received: example"
}
```

The SOAR-specific adapter is in `fn_test_app/components/test_echo.py`. The
framework-independent implementation is in `fn_test_app/util/echo_service.py`.

### `render_html`

`render_html` accepts one required text input, `html_content`, and returns the
input HTML unchanged:

```json
{
  "success": true,
  "html": "<h1>Example</h1>",
  "length": 16
}
```

The SOAR adapter is in `fn_test_app/components/render_html.py`; the independent
logic is in `fn_test_app/util/html_service.py`.

This function intentionally does not sanitize HTML. It is a test mode intended
to reveal which HTML elements and attributes IBM SOAR itself permits or removes.
Do not pass untrusted HTML to it in production. It does not execute or add
JavaScript.

## Rich Text incident field

The customization package includes the Rich Text-compatible Text Area field
`HTML Report` (`incident.properties.html_report`). A Playbook can assign the
standard function result to it with a post-processing script:

```python
result = playbook.functions.results.html_result

if result.success:
    incident.properties.html_report = helper.createRichText(
        result.content["html"]
    )
```

`FunctionResult` uses the standard IBM SOAR result envelope: `success` is on
the result object and the dictionary returned by the function is under
`result.content`.

## HTML rendering test

```html
<h1>IBM SOAR HTML Test</h1>

<p><strong>Status:</strong> Success</p>

<h2>Incident Information</h2>

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Application</td>
    <td>fn_test_app</td>
  </tr>
  <tr>
    <td>Status</td>
    <td>Running</td>
  </tr>
</table>

<h2>Steps</h2>

<ul>
  <li>Function executed</li>
  <li>HTML generated</li>
  <li>Result written to incident</li>
</ul>

<div style="border: 1px solid #4589ff; padding: 8px;">
  <p><em>Styled content inside a div.</em></p>
  <a href="https://www.ibm.com/products/qradar-soar">IBM QRadar SOAR</a>
</div>

<details>
  <summary>Additional details</summary>
  <p>Content inside details/summary.</p>
</details>

<pre><code>SOAR
  |
  v
App Host
  |
  v
render_html</code></pre>
```

Test inline SVG separately so it is clear whether SOAR removes SVG while
allowing the rest of the HTML:

```html
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="80" viewBox="0 0 240 80">
  <rect x="1" y="1" width="238" height="78" rx="8" fill="#edf5ff" stroke="#0f62fe" />
  <circle cx="40" cy="40" r="18" fill="#24a148" />
  <text x="70" y="47" font-family="sans-serif" font-size="20" fill="#161616">SOAR SVG Test</text>
</svg>
```

## Independent HTML report blocks

The app also provides five independent functions and Rich Text incident fields:

| Function | Required input | Result block | Incident field |
| --- | --- | --- | --- |
| `update_html_summary` | `summary_html` | `summary` | `incident.properties.html_summary` |
| `update_html_checklist` | `checklist_html` | `checklist` | `incident.properties.html_checklist` |
| `update_html_evidence` | `evidence_html` | `evidence` | `incident.properties.html_evidence` |
| `update_html_timeline` | `timeline_html` | `timeline` | `incident.properties.html_timeline` |
| `update_html_recommendations` | `recommendations_html` | `recommendations` | `incident.properties.html_recommendations` |

Each function returns the same standard content structure:

```json
{
  "success": true,
  "block": "summary",
  "html": "<h2>Summary</h2><p>...</p>",
  "length": 34
}
```

The common, framework-independent implementation is
`fn_test_app/util/html_block_service.py`. Functions return data only; updating
the incident remains the responsibility of the Playbook post-processing step.

### Playbook post-processing examples

Summary, using Function Output Name `summary_result`:

```python
result = playbook.functions.results.summary_result

if result.success:
    incident.properties.html_summary = helper.createRichText(
        result.content["html"]
    )
```

Checklist, using Function Output Name `checklist_result`:

```python
result = playbook.functions.results.checklist_result

if result.success:
    incident.properties.html_checklist = helper.createRichText(
        result.content["html"]
    )
```

Evidence, using Function Output Name `evidence_result`:

```python
result = playbook.functions.results.evidence_result

if result.success:
    incident.properties.html_evidence = helper.createRichText(
        result.content["html"]
    )
```

Timeline, using Function Output Name `timeline_result`:

```python
result = playbook.functions.results.timeline_result

if result.success:
    incident.properties.html_timeline = helper.createRichText(
        result.content["html"]
    )
```

Recommendations, using Function Output Name `recommendations_result`:

```python
result = playbook.functions.results.recommendations_result

if result.success:
    incident.properties.html_recommendations = helper.createRichText(
        result.content["html"]
    )
```

### Test HTML values

Summary:

```html
<h2>Summary</h2>
<p>Incident analysis completed successfully.</p>
```

Checklist:

```html
<h2>Checklist</h2>
<ul>
  <li>Validate source IP</li>
  <li>Validate destination IP</li>
  <li>Check user activity</li>
</ul>
```

Evidence:

```html
<h2>Evidence</h2>
<table border="1" cellpadding="6">
  <tr>
    <th>Type</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Source IP</td>
    <td>10.10.10.10</td>
  </tr>
</table>
```

Timeline:

```html
<h2>Timeline</h2>
<ul>
  <li>10:00 - Incident created</li>
  <li>10:02 - Analysis started</li>
  <li>10:05 - Analysis completed</li>
</ul>
```

Recommendations:

```html
<h2>Recommendations</h2>
<ol>
  <li>Review affected account</li>
  <li>Validate endpoint activity</li>
  <li>Close incident if confirmed legitimate</li>
</ol>
```

### Incident layout

The app does not modify an existing Incident Layout. After installation, add
the custom fields manually to a tab such as `Test`, in this order:

1. HTML Summary
2. HTML Checklist
3. HTML Evidence
4. HTML Timeline
5. HTML Recommendations

## UI capability experiments

Version 1.2.0 adds four test functions without changing the existing
functions:

| Function | Purpose | Incident field |
| --- | --- | --- |
| `render_ui_card` | Escaped, table-based, full-width incident card | `incident.properties.html_ui_card` |
| `render_javascript_test` | Diagnostic HTML for observing sanitizer/CSP behavior | `incident.properties.html_ui_card` |
| `render_sla_timer` | Static server-side SLA snapshot | `incident.properties.html_sla_timer` |
| `render_css_timer_experiment` | Visual-only CSS animation test | `incident.properties.html_sla_timer` |

`ui_events` and `sla_show_seconds` are Text inputs because Text is the input
schema already verified in this package and SDK. The SLA service accepts
`true`, `1`, `yes`, `y`, or `on` (case-insensitive) as true.

All values inserted into the UI card are HTML-escaped. The table layout is the
primary layout rather than a flex layout, so loss of flex-related CSS does not
collapse the left details/right summary structure.

### Playbook post-processing

UI card, using Function Output Name `res_ui_card`:

```python
res = playbook.functions.results.res_ui_card

if res.success and res.content.get("html"):
    incident.properties.html_ui_card = helper.createRichText(
        res.content["html"]
    )
```

SLA snapshot, using Function Output Name `res_sla`:

```python
res = playbook.functions.results.res_sla

if res.success and res.content.get("html"):
    incident.properties.html_sla_timer = helper.createRichText(
        res.content["html"]
    )
```

JavaScript capability test, using Function Output Name `res_js_test`:

```python
res = playbook.functions.results.res_js_test

if res.success and res.content.get("html"):
    incident.properties.html_ui_card = helper.createRichText(
        res.content["html"]
    )
```

These snippets are examples only and are not installed as production
Playbooks.

### SLA date/time behavior

`render_sla_timer` converts timezone-aware ISO-like values to UTC before
calculating the difference from `datetime.now(timezone.utc)`. A value without a
timezone is deliberately interpreted as UTC; it is never interpreted using the
container's local timezone. The output is a static snapshot, not a live ticking
timer. Invalid dates return a completed failure result rather than hanging.

### JavaScript, CSS, and sanitizer warning

`render_javascript_test` only returns a string. Python never executes the
embedded markup. The test includes clearly identified `onclick`, `script`,
`setInterval`, CSS animation, `details/summary`, an `about:blank` iframe, and
inline SVG. IBM SOAR may remove any or all of these through its sanitizer or
Content Security Policy. The function does not attempt to bypass those controls.

`render_css_timer_experiment` contains no JavaScript. Its progress bar, blinking
dot, and rotating indicator are visual experiments only and do not measure SLA
time accurately.

### Layout and custom UI limitation

The installed SDK 51.0.7.2.16540 can carry a complete `layouts` customization
object, but its `codegen` and `extract` commands expose no separate selector for
an HTML Block, Section, Header, Custom Tab, Custom View, widget, or UI Extension.
No supported package frontend/static-assets extension point was found in the
installed SDK project model. Therefore this app does not modify an Incident
Layout. A static HTML Block may be added manually in the SOAR Layout editor,
but it is not a dynamic `incident.properties` value and cannot receive a
FunctionResult through the field assignment shown above.

## Test

```shell
python -m pytest
```

## Validate and package

```shell
resilient-sdk validate -p . --validate
resilient-sdk package -p . --validate
```
