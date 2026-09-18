# fn_test_app

Minimal IBM QRadar SOAR App Host application used to verify the complete
development cycle: source, validation, tests, SDK package, and importable ZIP.

## Function

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

## Test

```shell
python -m pytest
```

## Validate and package

```shell
resilient-sdk validate -p . --validate
resilient-sdk package -p . --validate
```
