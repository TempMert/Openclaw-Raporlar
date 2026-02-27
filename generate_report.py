#!/usr/bin/env python3
"""Generate mobile-friendly HTML accordion report and push to public repo."""

import json, datetime, os, subprocess, sys

def push_to_public_repo(html_path):
    """Push HTML file to the public 'raporlar' remote."""
    try:
        subprocess.run(["git", "add", html_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        subprocess.run(["git", "commit", "-m", f"Add report {today}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        subprocess.run(["git", "push", "raporlar", "main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        print(f"🚀 Pushed to public repo")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Push failed (maybe repo not created yet?): {e}")
        return False

# Input
today = datetime.datetime.now().strftime("%Y-%m-%d")
json_path = f"/home/openclaw/.openclaw/workspace/raporlar/{today}_rapor.json"
out_dir = "/home/openclaw/.openclaw/workspace/raporlar"
html_path = f"{out_dir}/{today}_rapor.html"

if not os.path.exists(json_path):
    print(f"JSON not found: {json_path}")
    # Alert user: maybe run fetch_tweets first
    sys.exit(1)

with open(json_path) as f:
    data = json.load(f)

# HTML template (mobile-friendly)
html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Günlük AI Haberleri – {today}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background: #f5f7fa; color: #333; line-height: 1.6; }}
  .container {{ max-width: 800px; margin: 0 auto; padding: 16px; }}
  header {{ text-align: center; padding: 24px 0; }}
  h1 {{ color: #2c3e50; margin: 0; font-size: 1.6em; }}
  .subtitle {{ color: #7f8c8d; font-size: 0.9em; margin-top: 4px; }}
  details {{ background: white; border-radius: 10px; margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }}
  summary {{ padding: 14px 16px; cursor: pointer; font-weight: 600; color: #2c3e50; background: #fafafa; list-style: none; display: flex; align-items: center; justify-content: space-between; }}
  summary::-webkit-details-marker {{ display: none; }}
  summary::after {{ content: "+"; font-size: 1.2em; color: #3498db; }}
  details[open] summary::after {{ content: "-"; }}
  .content {{ padding: 16px; border-top: 1px solid #eee; }}
  .item {{ margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px dashed #eee; }}
  .item:last-child {{ border: none; margin: 0; padding: 0; }}
  .item h4 {{ margin: 0 0 6px; font-size: 1em; color: #2980b9; }}
  .item p {{ margin: 0 0 6px; color: #555; font-size: 0.95em; }}
  .item a {{ color: #27ae60; text-decoration: none; word-break: break-all; }}
  .item a:hover {{ text-decoration: underline; }}
  footer {{ text-align: center; padding: 24px; color: #95a5a6; font-size: 0.85em; }}
</style>
</head>
<body>
<div class="container">
<header>
<h1>📡 AI Haber Raporu</h1>
<div class="subtitle">{today}</div>
</header>
'''

icons = {"OpenClaw": "🦀", "VibeCoding": "🎸", "NanoBanana": "🍌"}

for category, items in data.items():
    if not items:
        continue
    html += f'''
<details>
<summary>{icons.get(category, "•")} {category} ({len(items)})</summary>
<div class="content">'''
    for item in items:
        title = item.get("title", "Başlık yok")
        content = item.get("content", "")
        url = item.get("url", "#")
        html += f'''
<div class="item">
<h4>{title}</h4>
<p>{content}</p>
<a href="{url}" target="_blank">🔗 Oku</a>
</div>'''
    html += '''
</div>
</details>'''

html += f'''
<footer>
Rapor oluşturuldu: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} • Tavily API
</footer>
</div>
</body>
</html>'''

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML report generated: {html_path} ({len(data)} categories)")

# Push to public repo
push_to_public_repo(html_path)
