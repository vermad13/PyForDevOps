#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reads YAML config and prints selected environment values.
Used to validate CI configuration before deployment.
"""

import os
import sys

try:
    import yaml
except Exception as e:
    print("Failed to import PyYAML. Did pip install run?")
    print(e)
    sys.exit(1)

ENV = os.getenv("APP_ENV", "dev")  # dev|prod
CONFIG_PATH = os.getenv("CONFIG_PATH", "configs/env.yaml")

def main():
    # Ensure file exists
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Config not found at: {CONFIG_PATH}")
        sys.exit(2)

    # Read YAML safely
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        try:
            cfg = yaml.safe_load(f)
        except yaml.YAMLError as ye:
            print("❌ YAML parse error:")
            print(ye)
            sys.exit(3)

    if ENV not in cfg:
        print(f"❌ Environment '{ENV}' missing in {CONFIG_PATH}. Available: {list(cfg.keys())}")
        sys.exit(4)

    print(f"✅ Active env: {ENV}")
    print(cfg[ENV])

if __name__ == "__main__":
    main()
