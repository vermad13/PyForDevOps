#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
from read_config import get_env_config

def main():
    cfg = get_env_config()
    port = int(cfg.get("app_port", 8080))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", port))

    if result == 0:
        print(f"❌ Port {port} is already in use")
        sys.exit(1)
    else:
        print(f"✅ Port {port} is free")

if __name__ == "__main__":
    main()
