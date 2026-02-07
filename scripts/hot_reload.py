#!/usr/bin/env python3
import os, sys, requests
from read_config import get_env_config
def main():
    cfg = get_env_config()
    url = os.getenv("RELOAD_URL") or "http://localhost:8080/admin/reload"
    token = os.getenv("RELOAD_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.post(url, headers=headers, timeout=10)
    r.raise_for_status()
    print("✅ Reload triggered:", r.status_code)
if __name__ == "__main__":
    main()
