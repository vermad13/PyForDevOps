#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email the latest HTML report as an attachment (optional).

If SMTP secrets are not configured (or partially configured),
the script will SKIP emailing gracefully and exit 0,
so your pipeline does not fail just because email isn't enabled yet.

Expected secrets (set in GitHub Actions):
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
"""

import os
import sys
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from read_config import get_env_config


def latest_report(report_dir: Path) -> Path | None:
    files = sorted(report_dir.glob("model_report_*.html"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def get_smtp_config():
    """Return (host, port, user, password) or (None, None, None, None) if not ready."""
    host = os.getenv("SMTP_HOST")
    port_raw = os.getenv("SMTP_PORT")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    # Normalize empty strings to None
    host = host if host and host.strip() else None
    user = user if user and user.strip() else None
    password = password if password and password.strip() else None

    # Port parsing with safe fallback to 587
    if port_raw and port_raw.strip():
        try:
            port = int(port_raw.strip())
        except ValueError:
            print(f"⚠️  SMTP_PORT is not a valid integer: {port_raw!r}. Falling back to 587.")
            port = 587
    else:
        port = 587

    if not all([host, user, password]):
        return None, None, None, None
    return host, port, user, password


def main():
    cfg = get_env_config()
    env = os.getenv("APP_ENV", "dev")
    report_dir = Path(cfg.get("report_dir", "reports"))
    to_addr = cfg.get("report_email_to")
    from_addr = cfg.get("report_email_from", "no-reply@company.com")

    rpt = latest_report(report_dir)
    if not rpt:
        print("ℹ️  No report found to email. Skipping email step.")
        return  # exit 0

    # If recipient missing, skip silently (not configured yet)
    if not to_addr:
        print("ℹ️  report_email_to missing in env.yaml. Skipping email step.")
        return  # exit 0

    host, port, user, password = get_smtp_config()
    if not all([host, port, user, password]):
        print("ℹ️  SMTP credentials not fully configured. Skipping email step.")
        print("    Provide SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD as Actions secrets to enable emailing.")
        return  # exit 0

    # Compose message
    subject = f"[{env}] Model Report: {rpt.name}"
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject

    body = f"Attached: {rpt.name}\nEnvironment: {env}"
    msg.attach(MIMEText(body, "plain"))

    html = rpt.read_text(encoding="utf-8")
    msg.attach(MIMEText(html, "html"))

    # Send
    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        print(f"✅ Email sent to {to_addr}")
    except Exception as e:
        # Don't fail the pipeline for transient SMTP issues; print and exit 0
        print(f"⚠️  Email send failed: {e}. Not failing the job.")
        return  # exit 0


if __name__ == "__main__":
    main()
