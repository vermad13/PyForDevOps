#!/usr/bin/env python3
import socket
import sys

PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(("127.0.0.1", PORT))

if result == 0:
    print(f"❌ Port {PORT} is already in use")
    sys.exit(1)
else:
    print(f"✅ Port {PORT} is free")
  
