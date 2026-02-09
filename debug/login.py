import requests
import time

CLIENT_ID = "4725a997e94b372b1c26e425086f4a17"
CLIENT_SECRET = "7e9379a4d444a3c21cf28da6a032154dc4b644eba523e7684f71818dec3beeb7"

PHONE = "989046699095"
PASSWORD = "Amir1383amir!"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fa",
    "Content-Type": "application/json",
    "Origin": "https://my.irancell.ir",
    "Referer": "https://my.irancell.ir/sessions/add",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    ),
    "X-App-Version": "9.68.1",
}

session = requests.Session()
session.headers.update(headers)

# STEP 1 — login options (sets cookie)
payload_1 = {
    "client_id": CLIENT_ID,
    "phone_number": PHONE
}

r1 = session.post(
    "https://my.irancell.ir/api/authorization/v1/login/options",
    json=payload_1
)

print("OPTIONS:", r1.json())

time.sleep(1)

# STEP 2 — token request
payload_2 = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "client_version": "9.68.1",
    "device_name": "Web Windows 10",
    "grant_type": "password",
    "installation_id": "1216ed29-501c-40c8-9362-eebca7f07672",
    "notifPermissionGranted": True,
    "phone_number": PHONE,
    "password": PASSWORD
}

r2 = session.post(
    "https://my.irancell.ir/api/authorization/v1/token",
    json=payload_2
)

print("TOKEN:", r2.json())
