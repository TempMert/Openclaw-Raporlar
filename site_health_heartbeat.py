#!/usr/bin/env python3
"""
Site Sağlık (Heartbeat) Ajanı – OpenClaw
Haftada bir, GitHub Pages'deki HTML dosyalarını kontrol eder.
Erişilemez veya yavaşsa Telegram'la acil bildirim gönderir.
SEO analizi: meta etiketleri, bozuk linkler.
"""

import requests, os, glob, time, json, re, subprocess
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKSPACE = "/home/openclaw/.openclaw/workspace"
REPORT_DIR = f"{WORKSPACE}/raporlar"
HEALTH_STATE_FILE = f"{WORKSPACE}/site_health_state.json"
GITHUB_PAGES_BASE = "https://tempmert.github.io/Openclaw-Raporlar"

def load_state():
    if os.path.exists(HEALTH_STATE_FILE):
        with open(HEALTH_STATE_FILE) as f:
            return json.load(f)
    return {"last_run": None, "alerts_sent": [], "performance_history": {}}

def save_state(state):
    with open(HEALTH_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def find_all_html_files():
    """raporlar/ altındaki tüm .html dosyalarını bul (recursive)."""
    pattern = f"{REPORT_DIR}/**/*.html"
    files = glob.glob(pattern, recursive=True)
    # GitHub Pages URL'lerine çevir
    urls = []
    for f in files:
        rel_path = os.path.relpath(f, WORKSPACE)
        url = f"{GITHUB_PAGES_BASE}/{rel_path.replace(os.sep, '/')}"
        urls.append(url)
    return urls

def check_url(url):
    """Bir URL'i kontrol et: status code, load time."""
    try:
        start = time.time()
        r = requests.get(url, timeout=10, allow_redirects=True)
        load_time = time.time() - start
        return {
            "url": url,
            "status": r.status_code,
            "load_time": round(load_time, 3),
            "ok": r.status_code == 200 and load_time < 5
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "load_time": None,
            "ok": False,
            "error": str(e)
        }

def send_telegram_alert(message):
    """Telegram bot ile mesaj gönder."""
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = "1103470495"
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN not set – skipping alert")
        return False
    
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message[:4096]},
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"⚠️ Telegram send failed: {e}")
        return False

def analyze_seo(url):
    """SEO analizi: meta tags, title, description, broken links (basic)."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"url": url, "seo_issues": ["Page not accessible"]}
        
        html = r.text
        issues = []
        
        # Check meta description
        if not re.search(r'<meta\s+name="description"', html, re.IGNORECASE):
            issues.append("Missing meta description")
        
        # Check title
        if not re.search(r'<title>.*?</title>', html):
            issues.append("Missing title tag")
        
        # Check for broken links (simple check for 404 in hrefs)
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
        # Only check a sample (avoid rate limits)
        broken = []
        for link in links[:5]:
            try:
                lr = requests.head(link, timeout=5, allow_redirects=True)
                if lr.status_code >= 400:
                    broken.append(link)
            except:
                broken.append(link)
        if broken:
            issues.append(f"Broken links: {len(broken)} found")
        
        return {"url": url, "seo_issues": issues}
    except Exception as e:
        return {"url": url, "seo_issues": [f"Analysis error: {e}"]}

def generate_health_report(results, state):
    """Site sağlık raporu HTML oluştur."""
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{WORKSPACE}/raporlar/site_health/site_health_{today}.html"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    total = len(results)
    healthy = sum(1 for r in results if r["ok"])
    unhealthy = total - healthy
    
    # SEO issues toplamı
    total_seo_issues = sum(len(r.get("seo_issues", [])) for r in results)
    
    # HTML – Koyu mod, blog style (aynı template)
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Site Sağlık Raporu – {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0f172a; --card: #1e293b; --text-main: #f1f5f9; --text-muted: #94a3b8;
    --accent: #3b82f6; --success: #10b981; --danger: #ef4444; --border: #334155;
}}
body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text-main); line-height: 1.7; max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
header {{ margin-bottom: 48px; border-bottom: 1px solid var(--border); padding-bottom: 24px; }}
h1 {{ font-size: 2.5rem; font-weight: 700; margin: 0 0 12px 0; }}
.meta {{ color: var(--text-muted); font-size: 1rem; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px 24px; margin: 16px 0; }}
.card-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }}
.stat {{ font-size: 2rem; font-weight: 700; color: var(--accent); }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
ul {{ list-style: none; padding: 0; }}
li {{ padding: 8px 0; border-bottom: 1px solid var(--border); }}
li:last-child {{ border-bottom: none; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 0.85rem; font-weight: 600; }}
.badge.danger {{ background: var(--danger); color: white; }}
.badge.success {{ background: var(--success); color: white; }}
footer {{ margin-top: 80px; text-align: center; color: var(--text-muted); font-size: 0.9rem; border-top: 1px solid var(--border); padding-top: 20px; }}
</style>
</head>
<body>
<header>
    <h1>🛡️ Site Sağlık Raporu</h1>
    <p class="meta">Oluşturulma: {today} • OpenClaw Heartbeat Agent • GitHub Pages İzleme</p>
</header>

<section class="card">
    <div class="card-title">📊 Genel Durum</div>
    <p>Toplam Sayfa: <span class="stat">{total}</span></p>
    <p>Sağlam: <span class="stat" style="color: var(--success);">{healthy}</span></p>
    <p>Sorunlu: <span class="stat" style="color: var(--danger);">{unhealthy}</span></p>
    <p>SEO Sorunları: <span class="stat" style="color: var(--danger);">{total_seo_issues}</span></p>
</section>

{"<section class='card'><div class='card-title'>❌ Sorunlu Sayfalar</div><ul>" + "".join([f'<li><a href="{r["url"]}" target="_blank">{r["url"]}</a> – Status: {r["status"]} – Load: {r["load_time"]}s</li>' for r in results if not r["ok"]]) + "</ul></section>" if unhealthy > 0 else "<section class='card'><div class='card-title'>✅ Tüm Sayfalar Sağlam</div><p>Hiçbir sorun tespit edilmedi.</p></section>"}

{"<section class='card'><div class='card-title'>🔍 SEO Sorunları</div><ul>" + "".join([f'<li><a href="{r["url"]}" target="_blank">{r["url"]}</a>: {", ".join(r["seo_issues"])}</li>' for r in results if r.get("seo_issues")]) + "</ul></section>" if total_seo_issues > 0 else ""}

<footer>
    Bu rapor otomatik olarak üretilmiştir. • Heartbeat Agent • {today}
</footer>
</body>
</html>'''
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Sağlık raporu oluşturuldu: {report_path}")
    return report_path

def push_and_verify(report_path):
    """Push to GitHub Pages (raporlar/site_health/) with cache bust."""
    filename = os.path.basename(report_path)
    public_url = f"{GITHUB_PAGES_BASE}/raporlar/site_health/{filename}"
    repo_root = WORKSPACE
    
    try:
        # Ensure file exists
        if not os.path.exists(report_path):
            print(f"❌ Report not found: {report_path}")
            return None
        
        # Cache bust: remove old from git (if tracked)
        try:
            subprocess.run(["git","rm","-f","--cached",report_path], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","commit","-m",f"Remove old {filename} (cache bust)"], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git","push","raporlar","main"], cwd=repo_root, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🗑️ Cache bust: removed old {filename}")
            time.sleep(3)
        except Exception:
            pass
        
        # Add and push new
        subprocess.run(["git","add",report_path], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m",f"Add site health report {filename}"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pushed health report")
        
        # Verify
        for attempt in range(1, 4):
            time.sleep(30)
            try:
                r = requests.head(public_url, timeout=10)
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
    print("🫀 Site Sağlık Kontrolü başlatılıyor...")
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Tüm HTML dosyalarını bul
    urls = find_all_html_files()
    print(f"🔍 {len(urls)} HTML dosyası bulundu")
    
    # 2. Paralel kontrol et ( ThreadPool )
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)
    
    # 3. SEO analizi (parallel)
    with ThreadPoolExecutor(max_workers=3) as executor:
        for future in as_completed(executor.submit(analyze_seo, r["url"]) for r in results):
            seo_result = future.result()
            # merge seo issues into results
            for r in results:
                if r["url"] == seo_result["url"]:
                    r["seo_issues"] = seo_result["seo_issues"]
    
    # 4. Sorunlu olanları tespit et
    unhealthy = [r for r in results if not r["ok"]]
    healthy = len(results) - len(unhealthy)
    
    # 5. Alert gönder (eğer sorun varsa)
    if unhealthy:
        alert_msg = f"🚨 SITE SAĞLIK SORUNU – {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for r in unhealthy[:5]:  # İlk 5 sorun
            alert_msg += f"• {r['url']} – Status: {r.get('status','???')} – Load: {r.get('load_time','???')}s\n"
        if len(unhealthy) > 5:
            alert_msg += f"...ve {len(unhealthy)-5} daha\n"
        alert_msg += f"\nToplam {len(unhealthy)} sorunlu sayfa."
        
        sent = send_telegram_alert(alert_msg)
        if sent:
            print("📨 Telegram alert gönderildi")
    else:
        print("✅ Tüm sayfalar sağlam")
    
    # 6. Rapor oluştur ve push
    report_path = generate_health_report(results, state)
    public_url = push_and_verify(report_path)
    
    # 7. State güncelle
    state["last_run"] = datetime.now().isoformat()
    state["performance_history"][today] = {
        "total": len(urls),
        "healthy": healthy,
        "unhealthy": len(unhealthy)
    }
    save_state(state)
    
    if public_url:
        print(f"📊 Sağlık raporu: {public_url}")
    else:
        print("⚠️ Rapor push edilemedi")

if __name__ == "__main__":
    main()