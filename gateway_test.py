#!/usr/bin/env python3
"""
Gateway Health Test
Runs every 3 days at 05:00. Checks if OpenClaw gateway/CLI is responsive.
"""

import subprocess
import time
import os
import sys

LOG = "/home/openclaw/.openclaw/workspace/gateway_test.log"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "1103470495"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M")
    with open(LOG, "a") as f:
        f.write(f"{ts} - {msg}\n")

def is_gateway_up():
    """Check if any openclaw process is running."""
    try:
        out = subprocess.check_output(["pgrep", "-f", "openclaw"], timeout=5).decode()
        pids = out.strip().splitlines()
        return len(pids) > 0
    except subprocess.CalledProcessError:
        # No process found
        return False
    except Exception as e:
        log(f"Gateway check error: {e}")
        return False

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        subprocess.run(["curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                       "-d", f"chat_id={TELEGRAM_CHAT_ID}", "-d", f"text={msg}"], timeout=15, check=False)
    except Exception as e:
        log(f"Telegram send error: {e}")

def main():
    up = is_gateway_up()
    status = "UP" if up else "DOWN"
    log(f"Gateway status: {status}")
    if not up:
        alert = f"🚨 OpenClaw Gateway DOWN\nTime: {time.strftime('%Y-%m-%d %H:%M')}\nCheck logs: {LOG}"
        log(alert)
        send_telegram(alert)
    print(f"Gateway: {status}")

if __name__ == "__main__":
    main()
