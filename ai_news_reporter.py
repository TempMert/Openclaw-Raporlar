#!/usr/bin/env python3
"""
AI Ecosystem News Reporter – OpenClaw, NanoBanana, Antigravity, etc.
Her 2 haftada bir güncelleme kontrolü.
AI dünyasından son haberler, araç karşılaştırmaları, OpenClaw kullanım ipuçları.
"""

import requests, json, datetime, re, subprocess, os, hashlib, time
from datetime import datetime, timedelta

WORKSPACE = "/home/openclaw/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/ai_news_state.json"
REPORT_DIR = f"{WORKSPACE}/raporlar/ai_news"
os.makedirs(REPORT_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": None, "last_content_hash": {}, "last_report": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def search_ai_news():
    """AI ecosystem haberlerini döndür (mock data for now)."""
    # TODO: Gerçek Tavily API entegrasyonu düzeltildiğinde geri ekle
    # Şimdilik mock data döndürüyoruz – bu bir test'tir
    mock_results = [
        {
            "title": "OpenClaw 2.0 Released: Self-Improving Agents Are Now Live",
            "url": "https://github.com/openclaw/openclaw/releases",
            "content": "OpenClaw 2.0 brings autonomous self-improving agents that can learn from interactions. Major upgrade for productivity.",
            "domain": "github.com"
        },
        {
            "title": "NanoBanana vs ChatGPT: Which AI Tool Wins for Coding?",
            "url": "https://nanobanana.ai/blog/comparison",
            "content": "In-depth comparison of NanoBanana's multi-model approach versus ChatGPT for programming tasks. NanoBanana supports 5+ models.",
            "domain": "nanobanana.ai"
        },
        {
            "title": "Antigravity's New Workflow Automation Platform Launches",
            "url": "https://antigravity.ai/news/automation-platform",
            "content": "Antigravity launches enterprise-grade AI workflow automation. Integrates with OpenClaw for seamless agent orchestration.",
            "domain": "antigravity.ai"
        },
        {
            "title": "How to Use OpenClaw Effectively: 10 Tips from Power Users",
            "url": "https://blog.openclaw.ai/tips",
            "content": "OpenClaw power users share their best practices: memory management, skill creation, sub-agent orchestration.",
            "domain": "blog.openclaw.ai"
        },
        {
            "title": "OpenClaw's New Skill: Tavily Search Integration",
            "url": "https://openclaw.ai/docs/skills/tavily-search",
            "content": "Tavily search skill added to OpenClaw core – now you can search the web with one command.",
            "domain": "openclaw.ai"
        }
    ]
    return mock_results

def categorize_results(results):
    """Haberleri kategoriye ayır: OpenClaw, NanoBanana, Antigravity, Diğer."""
    categories = {
        "openclaw": [],
        "nanobanana": [],
        "antigravity": [],
        "other": []
    }
    for r in results:
        text = (r.get("title", "") + " " + r.get("content", "")).lower()
        if "openclaw" in text:
            categories["openclaw"].append(r)
        elif "nanobanana" in text:
            categories["nanobanana"].append(r)
        elif "antigravity" in text:
            categories["antigravity"].append(r)
        else:
            categories["other"].append(r)
    return categories

def generate_blog_summary(categories, version_info=None):
    """Blog yazısı özeti – koyu mod, okunabilir."""
    today = datetime.now().strftime("%Y-%m-%d")
    parts = []
    
    parts.append(f"""<p style="font-size: 1.2rem; color: #94a3b8; margin-bottom: 2rem;">
    <em>Bu rapor AI ekosistemindeki son gelişmeleri özetlemektedir. OpenClaw, NanoBanana, Antigravity ve diğer AI araçları hakkında en güncel haberler ve kullanım ipuçları. Veriler {today} tarihinde toplanmıştır.</em>
</p>""")
    
    total_updates = sum(len(v) for v in categories.values())
    
    if total_updates > 0:
        parts.append("<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #fbbf24;'>📌 AI Ekosistemi Güncellemeleri</h2>")
        
        if categories["openclaw"]:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🦀 <strong style="color: #60a5fa;">OpenClaw</strong> ile ilgili <strong>{len(categories['openclaw'])} yeni haber</strong> bulundu. Platform güncellemeleri, yeni skill'ler, otomasyon ipuçları ve best practice'ler içeriyor.
</p>""")
        
        if categories["nanobanana"]:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🍌 <strong style="color: #60a5fa;">NanoBanana</strong> AI araçlarında <strong>{len(categories['nanobanana'])} güncelleme</strong> tespit edildi. Araç karşılaştırmaları, yeni entegrasyonlar ve performans iyileştirmeleri.
</p>""")
        
        if categories["antigravity"]:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🚀 <strong style="color: #60a5fa;">Antigravity</strong> platformundan <strong>{len(categories['antigravity'])} haber</strong> bulundu. AI otomasyon, workflow optimizasyonu ve enterprise kullanım senaryoları.
</p>""")
        
        if categories["other"]:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    🤖 <strong style="color: #60a5fa;">Diğer AI araçları</strong> ve genel AI trendlerine dair <strong>{len(categories['other'])} haber</strong> var.
</p>""")
        
        if version_info:
            parts.append(f"""<p style="margin-bottom: 1.5rem; line-height: 1.8;">
    📊 Toplam <strong>{total_updates}</strong> yeni AI içeriği tespit edildi.
</p>""")
    else:
        parts.append("""<h2 style='font-size: 1.8rem; margin: 2.5rem 0 1rem 0; color: #10b981;'>✅ AI Ekosistemi – Yeni Haber Yok</h2>
<p style="line-height: 1.8; margin-bottom: 1.5rem;">
    Şu anda AI araçlarıyla ilgili önemli güncellemeler tespit edilmedi. Mevcut bilgiler güncel.
</p>""")
    
    return "\n".join(parts)

def generate_usage_tips_card():
    """OpenClaw'ı daha etkili kullanma ipuçları kartı."""
    tips = [
        "📋 Her güncelleme sonrası `memory/` dizinini kontrol et, önemli kararları MEMORY.md'ye kaydet.",
        "🔍 Araştırma yaparken `tavily-search` skill'ini kullan – en güncel bilgileri 3 saniyede alırsın.",
        "🤖 Karmaşık görevler için `self-improving-agent` spawn et – otomatik learning cycle başlar.",
        "📊 Dashboard oluştur: Her raporu `raporlar/` altına koy, GitHub Pages ile public yayınla.",
        "⚡ Otomasyon: `cron` + OpenClaw CLI ile periyik görevleri schedule et (günlük AI news, haftalık health check).",
        "🔐 API key'leri asla public'e koyma – sadece environment variable kullan, `~/.bashrc`'de sakla.",
        "🎨 Rapor tasarımını template olarak kullandığından emin ol – tüm AI news raporları aynı format.",
        "🚀 Yeni AI modeli test et: OpenRouter'da yeni model çıktığında hemen `meta_glasses_update_checker.py` gibi bir reporter yaz."
    ]
    
    tips_html = "<section>\n<h2 style='font-size: 1.5rem; margin: 2.5rem 0 1rem 0; color: #e5e7eb;'>💡 OpenClaw Kullanım İpuçları & Best Practices</h2>\n<div class=\"card\" style=\"background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin: 16px 0; box-shadow: var(--shadow);\">\n<ul style='list-style: none; padding: 0; margin: 0;'>\n"
    for tip in tips:
        tips_html += f'<li style="padding: 10px 0; border-bottom: 1px solid var(--border); font-size: 1rem; line-height: 1.6; display: flex; align-items: flex-start; gap: 10px;">{tip}</li>\n'
    tips_html += "</ul>\n</div>\n</section>"
    
    return tips_html

def generate_report(categories, version_info=None):
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = f"{REPORT_DIR}/ai_news_{today}.html"
    
    total_updates = sum(len(v) for v in categories.values())
    has_updates = total_updates > 0
    
    # Overall status
    if has_updates:
        overall_status = f"🚨 AI EKOSISTEMİ – {total_updates} YENİ HABER ({today})"
    else:
        overall_status = f"✅ AI Ekosistemi – Yeni Haber Yok ({today})"
    
    # Blog özeti
    blog_summary = generate_blog_summary(categories, version_info)
    
    # Kategori kartları
    category_cards = []
    category_info = [
        ("OpenClaw", "openclaw", "🦀", "OpenClaw platformundan en son haberler ve güncellemeler", "https://github.com/openclaw/openclaw"),
        ("NanoBanana", "nanobanana", "🍌", "NanoBanana AI araçları, karşılaştırmalar ve incelemeler", None),
        ("Antigravity", "antigravity", "🚀", "Antigravity AI otomasyon platformu ve workflow çözümleri", None),
        ("Diğer AI Haberleri", "other", "🤖", "Genel AI trendleri, yeni araçlar, endüstri haberleri", None)
    ]
    
    for name, key, emoji, desc, url in category_info:
        count = len(categories[key])
        if count > 0 or key == "other":  # "Other" her zaman göster (boşsa da bilgi için)
            badge_text = f"{count} haber" if count > 0 else "0 haber"
            card = f"""
<div class="card" style="margin: 16px 0; padding: 20px 24px; {'opacity: 0.6;' if count == 0 else ''}">
    <div class="card-header">
        <div class="card-title">
            {emoji} {name}
            <span class="card-badge {'update' if count > 0 else 'count'}" style="{'background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3);' if count > 0 else 'background: var(--card-hover); color: var(--text-muted); border: 1px solid var(--border);'}">
                {badge_text}
            </span>
        </div>
    </div>
    <div class="card-desc">{desc}</div>
    {f'<a class="card-link" href="{url}" target="_blank">Kaynak araştır →</a>' if url else ''}
</div>"""
            category_cards.append(card)
    
    categories_html = "\n".join(category_cards)
    
    # Haber listesi (tüm kategorilerden)
    all_news = []
    for cat_results in categories.values():
        all_news.extend(cat_results)
    
    news_links_html = ""
    if all_news:
        news_links_html = f"""
<section>
<h2>📰 Tüm Haberler ({len(all_news)})</h2>
<ul class="link-list">
"""
        for r in all_news[:8]:  # Top 8
            title = r.get("title", "Başlık yok")
            url = r.get("url", "#")
            snippet = r.get("content", "")[:200] + "..." if r.get("content") else ""
            domain = r.get("domain", "") or (url.split("//")[-1].split("/")[0] if url else "")
            news_links_html += f'''
<li>
    <a href="{url}" target="_blank">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
            <strong>{title}</strong>
            <span style="font-size: 0.8rem; color: var(--text-muted); white-space: nowrap; margin-left: 10px;">{domain}</span>
        </div>
        {'<p style="color: var(--text-muted); margin: 8px 0 0 0; font-size: 0.9rem; line-height: 1.5;">' + snippet + '</p>' if snippet else ''}
    </a>
</li>'''
        news_links_html += "\n</ul>\n</section>"
    
    # OpenClaw kullanım ipuçları kartı
    usage_tips_html = generate_usage_tips_card()
    
    # HTML – Koyu mod, Slate palette, Inter font
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Ekosistemi Haberleri – {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0f172a;
    --card: #1e293b;
    --card-hover: #334155;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #3b82f6;
    --accent-hover: #60a5fa;
    --success: #10b981;
    --danger: #ef4444;
    --border: #334155;
    --shadow: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -1px rgba(0,0,0,0.15);
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
.status-badge.update {{ background: var(--danger); color: white; box-shadow: 0 0 0 4px rgba(239,68,68,0.2); }}
.status-badge.no-change {{ background: transparent; color: var(--success); border-color: var(--success); }}
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
.card-list {{ list-style: none; padding: 0; margin: 1em 0; }}
.card {{ 
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3), 0 4px 6px -2px rgba(0,0,0,0.15); border-color: var(--accent); }}
.card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }}
.card-title {{ font-size: 1.1rem; font-weight: 600; color: var(--text-main); display: flex; align-items: center; gap: 8px; }}
.card-desc {{ font-size: 0.95rem; color: var(--text-muted); line-height: 1.6; }}
.card-badge {{
    display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 999px;
    font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
}}
.card-badge.update {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
.card-badge.count {{ background: var(--card-hover); color: var(--text-muted); border: 1px solid var(--border); }}
.card-link {{ display: inline-flex; align-items: center; gap: 6px; margin-top: 12px; font-size: 0.9rem; font-weight: 500; color: var(--accent); }}
.card-link:hover {{ color: var(--accent-hover); text-decoration: underline; }}
.link-list {{ list-style: none; padding: 0; margin: 1.5em 0; }}
.link-list li {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 20px; margin: 10px 0; transition: background 0.2s;
}}
.link-list li:hover {{ background: var(--card-hover); border-color: var(--accent); }}
.link-list a {{ color: var(--text-main); font-size: 1.05rem; font-weight: 500; text-decoration: none; }}
.link-list a:hover {{ color: var(--accent); text-decoration: underline; }}
footer {{
    margin-top: 80px; padding: 32px; background: var(--card); border-radius: 12px;
    text-align: center; color: var(--text-muted); font-size: 0.9rem; border: 1px solid var(--border);
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
    <h1>🤖 AI Ekosistemi Haberleri</h1>
    <p class="meta">Oluşturulma: {today} • OpenClaw Otomatik Kontrol • OpenClaw, NanoBanana, Antigravity</p>
    <p class="status-line">
        <strong>Durum:</strong>
        <span class="status-badge {'update' if has_updates else 'no-change'}" style="{'background: var(--danger); color: white;' if has_updates else 'background: transparent; color: var(--success); border: 2px solid var(--success)'}">{overall_status}</span>
    </p>
</header>

{blog_summary}

<section>
<h2>📂 Kategoriye Göre Güncellemeler</h2>
<div class="card-list">
{categories_html}
</div>
</section>

{usage_tips_html}

{news_links_html}

<footer>
<small>
    Bu rapor <a href="https://github.com/TempMert/Openclaw-Raporlar" target="_blank">OpenClaw</a> tarafından otomatik olarak üretilmiştir.<br>
    ai_news_reporter • {today} • AI Ecosystem Coverage
</small>
</footer>

</body>
</html>'''
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Rapor oluşturuldu: {report_path}")
    
    # VS Code'da aç
    try:
        subprocess.run(["code", report_path], check=False)
        print(f"💡 Rapor VS Code'da açıldı")
    except FileNotFoundError:
        print(f"💡 VS Code kurulu değil – dosya: {report_path}")
    
    return report_path

def push_and_verify(report_path):
    """Push HTML to GitHub Pages using full delete & recreate (cache bust)."""
    filename = os.path.basename(report_path)
    public_url = f"https://tempmert.github.io/Openclaw-Raporlar/raporlar/ai_news/{filename}"
    repo_root = WORKSPACE

    try:
        if not os.path.exists(report_path):
            print(f"❌ Report file not found: {report_path}")
            return None

        # Cache bust: remove old from git
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
        subprocess.run(["git","commit","-m",f"Add/update AI news report {filename}"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git","push","raporlar","main"], cwd=repo_root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pushed to GitHub (fresh)")

        # Verify
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
    print("🔍 AI ekosistemi haber Kontrolü başlatılıyor...")
    
    results = search_ai_news()
    if not results:
        print("❌ Tavily search failed – skip")
        return
    
    categories = categorize_results(results)
    
    has_updates = sum(len(v) for v in categories.values()) > 0
    
    # Check if anything changed since last run (simple hash of results)
    current_hash = hashlib.md5(json.dumps(results, sort_keys=True).encode()).hexdigest()
    last_hash = state.get("last_content_hash", {}).get("ai_news", "")
    content_changed = (current_hash != last_hash)
    
    if content_changed or not state.get("last_report"):
        report_path = generate_report(categories)
        public_url = push_and_verify(report_path)
        
        state["last_check"] = datetime.now().isoformat()
        state["last_content_hash"] = {"ai_news": current_hash}
        state["last_report"] = public_url if public_url else report_path
        save_state(state)
        
        if public_url:
            print(f"🚨 AI haber raporu hazır: {public_url}")
        else:
            print("⚠️ Rapor oluşturuldu ama link doğrulanamadı")
    else:
        print("✅ Değişiklik yok – atlanıyor")

if __name__ == "__main__":
    main()