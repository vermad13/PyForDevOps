#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic smoke test after model refresh:
- Verifies the 'current' symlink exists (even if it's a symlink) and resolves to a real file.
- Writes a simple JSON summary to the reports directory.

Exit codes:
  0 → success
  2 → missing/dangling symlink or target not a file
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

from read_config import get_env_config


def main() -> None:
    cfg = get_env_config()

    current_link = Path(cfg.get("model_current_symlink", "artifacts/current_model.pkl"))
    report_dir = Path(cfg.get("report_dir", "reports"))
    report_dir.mkdir(parents=True, exist_ok=True)

    # Detect presence of symlink or file (lexists handles dangling symlink)
    if not os.path.lexists(current_link):
        print("❌ Current model symlink not found:", current_link)
        sys.exit(2)

    # Resolve target; strict=True raises if dangling
    try:
        model_target = current_link.resolve(strict=True)
    except FileNotFoundError:
        print("❌ Current model symlink is dangling (target missing):", current_link)
        sys.exit(2)

    if not model_target.is_file():
        print("❌ Resolved model target is not a regular file:", model_target)
        sys.exit(2)

    summary = {
        "env": os.getenv("APP_ENV", "dev"),
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "symlink": str(current_link),
        "model_file": str(model_target),
        "file_size_bytes": model_target.stat().st_size,
        "smoketest": "ok"
    }

    out_json = report_dir / "smoketest_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("✅ Smoke test summary written:", out_json)


if __name__ == "__main__":
    main()
