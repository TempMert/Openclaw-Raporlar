#!/usr/bin/env python3
"""
Rayban Meta GEN1 Glasses – 2 haftada bir güncelleme kontrolü.
SADECE GEN1 modeli için.
Meta resmi help sayfası, newsroom, Reddit, tech blogs.
"""

import requests, json, datetime, re, subprocess, os, hashlib, time
from datetime import datetime, timedelta

WORKSPACE = "/home/openclaw/.openclaw/workspace"
META_HELP_URL = "https://www.meta.com/help/ai-glasses/1809764829519902/"
STATE_FILE = f"{WORKSPACE}/meta_glasses_state.json"
REPORT_DIR = f"{WORKSPACE}/raporlar/meta_glasses"
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
            # SADECE GEN1 ile ilgili içerik
            if ("ray-ban" in text or "meta glasses" in text or "ai glasses" in text) and ("gen1" in text or "first gen" in text or "original" in text):
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
            if "gen1" in text or "first gen" in text or "original" in text:
                return True
    except:
        pass
    return False

def search_tech_blogs():
    try:
        TAVILY_KEY = os.getenv("TAVILY_API_KEY", "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")
        query = "Ray Ban Meta GEN1 glasses update release date 2025 2026"
        r = requests.post("https://api.tavily.com/search",
                          headers={"Authorization":f"Bearer {TAVILY_KEY}", "Content-Type":"application/json"},
                          json={"query": query, "max_results": 5, "time_range": "month"},
                          timeout=20)
        if r.status_code == 200:
            data = r.json()
            results = data.get("results", [])
            # Filter GEN1 only
            filtered = []
            for res in results:
                text = (res.get("title", "") + " " + res.get("content", "")).lower()
                if "gen1" in text or "first gen" in text or "original" in text:
                    filtered.append(res)
            return filtered
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
        from collections import Counter
        return Counter(versions).most_common(1)[0][0]
    return "Bilinmiyor"

def generate_blog_summary(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info=None):
    """Referans blog'a benzer blog yazısı özeti (Türkçe, koyu mod) – GEN1 spesifik."""
    today = datetime.now().strftime("%Y-%m-%d")
    parts = []
    
    parts.append(f"""<p style="font-size: 1.2rem; color: #9ca3af; margin-bottom: 2rem;">
    <em>Bu rapor Rayban Meta <strong>GEN1</strong> gözlüklerinin son güncelleme durumunu inceliyor. Veriler otomatik olarak toplanmış ve <strong>{today}</strong> tarihinde rapor hazırlanmıştır.</em>
</p>""")
    
    has_updates = any([meta_changed, newsroom_flag, reddit_flag, blog_results])
    
    if has_updates:
        parts.append("<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #fbbf24;'>📌 Son Güncellemeler (GEN1)</h2>")
        
        if meta_changed:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🔍 <strong style="color: #60a5fa;">Meta'nın resmi Help Sayfası</strong> güncellenmiş görünüyor. Bu, GEN1 kullanıcılar için en güncel kullanım kılavuzları, AI özellikleri açıklamaları ve sorun giderme bilgileri eklenmiş demek.
</p>""")
        
        if newsroom_flag:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    📢 <strong style="color: #60a5fa;">Meta Newsroom</strong>’da AI Glasses ile ilgili yeni içerikler yayınlanmış. Resmi duyurular, ürün güncellemeleri veya pazarlama materyalleri olabilir.
</p>""")
        
        if reddit_flag:
            parts.append("""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    💬 <strong style="color: #60a5fa;">Reddit r/MetaGlasses</strong> topluluğunda aktivite tespit edildi. Kullanıcılar yeni özellikleri test ediyor, geri bildirimlerini paylaşıyor veya sorunları konuşuyor.
</p>""")
        
        if blog_results:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    📰 Teknoloji bloglarında <strong style="color: #fbbf24;">{len(blog_results)} yeni haber</strong> bulundu. Bu haberler GEN1 modeline odaklanmış olabilir.
</p>""")
        
        if version_info and version_info != "Bilinmiyor":
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🏷️ Tahmini GEN1 sürüm bilgisi: <code style="background: #1f2937; padding: 4px 8px; border-radius: 4px; color: #f3f4f6;">{version_info}</code>
</p>""")
    else:
        parts.append("""<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #10b981;'>✅ Rayban Meta GEN1 – Güncelleme Yok</h2>
<p style="line-height: 1.8; margin-bottom: 1.5rem;">
    Şu anda Rayban Meta <strong>GEN1</strong> gözlükleri için herhangi bir resmi güncelleme tespit edilmedi. Mevcut sürümde devam edebilirsiniz.
</p>""")
    
    return "\n".join(parts)

def generate_report(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info=None):
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{REPORT_DIR}/meta_glasses_{today}.html"
    
    # Extract version from blog results if available
    if not version_info and blog_results:
        version_info = extract_version_from_results(blog_results)
    
    # Overall status – GEN1 specific with date
    has_updates = any([meta_changed, newsroom_flag, reddit_flag, blog_results])
    if has_updates:
        overall_status = f"🚨 RAYBAN META GEN1 – GÜNCELLEME VAR ({today})"
        status_badge_class = "update"
        badge_style = "background: #ef4444; color: white;"
    else:
        overall_status = "✅ Rayban Meta GEN1 – Güncelleme Yok"
        status_badge_class = "no-change"
        badge_style = "background: transparent; color: #10b981; border: 2px solid #10b981;"
    
    # Blog yazısı özeti
    blog_summary = generate_blog_summary(meta_changed, newsroom_flag, reddit_flag, blog_results, version_info)
    
    # Kontrol sonuçları listesi – MODERN KARTLAR
    kontrol_items = [
        ("Meta Resmi Help Sayfası", meta_changed, META_HELP_URL, "Meta'nın resmi AI Glasses rehber sayfası"),
        ("Meta Newsroom", newsroom_flag, "https://about.fb.com/news/", "Meta'nın resmi blog yayınları"),
        ("Reddit r/MetaGlasses", reddit_flag, "https://www.reddit.com/r/MetaGlasses/", "Kullanıcı topluluğu tartışmaları"),
        ("Teknoloji Blogları", len(blog_results) > 0, None, "GEN1 teknoloji haberleri")
    ]
    
    kontrol_html = ""
    for name, is_update, url, desc in kontrol_items:
        badge_class = "update" if is_update else "no-change"
        badge_text = "GÜNCELLENDI" if is_update else "DEĞİŞİKLİK YOK"
        badge_icon = "✓" if not is_update else "✕"
        link_icon = f'<a href="{url}" target="_blank" style="color: var(--accent); margin-left: 8px; font-size: 1rem;">🔗</a>' if url else ""
        
        kontrol_html += f"""
<li class="card" style="margin: 12px 0; padding: 20px 24px;">
    <div class="card-header">
        <div class="card-title">
            {name}
            <span class="card-badge {badge_class}" style="{badge_style if is_update else 'background: transparent; color: var(--success); border: 1px solid var(--success);'}">
                {badge_icon} {badge_text}
            </span>
        </div>
    </div>
    <div class="card-desc">
        {desc}
    </div>
    {f'<a class="card-link" href="{url}" target="_blank">Şuradan incele {link_icon}</a>' if url else ''}
</li>"""
    
    # Blog haberleri listesi – MODERN TARZDA
    blog_links_html = ""
    if blog_results:
        blog_links_html = f"""
<section>
<h2>🔍 Güncellenmiş Haberler ({len(blog_results)})</h2>
<ul class="link-list">
"""
        for r in blog_results[:5]:
            title = r.get("title", "Başlık yok")
            url = r.get("url", "#")
            snippet = r.get("content", "")[:150] + "..." if r.get("content") else ""
            blog_links_html += f'''
<li>
    <a href="{url}" target="_blank">
        <strong>{title}</strong>
        {'<p style="color: var(--text-muted); margin: 8px 0 0 0; font-size: 0.9rem; line-height: 1.5;">' + snippet + '</p>' if snippet else ''}
    </a>
</li>'''
        blog_links_html += "\n</ul>\n</section>"
    
    # HTML – Okuma dostu koyu mod, Slate renk paleti, Inter font
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rayban Meta GEN1 Güncelleme Raporu – {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0f172a;          /* Slate 900 – yumuşak koyu */
    --card: #1e293b;        /* Slate 800 – card background */
    --card-hover: #334155;  /* Slate 700 – hover */
    --text-main: #f1f5f9;   /* Slate 100 – parlak, okunabilir */
    --text-muted: #94a3b8;  /* Slate 400 – ikincil metin */
    --accent: #3b82f6;      /* Blue 500 – linkler */
    --accent-hover: #60a5fa;
    --success: #10b981;     /* Emerald 500 */
    --danger: #ef4444;      /* Red 500 */
    --border: #334155;      /* Slate 700 */
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.15);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text-main);
    line-height: 1.7;
    margin: 0 auto;
    max-width: 900px;
    padding: 40px 20px;
    font-size: 16px;
}}

a {{ color: var(--accent); text-decoration: none; transition: color 0.2s; }}
a:hover {{ color: var(--accent-hover); text-decoration: underline; }}

header {{
    text-align: left;
    margin-bottom: 48px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: var(--text-main);
    letter-spacing: -0.03em;
    line-height: 1.2;
}}

.meta {{
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 4px;
    font-weight: 500;
}}

.status-line {{
    margin-top: 16px;
    font-size: 1.25rem;
    color: var(--text-main);
    font-weight: 600;
}}

.status-badge {{
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    border-radius: 999px;
    font-weight: 700;
    margin-left: 10px;
    font-size: 1rem;
    border: 2px solid transparent;
}}
.status-badge.update {{
    background: var(--danger);
    color: white;
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.2);
}}
.status-badge.no-change {{
    background: transparent;
    color: var(--success);
    border-color: var(--success);
}}

section {{ margin: 48px 0; }}

h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 24px 0;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--border);
}}

p {{ margin-bottom: 1.5rem; font-size: 1.05rem; line-height: 1.8; color: var(--text-main); }}
p em {{ color: var(--text-muted); font-style: normal; }}
p strong {{ color: var(--text-main); font-weight: 600; }}
code {{
    background: var(--card);
    padding: 4px 10px;
    border-radius: 6px;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    color: var(--accent);
    border: 1px solid var(--border);
}}

.card-list {{ list-style: none; padding: 0; margin: 1em 0; }}
.card-list li {{ margin: 0; }}

/* Modern kartlar */
.card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 8px;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

.card-badge {{
    display: inline-flex;
    align-items: center;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.card-badge.update {{
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}}
.card-badge.no-change {{
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}}

.card-link {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--accent);
}}
.card-link:hover {{ color: var(--accent-hover); text-decoration: underline; }}

/* Liste bağlantıları (blog haberleri) */
.link-list {{
    list-style: none;
    padding: 0;
    margin: 1.5em 0;
}}
.link-list li {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 10px 0;
    transition: background 0.2s;
}}
.link-list li:hover {{
    background: var(--card-hover);
    border-color: var(--accent);
}}
.link-list a {{
    color: var(--text-main);
    font-size: 1.05rem;
    font-weight: 500;
    text-decoration: none;
}}
.link-list a:hover {{
    color: var(--accent);
    text-decoration: underline;
}}

footer {{
    margin-top: 80px;
    padding: 32px;
    background: var(--card);
    border-radius: 12px;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
    border: 1px solid var(--border);
}}

@media (max-width: 600px) {{
    body {{ padding: 16px; }}
    h1 {{ font-size: 2rem; }}
    h2 {{ font-size: 1.3rem; }}
    .card {{ padding: 16px; }}
}}
</style>
</head>
<body>

<header>
    <h1>🕶️ Rayban Meta GEN1 – Güncelleme Raporu</h1>
    <p class="meta">Oluşturulma: {today} • OpenClaw Otomatik Kontrol • Sadece GEN1 modeli için</p>
    <p class="status-line">
        <strong>Durum:</strong>
        <span class="status-badge {'update' if has_updates else 'no-change'}" style="{'background: var(--danger); color: white;' if has_updates else 'background: transparent; color: var(--success); border: 2px solid var(--success);'}">{overall_status}</span>
    </p>
</header>

{blog_summary}

<section>
<h2>📊 Kontrol Sonuçları</h2>
<ul class="card-list">
{kontrol_html}
</ul>
</section>

{blog_links_html}

<footer>
<small>
    Bu rapor <a href="https://github.com/TempMert/Openclaw-Raporlar" target="_blank">OpenClaw</a> tarafından otomatik olarak üretilmiştir.<br>
    meta_glasses_update_checker • {today} • GEN1 Modeli
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
    """Push HTML to GitHub Pages using full delete & recreate (cache bust)."""
    filename = os.path.basename(report_path)
    public_url = f"https://tempmert.github.io/Openclaw-Raporlar/raporlar/meta_glasses/{filename}"
    repo_root = WORKSPACE

    try:
        # Step 1: Ensure file exists
        if not os.path.exists(report_path):
            print(f"❌ Report file not found: {report_path}")
            return None

        # Step 2: Remove old file from git index (if tracked) – cache bust
        try:
            subprocess.run(["git","rm","-f","--cached",report_path], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","commit","-m",f"Remove old {filename} (cache bust)"], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","push","raporlar","main"], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🗑️ Cache bust: removed old {filename} from git")
            time.sleep(3)
        except Exception:
            pass

        # Step 3: Add new file and push
        subprocess.run(["git","add",report_path], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m",f"Add/update Meta Glasses report {filename} (GEN1)"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pushed to GitHub (fresh)")

        # Step 4: Verify with retries
        for attempt in range(1, 4):
            time.sleep(30)
            try:
                r = requests.head(public_url, timeout=10, allow_redirects=True)
                if r.status_code == 200:
                    print(f"✅ Verified: {public_url}")
                    return public_url
                print(f"⚠️ Attempt {attempt}: HTTP {r.status_code}")
            except Exception as e:
                print(f"⚠️ Check error: {e}")

        print(f"❌ Verification failed: {public_url}")
        return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return None

def main():
    state = load_state()
    print("🔍 Meta Glasses GEN1 güncelleme kontrolü başlatılıyor...")
    
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

def send_telegram_report(public_url, has_updates):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = "1103470495"
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN not set – skipping notification")
        return
    
    if public_url:
        text = f"🕶️ Rayban Meta GEN1 güncelleme raporu hazır.\n\n🔗 {public_url}"
    else:
        text = "⚠️ Rayban Meta GEN1 güncelleme raporu oluşturuldu ancak link doğrulanamadı."
    
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                         json={"chat_id": TELEGRAM_CHAT_ID, "text": text[:4096]}, timeout=10)
        if r.status_code == 200:
            print("📨 Telegram bildirimi gönderildi")
    except Exception as e:
        print(f"⚠️ Telegram send failed: {e}")

if __name__ == "__main__":
    main()