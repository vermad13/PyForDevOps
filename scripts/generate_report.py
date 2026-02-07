#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate an HTML report summarizing the current model version and basic metrics,
and save it under reports/model_report_<timestamp>.html.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
from read_config import get_env_config

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Model Report - {{ timestamp }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 1.5rem; }
    h1 { margin-bottom: 0.2rem; }
    .meta { color: #666; margin-bottom: 1rem; }
    pre { background: #f6f8fa; padding: 1rem; border-radius: 6px; }
    img { max-width: 640px; border: 1px solid #ddd; }
  </style>
</head>
<body>
  <h1>Model Report</h1>
  <div class="meta">Environment: <b>{{ env }}</b> | Generated at: <b>{{ timestamp }}</b></div>

  <h2>Current Model</h2>
  <pre>{{ model_info | tojson(indent=2) }}</pre>

  <h2>Daily Count (Example Chart)</h2>
  <p>This chart is a placeholder to show chart embedding. Replace with real KPI.</p>
  <img src="data:image/png;base64,{{ chart_b64 }}" alt="chart" />

  <h2>Notes</h2>
  <ul>
    <li>Replace the dummy data with your real evaluation metrics.</li>
    <li>Attach additional artifacts as needed.</li>
  </ul>
</body>
</html>
"""

def render_chart_b64():
    # Dummy chart (replace with your metrics)
    days = pd.date_range(end=pd.Timestamp.today(), periods=7)
    values = [10, 13, 8, 12, 15, 14, 11]
    fig, ax = plt.subplots()
    ax.plot(days, values, marker="o")
    ax.set_title("Requests per Day (Dummy)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")

def main():
    cfg = get_env_config()
    env = os.getenv("APP_ENV", "dev")
    report_dir = Path(cfg.get("report_dir", "reports"))
    report_dir.mkdir(parents=True, exist_ok=True)

    smoketest_json = report_dir / "smoketest_summary.json"
    model_info = {}
    if smoketest_json.exists():
        model_info = json.loads(smoketest_json.read_text(encoding="utf-8"))

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    chart_b64 = render_chart_b64()
    html = Template(HTML_TEMPLATE).render(
        env=env,
        timestamp=f"{ts}Z",
        model_info=model_info,
        chart_b64=chart_b64
    )
    out_html = report_dir / f"model_report_{ts}.html"
    out_html.write_text(html, encoding="utf-8")
    print("✅ Report generated:", out_html)

if __name__ == "__main__":
    main()
