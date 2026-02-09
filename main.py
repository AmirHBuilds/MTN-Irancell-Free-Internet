import requests
import random
import time
import os
import json
import sys
import csv
import uuid

# --- CONFIGURATION ---
CONFIG_FILE = "config.json"
DATA_DIR = "data"
RESULT_FILE = "results.csv"

# Number Prefixes
PREFIXES = [
    "98900", "98901", "98902", "98903", "98904", "98905", 
    "98930", "98933", "98935", "98936", "98937", "98938", 
    "98939", "98941"
]

class IrancellScanner:
    def __init__(self):
        # 1. Setup Directory
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created directory: {DATA_DIR}")

        # 2. Load Config
        self.config = self.load_config()
        if not self.config:
            print(f"(!) Please fill in '{CONFIG_FILE}' and restart.")
            sys.exit(1)

        # URLs
        self.url_check = self.config.get("url")
        self.url_notify = self.config.get("notify_url", f"{self.url_check}/notify")

        # Headers
        self.headers = self.config.get("headers")
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # CSV Path
        self.csv_path = os.path.join(DATA_DIR, RESULT_FILE)

        # Internal memory
        self.history_set = set()
        self.buffer = []

        self.counters = {
            "Success": 0,
            "Non-MTNI": 0,
            "Ineligible": 0,
            "Invalid": 0,
            "Ignored/Error": 0
        }
        self.attempts = 0

        # Load previous history
        self.load_history()

    # ---------------- CONFIG ----------------
    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            print(f"Config file '{CONFIG_FILE}' missing. Creating default...")
            default_config = {
                "url": "https://my.irancell.ir/api/gift/v1/refer_a_friend",
                "notify_url": "https://my.irancell.ir/api/gift/v1/refer_a_friend/notify",
                "auth": {
                    "client_id": "YOUR_CLIENT_ID",
                    "client_secret": "YOUR_CLIENT_SECRET",
                    "phone_number": "989XXXXXXXXX",
                    "password": "YOUR_PASSWORD",
                    "installation_id": "YOUR_INSTALLATION_ID"
                },
                "headers": {
                    "authorization": "Bearer PASTE_TOKEN_HERE",
                    "accept": "application/json, text/plain, */*",
                    "content-type": "application/json",
                    "user-agent": "Mozilla/5.0",
                    "x-app-version": "9.68.1",
                    "origin": "https://my.irancell.ir",
                    "referer": "https://my.irancell.ir/sessions/add"
                }
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            return None

        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: '{CONFIG_FILE}' is not valid JSON.")
            return None

    def save_config_disk(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config file: {e}")

    # ---------------- HISTORY ----------------
    def load_history(self):
        if not os.path.exists(self.csv_path):
            return

        print("Loading history from CSV...")
        count = 0
        try:
            with open(self.csv_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row and len(row) > 0:
                        self.history_set.add(row[0])
                        count += 1
        except Exception as e:
            print(f"Error reading history: {e}")
        print(f"Loaded {count} numbers to skip.")

    def save_buffer(self):
        if not self.buffer:
            return

        file_exists = os.path.isfile(self.csv_path)
        try:
            with open(self.csv_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Phone Number", "Status"])
                writer.writerows(self.buffer)
            print(f"--- Saved {len(self.buffer)} records to CSV (Total Attempts: {self.attempts}) ---")
            self.buffer = []
        except IOError as e:
            print(f"Error writing to file: {e}")

    # ---------------- NUMBER GENERATION ----------------
    def generate_number(self):
        while True:
            prefix = random.choice(PREFIXES)
            suffix = str(random.randint(0, 9999999)).zfill(7)
            number = prefix + suffix
            if number not in self.history_set:
                return number

    # ---------------- AUTH ----------------
    def login(self):
        print("🔐 401 received → logging in...")

        auth = self.config["auth"]

        payload = {
            "client_id": auth["client_id"],
            "client_secret": auth["client_secret"],
            "client_version": "9.68.1",
            "device_name": "Web Windows 10",
            "grant_type": "password",
            "installation_id": auth["installation_id"],
            "notifPermissionGranted": True,
            "phone_number": auth["phone_number"],
            "password": auth["password"]
        }

        headers = {
            "content-type": "application/json",
            "user-agent": self.session.headers.get("user-agent"),
            "x-app-version": "9.68.1",
            "origin": "https://my.irancell.ir",
            "referer": "https://my.irancell.ir/sessions/add",
            "accept-language": self.session.headers.get("accept-language", "fa")
        }

        resp = requests.post(
            "https://my.irancell.ir/api/authorization/v1/token",
            json=payload,
            headers=headers,
            timeout=10
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Login failed ({resp.status_code}): {resp.text}")

        data = resp.json()
        token = data["access_token"]
        bearer = f"{token}"

        # Update runtime headers
        self.session.headers["authorization"] = bearer

        # Persist to config
        self.config["headers"]["authorization"] = bearer
        self.save_config_disk()

        print("✅ Authorization refreshed successfully")


    # ---------------- REQUEST WRAPPER ----------------
    def post_with_auth_retry(self, url, payload):
        resp = self.session.post(url, json=payload, timeout=7)

        if resp.status_code == 401:
            self.login()
            resp = self.session.post(url, json=payload, timeout=7)

        return resp

    # ---------------- MAIN SCAN ----------------
    def run(self, max_attempts=1000):
        print(f"Starting scan (Dual-Step Mode)...")
        print(f"Check URL:  {self.url_check}")
        print(f"Notify URL: {self.url_notify}")

        try:
            while self.attempts < max_attempts:
                friend_number = self.generate_number()
                
                payload = {
                    "application_name": "NGMI",
                    "friend_number": friend_number,
                }

                # Generate UUID for this attempt
                correlation_id = uuid.uuid4().hex
                self.session.headers["X-Correlation-ID"] = correlation_id

                status_label = None
                should_save = False

                try:
                    # --- STEP 1: CHECK ELIGIBILITY ---
                    resp = self.post_with_auth_retry(self.url_check, payload)
                    self.attempts += 1

                    if resp.status_code == 200:
                        print(f"[{self.attempts}] CHECK {friend_number} -> Eligible (Sending Notify...)")
                        
                        # --- STEP 2: NOTIFY ---
                        resp_notify = self.post_with_auth_retry(self.url_notify, payload)
                        if resp_notify.status_code == 200:
                            status_label = "Success"
                            should_save = True
                            self.counters["Success"] += 1
                            print(f"[{self.attempts}] OK    {friend_number} -> 200 (SUCCESS)")
                            time.sleep(300)
                        else:
                            print(f"[{self.attempts}] ERROR {friend_number} -> Notify failed: {resp_notify.status_code}")
                            self.counters["Ignored/Error"] += 1

                    else:
                        try:
                            json_data = resp.json()
                        except:
                            json_data = {}

                        title = json_data.get("title", "")
                        details = json_data.get("details", "")

                        # Case 1: 5 Min Limit
                        if title == "you can refer one persion in 5 min":
                            print(f"[{self.attempts}] LIMIT {friend_number} -> 5 min wait... (Retry later)")
                            should_save = False
                            time.sleep(300)

                        # Case 2: Non-MTNI
                        elif details == "Non-MTNI referent":
                            status_label = "Non-MTNI"
                            should_save = True
                            self.counters["Non-MTNI"] += 1
                            print(f"[{self.attempts}] FAIL  {friend_number} -> Non-MTNI")

                        # Case 3: Ineligible
                        elif "The referent phone number is ineligible" in details or \
                             "The referral request has failed due to ineligibility" in title or \
                             "The referral request has failed due to ineligibility" in details:
                            status_label = "Ineligible"
                            should_save = True
                            self.counters["Ineligible"] += 1
                            print(f"[{self.attempts}] FAIL  {friend_number} -> Ineligible")

                        # Case 4: Invalid Referent
                        elif "Invalid referent" in title or "Invalid referent" in details:
                            status_label = "Invalid"
                            should_save = True
                            self.counters["Invalid"] += 1
                            print(f"[{self.attempts}] FAIL  {friend_number} -> Invalid Referent")

                        # Case 5: Other Errors
                        else:
                            self.counters["Ignored/Error"] += 1
                            print(f"[{self.attempts}] ERROR {friend_number} -> {resp.status_code} | {title or details} (Not saving)")
                            should_save = False

                except requests.RequestException as e:
                    self.attempts += 1
                    self.counters["Ignored/Error"] += 1
                    print(f"[{self.attempts}] ERROR {friend_number} -> Connection Failed (Not saving)")
                    should_save = False
                    time.sleep(2)

                if should_save and status_label:
                    self.history_set.add(friend_number)
                    self.buffer.append([friend_number, status_label])

                if self.attempts % 10 == 0:
                    self.save_buffer()

        except KeyboardInterrupt:
            print("\nStopping script (Ctrl+C)...")

        finally:
            print("Finalizing...")
            self.save_buffer()
            self.print_summary()

    def print_summary(self):
        print("\n=== Finished ===")
        print(f"Total Attempts: {self.attempts}")
        print(f"Success:        {self.counters['Success']}")
        print(f"Non-MTNI:       {self.counters['Non-MTNI']}")
        print(f"Ineligible:     {self.counters['Ineligible']}")
        print(f"Invalid:        {self.counters['Invalid']}")
        print(f"Errors/Ignored: {self.counters['Ignored/Error']}")
        print(f"File saved:     {self.csv_path}")


if __name__ == "__main__":
    scanner = IrancellScanner()
    scanner.run(max_attempts=10000)
