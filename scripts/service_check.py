#!/usr/bin/env python3
import subprocess
import sys

PROCESS_NAME = "python"  # example

result = subprocess.run(
    ["ps", "-ef"],
    capture_output=True,
    text=True
)

if PROCESS_NAME in result.stdout:
    print(f"✅ Process '{PROCESS_NAME}' is running")
else:
    print(f"❌ Process '{PROCESS_NAME}' NOT running")
    sys.exit(1)
  
