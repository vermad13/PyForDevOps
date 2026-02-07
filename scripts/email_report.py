#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email the latest HTML report as an attachment.

Secrets (set in GitHub Actions secrets):
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

Config (env.yaml):
  report_dir, report_email_to, report_email_from
"""

import os
import sys
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from read_config import get_env_config

def latest_report(report_dir: Path) -> Path | None:
    files = sorted(report_dir.glob("model_report_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def main():
    cfg = get_env_config()
    env = os.getenv("APP_ENV", "dev")
    report_dir = Path(cfg.get("report_dir", "reports"))
    to_addr = cfg.get("report_email_to")
    from_addr = cfg.get("report_email_from", "no-reply@company.com")

    if not to_addr:
        print("❌ report_email_to missing in env.yaml")
        sys.exit(2)

    rpt = latest_report(report_dir)
    if not rpt:
        print("❌ No report found to email.")
        sys.exit(3)

    # Compose email
    subject = f"[{env}] Model Report: {rpt.name}"
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject

    body = f"Attached: {rpt.name}\nEnvironment: {env}"
    msg.attach(MIMEText(body, "plain"))

    html = rpt.read_text(encoding="utf-8")
    msg.attach(MIMEText(html, "html"))

    # Send via SMTP
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    if not all([host, port, user, password]):
        print("❌ SMTP credentials missing (SMTP_HOST/PORT/USER/PASSWORD).")
        sys.exit(4)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

    print(f"✅ Email sent to {to_addr}")

if __name__ == "__main__":
    main()
