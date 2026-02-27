#!/usr/bin/env python3
from weasyprint import HTML, CSS
import markdown

md_path = "/home/openclaw/.openclaw/workspace/raporlar/openclaw_twitter_otomasyonlari_test.md"
pdf_path = md_path.replace(".md", ".pdf")

with open(md_path) as f:
    html_content = markdown.markdown(f.read(), extensions=['extra', 'toc'])

html_full = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>OpenClaw Twitter Otomasyonları</title>
  <style>
    body {{ font-family: 'DejaVu Sans', sans-serif; margin: 2cm; line-height: 1.6; }}
    h1 {{ color: #f4793b; border-bottom: 3px solid #f4793b; padding-bottom: 10px; }}
    h2 {{ color: #7c4a1e; margin-top: 2em; }}
    ul {{ margin-left: 1.5em; }}
    strong {{ color: #d97706; }}
    .meta {{ color: #666; font-size: 0.9em; margin-bottom: 30px; }}
    .section {{ margin-bottom: 40px; page-break-inside: avoid; }}
    @page {{ margin: 2cm; }}
  </style>
</head>
<body>
<h1>OpenClaw İçin Twitter Otomasyonları - Top 5</h1>
<div class="meta">
  <p><strong>Hazırlayan:</strong> Claw (OpenClaw Assistant)</p>
  <p><strong>Tarih:</strong> 26 Şubat 2025</p>
  <p><strong>Periyot:</strong> 3 günde bir</p>
  <p><strong>Dil:</strong> Türkçe</p>
</div>
{html_content}
</body>
</html>
"""

try:
    HTML(string=html_full).write_pdf(pdf_path)
    print(f"✅ PDF created: {pdf_path}")
except Exception as e:
    print(f"❌ PDF error: {e}")
