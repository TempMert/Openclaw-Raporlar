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
        from collections import Counter
        return Counter(versions).most_common(1)[0][0]
    return "Bilinmiyor"

def generate_blog_summary(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info=None):
    """Güncellemeler hakkında blog yazısı formatında özet oluştur."""
    today = datetime.now().strftime("%Y-%m-%d")
    summary = []
    
    # Giriş
    summary.append(f"<p><em>Bu rapor Rayban Meta Glasses'in güncel durumunu ve son güncellemeleri analiz ediyor. Tüm veriler otomatik olarak toplanmış ve {today} tarihinde oluşturulmuştur.</em></p>")
    
    if any([meta_changed, newsroom_flag, reddit_flag, blog_results]):
        summary.append("<h2>📌 Son Güncellemeler</h2>")
        
        if meta_changed:
            summary.append("<p>🔍 <strong>Meta'nın resmi Help Sayfası</strong> güncellenmiş görünüyor. Bu, kullanıcıların en güncel kullanım bilgilerine ulaşabileceği anlamına geliyor. Değişiklikler muhtemelen yeni AI özellikleri, kullanım ipuçları veya sorun gidermelerini içeriyor.</p>")
        
        if newsroom_flag:
            summary.append("<p>📢 <strong>Meta Newsroom</strong>'da AI Glasses ile ilgili yeni içerikler paylaşıldı. Resmi duyurular, blog yazıları veya medya bültenleri bu kapsamda olabilir.</p>")
        
        if reddit_flag:
            summary.append("<p>💬 <strong>Reddit r/MetaGlasses</strong> topluluğunda güncelleme ile ilgili aktivite tespit edildi. Kullanıcılar yeni özellikleri deniyor, geri bildirim paylaşıyor veya sorunları konuşuyor.</p>")
        
        if blog_results:
            summary.append(f"<p>📰 Teknoloji bloglarında <strong>{len(blog_results)} yeni haber</strong> bulundu. Bu haberler genellikle kıdemli teknoloji yazarları tarafından detaylı analizler içeriyor.</p>")
        
        if version_info and version_info != "Bilinmiyor":
            summary.append(f"<p>🏷️ Tahmini sürüm bilgisi: <code>{version_info}</code></p>")
    else:
        summary.append("<h2>✅ Hiç Güncelleme Yok</h2>")
        summary.append("<p>Şu an Meta Glasses üzerinde herhangi bir resmi güncelleme tespit edilmedi. Mevcut sürümde devam edebilirsiniz.</p>")
    
    return "\n".join(summary)

def generate_report(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info=None):
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{REPORT_DIR}/meta_glasses_{today}.html"
    
    # Extract version from blog results if available
    if not version_info and blog_results:
        version_info = extract_version_from_results(blog_results)
    
    # Overall status
    overall_status = "🚨 GÜNCELLEME VAR" if any([meta_changed, newsroom_flag, reddit_flag, blog_results]) else "✅ Değişiklik Yok"
    
    # Blog yazısı özeti
    blog_summary = generate_blog_summary(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info)
    
    # Kontrol sonuçları listesi
    kontrol = [
        ("Meta Resmi Help Sayfası", meta_changed, "DEĞİŞİKLİK VAR" if meta_changed else "Değişiklik yok", META_HELP_URL),
        ("Meta Newsroom", newsroom_flag, "YENİ İÇERİK" if newsroom_flag else "Değişiklik yok", "https://about.fb.com/news/"),
        ("Reddit r/MetaGlasses", reddit_flag, "AKTİVİTE VAR" if reddit_flag else "Aktivite yok", "https://www.reddit.com/r/MetaGlasses/"),
        ("Teknoloji Blogları", len(blog_results) > 0, f"{len(blog_results)} haber", None)
    ]
    
    # HTML şablonu – Blog tarzı, sade, okunaklı
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rayban Meta Glasses Güncelleme Raporu – {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
    --text: #1a1a1a;
    --text-light: #555;
    --accent: #2563eb;
    --bg: #ffffff;
    --muted: #f3f4f6;
    --border: #e5e7eb;
    --success: #059669;
    --danger: #dc2626;
}}
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.7;
    color: var(--text);
    background: var(--bg);
    margin: 0 auto;
    max-width: 800px;
    padding: 40px 20px;
}}
header {{
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}}
h1 {{
    font-family: 'Merriweather', serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    color: var(--text);
}}
h2 {{
    font-size: 1.4rem;
    font-weight: 600;
    margin: 2em 0 0.5em 0;
    color: var(--text);
}}
p, li {{
    font-size: 1.05rem;
}}
.meta {{
    color: var(--text-light);
    font-size: 0.95rem;
    margin-top: 5px;
}}
.badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-left: 8px;
}}
.badge.update {{ background: #fee2e2; color: var(--danger); }}
.badge.no-change {{ background: #dcfce7; color: var(--success); }}
.badge.count {{ background: var(--muted); color: var(--text-light); }}
ul.checklist {{
    list-style: none;
    padding: 0;
    margin: 1em 0;
}}
ul.checklist li {{
    padding: 12px 16px;
    background: var(--muted);
    margin: 8px 0;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-left: 4px solid transparent;
}}
ul.checklist li.status-update {{ border-left-color: var(--danger); background: #fef2f2; }}
ul.checklist li.status-no-change {{ border-left-color: var(--success); background: #ecfdf5; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{
    background: var(--muted);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
}}
footer {{
    margin-top: 60px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    color: var(--text-light);
    font-size: 0.9rem;
    text-align: center;
}}
.em {{
    font-style: italic;
    color: var(--text-light);
}}
</style>
</head>
<body>
<header>
    <h1>🕶️ Rayban Meta Glasses Güncelleme Raporu</h1>
    <p class="meta">Oluşturulma: {today} • OpenClaw Otomatik Kontrol</p>
    <p style="font-size: 1.2rem; margin-top: 12px;">
        <strong>Genel Durum:</strong> <span style="color: {'var(--danger)' if overall_status.startswith('🚨') else 'var(--success)'};">{overall_status}</span>
    </p>
</header>

{blog_summary}

<section>
<h2>📊 Kontrol Sonuçları</h2>
<ul class="checklist">
<li class="status-{'update' if meta_changed else 'no-change'}">
    <span>
        <strong>Meta Resmi Help Sayfası</strong><br>
        <small class="em">Meta'nın resmi AI Glances rehber sayfası</small>
    </span>
    <span class="badge {'update' if meta_changed else 'no-change'}">{kontrol[0][2]}</span>
</li>
<li class="status-{'update' if newsroom_flag else 'no-change'}">
    <span>
        <strong>Meta Newsroom</strong><br>
        <small class="em">Meta'nın resmi blog yayınları</small>
    </span>
    <span class="badge {'update' if newsroom_flag else 'no-change'}">{kontrol[1][2]}</span>
</li>
<li class="status-{'update' if reddit_flag else 'no-change'}">
    <span>
        <strong>Reddit r/MetaGlasses</strong><br>
        <small class="em">Kullanıcı topluluğu tartışmaları</small>
    </span>
    <span class="badge {'update' if reddit_flag else 'no-change'}">{kontrol[2][2]}</span>
</li>
<li>
    <span>
        <strong>Teknoloji Blogları</strong><br>
        <small class="em">Teknik analiz ve haberler</small>
    </span>
    <span class="badge {'update' if blog_results else 'no-change'}">{len(blog_results)} haber</span>
</li>
</ul>
</section>

{f'''<section>
<h2>🔍 Güncellenmiş Kaynaklar</h2>
<ul>''' if blog_results else ''}
{chr(10).join([f'<li><a href="{r.get("url")}" target="_blank">{r.get("title", "Başlık yok")}</a></li>' for r in blog_results[:5]]) if blog_results else ''}
{f'''</ul>
</section>''' if blog_results else ''}

<footer>
Bu rapor <a href="https://github.com/TempMert/Openclaw-Raporlar" target="_blank">OpenClaw</a> tarafından otomatik olarak üretilmiştir.<br>
meta_glasses_update_checker • {today}
</footer>
</body>
</html>'''
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Rapor oluşturuldu: {report_path}")
    
    # VS Code'da otomatik aç
    try:
        subprocess.run(["code", report_path], check=False)
        print(f"💡 Rapor VS Code'da açıldı")
    except FileNotFoundError:
        print(f"💡 VS Code kurulu değil – dosya: {report_path}")
    
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
