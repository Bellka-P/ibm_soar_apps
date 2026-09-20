# fn_test_app

Minimal IBM QRadar SOAR App Host application used to verify the complete
development cycle and Rich Text rendering. Current version: `1.1.1`.

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

## Test

```shell
python -m pytest
```

## Validate and package

```shell
resilient-sdk validate -p . --validate
resilient-sdk package -p . --validate
```
