#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess  #used to run external commands (here, ps -ef)
import sys
from read_config import get_env_config

def main():
    cfg = get_env_config()
    process_name = str(cfg.get("service_name", "python"))

    result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)   #executes the Unix command ps -ef, which prints all running processes with details
    if process_name in result.stdout:
        print(f"✅ Process '{process_name}' is running")
    else:
        print(f"❌ Process '{process_name}' NOT running")
        sys.exit(1)

if __name__ == "__main__":
    main()
