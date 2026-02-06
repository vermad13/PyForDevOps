#!/usr/bin/env python3
import yaml
import sys

REQUIRED_KEYS = ["app_port", "debug"]

with open("configs/env.yaml") as f:
    cfg = yaml.safe_load(f)

env = "dev"

missing = [k for k in REQUIRED_KEYS if k not in cfg[env]]

if missing:
    print(f"❌ Missing config keys: {missing}")
    sys.exit(1)

print("✅ Config validation passed")
