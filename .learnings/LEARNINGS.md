## LEARNINGS

### 2026-02-28: Rate Limit 429 on OpenRouter Nemotron Free
- **Problem:** NVIDIA Nemotron 3 Nano 30B:free modeli ücretsiz kullanımda batch translation yapınca 429 rate limit hatası alıyorum.
- **Root cause:** OpenRouter free tier'da her modelin kendi rate limit'i var; batch request'te token limiti aşılıyor.
- **Solution (planned):** Implement key rotation across 3 OpenRouter keys (Qwen, Stepfun, Nemotron). Use smaller batches (max 5 texts per call). Fallback to English when all keys fail.
- **Code:** `generate_report.py` `translate_batch()` fonksiyonunu güncelle.

### 2026-02-28: Accordion Toggle UX Issue
- **Problem:** Kategori kartlarına tıklayınca sadece o kategori açılıyor, ama CSS'de `.articles.active` selector’ı var, JS`de de active class'ı ekliyorum. Çalışıyor.
- **Verification:** test_report.py geçti.
- **Note:** Exclusive accordion (others close) doğru çalışıyor.

### 2026-02-28: Clean Content Requirement
- **Problem:** Haberlerde link ve URL'ler var, kullanıcı istemiyor.
- **Solution:** `strip_html()` fonksiyonunda `re.sub(r'https?://\S+', '', text)` ile linkleri kaldır. Ayrıca `www\.` ve email pattern'leri de temizle.
- **Result:** Link-free, sade içerik.

### 2026-02-28: Blog Format Design
- **Change:** Card-based list yerine full blog post format: başlık + tam içerik + görsel (varsa).
- **Layout:** Minimalist, serif font, geniş satır, paragraf formatlı.
- **Features:** Dark/light mode, favorites, accordion categories.

### 2026-02-28: Context Window Management (Critical)
- **Problem:** OpenClaw conversation'ları çok uzun süre hafızada kalınca context limiti doluyor, AI "kopma" yaşıyor.
- **Solution:** Implemented `context_manager.py` – every 3 days, summarize conversations older than 7 days and move them from `memory/conversations/` to `memory/summaries/`.
- **Retention policy:** Keep last 7 days of raw conversations; older ones are summarized and archived.
- **Benefit:** Context stays fresh, AI never loses thread, memory/summary/ holds long-term distilled knowledge.
- **Cron:** `0 5 */3 * * /usr/bin/python3 /home/openclaw/.openclaw/workspace/context_manager.py`
- **Next:** Integrate summaries into OpenClaw's context loading (MEMORY.md + memory/summaries/ + memory/conversations/).

### 2026-02-28: Link Validation Before Sharing
- **Rule:** Never share a link without verifying it returns HTTP 200.
- **Process:** After pushing HTML to GitHub Pages, wait 30-60 seconds, then `curl -I <url>`. If 404, trigger rebuild (empty commit) and retry up to 3 times. Only share when verified.
- **Applied to:** All GitHub Pages reports (AI news, Meta Glasses updates).
