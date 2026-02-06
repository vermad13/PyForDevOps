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
