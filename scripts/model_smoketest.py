#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
After refresh/deploy, run a basic smoke test:
- Confirms current model exists
- Optionally calls a running API endpoint (if you expose one)
- Writes a small JSON summary for the report
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from read_config import get_env_config

def main():
    cfg = get_env_config()
    current_link = Path(cfg.get("model_current_symlink", "artifacts/current_model.pkl"))
    report_dir = Path(cfg.get("report_dir", "reports"))
    report_dir.mkdir(parents=True, exist_ok=True)

    if not current_link.exists():
        print("❌ Current model symlink not found.")
        sys.exit(2)

    model_target = current_link.resolve()
    summary = {
        "env": os.getenv("APP_ENV", "dev"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model_file": str(model_target),
        "file_size_bytes": model_target.stat().st_size if model_target.exists() else None,
        "smoketest": "ok"
    }

    out_json = report_dir / "smoketest_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("✅ Smoke test summary written:", out_json)

if __name__ == "__main__":
    main()
