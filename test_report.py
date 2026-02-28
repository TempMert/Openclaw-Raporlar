#!/usr/bin/env python3
"""Validate generated HTML report structure and functionality."""

import re, sys, os
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
html_path = f"/home/openclaw/.openclaw/workspace/raporlar/{today}_rapor.html"

if not os.path.exists(html_path):
    print(f"❌ HTML not found: {html_path}")
    sys.exit(1)

with open(html_path) as f:
    html = f.read()

errors = []
warnings = []

# 1. Category cards count (should be 4)
cards = re.findall(r'<div class="category-card"', html)
if len(cards) != 4:
    errors.append(f"Expected 4 category cards, got {len(cards)}")
else:
    print(f"✅ Found 4 category cards")

# 2. Articles sections count (should be 4)
articles = re.findall(r'<div class="articles" id="articles-', html)
if len(articles) != 4:
    errors.append(f"Expected 4 articles sections, got {len(articles)}")
else:
    print(f"✅ Found 4 articles sections")

# 3. Each category should have articles
expected_cats = ["OpenClaw", "VibeCoding", "NanoBanana", "Antigravity"]
for cat in expected_cats:
    pattern = rf'<div class="articles" id="articles-{cat}">(.*?)</div>'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        errors.append(f"Missing articles section for {cat}")
    else:
        inner = m.group(1)
        inner_cards = re.findall(r'<article class="post"', inner)
        if inner_cards:
            print(f"✅ {cat}: {len(inner_cards)} article cards")
        else:
            errors.append(f"No article cards in {cat}")

# 4. Check that category-card has onclick calling toggleCategory
for cat in expected_cats:
    if f'onclick="toggleCategory(\'{cat}\')"' not in html:
        warnings.append(f"Category card for {cat} may not have onclick toggleCategory")

# 5. Check JS functions exist
js_functions = ['toggleCategory', 'toggleTheme', 'toggleFavorite', 'toggleFavPanel']
for func in js_functions:
    if f'function {func}(' not in html:
        errors.append(f"Missing JS function: {func}")

# 6. Check CSS for articles open style
if re.search(r'\.articles\s*\{[^}]*display:\s*none', html):
    if re.search(r'\.articles\.active\s*\{[^}]*display:\s*block', html):
        print("✅ CSS: articles hidden by default, shown when active")
    else:
        errors.append("Missing CSS: .articles.active { display:block; }")
else:
    warnings.append("Articles default display may not be none")

# 7. Check for Turkish translation markers (common Turkish characters)
turkish_chars = ['ı', 'ğ', 'ü', 'ş', 'ö', 'ç', 'İ', 'Ğ', 'Ü', 'Ş', 'Ö', 'Ç']
found_turkish = any(c in html for c in turkish_chars)
if found_turkish:
    print("✅ Turkish characters detected")
else:
    warnings.append("No Turkish characters found – content may still be English")

# 8. Check that toggleTheme function uses localStorage
if 'localStorage.setItem(\'theme\'' in html:
    print("✅ Theme toggle uses localStorage")
else:
    warnings.append("Theme toggle may not persist")

# 9. Check that favorite toggle uses localStorage
if 'localStorage.setItem(\'favorites\'' in html:
    print("✅ Favorites use localStorage")
else:
    warnings.append("Favorites may not persist")

# 10. Check that fav panel toggle exists
if 'toggleFavPanel()' in html:
    print("✅ Favorites panel toggle exists")
else:
    errors.append("Missing favorites panel toggle")

# Summary
print("\n--- Validation Summary ---")
if errors:
    print(f"❌ {len(errors)} error(s):")
    for e in errors:
        print(f"   - {e}")
if warnings:
    print(f"⚠️  {len(warnings)} warning(s):")
    for w in warnings:
        print(f"   - {w}")

if errors:
    print("\n❌ Report validation FAILED")
    sys.exit(1)
else:
    print("\n✅ Report validation PASSED")
    sys.exit(0)
