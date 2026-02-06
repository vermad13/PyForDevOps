#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper to read environment-scoped config from configs/env.yaml.

Usage from other scripts:
    from read_config import get_env_config
    cfg = get_env_config()          # uses APP_ENV or 'dev'
    port = cfg["app_port"]
"""

import os
import sys
import yaml
from typing import Dict, Any

DEFAULT_ENV = "dev"
DEFAULT_CONFIG_PATH = "configs/env.yaml"

def _load_config(config_path: str) -> Dict[str, Any]:
    if not os.path.exists(config_path):
        print(f"❌ Config not found: {config_path}", file=sys.stderr)
        sys.exit(2)
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError as ye:
            print("❌ YAML parse error:", file=sys.stderr)
            print(ye, file=sys.stderr)
            sys.exit(3)

def get_env_config(env: str | None = None, config_path: str | None = None) -> Dict[str, Any]:
    env = env or os.getenv("APP_ENV", DEFAULT_ENV)
    cfg_path = config_path or os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)
    all_cfg = _load_config(cfg_path)
    if env not in all_cfg:
        print(f"❌ Environment '{env}' not found in {cfg_path}. Available: {list(all_cfg.keys())}", file=sys.stderr)
        sys.exit(4)
    return all_cfg[env]

if __name__ == "__main__":
    # Debug print
    env = os.getenv("APP_ENV", DEFAULT_ENV)
    current = get_env_config(env)
    print(f"Active env: {env}")
    print(current)
