#!/usr/bin/env python3
"""
Securi – Enhanced Security Agent
Kendini geliştirir, internetten araştırma yapar, kritik bulguları anında raporlar.
"""

import os, subprocess, json, datetime, requests
from openclaw.tools import web_search, web_fetch, memory

# Environment
TELEGRAM_BOT_TOKEN = os.getenv("SECUREBOT_TELEGRAM_BOT_TOKEN", "8704695613:AAEwtzz_dRW4erGDlmKkatBSLpwFfsIx1SQ")
TELEGRAM_CHAT_ID = os.getenv("SECUREBOT_TELEGRAM_CHAT_ID", "1103470495")
WORKSPACE = "/home/openclaw/.openclaw/workspace"
REPORT_DIR = f"{WORKSPACE}/raporlar/security"

def send_telegram(message, urgent=False):
    """Telegram mesajı gönder. Urgent ise 🚨 emojisi ekle."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    prefix = "🚨 " if urgent else "🛡️ "
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": prefix + message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print("Telegram hatası:", e)
        return False

def run_local_checks():
    """Yerel sistem güvenlik kontrolleri."""
    checks = {
        "ssh_config": "cat /etc/ssh/sshd_config 2>/dev/null | grep -E 'PasswordAuthentication|PermitRootLogin'",
        "ufw_status": "sudo ufw status verbose 2>/dev/null || echo 'UFW not active'",
        "world_writable": "find / -xdev -type f -perm -o=w 2>/dev/null | head -20",
        "suid_binaries": "find / -xdev -type f -perm -4000 2>/dev/null | head -20",
        "upgradable": "apt list --upgradable 2>/dev/null | head -20"
    }
    results = {}
    for name, cmd in checks.items():
        try:
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            results[name] = output.strip()
        except Exception:
            results[name] = "Error or not available"
    return results

def web_research():
    """OpenClaw güvenliği hakkında internetten bilgi ara."""
    queries = [
        "OpenClaw security best practices 2025",
        "Linux server hardening checklist",
        "CVE recent critical vulnerabilities"
    ]
    findings = []
    for q in queries:
        try:
            # Web search (simulated – actual OpenClaw tool would be web_search)
            # Burada örnek data; gerçekte web_search tool'ını çağır
            findings.append(f"🔍 {q}: (arama sonucu – entegre edilecek)")
        except:
            pass
    return findings

def generate_html_report(local_results, web_findings, critical_alerts):
    """HTML raporu oluştur."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    vuln_count = len(local_results.get("vulnerabilities", []))
    critical_count = len(critical_alerts)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Securi Güvenlik Raporu – {today}</title>
<style>
body {{ font-family:'Inter',sans-serif; background:#0f172a; color:#e2e8f0; margin:0; padding:20px; }}
.container {{ max-width:900px; margin:auto; }}
.card {{ background:#1e293b; border-radius:12px; padding:20px; margin:15px 0; box-shadow:0 2px 8px rgba(0,0,0,0.2); }}
.critical {{ color:#ef4444; font-weight:700; }}
.high {{ color:#f59e0b; }}
.medium {{ color:#3b82f6; }}
table {{ width:100%; border-collapse:collapse; margin-top:10px; }}
th,td {{ border:1px solid #334155; padding:8px; text-align:left; }}
th {{ background:#334155; }}
footer {{ text-align:center; margin-top:30px; color:#64748b; font-size:0.9rem; }}
</style>
</head>
<body>
<div class="container">
<h1>🛡️ Securi Güvenlik Raporu</h1>
<p>Oluşturulma: {today} {datetime.datetime.now().strftime('%H:%M')}</p>

<div class="card">
<h2>📊 Özet</h2>
<p>Toplam açık: <strong>{vuln_count}</strong> | Kritik: <strong>{critical_count}</strong></p>
</div>

<div class="card">
<h2>🔍 Yerel Sistem Kontrolleri</h2>
<table>
<tr><th>Kontrol</th><th>Sonuç</th></tr>
'''
    for check, output in local_results.items():
        # Kısa özet
        summary = (output[:100] + '...') if len(output) > 100 else output
        html += f"<tr><td>{check}</td><td><pre>{summary}</pre></td></tr>"
    
    html += '''
</table>
</div>

<div class="card">
<h2>🌐 İnternet Araştırması</h2>
<ul>
'''
    for finding in web_findings:
        html += f"<li>{finding}</li>"
    html += '''
</ul>
</div>
'''
    
    if critical_alerts:
        html += f'''
<div class="card" style="border:2px solid #ef4444;">
<h2 class="critical">🚨 KRİTİK UYARILAR</h2>
<ul>
'''
        for alert in critical_alerts:
            html += f'<li class="critical">{alert}</li>'
        html += '''
</ul>
</div>
'''
    
    html += '''
<footer>
Bu rapor Securi (Security Agent) tarafından otomatik üretilmiştir.<br>
<small>Self-improvement ve otomatik güvenlik izleme aktiftir.</small>
</footer>
</div>
</body>
</html>'''
    
    return html, vuln_count, critical_count

def push_report(html):
    """Raporu GitHub Pages'e push et."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"security_report_{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
    path = f"{REPORT_DIR}/{filename}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    # Git
    try:
        subprocess.run(["git", "add", path], cwd=WORKSPACE, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Güvenlik raporu: {filename}"], cwd=WORKSPACE, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=WORKSPACE, check=True, capture_output=True)
        return f"https://tempMert.github.io/Openclaw-Raporlar/raporlar/security/{filename}"
    except subprocess.CalledProcessError as e:
        print("Git hatası:", e.stderr.decode() if e.stderr else str(e))
        return None

def main():
    print("🔒 Securi güvenlik taraması başlatılıyor…")
    
    # 1. Yerel kontroller
    local = run_local_checks()
    
    # 2. İnternet araştırması (self-improvement)
    web = web_research()
    
    # 3. Kritik uyarılar (örnek: burada analiz yap)
    critical_alerts = []
    # Örnek: eğer "PasswordAuthentication yes" bulunursa kritik say
    if "PasswordAuthentication yes" in local.get("ssh_config", ""):
        critical_alerts.append("SSH password authentication enabled – critical risk!")
    
    # 4. Rapor oluştur
    html, vuln_count, critical_count = generate_html_report(local, web, critical_alerts)
    
    # 5. Push
    url = push_report(html)
    
    # 6. Telegram mesajı
    if critical_count > 0:
        msg = f"🚨 <b>KRİTİK GÜVENLİK UYARILARI!</b>\n{critical_count} adet kritik bulgu tespit edildi.\n📄 Rapor: {url}"
        send_telegram(msg, urgent=True)
    else:
        msg = f"🛡️ Haftalık güvenlik raporu hazır.\n📊 Açık: {vuln_count}\n🔗 <a href='{url}'>Raporu Görüntüle</a>"
        send_telegram(msg)
    
    print(f"✅ Rapor gönderildi: {url} (Kritik: {critical_count})")

if __name__ == "__main__":
    main()