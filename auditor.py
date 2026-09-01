#!/usr/bin/env python3
"""
Password Security Auditor
--------------------------
A command-line tool that audits password strength and checks whether a
password has appeared in known data breaches, without ever sending the
full password over the network.

How the breach check works (k-anonymity model, same approach used by
"Have I Been Pwned"):
  1. The password is hashed locally with SHA-1.
  2. Only the FIRST 5 CHARACTERS of the hash are sent to the API.
  3. The API returns all hash suffixes that share that 5-character prefix.
  4. The tool checks locally whether the full hash appears in that list.

This means the real password (and even its full hash) never leaves your
machine. This is the same privacy-preserving technique used by browsers
like Chrome and Firefox to warn you about compromised passwords.

Usage:
    python auditor.py                  # interactive prompt (hidden input)
    python auditor.py --password "x"   # audit a single password directly
    python auditor.py --file passwords.txt --report report.json
"""

import argparse
import getpass
import hashlib
import json
import math
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from typing import Optional


HIBP_API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
USER_AGENT = "PasswordSecurityAuditor/1.0 (educational-resume-project)"


# ---------------------------------------------------------------------------
# Strength analysis
# ---------------------------------------------------------------------------

@dataclass
class StrengthResult:
    length: int
    has_lower: bool
    has_upper: bool
    has_digit: bool
    has_symbol: bool
    entropy_bits: float
    score: int          # 0-4
    label: str           # Very Weak ... Very Strong
    feedback: list


COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123", "letmein",
    "monkey", "111111", "iloveyou", "admin", "welcome", "password1",
}


def analyze_strength(password: str) -> StrengthResult:
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    pool = 0
    if has_lower:
        pool += 26
    if has_upper:
        pool += 26
    if has_digit:
        pool += 10
    if has_symbol:
        pool += 32

    entropy_bits = length * math.log2(pool) if pool else 0.0

    feedback = []
    if length < 12:
        feedback.append("Use at least 12 characters.")
    if not has_upper:
        feedback.append("Add uppercase letters.")
    if not has_lower:
        feedback.append("Add lowercase letters.")
    if not has_digit:
        feedback.append("Add numbers.")
    if not has_symbol:
        feedback.append("Add symbols (e.g. !@#$%).")
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a well-known common password. Avoid it entirely.")
        entropy_bits = 0.0

    # Score 0-4 based on entropy bits
    if entropy_bits < 28:
        score, label = 0, "Very Weak"
    elif entropy_bits < 36:
        score, label = 1, "Weak"
    elif entropy_bits < 60:
        score, label = 2, "Reasonable"
    elif entropy_bits < 80:
        score, label = 3, "Strong"
    else:
        score, label = 4, "Very Strong"

    if not feedback:
        feedback.append("Looks good. No obvious weaknesses detected.")

    return StrengthResult(
        length=length,
        has_lower=has_lower,
        has_upper=has_upper,
        has_digit=has_digit,
        has_symbol=has_symbol,
        entropy_bits=round(entropy_bits, 1),
        score=score,
        label=label,
        feedback=feedback,
    )


# ---------------------------------------------------------------------------
# Breach check (HIBP k-anonymity API)
# ---------------------------------------------------------------------------

def check_breach(password: str, timeout: float = 8.0) -> Optional[int]:
    """
    Returns the number of times this password has been seen in known
    breaches, or None if the check could not be completed (e.g. offline).
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = HIBP_API_URL.format(prefix=prefix)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"[!] Could not reach breach database: {e}", file=sys.stderr)
        return None

    for line in body.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(label: str, strength: StrengthResult, breach_count: Optional[int]):
    print(f"\n=== Audit: {label} ===")
    print(f"Length:        {strength.length}")
    print(f"Character mix: "
          f"{'lower ' if strength.has_lower else ''}"
          f"{'upper ' if strength.has_upper else ''}"
          f"{'digit ' if strength.has_digit else ''}"
          f"{'symbol' if strength.has_symbol else ''}".strip() or "none")
    print(f"Entropy:       {strength.entropy_bits} bits")
    print(f"Strength:      {strength.label} ({strength.score}/4)")

    if breach_count is None:
        print("Breach check:  skipped (no network / API error)")
    elif breach_count == 0:
        print("Breach check:  Not found in known breaches")
    else:
        print(f"Breach check:  FOUND in {breach_count:,} known breaches — do not use!")

    print("Suggestions:")
    for tip in strength.feedback:
        print(f"  - {tip}")


def build_record(label: str, strength: StrengthResult, breach_count: Optional[int]) -> dict:
    record = {"label": label, "strength": asdict(strength), "breach_count": breach_count}
    return record


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Audit password strength and breach exposure.")
    parser.add_argument("--password", help="Password to audit (avoid in shared shells; prefer interactive mode).")
    parser.add_argument("--file", help="Path to a file with one password per line to audit in bulk.")
    parser.add_argument("--report", help="Optional path to write a JSON report of results.")
    parser.add_argument("--no-breach-check", action="store_true", help="Skip the online breach check (offline mode).")
    args = parser.parse_args()

    results = []

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
        for i, pw in enumerate(passwords, 1):
            label = f"password #{i}"
            strength = analyze_strength(pw)
            breach = None if args.no_breach_check else check_breach(pw)
            print_report(label, strength, breach)
            results.append(build_record(label, strength, breach))
            time.sleep(0.3)  # be polite to the API
    else:
        pw = args.password or getpass.getpass("Enter password to audit (hidden): ")
        strength = analyze_strength(pw)
        breach = None if args.no_breach_check else check_breach(pw)
        print_report("input password", strength, breach)
        results.append(build_record("input password", strength, breach))

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nReport written to {args.report}")


if __name__ == "__main__":
    main()
