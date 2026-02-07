#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

def run(step, cmd):
    print(f"\n=== {step} ===")
    subprocess.run(cmd, shell=True, check=True)

def main():
    try:
        run("Refresh model", "python scripts/model_refresh.py")
        run("Smoke test",    "python scripts/model_smoketest.py")
        run("Generate report","python scripts/generate_report.py")
        run("Email report",  "python scripts/email_report.py")
        print("\n✅ Maintenance completed")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Maintenance failed at: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
