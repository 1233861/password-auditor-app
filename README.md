# Password Security Auditor

A command-line tool written in Python that audits password strength and
checks passwords against known data breaches — without ever exposing the
actual password over the network.

## Why this project

Weak and reused passwords are still one of the most common root causes of
account compromise. This tool demonstrates two real security practices:

1. **Entropy-based strength scoring** — instead of naive rules like "must
   contain a symbol," it estimates the actual bit-strength of a password
   based on character pool size and length.
2. **Privacy-preserving breach checking** — using the [Have I Been Pwned
   Pwned Passwords API](https://haveibeenpwned.com/API/v3#PwnedPasswords)
   via the **k-anonymity model**: only the first 5 characters of the
   password's SHA-1 hash are sent to the API. The full password, and even
   the full hash, never leave your machine. This is the same technique
   used by Chrome, Firefox, and 1Password to warn users about compromised
   credentials.

## Features

- Interactive mode with hidden password input (`getpass`)
- Single-password or bulk (file-based) auditing
- Strength scoring (0–4) with actionable feedback
- Breach exposure check with real breach counts
- JSON report export for record-keeping or integration into other tools
- Offline mode (`--no-breach-check`) if you don't want any network calls
- Zero external dependencies — pure Python standard library

## Setup

Requires Python 3.8+. No installation needed.

```bash
git clone <your-repo-url>
cd password-security-auditor
```

## Usage

**Interactive (recommended — password isn't shown or stored in shell history):**
```bash
python auditor.py
```

**Audit a single password directly:**
```bash
python auditor.py --password "correcthorsebatterystaple"
```

**Bulk audit from a file (one password per line) and save a JSON report:**
```bash
python auditor.py --file sample_passwords.txt --report report.json
```

**Offline mode (skip the breach-check API call):**
```bash
python auditor.py --password "test123" --no-breach-check
```

### Example output

```
=== Audit: input password ===
Length:        8
Character mix: lower
Entropy:       0.0 bits
Strength:      Very Weak (0/4)
Breach check:  FOUND in 9,545,824 known breaches — do not use!
Suggestions:
  - Use at least 12 characters.
  - Add uppercase letters.
  - Add numbers.
  - Add symbols (e.g. !@#$%).
  - This is a well-known common password. Avoid it entirely.
```

## Running tests

```bash
python -m unittest test_auditor.py -v
```

## How the k-anonymity breach check works

1. Hash the password locally with SHA-1.
2. Send only the **first 5 hex characters** of the hash to the API.
3. The API returns every known breached hash suffix sharing that prefix
   (usually several hundred).
4. Locally, check if your password's full hash suffix is in that list.

This means the API never sees your actual password or even your full
hash — it's mathematically impossible to reverse-engineer the password
from a 5-character prefix shared by hundreds of other hashes.

## Possible extensions

- Add a `--generate` flag to suggest a strong random password
- Add support for checking passwords against a custom breach wordlist
  (for fully offline/air-gapped environments)
- Wrap this in a small Flask API or web UI
- Add rate-limit handling / retries for large bulk audits

## Resume bullet point examples

- *Built a Python CLI tool that audits password strength using
  entropy-based scoring and checks breach exposure via the HIBP API's
  k-anonymity model, ensuring zero sensitive data transmission.*
- *Implemented a privacy-preserving credential-checking pipeline
  processing bulk password lists with JSON reporting, covered by a
  unit test suite.*

## Disclaimer

This is an educational/portfolio project. Never enter real, currently-in-use
passwords for accounts you care about into any third-party tool — including
this one — unless you've read and trust the code. Feel free to test with the
included `sample_passwords.txt`.
