#!/usr/bin/env python3
import os
import shutil
import sys

THRESHOLD = float(os.getenv("DISK_FREE_THRESHOLD", "20"))

def main():
    total, used, free = shutil.disk_usage("/")
    free_percent = (free / total) * 100
    print(f"Total: {total/1e9:.2f} GB  Used: {used/1e9:.2f} GB  Free: {free/1e9:.2f} GB")
    print(f"Free disk space: {free_percent:.2f}% (threshold: {THRESHOLD}%)")

    os.makedirs("logs", exist_ok=True)
    with open("logs/disk_check.log", "a") as f:
        f.write(f"Free: {free_percent:.2f}%\n")

    if free_percent < THRESHOLD:
        print("⚠️  ALERT: Low disk space")
        sys.exit(2)

if __name__ == "__main__":
    main()
