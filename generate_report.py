#!/usr/bin/env python3
"""
AI News Blog – Full Turkish, clean content, key rotation, exclusive accordion.
"""

import json, os, re, hashlib, subprocess, sys
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
json_path = f"/home/openclaw/.openclaw/workspace/raporlar/{today}_rapor.json"
out_dir = "/home/openclaw/.openclaw/workspace/raporlar"
html_path = f"{out_dir}/{today}_rapor.html"

if not os.path.exists(json_path):
    print(f"JSON not found: {json_path}")
    sys.exit(1)

with open(json_path) as f:
    data = json.load(f)

categories = ["OpenClaw", "VibeCoding", "NanoBanana", "Antigravity"]
icons = {"OpenClaw":"🦀","VibeCoding":"🎸","NanoBanana":"🍌","Antigravity":"🚀"}

def clean_text(text):
    if not text: return ""
    # Remove URLs, emails, HTML tags
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
    text = re.sub(r'<(script|style).*?>.*?</\1>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_images(raw):
    return re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', raw, re.IGNORECASE) if raw else []

def translate_batch(texts, key_index=0):
    if not any(texts): return texts
    OPENROUTER_KEYS = [
        os.getenv("OPENROUTER_KEY_1", "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"),
        os.getenv("OPENROUTER_KEY_2", "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"),
        os.getenv("OPENROUTER_KEY_3", "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")
    ]
    OPENROUTER_MODELS = [
        "stepfun/step-3.5-flash:free",
        "openrouter/auto",
        "nvidia/nemotron-3-nano-30b-a3b:free"
    ]
    for i in range(len(OPENROUTER_KEYS)):
        key = OPENROUTER_KEYS[(key_index + i) % len(OPENROUTER_KEYS)]
        model = OPENROUTER_MODELS[(key_index + i) % len(OPENROUTER_MODELS)]
        try:
            import requests
            numbered = []
            for idx, t in enumerate(texts, 1):
                if t and len(t) > 5:
                    numbered.append(f"{idx}. {t[:1000]}")
                else:
                    numbered.append(f"{idx}. (empty)")
            prompt = "Aşağıdaki İngilizce metinleri Türkçeye çevir. Anlamı koru, profesyonel ve anlaşılır olsun. Sadece numaralı cevap ver. Örnek: 1. Çeviri\n2. Çeviri\n\n" + "\n".join(numbered)
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                              json={
                                  "model": model,
                                  "messages": [{"role":"user","content":prompt}],
                                  "temperature": 0.3,
                                  "max_tokens": 2500
                              }, timeout=60)
            if r.status_code == 200:
                resp = r.json()
                content = resp["choices"][0]["message"]["content"]
                translations = {}
                for line in content.splitlines():
                    m = re.match(r'(\d+)\.\s*(.+)', line.strip())
                    if m:
                        translations[int(m.group(1))-1] = m.group(2)
                result = []
                for j in range(len(texts)):
                    result.append(translations.get(j, texts[j]))
                print(f"✅ Batch ok: {model} (key-index {(key_index+i)%len(OPENROUTER_KEYS)})")
                return result
            else:
                print(f"⚠️ Key {key[:8]}... model {model} err {r.status_code}")
                continue
        except Exception as e:
            print(f"⚠️ Trans fail key {key[:8]}...: {e}")
            continue
    print("❌ Tüm key'ler batch translation için başarısız")
    return texts

# Process
processed = {}
all_texts = []
items_by_cat = {}

for cat in categories:
    items = data.get(cat, [])[:5]
    items_by_cat[cat] = []
    for it in items:
        title = it.get("title", "Başlık yok")
        url = it.get("url", "#")
        raw = it.get("raw_content")
        content = it.get("content", "")
        images = extract_images(raw)[:1] if raw else []
        # Clean full text
        if raw and len(raw) > 200:
            full_text = clean_text(raw)
        else:
            full_text = clean_text(content)
        items_by_cat[cat].append({
            "title": title,
            "url": url,
            "full_text": full_text[:3000],
            "image": images[0] if images else None
        })
        all_texts.append(full_text[:1500])

# Batch translate with rotation
translations = translate_batch(all_texts, key_index=0)

# Map back
idx = 0
for cat in categories:
    proc_items = []
    for it in items_by_cat[cat]:
        full_tr = translations[idx] if idx < len(translations) else it["full_text"]
        idx += 1
        if not full_tr or len(full_tr) < len(it["full_text"])*0.5:
            full_tr = it["full_text"]  # fallback English cleaned
        proc_items.append({
            "title": it["title"],
            "url": it["url"],
            "full_text": full_tr,
            "image": it["image"]
        })
    processed[cat] = proc_items

# HTML (Blog format)
html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Haber Raporu – {today}</title>
<style>
:root {{ --bg:#f8f9fa; --card:#fff; --text:#2d3748; --muted:#718096; --accent:#3182ce; --border:#e2e8f0; --shadow:rgba(0,0,0,0.08); }}
[data-theme="dark"] {{ --bg:#1a202c; --card:#2d3748; --text:#e2e8f0; --muted:#a0aec0; --accent:#63b3ed; --border:#4a5568; --shadow:rgba(0,0,0,0.3); }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:0; background:var(--bg); color:var(--text); font-family:"Merriweather","Georgia",serif; line-height:1.8; }}
.container {{ max-width:800px; margin:0 auto; padding:24px 16px; }}
header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:32px; padding-bottom:16px; border-bottom:1px solid var(--border); }}
h1 {{ margin:0; font-size:1.8em; color:var(--text); font-weight:700; }}
.controls {{ display:flex; gap:12px; align-items:center; }}
.theme-toggle, .fav-toggle {{ background:var(--card); border:1px solid var(--border); border-radius:50%; width:44px; height:44px; cursor:pointer; font-size:1.4em; display:flex; align-items:center; justify-content:center; }}
.hero {{ text-align:center; margin-bottom:32px; color:var(--muted); font-size:1.1em; }}
.categories {{ display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin-bottom:40px; }}
.category-card {{ background:var(--card); border:1px solid var(--border); border-radius:16px; padding:18px 20px; width:180px; text-align:center; cursor:pointer; box-shadow:0 2px 6px var(--shadow); transition:transform 0.2s, box-shadow 0.2s; }}
.category-card:hover {{ transform:translateY(-3px); box-shadow:0 6px 12px var(--shadow); }}
.category-card .icon {{ font-size:2.2em; margin-bottom:6px; }}
.category-card h3 {{ margin:0; font-size:1em; color:var(--accent); font-weight:600; }}
.category-card.active {{ border-color:var(--accent); background:var(--bg); }}
.articles {{ display:none; margin-top:16px; }}
.articles.active {{ display:block; }}
.post {{ background:var(--card); border:1px solid var(--border); border-radius:14px; padding:24px; margin-bottom:24px; box-shadow:0 2px 8px var(--shadow); }}
.post h2 {{ margin:0 0 12px; font-size:1.4em; color:var(--accent); line-height:1.3; }}
.post h2 a {{ color:var(--accent); text-decoration:none; }}
.post h2 a:hover {{ text-decoration:underline; }}
.post .meta {{ font-size:0.85em; color:var(--muted); margin-bottom:16px; display:flex; justify-content:space-between; }}
.post img {{ max-width:100%; height:auto; border-radius:8px; margin:12px 0; }}
.post .content {{ line-height:1.8; font-size:1.05em; }}
.post .content p {{ margin:0 0 1.2em; }}
.fav-btn {{ background:none; border:none; cursor:pointer; font-size:1.3em; opacity:0.6; position:absolute; top:12px; right:12px; }}
.fav-btn.active {{ opacity:1; color:#e53e3e; }}
.post-position {{ position:relative; }}
footer {{ text-align:center; margin-top:40px; color:var(--muted); font-size:0.9em; }}
@media (max-width:600px) {{ .container {{ padding:12px; }} h1 {{ font-size:1.5em; }} .category-card {{ width:100%; }} .post {{ padding:16px; }} }}
</style>
</head>
<body>
<div class="container">
<header>
<h1>📡 AI Haber Raporu – {today}</h1>
<div class="controls">
<button class="fav-toggle" title="Favoriler" onclick="toggleFavPanel()">❤️</button>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Tema">🌙</button>
</div>
</header>
<div class="hero">Son 7 gündeki en önemli AI haberleri – Türkçe blog</div>

<!-- Favori Paneli -->
<div id="fav-panel" style="display:none; margin-bottom:24px; padding:16px; background:var(--card); border:1px solid var(--border); border-radius:12px;">
<h2 style="margin-top:0;">Beğendiğiniz Haberler</h2>
<div id="fav-list"></div>
</div>

<!-- Kategori Kartları -->
<div class="categories">
'''

for cat in categories:
    icon = icons.get(cat, "•")
    html += f'''<div class="category-card" onclick="toggleCategory('{cat}')">
<div class="icon">{icon}</div>
<h3>{cat}</h3>
</div>
'''
html += '''</div>

<!-- Blog Posts -->
'''

for cat in categories:
    items = processed.get(cat, [])
    html += f'<div class="articles" id="articles-{cat}">\n'
    if not items:
        html += f'<div class="post"><p>Bu hafta {cat} hakkında yeni haber bulunamadı.</p></div>\n'
    else:
        for it in items:
            title = it["title"]
            url = it["url"]
            full_text = it["full_text"]
            image = it["image"]
            item_id = hashlib.md5(url.encode()).hexdigest()[:8]
            html += f'<article class="post" data-id="{item_id}">\n'
            html += f'<div class="post-position">\n'
            html += f'<h2><a href="{url}" target="_blank">{title}</a></h2>\n'
            html += f'<button class="fav-btn" onclick="toggleFavorite(\'{item_id}\')">🤍</button>\n'
            html += '</div>\n'
            if image:
                html += f'<img src="{image}" alt="" class="max-w">\n'
            html += f'<div class="meta"><span>📅 {today}</span> <span>{cat}</span></div>\n'
            for para in full_text.split('\n\n'):
                if para.strip():
                    html += f'<p class="content">{para.strip()}</p>\n'
            html += '</article>\n'
    html += '</div>\n'

html += '''<footer>
Rapor otomatik oluşturuldu • OpenRouter AI • GitHub Pages
</footer>

<script>
function toggleTheme() {
  const b = document.body;
  const t = b.getAttribute('data-theme');
  const n = t === 'dark' ? 'light' : 'dark';
  b.setAttribute('data-theme', n);
  localStorage.setItem('theme', n);
}
function toggleCategory(cat) {
  const articles = document.getElementById('articles-' + cat);
  if (articles) {
    const isOpen = articles.classList.contains('active');
    document.querySelectorAll('.articles').forEach(el => el.classList.remove('active'));
    if (!isOpen) articles.classList.add('active');
  }
}
function toggleFavorite(id) {
  const card = document.querySelector(`[data-id="${id}"]`);
  const btn = card.querySelector('.fav-btn');
  const isActive = btn.classList.toggle('active');
  btn.textContent = isActive ? '❤️' : '🤍';
  const favs = JSON.parse(localStorage.getItem('favorites') || '{}');
  favs[id] = isActive;
  localStorage.setItem('favorites', JSON.stringify(favs));
  updateFavPanel();
}
function toggleFavPanel() {
  const panel = document.getElementById('fav-panel');
  panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
  if (panel.style.display === 'block') updateFavPanel();
}
function updateFavPanel() {
  const favs = JSON.parse(localStorage.getItem('favorites') || '{}');
  const list = document.getElementById('fav-list');
  list.innerHTML = '';
  Object.entries(favs).forEach(([id, on]) => {
    if (on) {
      const card = document.querySelector(`[data-id="${id}"]`);
      if (card) {
        const title = card.querySelector('h2 a').textContent;
        const link = card.querySelector('h2 a').href;
        const item = document.createElement('div');
        item.style.padding = '8px 0';
        item.innerHTML = `<a href="${link}" target="_blank">${title}</a>`;
        list.appendChild(item);
      }
    }
  });
  if (list.children.length === 0) {
    list.innerHTML = '<p style="color:var(--muted);">Henüz favori haber eklemediniz.</p>';
  }
}

// Init
document.body.setAttribute('data-theme', localStorage.getItem('theme') || 'light');
const favs = JSON.parse(localStorage.getItem('favorites') || '{}');
Object.entries(favs).forEach(([id, on]) => {
  const card = document.querySelector(`[data-id="${id}"]`);
  if (card) {
    const btn = card.querySelector('.fav-btn');
    btn.textContent = '❤️';
    btn.classList.add('active');
  }
});
</script>
</div>
</body>
</html>'''

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Blog report generated: {html_path} ({sum(len(v) for v in processed.values())} posts)")

# Push
try:
    subprocess.run(["git","add",html_path], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git","commit","-m",f"Update blog {today}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git","push","raporlar","main"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("🚀 Pushed")
except Exception as e:
    print(f"Push error: {e}")
