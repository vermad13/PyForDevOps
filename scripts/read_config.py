#!/usr/bin/env python3
"""
Reads YAML config and prints selected environment values.
Used to validate CI configuration before deployment.
"""
import os
import yaml

ENV = os.getenv("APP_ENV", "dev")  # dev|prod

with open("devops-python/configs/env.yaml") as f:
    cfg = yaml.safe_load(f)

print(f"Active env: {ENV}")
print(cfg[ENV])
``
