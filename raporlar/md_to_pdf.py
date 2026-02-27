#!/usr/bin/env python3
import markdown
from weasyprint import HTML, CSS

md_path = "/home/openclaw/.openclaw/workspace/raporlar/openclaw_twitter_otomasyonlari_test.md"
pdf_path = md_path.replace(".md", ".pdf")

with open(md_path) as f:
    html_content = markdown.markdown(f.read(), extensions=['extra', 'toc'])

# Add basic styling
html_full = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'DejaVu Sans', sans-serif; margin: 2cm; }}
    h1 {{ color: #f4793b; border-bottom: 2px solid #f4793b; padding-bottom: 5px; }}
    h2 {{ color: #7c4a1e; margin-top: 1.5em; }}
    ul {{ margin-left: 1.5em; }}
    strong {{ color: #d97706; }}
  </style>
</head>
<body>
{html_content}
</body>
</html>
"""

HTML(string=html_full).write_pdf(pdf_path)
print(f"✅ PDF created: {pdf_path}")
