#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refresh model artifact from S3 (or local) and update a 'current' symlink.
If a new model is pulled, we print the version and exit 0.
If no update is needed, we print and exit 0 (idempotent).
On any fatal error, exit non-zero.

Requires:
  - boto3 (when model_source = s3)
  - env config in configs/env.yaml
  - APP_ENV & CONFIG_PATH exported by the workflow

Outputs:
  - artifacts/models/<model_filename>
  - artifacts/current_model.pkl (symlink to latest)
  - artifacts/.model_version (text)
"""

import os
import sys
import time
import json
from pathlib import Path
from read_config import get_env_config

def ensure_dirs(*paths):
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)

def write_model_version(version_file: Path, version: str):
    version_file.write_text(version, encoding="utf-8")

def read_model_version(version_file: Path) -> str | None:
    return version_file.read_text(encoding="utf-8").strip() if version_file.exists() else None

def set_symlink(target: Path, link: Path):
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(target)

def latest_s3_object(bucket, prefix):
    import boto3
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    latest = None
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".pkl"):  # filter model files
                if (latest is None) or (obj["LastModified"] > latest["LastModified"]):
                    latest = obj
    return latest  # dict with Key, LastModified, Size, etc.

def download_s3_object(bucket, key, dest_path: Path):
    import boto3
    s3 = boto3.client("s3")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, key, str(dest_path))

def main():
    cfg = get_env_config()
    model_source = cfg.get("model_source", "s3")
    model_dir = Path(cfg.get("model_local_dir", "artifacts/models"))
    current_link = Path(cfg.get("model_current_symlink", "artifacts/current_model.pkl"))
    version_file = Path("artifacts/.model_version")

    ensure_dirs(model_dir, current_link.parent, version_file.parent)

    prev_version = read_model_version(version_file)
    print(f"Previous version: {prev_version}")

    if model_source == "s3":
        bucket = cfg["model_s3_bucket"]
        prefix = cfg["model_s3_prefix"]
        latest = latest_s3_object(bucket, prefix)
        if not latest:
            print("❌ No model found in S3 prefix.")
            sys.exit(2)
        latest_key = latest["Key"]
        latest_version = latest_key.rsplit("/", 1)[-1]  # filename as version proxy
        if latest_version == prev_version:
            print("✅ Model already up-to-date.")
            return

        dest = model_dir / latest_version
        print(f"⬇️  Downloading s3://{bucket}/{latest_key} -> {dest}")
        download_s3_object(bucket, latest_key, dest)
        set_symlink(dest, current_link)
        write_model_version(version_file, latest_version)
        print(f"✅ Updated to version: {latest_version}")

    elif model_source == "local":
        # Expect a new file to appear under model_dir; pick the most recent
        files = sorted(model_dir.glob("*.pkl"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not files:
            print("❌ No local model files found in artifacts/models.")
            sys.exit(2)
        latest = files[0]
        latest_version = latest.name
        if latest_version == prev_version:
            print("✅ Model already up-to-date.")
            return
        set_symlink(latest, current_link)
        write_model_version(version_file, latest_version)
        print(f"✅ Updated to version: {latest_version}")

    else:
        print(f"❌ Unsupported model_source: {model_source}")
        sys.exit(3)

if __name__ == "__main__":
    main()
