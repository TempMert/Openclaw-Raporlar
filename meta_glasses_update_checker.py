#!/usr/bin/env python3
"""
Rayban Meta Gen1 Glasses – 2 haftada bir güncelleme kontrolü.
Meta resmi help sayfası, newsroom, Reddit, tech blogs.
"""

import requests, json, datetime, re, subprocess, os, hashlib, time
from datetime import datetime, timedelta

WORKSPACE = "/home/openclaw/.openclaw/workspace"
META_HELP_URL = "https://www.meta.com/help/ai-glasses/1809764829519902/"
STATE_FILE = f"{WORKSPACE}/meta_glasses_state.json"
REPORT_DIR = f"{WORKSPACE}/meta_glasses_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": None, "last_content_hash": None, "last_report": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_meta_help():
    try:
        r = requests.get(META_HELP_URL, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200:
            return r.text
        else:
            print(f"⚠️ Meta help fetch error {r.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Meta help fetch exception: {e}")
        return None

def content_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def check_meta_newsroom():
    newsroom_url = "https://about.fb.com/news/"
    try:
        r = requests.get(newsroom_url, timeout=15)
        if r.status_code == 200:
            text = r.text.lower()
            if "ray-ban" in text or "meta glasses" in text or "ai glasses" in text:
                return True
    except:
        pass
    return False

def check_reddit():
    reddit_url = "https://www.reddit.com/r/MetaGlasses/new/"
    try:
        r = requests.get(reddit_url, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200:
            text = r.text.lower()
            if "update" in text or "new feature" in text or "firmware" in text:
                return True
    except:
        pass
    return False

def search_tech_blogs():
    try:
        TAVILY_KEY = os.getenv("TAVILY_API_KEY", "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")
        query = "Ray Ban Meta Glasses new features update 2025"
        r = requests.post("https://api.tavily.com/search",
                          headers={"Authorization":f"Bearer {TAVILY_KEY}", "Content-Type":"application/json"},
                          json={"query": query, "max_results": 5, "time_range": "month"},
                          timeout=20)
        if r.status_code == 200:
            data = r.json()
            results = data.get("results", [])
            if results:
                return results
    except Exception as e:
        print(f"⚠️ Tavily search failed: {e}")
    return []

def extract_version_from_results(blog_results):
    """Extract version number from blog titles/snippets (e.g., v22.0, version 3.0)."""
    import re
    versions = []
    pattern = r'(v[\d\.]+|version\s+[\d\.]+)'
    for res in blog_results:
        text = (res.get("title", "") + " " + res.get("content", "")).lower()
        matches = re.findall(pattern, text, re.IGNORECASE)
        versions.extend(matches)
    if versions:
        # Return the most frequent version
        from collections import Counter
        return Counter(versions).most_common(1)[0][0]
    return "Bilinmiyor"

def generate_report(meta_changed, newsroom_flag, reddit_flag, blog_results):
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{REPORT_DIR}/meta_glasses_{today}.html"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Rayban Meta Glasses Güncelleme Raporu – {today}</title>
<style>
body {{ font-family:Arial,sans-serif; margin:40px; line-height:1.6; }}
h1 {{ color:#2c3e50; }}
.section {{ margin:24px 0; padding:16px; background:#f8f9fa; border-radius:8px; }}
.findings {{ color:#e74c3c; font-weight:bold; }}
.no-change {{ color:#27ae60; }}
ul {{ padding-left:20px; }}
</style>
</head>
<body>
<h1>🕶️ Rayban Meta Glasses – Güncelleme Kontrol Raporu</h1>
<p><strong>Tarih:</strong> {today}</p>

<div class="section">
<h2>📊 Kontrol Sonuçları</h2>
<ul>
<li>Meta Resmi Help Sayfası: {"<span class='findings'>DEĞİŞİKLİK TESPİT EDİLDİ</span>" if meta_changed else "<span class='no-change'>Değişiklik yok</span>"}</li>
<li>Meta Newsroom: {"<span class='findings'>Yeni içerik var</span>" if newsroom_flag else "<span class='no-change'>Yeni içerik yok</span>"}</li>
<li>Reddit r/MetaGlasses: {"<span class='findings'> Aktivite tespit edildi</span>" if reddit_flag else "<span class='no-change'> Aktivite yok</span>"}</li>
<li>Tech Blog Araması: {len(blog_results)} sonuç</li>
</ul>
</div>
'''
    
    if meta_changed:
        html += '''<div class="section">
<h2>📌 Meta Resmi Sayfasında Değişiklik</h2>
<p>Resmi help sayfası güncellenmiş gibi görünüyor. Detayları inceleyin:</p>
<p><a href="''' + META_HELP_URL + '''" target="_blank">Meta Help – AI Glasses</a></p>
</div>'''
    
    if newsroom_flag:
        html += '''<div class="section">
<h2>📢 Meta Newsroom'da İçerik Güncellemesi</h2>
<p>Meta'nın resmi blogunda AI Glasses ile ilgili yeni içerikler var.</p>
</div>'''
    
    if reddit_flag:
        html += '''<div class="section">
<h2>💬 Reddit'te Konuşma Aktivitasi</h2>
<p>r/MetaGlasses'te güncelleme ile ilgili gönderiler/haberler var.</p>
</div>'''
    
    if blog_results:
        html += '''<div class="section">
<h2>🔍 Teknoloji Bloglarındaki Haberler</h2>
<ul>'''
        for res in blog_results[:5]:
            title = res.get("title", "Başlık yok")
            url = res.get("url", "#")
            html += f'<li><a href="{url}" target="_blank">{title}</a></li>\n'
        html += '''</ul>
</div>'''
    
    if not any([meta_changed, newsroom_flag, reddit_flag, blog_results]):
        html += '''<div class="section">
<p class="no-change">✅ Hiçbir güncelleme tespit edilmedi. Mevcut sürümde devam edin.</p>
</div>'''
    
    html += '''<hr>
<footer>
<small>Bu rapor OpenClaw tarafından otomatik olarak üretilmiştir. • meta_glasses_update_checker</small>
</footer>
</body>
</html>'''
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Rapor oluşturuldu: {report_path}")
    return report_path

def push_and_verify(report_path):
    """Push HTML to GitHub Pages and verify it's accessible."""
    try:
        subprocess.run(["git","add",report_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m",f"Add Meta Glasses report {os.path.basename(report_path)}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
        return None
    
    # Construct public URL (Pages serves /raporlar/ as root)
    filename = os.path.basename(report_path)
    public_url = f"https://tempmert.github.io/Openclaw-Raporlar/raporlar/meta_glasses/{filename}"
    
    # Wait for build and verify (retry up to 3 times)
    max_attempts = 3
    for attempt in range(1, max_attempts+1):
        time.sleep(30)  # allow GitHub Pages build
        try:
            r = requests.head(public_url, timeout=10, allow_redirects=True)
            if r.status_code == 200:
                print(f"✅ Link verified (HTTP 200): {public_url}")
                return public_url
            else:
                print(f"⚠️ Attempt {attempt}: HTTP {r.status_code}")
        except Exception as e:
            print(f"⚠️ Check error: {e}")
    
    # Trigger rebuild if still failing
    print("🔄 Triggering rebuild with empty commit...")
    try:
        subprocess.run(["git","commit","--allow-empty","-m","trigger rebuild"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(30)
        r = requests.head(public_url, timeout=10)
        if r.status_code == 200:
            print(f"✅ Verified after rebuild: {public_url}")
            return public_url
    except Exception as e:
        print(f"❌ Rebuild failed: {e}")
    
    print(f"❌ Link verification failed for {public_url}")
    return None

def send_telegram_report(public_url, has_updates):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = "1103470495"
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN not set – skipping notification")
        return
    
    if public_url:
        text = f"🕶️ Rayban Meta Glasses güncelleme raporu hazır.\n\n🔗 {public_url}"
    else:
        text = "⚠️ Rayban Meta Glasses güncelleme raporu oluşturuldu ancak link doğrulanamadı."
    
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                         json={"chat_id": TELEGRAM_CHAT_ID, "text": text[:4096]}, timeout=10)
        if r.status_code == 200:
            print("📨 Telegram bildirimi gönderildi")
    except Exception as e:
        print(f"⚠️ Telegram send failed: {e}")

def main():
    state = load_state()
    print("🔍 Meta Glasses güncelleme kontrolü başlatılıyor...")
    
    meta_html = fetch_meta_help()
    if not meta_html:
        print("❌ Meta help page fetch failed – skip")
        return
    
    current_hash = content_hash(meta_html)
    meta_changed = (state.get("last_content_hash") != current_hash)
    
    newsroom_flag = check_meta_newsroom()
    reddit_flag = check_reddit()
    blog_results = search_tech_blogs()
    
    has_updates = any([meta_changed, newsroom_flag, reddit_flag, blog_results])
    
    if has_updates or not state.get("last_report"):
        report_path = generate_report(meta_changed, newsroom_flag, reddit_flag, blog_results)
        # Push and verify link
        public_url = push_and_verify(report_path)
        send_telegram_report(public_url, has_updates)
        
        # Update state
        state["last_check"] = datetime.now().isoformat()
        state["last_content_hash"] = current_hash
        state["last_report"] = public_url if public_url else report_path
        save_state(state)
        
        if has_updates and public_url:
            print(f"🚨 Güncelleme tespit edildi – rapor ve bildirim gönderildi: {public_url}")
        elif has_updates:
            print("⚠️ Güncelleme var ama link doğrulanamadı")
        else:
            print("✅ İlk rapor oluşturuldu (ilk kontrol)")
    else:
        print("✅ Değişiklik yok – atlanıyor")

if __name__ == "__main__":
    main()
