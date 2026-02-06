#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Send a simple alert to Slack or Teams using an incoming webhook.

Environment variables:
- ALERT_WEBHOOK_URL (required)
- ALERT_FORMAT = "slack" | "teams" (default: slack)
- ALERT_TEXT (fallback text)
- APP_ENV (for context)
"""

import os
import sys
import json
import requests

def send_slack(url: str, text: str):
    payload = {"text": text}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

def send_teams(url: str, text: str):
    # Teams expects a card or simple text in "text" field
    payload = {"text": text}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

def main():
    url = os.getenv("ALERT_WEBHOOK_URL")
    fmt = os.getenv("ALERT_FORMAT", "slack").lower()
    env = os.getenv("APP_ENV", "dev")
    text = os.getenv("ALERT_TEXT", f"🚨 PyForDevOps: pipeline failed for env={env}")

    if not url:
        print("ALERT_WEBHOOK_URL is not set; skipping notification.")
        return

    try:
        if fmt == "teams":
            send_teams(url, text)
        else:
            send_slack(url, text)
        print("✅ Alert sent")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
