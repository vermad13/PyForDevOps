
import psutil
import platform
from datetime import datetime

def get_system_health():
    data = {
        "timestamp": datetime.now().isoformat(),
        "os": platform.platform(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return data

if __name__ == "__main__":
    health = get_system_health()
    print("=== SYSTEM HEALTH REPORT ===")
    for key, value in health.items():
        print(f"{key}: {value}")
