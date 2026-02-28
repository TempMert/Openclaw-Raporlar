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
    """Referans blog'a benzer blog yazısı özeti (Türkçe, koyu mod)."""
    today = datetime.now().strftime("%Y-%m-%d")
    parts = []
    
    # Giriş paragrafı
    parts.append(f"""<p style="font-size: 1.2rem; color: #9ca3af; margin-bottom: 2rem;">
    <em>Bu analiz Rayban Meta Glasses'in son güncelleme durumunu inceliyor. Veriler otomatik olarak toplanmış ve {today} tarihinde rapor hazırlanmıştır.</em>
</p>""")
    
    if any([meta_changed, newsroom_flag, reddit_flag, blog_results]):
        parts.append("<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #e5e7eb;'>📌 Son Güncellemeler</h2>")
        
        if meta_changed:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🔍 <strong style="color: #60a5fa;">Meta'nın resmi Help Sayfası</strong> güncellenmiş görünüyor. Bu, kullanıcılar için en güncel kullanım kılavuzları, AI özellikleri açıklamaları ve sorun giderme bilgileri eklenmiş demek. Değişiklikler doğrudan kullanıcı deneyimini etkileyebilir.
</p>""")
        
        if newsroom_flag:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    📢 <strong style="color: #60a5fa;">Meta Newsroom</strong>’da AI Glasses ile ilgili yeni içerikler yayınlanmış. Bu, resmi duyurular, ürün güncellemeleri veya pazarlama materyalleri olabilir. Meta’nın resmi kanalıdır, takip etmek önemli.
</p>""")
        
        if reddit_flag:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    💬 <strong style="color: #60a5fa;">Reddit r/MetaGlasses</strong> topluluğunda aktivite tespit edildi. Kullanıcılar yeni özellikleri test ediyor, geri bildirimlerini paylaşıyor veya sorunları konuşuyor. Bu, topluluktepkisini anlamak için değerli.
</p>""")
        
        if blog_results:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    📰 Teknoloji bloglarında <strong style="color: #fbbf24;">{len(blog_results)} yeni haber</strong> bulundu. Bu kaynaklar genellikle derinlemesine analizler, kıdemli yazarların görüşleri ve diğer medya kanallarında olmayan detayları içeriyor.
</p>""")
        
        if version_info and version_info != "Bilinmiyor":
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🏷️ Tahmini sürüm bilgisi: <code style="background: #1f2937; padding: 4px 8px; border-radius: 4px; color: #f3f4f6;">{version_info}</code>
</p>""")
    else:
        parts.append("""<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #10b981;'>✅ Hiç Güncelleme Yok</h2>
<p style="line-height: 1.8; margin-bottom: 1.5rem;">
    Şu anda Meta Glasses üzerinde herhangi bir resmi güncelleme tespit edilmedi. Mevcut sürümde devam edebilirsiniz. Güncelleme geldiğinde otomatik bildirim alacaksınız.
</p>""")
    
    return "\n".join(parts)

def generate_report(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info=None):
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{REPORT_DIR}/meta_glasses_{today}.html"
    
    # Extract version from blog results if available
    if not version_info and blog_results:
        version_info = extract_version_from_results(blog_results)
    
    # Overall status
    overall_status = "🚨 GÜNCELLEME VAR" if any([meta_changed, newsroom_flag, reddit_flag, blog_results]) else "✅ Değişiklik Yok"
    status_color = "#ef4444" if overall_status.startswith("🚨") else "#10b981"
    
    # Blog yazısı özeti
    blog_summary = generate_blog_summary(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info)
    
    # Kontrol sonuçları listesi
    kontrol_items = [
        ("Meta Resmi Help Sayfası", meta_changed, META_HELP_URL),
        ("Meta Newsroom", newsroom_flag, "https://about.fb.com/news/"),
        ("Reddit r/MetaGlasses", reddit_flag, "https://www.reddit.com/r/MetaGlasses/"),
        ("Teknoloji Blogları", len(blog_results) > 0, None)
    ]
    
    kontrol_html = ""
    for name, is_update, url in kontrol_items:
        status_text = "DEĞİŞİKLİK VAR" if is_update else "Değişiklik yok"
        badge_class = "update" if is_update else "no-change"
        badge_color_style = "background: #fee2e2; color: #dc2626;" if is_update else "background: #1f2937; color: #9ca3af;"
        link_part = f'<a href="{url}" target="_blank" style="color: #60a5fa; margin-left: 8px; font-size: 0.9rem;">🔗</a>' if url else ""
        
        kontrol_html += f"""
<li class="{'status-update' if is_update else 'status-no-change'}" style="padding: 16px; background: {'#1f2937' if not is_update else '#450a0a'}; margin: 12px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid {'#ef4444' if is_update else '#10b981'};">
    <span>
        <strong style="color: #e5e7eb;">{name}</strong><br>
        <small style="color: #9ca3af; font-size: 0.9rem;">{'Meta resmi sayfası' if 'Meta Resmi' in name else 'Resmi duyurular' if 'Newsroom' in name else 'Kullanıcı topluluğu' if 'Reddit' in name else 'Teknik analizler'}</small>
    </span>
    <span class="badge" style="{badge_color_style}">{status_text}{link_part}</span>
</li>"""
    
    # Blog haberleri listesi
    blog_links_html = ""
    if blog_results:
        blog_links_html = "<section>\n<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #e5e7eb;'>🔍 Güncellenmiş Kaynaklar</h2>\n<ul style='list-style: none; padding: 0;'>\n"
        for r in blog_results[:5]:
            title = r.get("title", "Başlık yok")
            url = r.get("url", "#")
            blog_links_html += f'<li style="margin: 12px 0; padding: 12px; background: #1f2937; border-radius: 8px;"><a href="{url}" target="_blank" style="color: #60a5fa; font-size: 1.05rem; text-decoration: none;">{title}</a></li>\n'
        blog_links_html += "</ul>\n</section>"
    
    # HTML – Koyu mod, blog tarzı, Inter font
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rayban Meta Glasses Güncelleme Raporu – {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg: #0a0a0a;
    --card: #1a1a1a;
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;
    --accent: #3b82f6;
    --accent-hover: #60a5fa;
    --success: #10b981;
    --danger: #ef4444;
    --border: #2d2d2d;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text-main);
    line-height: 1.8;
    margin: 0 auto;
    max-width: 800px;
    padding: 40px 20px;
    font-size: 16px;
}}

a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ color: var(--accent-hover); text-decoration: underline; }}

header {{
    text-align: left;
    margin-bottom: 60px;
    padding-bottom: 30px;
    border-bottom: 1px solid var(--border);
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 0 8px 0;
    color: var(--text-main);
    letter-spacing: -0.02em;
}}

.meta {{
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 4px;
}}

.status-line {{
    margin-top: 16px;
    font-size: 1.25rem;
    color: var(--text-main);
}}

.status-badge {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
    margin-left: 8px;
    font-size: 1rem;
}}

.status-badge.update {{ background: var(--danger); color: white; }}
.status-badge.no-change {{ background: var(--card); color: var(--success); border: 1px solid var(--success); }}

section {{ margin: 40px 0; }}

h2 {{
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0 0 20px 0;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 10px;
}}

p {{
    margin-bottom: 1.5rem;
    font-size: 1.05rem;
}}

ul {{ list-style: none; padding: 0; margin: 1em 0; }}

li {{ margin: 12px 0; }}

.badge-small {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 6px;
    background: var(--card);
    color: var(--text-muted);
    border: 1px solid var(--border);
}}

footer {{
    margin-top: 80px;
    padding-top: 30px;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.9rem;
    text-align: center;
}}

@media (max-width: 600px) {{
    body {{ padding: 20px; }}
    h1 {{ font-size: 2rem; }}
    h2 {{ font-size: 1.4rem; }}
}}
</style>
</head>
<body>

<header>
    <h1>🕶️ Rayban Meta Glasses Güncelleme Raporu</h1>
    <p class="meta">Oluşturulma: {today} • OpenClaw Otomatik Kontrol</p>
    <p class="status-line">
        <strong>Genel Durum:</strong>
        <span class="status-badge {'update' if overall_status.startswith('🚨') else 'no-change'}">{overall_status}</span>
    </p>
</header>

{blog_summary}

<section>
<h2>📊 Kontrol Sonuçları</h2>
<ul>
{kontrol_html}
</ul>
</section>

{blog_links_html}

<footer>
<small>
    Bu rapor <a href="https://github.com/TempMert/Openclaw-Raporlar" target="_blank">OpenClaw</a> tarafından otomatik olarak üretilmiştir.<br>
    meta_glasses_update_checker • {today}
</small>
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
    """Push HTML to GitHub Pages using delete-then-recreate to bust cache."""
    filename = os.path.basename(report_path)
    public_url = f"https://tempmert.github.io/Openclaw-Raporlar/raporlar/meta_glasses/{filename}"

    try:
        # Step 1: Remove old file if tracked (cache bust)
        try:
            subprocess.run(["git","rm","-f",report_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","commit","-m",f"Remove old report {filename} (cache bust)"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","push","raporlar","main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🗑️ Removed old {filename} from git (cache bust)")
            time.sleep(5)  # brief wait for GitHub to process deletion
        except subprocess.CalledProcessError:
            pass  # file may not be tracked yet, continue

        # Step 2: Add new file and push
        subprocess.run(["git","add",report_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m",f"Add/update Meta Glasses report {filename}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pushed to GitHub (fresh deploy)")

        # Step 3: Verify with retries
        max_attempts = 3
        for attempt in range(1, max_attempts+1):
            time.sleep(30)  # allow build
            try:
                r = requests.head(public_url, timeout=10, allow_redirects=True)
                if r.status_code == 200:
                    print(f"✅ Link verified (HTTP 200): {public_url}")
                    return public_url
                else:
                    print(f"⚠️ Attempt {attempt}: HTTP {r.status_code}")
            except Exception as e:
                print(f"⚠️ Check error: {e}")

        # If still failing, try empty commit to trigger rebuild
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

    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
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
