import psutil
import GPUtil
import requests
import time
from datetime import datetime, timezone

WEBHOOK_URL = "http://localhost:8000/alert"

THRESHOLDS = {
    # in %
    "cpu": 90,
    "ram": 85,
    "disk": 95,
    "gpu": 90,
}

INTERVAL = 10  # check each 10 seconds


def check_and_alert():
    alerts = []

    # CPU
    cpu = psutil.cpu_percent(interval=1)
    if cpu > THRESHOLDS["cpu"]:
        alerts.append(
            f"CPU usage at {cpu}% on {get_hostname()} at {now()}. "
            f"Threshold exceeded: {THRESHOLDS['cpu']}%."
        )

    # RAM
    ram = psutil.virtual_memory()
    if ram.percent > THRESHOLDS["ram"]:
        alerts.append(
            f"RAM usage at {ram.percent}% on {get_hostname()} at {now()}. "
            f"Available: {mb(ram.available)}MB of {mb(ram.total)}MB."
        )

    # Disk
    disk = psutil.disk_usage("C:\\")
    if disk.percent > THRESHOLDS["disk"]:
        alerts.append(
            f"Disk usage at {disk.percent}% on C:\\ at {now()}. "
            f"Free: {gb(disk.free)}GB of {gb(disk.total)}GB."
        )

    # GPU
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            if gpu.load * 100 > THRESHOLDS["gpu"]:
                alerts.append(
                    f"GPU usage at {round(gpu.load * 100)}% on {get_hostname()} at {now()}. "
                    f"GPU: {gpu.name}. Temp: {gpu.temperature}C. "
                    f"Memory: {round(gpu.memoryUsed)}MB of {round(gpu.memoryTotal)}MB."
                )
    except Exception:
        pass  # no GPU or driver not available

    for alert in alerts:
        send_alert(alert)


def send_alert(alert: str):
    print(f"\n[ALERT] {alert}")
    try:
        response = requests.post(WEBHOOK_URL, json={"alert": alert})
        data = response.json()
        print(f"[AGENT] {data['conclusion'][:300]}...")
    except Exception as e:
        print(f"[ERROR] Could not reach webhook: {e}")


def get_hostname():
    import socket
    return socket.gethostname()

def now():
    return datetime.now(timezone.utc).strftime("%H:%M UTC")

def mb(bytes): return round(bytes / 1024 / 1024)
def gb(bytes): return round(bytes / 1024 / 1024 / 1024, 1)


if __name__ == "__main__":
    print(f"Monitoring started. Checking every {INTERVAL}s...")
    print(f"Thresholds: CPU>{THRESHOLDS['cpu']}% | RAM>{THRESHOLDS['ram']}% | Disk>{THRESHOLDS['disk']}% | GPU>{THRESHOLDS['gpu']}%\n")

    while True:
        check_and_alert()
        time.sleep(INTERVAL)