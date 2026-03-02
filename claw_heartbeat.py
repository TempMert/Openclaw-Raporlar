#!/usr/bin/env python3
"""
Claw Heartbeat – Gateway restart sonrası Telegram mesajlarını kontrol et.
"""

import os, requests, json, time

# Telegram credentials (ana kanal)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8786643587:AAFpV6Kri5GJNZe5mFW36gyb705CLr_1ZTk")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1103470495")
OFFSET_FILE = "/home/openclaw/.openclaw/workspace/claw_heartbeat_offset.txt"

def load_offset():
    try:
        with open(OFFSET_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_offset(offset):
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))

def get_updates(offset):
    """Telegram'dan bekleyen mesajları çek."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 10, "limit": 100}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"❌ Telegram getUpdates hatası: {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ getUpdates exception: {e}")
        return None

def send_ack(message):
    """Kullanıcıya 'mesaj alındı' bildirimi gönder."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"✅ Mesajınız aldım (heartbeat kontrol): {message[:50]}...",
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")
        return False

def main():
    print("🔍 Heartbeat: Telegram mesajları kontrol ediliyor...")
    offset = load_offset()
    data = get_updates(offset)
    
    if not data or not data.get("ok"):
        print("❌ getUpdates başarısız")
        return
    
    results = data.get("result", [])
    if not results:
        print("✅ Yeni mesaj yok")
        return
    
    print(f"📥 {len(results)} yeni mesaj bulundu")
    for update in results:
        update_id = update["update_id"]
        message = update.get("message", {})
        text = message.get("text", "")
        if text:
            print(f"   → Mesaj: {text[:50]}")
            # Mesaj işlendi bildirimi gönder
            send_ack(text)
        # Offset'ı güncelle (her mesaj için ayrı ayrı kaydet)
        save_offset(update_id)
    
    print("✅ Heartbeat tamamlandı")

if __name__ == "__main__":
    main()