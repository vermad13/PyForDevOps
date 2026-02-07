#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refresh model artifact and update a stable 'current' symlink.

Behavior:
- Reads environment config via read_config.get_env_config()
- Supports two sources:
  * s3    → downloads the latest .pkl by LastModified from S3
  * local → picks the most recently modified .pkl in model_local_dir
- Updates an absolute symlink at 'model_current_symlink'
- Writes the selected version filename to 'artifacts/.model_version'

Exit codes:
  0 → success / already up-to-date
  2 → missing prerequisites (e.g., no local models, missing AWS env, no S3 objects)
  3 → unsupported model_source
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from read_config import get_env_config


def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def version_file_path() -> Path:
    return Path("artifacts/.model_version")


def read_model_version(vfile: Path) -> Optional[str]:
    return vfile.read_text(encoding="utf-8").strip() if vfile.exists() else None


def write_model_version(vfile: Path, version: str) -> None:
    vfile.write_text(version, encoding="utf-8")


def set_symlink(target: Path, link: Path) -> None:
    """
    Create/replace a symlink 'link' pointing to 'target'.
    Always use an absolute target path to avoid accidental dangling links.
    """
    target_abs = target.resolve()  # absolute path to actual file
    try:
        link.unlink()
    except FileNotFoundError:
        pass
    link.symlink_to(target_abs)


def latest_s3_object(bucket: str, prefix: str) -> Optional[Dict[str, Any]]:
    import boto3
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    latest = None
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".pkl"):
                if (latest is None) or (obj["LastModified"] > latest["LastModified"]):
                    latest = obj
    return latest


def download_s3_object(bucket: str, key: str, dest: Path) -> None:
    import boto3
    s3 = boto3.client("s3")
    dest.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, key, str(dest))


def main() -> None:
    cfg = get_env_config()

    model_source = cfg.get("model_source", "s3")
    model_dir = Path(cfg.get("model_local_dir", "artifacts/models"))
    current_link = Path(cfg.get("model_current_symlink", "artifacts/current_model.pkl"))
    vfile = version_file_path()

    ensure_dirs(model_dir, current_link.parent, vfile.parent)

    prev_version = read_model_version(vfile)
    print(f"Previous version: {prev_version}")

    if model_source == "s3":
        # Validate AWS env; fail clearly if not provided
        missing = [k for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION")
                   if not os.getenv(k)]
        if missing:
            print(f"❌ model_source=s3 but missing AWS env: {missing}. "
                  f"Either set these secrets or use model_source=local.")
            sys.exit(2)

        bucket = cfg["model_s3_bucket"]
        prefix = cfg["model_s3_prefix"]

        latest = latest_s3_object(bucket, prefix)
        if not latest:
            print("❌ No model objects (*.pkl) found in the specified S3 prefix.")
            sys.exit(2)

        latest_key = latest["Key"]
        latest_version = latest_key.rsplit("/", 1)[-1]

        if latest_version == prev_version:
            print("✅ Model already up-to-date.")
            return

        dest = model_dir / latest_version
        print(f"⬇️  Downloading s3://{bucket}/{latest_key} -> {dest}")
        download_s3_object(bucket, latest_key, dest)

        set_symlink(dest, current_link)
        write_model_version(vfile, latest_version)
        print(f"✅ Updated to version: {latest_version}")
        return

    elif model_source == "local":
        files = sorted(model_dir.glob("*.pkl"),
                       key=lambda p: p.stat().st_mtime,
                       reverse=True)
        if not files:
            print(f"❌ No local model files found in {model_dir}. "
                  f"Add at least one *.pkl and re-run.")
            sys.exit(2)

        latest = files[0]
        latest_version = latest.name

        if latest_version == prev_version:
            print("✅ Model already up-to-date.")
            return

        set_symlink(latest, current_link)
        write_model_version(vfile, latest_version)
        print(f"✅ Updated to version: {latest_version}")
        return

    else:
        print(f"❌ Unsupported model_source: {model_source}")
        sys.exit(3)


if __name__ == "__main__":
    main()
