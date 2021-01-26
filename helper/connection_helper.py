import requests


def is_online():
    online_status = False
    try:
        resp = requests.get("http://www.google.com")
        if resp.status_code == 200:
            online_status = True
    except Exception:
        pass

    return online_status