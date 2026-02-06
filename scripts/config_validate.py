#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from read_config import get_env_config

REQUIRED_KEYS = ["app_port", "debug", "disk_free_threshold", "service_name"]

def main():
    cfg = get_env_config()
    missing = [k for k in REQUIRED_KEYS if k not in cfg]
    if missing:
        print(f"❌ Missing config keys: {missing}")
        sys.exit(1)
    print("✅ Config validation passed")

if __name__ == "__main__":
    main()
