import requests

def log_event(stack, level, package, message):
    url = "http://<test-server-url>/log"  # Replace with actual endpoint
    data = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message,
    }
    try:
        requests.post(url, json=data)
    except Exception:
        pass  # Don't interrupt main logic
