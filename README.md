# MTN Irancell Referral Scanner

A Python-based automation script for testing the MTN Irancell **Refer-a-Friend** flow by checking referral eligibility and, when eligible, sending the corresponding notify request.

> [!WARNING]
> This project interacts with real telecom APIs. Use it responsibly, comply with applicable laws and platform terms, and only operate with accounts and data you are authorized to use.

## Overview

This project provides a scanner that:

- Generates candidate mobile numbers from predefined Irancell prefixes.
- Sends a **check** request to the referral endpoint.
- If eligible, sends a **notify** request.
- Handles `401` responses by re-authenticating automatically.
- Stores processed numbers and statuses in CSV to avoid duplicate checks.
- Prints live counters and a final execution summary.

## Repository Structure

```text
.
├── main.py              # Main scanner implementation
├── config.json          # Runtime configuration (auth + headers + endpoints)
├── data/
│   └── results.csv      # Persisted scan results/history
└── debug/
    ├── login.py         # Helper script to test login/token flow
    └── test2.py         # Helper script for direct endpoint testing
```

## Requirements

- Python 3.9+
- `requests`

Install dependency:

```bash
pip install requests
```

## Configuration

The scanner reads configuration from `config.json`.

### Quick start

1. Ensure `config.json` exists.
   - If the file is missing, running `main.py` once will generate a default template.
2. Fill in all values in `auth` and `headers`.
3. Confirm API endpoints:
   - `url` → eligibility check endpoint
   - `notify_url` → referral notify endpoint

### Expected config shape

```json
{
  "url": "https://my.irancell.ir/api/gift/v1/refer_a_friend",
  "notify_url": "https://my.irancell.ir/api/gift/v1/refer_a_friend/notify",
  "auth": {
    "client_id": "...",
    "client_secret": "...",
    "phone_number": "989XXXXXXXXX",
    "password": "...",
    "installation_id": "..."
  },
  "headers": {
    "authorization": "Bearer_or_raw_token",
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0",
    "x-app-version": "9.68.1",
    "origin": "https://my.irancell.ir",
    "referer": "https://my.irancell.ir/sessions/add"
  }
}
```

> [!TIP]
> On successful re-login, the script updates the authorization value in `config.json` automatically.

## Usage

Run the scanner:

```bash
python main.py
```

By default, the script starts `IrancellScanner` and runs with:

- `max_attempts=10000`
- periodic CSV flush every 10 attempts
- cooldown waits in specific API states (for example, a 5-minute limit response)

To customize attempts, edit the final line in `main.py`.

## Output & Data Persistence

Results are appended to:

- `data/results.csv`

CSV columns:

- `Phone Number`
- `Status`

Status values currently used:

- `Success`
- `Non-MTNI`
- `Ineligible`
- `Invalid`

Numbers recorded in CSV are loaded at startup and skipped in future runs.

## Runtime Behavior

The scanner tracks these counters:

- Success
- Non-MTNI
- Ineligible
- Invalid
- Ignored/Error

At shutdown (normal or Ctrl+C), buffered rows are saved and a summary is printed.

## Troubleshooting

- **`401` Unauthorized repeatedly**
  - Verify `auth` credentials and client details in `config.json`.
  - Check whether account/session policies changed.

- **No rows written to CSV**
  - Ensure responses are mapped to one of the savable statuses.
  - Confirm the process has write permission to `data/`.

- **Frequent connection errors**
  - Check network stability.
  - Increase request timeouts in `main.py` if needed.

## Security Notes

- Do **not** commit real credentials, tokens, cookies, or phone/password combinations.
- Rotate any secrets that may have been exposed.
- Prefer environment-based secret injection for production-like workflows.

## Disclaimer

This repository is provided for educational and controlled testing purposes. You are solely responsible for lawful and compliant use.
