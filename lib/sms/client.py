import requests


def send_sms(mobile, code):
    params = {'mobile': mobile, 'code': code}
    resp = requests.get("SMS server", params=params, timeout=120.0)
    print(resp.json())
    return True
