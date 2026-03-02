#!/usr/bin/env python3
"""
Claw Message Watcher – Telegram mesajlarını izler, cevap verir.
Her 10 dakikada bir çalışır (cron ile).
- Kullanıcı mesajını kontrol eder
- Eğer Claw'ın cevabı yoksa → mesajı işler ve cevap atar
- Komutları destekler (/start, /agents, /status, /help)
"""

import os, requests, json, datetime, subprocess

# Telegram config
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8786643587:AAFpV6Kri5GJNZe5mFW36gyb705CLr_1ZTk")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1103470495")
OFFSET_FILE = "/home/openclaw/.openclaw/workspace/claw_watcher_offset.txt"

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
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 2, "limit": 50}  # Çok kısa timeout, az limit
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 409:
            # Conflict – another long poll active. advance offset to skip conflicting updates
            print(f"[WARN] 409 Conflict – advancing offset to avoid stuck")
            # Diğer session'ın aldığı mesajları atlamak için offset'i birkaç birim ilerlet
            new_offset = offset + 1
            save_offset(new_offset)
            return None
        else:
            print(f"[ERROR] getUpdates failed: {r.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] getUpdates exception: {e}")
        return None

def send_message(text, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"[ERROR] Send message failed: {e}")
        return False

def process_message(message):
    """Kullanıcı mesajını işle."""
    text = message.get("text", "")
    user = message.get("from", {}).get("first_name", "Kullanıcı")
    msg_id = message.get("message_id")
    
    print(f"[INFO] Mesaj işleniyor: {text[:50]}")
    
    # Komutları işle
    if text.startswith("/"):
        response = handle_command(text, user)
    else:
        # Normal mesaj – Cooder'a yönlendir?
        keywords = ['cooder', 'dashboard', 'rapor', 'html', 'css', 'tasarım', 'oluştur', 'şablon', 'login', 'design', 'web', 'gui']
        if any(k in text.lower() for k in keywords):
            response = route_to_cooder(text)
        else:
            response = f"✅ Mesajınız aldım, {user}\n\nŞu anda çalışıyorum. Eğer bir iş emrettiyseniz, hemen yapacağım. Komutları görmek için /help yazabilirsiniz."
    
    # Cevap gönder
    if send_message(response):
        print(f"[INFO] Cevap gönderildi: {msg_id}")
    else:
        print(f"[ERROR] Cevap gönderilemedi: {msg_id}")

def route_to_cooder(task_text):
    """Mesajı Cooder'a yönlendir ve sonucu döndür."""
    try:
        clean_task = task_text.strip()
        # Cooder agent'ını çalıştır (sessions_spawn)
        result = subprocess.run(
            ["openclaw", "sessions", "spawn", "--agent", "cooder-agent", "--mode", "run", "--task", clean_task],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            # JSON formatına çevirmeye çalış
            try:
                resp = json.loads(output)
                if resp.get("url"):
                    return f"✅ Cooder tasarımını oluşturdu:\n\n🌐 {resp['url']}\n\n📄 HTML önizleme (ilk 500 karakter):\n<pre>{resp.get('html', '')[:500]}</pre>"
                else:
                    return f"✅ Cooder yanıtı:\n<pre>{output[:2000]}</pre>"
            except json.JSONDecodeError:
                return f"✅ Cooder yanıtı:\n<pre>{output[:2000]}</pre>"
        else:
            return f"❌ Cooder çalıştırılırken hata: {result.stderr[:500]}"
    except Exception as e:
        return f"❌ Cooder yönlendirme hatası: {e}"

def handle_command(cmd, user):
    cmd = cmd.lower().strip()
    
    if cmd == "/start":
        return f"🛡️ Merhaba {user}! Ben Claw, OpenClaw asistanınızım.\n\n<b>Aktif Agent'lar:</b>\n• 🛡️ Security Agent – Güvenlik\n• 👨🏾‍💻 Cooder – Developer/Designer\n\nKomutlar:\n/agents – Agent listesi\n/status – Sistem durumu\n/help – Yardım"
    
    elif cmd == "/agents":
        try:
            result = subprocess.run(["openclaw", "agents", "list", "--all"], capture_output=True, text=True, timeout=10)
            agents = result.stdout.strip()
            if not agents:
                agents = "Hiç agent yok veya hata oluştu."
            return f"<b>Agent Listesi:</b>\n<pre>{agents}</pre>"
        except Exception as e:
            return f"❌ Agent listesi alınamadı: {e}"
    
    elif cmd == "/status":
        try:
            gw = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True, timeout=5)
            agents = subprocess.run(["openclaw", "agents", "list"], capture_output=True, text=True, timeout=5)
            return f"<b>Gateway Durumu:</b>\n<pre>{gw.stdout}</pre>\n<b>Agents:</b>\n<pre>{agents.stdout}</pre>"
        except Exception as e:
            return f"❌ Status alınamadı: {e}"
    
    elif cmd == "/heartbeat":
        # Heartbeat kontrol
        try:
            log = subprocess.run(["tail", "-20", "/home/openclaw/.openclaw/workspace/logs/claw_heartbeat.log"], capture_output=True, text=True)
            return f"<b>Heartbeat son logları:</b>\n<pre>{log.stdout[-1000:]}</pre>"
        except:
            return "❌ Heartbeat log okunamadı."
    
    elif cmd == "/logs":
        # Genel loglar
        try:
            log = subprocess.run(["tail", "-30", "/home/openclaw/.openclaw/workspace/logs/claw_message_watcher.log"], capture_output=True, text=True)
            return f"<b>Message Watcher log:</b>\n<pre>{log.stdout[-1500:]}</pre>"
        except:
            return "❌ Log okunamadı."
    
    elif cmd == "/help":
        return """<b>Komutlar:</b>
/start – Başlangıç mesajı
/agents – Tüm agent'ları listele
/status – Gateway ve agent durumları
/heartbeat – Heartbeat script logları
/logs – Message watcher logları
/help – Bu yardım mesajı

Herhangi bir mesajınız anlık olarak işlenir."""
    
    else:
        return f"❓ Bilinmeyen komut: {cmd}. /help yazın."

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Claw Message Watcher çalışıyor...")
    offset = load_offset()

    data = get_updates(offset)
    if not data or not data.get("ok"):
        print(f"[{now}] getUpdates başarısız, çıkıyorum.")
        return

    results = data.get("result", [])
    if not results:
        print(f"[{now}] Yeni güncelleme yok.")
        return

    # Sadece bizim chat_id için mesajları filtrele
    my_chats = []
    for update in results:
        msg = update.get("message", {})
        if not msg or msg.get("chat", {}).get("id") != int(CHAT_ID):
            continue
        my_chats.append((update["update_id"], msg))

    if not my_chats:
        print(f"[{now}] Bizim chat için mesaj yok.")
        return

    # Update_id'ye göre sırala (artan)
    my_chats.sort(key=lambda x: x[0])
    # Sadece işlenmemiş mesajları al (offset'ten büyük olanlar)
    unprocessed = [(uid, m) for uid, m in my_chats if uid > offset]

    if not unprocessed:
        print(f"[{now}] İşlenmemiş mesaj yok. Offset={offset}, son mesaj ID={my_chats[-1][0]}")
        return

    print(f"[{now}] {len(unprocessed)} işlenmemiş mesaj bulundu.")
    for update_id, message in unprocessed:
        print(f"[{now}] → İşleniyor: update_id={update_id}, text={message.get('text','')[:50]}")
        process_message(message)
        save_offset(update_id)  # her mesaj sonrası offset güncelle

    print(f"[{now}] İşlem tamamlandı. Yeni offset={offset}")
        save_offset(last_update_id)
    else:
        print(f"[{now}] ℹ️ Mesaj zaten işlenmiş (offset={offset}, msg_id={last_update_id})")
    
    print(f"[{now}] İşlem tamamlandı.")

if __name__ == "__main__":
    main()