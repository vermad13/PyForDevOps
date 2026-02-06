# PyForDevOps — Python Automation for DevOps Pre‑Deployment Gates

This repository showcases a **Python-driven pre‑deployment quality gate** built on **GitHub Actions**.  
Before any (simulated) deployment proceeds, multiple safety checks run as a **Prechecks** stage.  
Only if all gates pass does the **Deploy** stage run.

## 🎯 What this project demonstrates

- **System safety checks** (disk, port)
- **Configuration validation** (YAML)
- **Process health checks** (service presence via `ps -ef`)
- **Environment-driven behavior** (using `configs/env.yaml`)
- **CI orchestration** with `prechecks → deploy` and optional **rollback**

## 📁 Repository structure
.
├── .github/workflows/
│   └── devops-ci.yml        # CI pipeline: Prechecks → Deploy
├── configs/
│   └── env.yaml             # Environment configs (dev/prod)
├── scripts/
│   ├── config_validate.py   # Validates required keys in env config
│   ├── disk_check.py        # Fails if free disk < threshold
│   ├── port_guard.py        # Fails if a TCP port is already in use
│   ├── read_config.py       # Reads YAML config for given APP_ENV
│   ├── service_check.py     # Verifies a process exists (fallback approach)
│   ├── deploy.py            # (Simulated) deployment logic
│   └── rollback.py          # (Simulated) rollback logic
├── requirements.txt         # Python dependencies for CI runners
└── README.md

## 🔐 Prechecks (Quality Gates)

Each script exits **non‑zero** on failure, which stops the pipeline:

- `scripts/disk_check.py`  
  Uses `shutil.disk_usage("/")` to compute free space. Threshold is set via env var `DISK_FREE_THRESHOLD`.

- `scripts/port_guard.py`  
  Fails if a required TCP port (e.g., 8080) is already in use.

- `scripts/config_validate.py`  
  Confirms required keys exist in `configs/env.yaml` (e.g., `app_port`, `debug`).

- `scripts/read_config.py`  
  Loads the YAML config for `APP_ENV` (default `dev`). Helpful for verifying environment wiring.

- `scripts/service_check.py`  
  Searches the process list (`ps -ef`) for a given process name—useful when `systemctl` isn’t available (like CI runners).

## 🚦 CI/CD Flow (GitHub Actions)

The workflow `.github/workflows/devops-ci.yml` defines two jobs:

1. **`prechecks`** — Runs all safety gates.  
2. **`deploy`** — Runs **only if** prechecks pass (`needs: prechecks`). This is currently **simulated**.

> To test gating, temporarily set `DISK_FREE_THRESHOLD` to a high value (e.g., `"95"`) in the workflow.  
> The **Deploy** job should **not** run if prechecks fail.

## 🧪 How to run locally (optional)

If you want to test scripts locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run scripts
python scripts/disk_check.py
APP_ENV=dev python scripts/read_config.py
python scripts/config_validate.py
python scripts/port_guard.py
python scripts/service_check.py
