import requests


def request_response(url, params, headers=None):
    headers = headers or {}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json()
