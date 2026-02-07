#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil  #used for disk usage stats via shutil.disk_usage
import sys
from read_config import get_env_config

def main():
    cfg = get_env_config()
    threshold = float(cfg.get("disk_free_threshold", 20))

    total, used, free = shutil.disk_usage("/")     #It returns three numbers (all in bytes)
    free_percent = (free / total) * 100

    print(f"Total: {total/1e9:.2f} GB  Used: {used/1e9:.2f} GB  Free: {free/1e9:.2f} GB")
    print(f"Free disk space: {free_percent:.2f}% (threshold: {threshold}%)")

    # Optional log
    import os
    os.makedirs("logs", exist_ok=True)
    with open("logs/disk_check.log", "a", encoding="utf-8") as f:
        f.write(f"Free: {free_percent:.2f}%\n")

    if free_percent < threshold:
        print("⚠️  ALERT: Low disk space")
        sys.exit(2)

if __name__ == "__main__":
    main()
