#!/usr/bin/env python3
import os
import yaml

ENV = os.getenv("APP_ENV", "dev")  # dev|prod

with open("configs/env.yaml") as f:
    cfg = yaml.safe_load(f)

print(f"Active env: {ENV}")
print(cfg[ENV])
