"""Framework-independent echo business logic."""


def echo(text: str) -> dict:
    """Build the result returned by the test_echo SOAR function."""
    return {
        "success": True,
        "input": text,
        "message": "Received: " + text,
    }
