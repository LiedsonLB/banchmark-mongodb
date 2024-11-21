import time

LOG_FILE = "benchmark_log.txt"

def log_action(action, message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {message}\n")
