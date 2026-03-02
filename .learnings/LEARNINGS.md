## LEARNINGS

### 2026-02-28: Seyahat Tercihleri – Uçak Bilet Arama (CRITICAL)
- **Kullanıcı:** Mertko
- **Tarihler:**
  - Gidiş: 22-24 Mart 2026 (herhangi bir gün)
  - Dönüş: 5-6 Haziran 2026 (herhangi bir gün)
- **Rotalar:**
  - İstanbul (IST/SAW) → Osaka, Japonya
  - İstanbul (IST/SAW) → Tokyo, Japonya
- **Yolcu Sayısı:** 2 kişi
- **Aktarma:** Maksimum 5 saat (kısa aktarma)
- **Havayolları:** Tercih yok (ucuz bilet)
- **Kaynaklar:** SkyScanner, Google Flights, doğrudan havayolları (JAL, ANA, Turkish Airlines, Air China, etc.)
- **Not:** Kullanıcı bu kriterlere uyan biletleri bulduğumda (herhangi bir arama sonucu) linkleri ile birlikte paylaşmalıyım.

### 2026-02-28: ULTRA-CRITICAL USER CONSENT POLICY (NEW)
- **ABSOLUTE RULE:** Before performing any system-altering action on the host machine, **ALWAYS obtain explicit user confirmation first**.
- **Actions requiring confirmation:**
  - Installing any software (apt, snap, pip, npm, brew, curl|bash)
  - Deleting or modifying files outside workspace (rm, mv, dd, etc.)
  - Changing system configuration (network, firewall, cron, services)
  - Accessing personal data (email, messages, files outside workspace)
  - Making outbound requests that could be tracked (webhooks, API calls to new services)
  - Sharing any data externally (posts, uploads, messages to others)
- **Process:** Clearly state what will be done, why, and potential impact. Wait for user's "yes" or explicit approval before proceeding.
- **Exception:** Emergency safety fixes (imminent data loss, security breach) – act first, inform immediately after.
- **Enforcement:** If unsure whether an action requires consent, err on the side of asking.

### 2026-02-28: GitHub Pages Cache Busting – Always Fresh Deploy (CRITICAL)
- **Problem:** GitHub Pages caches HTML files aggressively (up to hours). Updating a file may not reflect immediately, causing users to see stale content.
- **Solution:** For every report update, use **delete-then-recreate** workflow:
  1. Delete the old HTML file from git: `git rm path/to/report.html`
  2. Commit & push removal (this busts the cache)
  3. Wait 5 seconds
  4. Regenerate the report fresh (new file created in same location)
  5. Add, commit & push the new file
  6. Verify with `curl -I <url>` – should return HTTP 200 and recent `Last-Modified`
- **Why this works:** Removing the file forces GitHub Pages to invalidate the cache entry. When the new file is added, it's treated as a brand new resource, bypassing CDN cache.
- **Automation:** All OpenClaw report generators must implement this exact pattern (see `meta_glasses_update_checker.py:push_and_verify`).
- **Important:** Must use **correct path** (`raporlar/<report_type>/`) – not `meta_glasses_reports/`. GitHub Pages serves from `/raporlar/` subtree.
- **Verification:** After push, check `curl -I <url>` – `Last-Modified` should be within 1 minute. If not, repeat cycle.
- **User instruction:** When sharing links, always verify with `curl -I`. If stale, trigger rebuild.

### 2026-02-28: HTML Report Design Pattern – Modern Dark Blog Style (CRITICAL)
- **Design Philosophy:** Use the same template for all HTML reports (AI news, Meta Glasses, etc.).
- **Core Template:** Dark mode (`#0f172a` slate 900), Inter font, max-width 900px, line-height 1.7.
- **Components:**
  - Header: Title (emoji + model/type), meta line (date, automation), status badge (update/no-update with date)
  - Blog Summary: Paragraph-based, emoji-start, clear explanations, model-specific (e.g., "GEN1", "OpenClaw ecosystem")
  - Control/Kontroll成果: Card-style list (hover effects, rounded corners, left border accent)
  - News Links: Modern card list with title + snippet, hover accent border
  - Footer: Attribution, date, model tag
- **Color Palette (Slate):**
  - `--bg: #0f172a` (slate 900)
  - `--card: #1e293b` (slate 800)
  - `--text-main: #f1f5f9` (slate 100)
  - `--accent: #3b82f6` (blue 500)
  - `--success: #10b981` (emerald 500)
  - `--danger: #ef4444` (red 500)
- **Cache Bust:** Always delete-then-recreate to ensure fresh deploy.
- **Consistency:** All reports must follow this exact pattern for brand consistency.

### 2026-02-28: ULTRA-CRITICAL API KEY SECURITY POLICY
- **ABSOLUTELY FORBIDDEN:** Never hardcode or commit API keys (OpenRouter, Tavily, GitHub, Telegram, Google) to ANY repository (public or private).
- **Storage:** API keys ONLY in environment variables (`~/.bashrc`, OpenClaw config). No default fallback values in code.
- **Public repos:** Only static assets (HTML, CSS, JS). No Python/Node/JSON config files.
- **Private repos:** Scripts allowed but must read keys from environment only. Never include .env or config with secrets.
- **Exposure response:** If a key is found in public (GitHub alert, grep scan), immediately:
  1. Revoke the exposed key.
  2. Generate a new key.
  3. Update environment variables.
  4. **Require 2x user confirmation** before any further action (rotate other keys, notify services, etc.).
- **Audit cadence:** Automated scan every 3 days: `grep -rE "(sk-or-v1|tvly-dev|ghp_)" --include="*.py" --include="*.js" --include="*.md" --include="*.json" workspace/`.
- **Violation consequences:** Trust broken, system compromised. Immediate revocation and user notification.

### 2026-02-28: Context Window Management (Critical)
- **Problem:** OpenClaw conversation'ları çok uzun süre hafızada kalınca context limiti doluyor, AI "kopma" yaşıyor.
- **Solution:** Implemented `context_manager.py` – every 3 days, summarize conversations older than 7 days and move them from `memory/conversations/` to `memory/summaries/`.
- **Retention policy:** Keep last 7 days of raw conversations; older ones are summarized and archived.
- **Benefit:** Context stays fresh, AI never loses thread, memory/summary/ holds long-term distilled knowledge.
- **Cron:** `0 5 */3 * * /usr/bin/python3 /home/openclaw/.openclaw/workspace/context_manager.py`
- **Next:** Integrate summaries into OpenClaw's context loading (MEMORY.md + memory/summaries/ + memory/conversations/).

### 2026-02-28: Link Validation Before Sharing (CRITICAL)
- **Rule:** Never share a link without verifying it returns HTTP 200.
- **Process:** After pushing HTML to GitHub Pages, wait 60 seconds, then `curl -I <url>`. If 404, trigger rebuild (empty commit) and retry up to 3 times. Only share when verified.
- **Applied to:** All GitHub Pages reports (AI news, Meta Glasses updates).
- **Fail-safe:** If verification fails after 3 attempts, do NOT share link; report error and retry later.

### 2026-02-28: GitHub Pages Deployment Checklist
- ✅ Push HTML to public repo (`Openclaw-Raporlar`)
- ✅ Wait 60 seconds for build
- ✅ Verify URL with `curl -I` → HTTP 200
- ✅ If 404, trigger rebuild (empty commit) and wait 30s, retry
- ✅ After 3 failures, abort and log error
- ✅ Only share verified URL

### 2026-02-28: Self-Improving Agent Activations
- **Skills in use:** `tavily-search`, `ontology`, `openai-image-gen`, `self-improving-agent`
- **Logging:** `.learnings/ERRORS.md` and `.learnings/LEARNINGS.md` updated after each fix
- **Autonomous checks:** `gateway_test.py` (every 3 days), `context_manager.py` (every 3 days), `meta_glasses_update_checker.py` (every 2 weeks)
- **Policy:** Do not wait for user permission to fix critical bugs (security, broken links). Implement fix, log it, inform user.
- **Proactive research:** Actively follow trends in OpenClaw, VibeCoding, NanoBanana via Tavily; incorporate insights into future versions.

### 2026-02-28: API Key Security Incident (OpenRouter Alert)
- **Incident:** OpenRouter security alert indicated potential key exposure in public repository.
- **Cause:** Hardcoded API keys in `generate_report.py` (public repo `Openclaw-Raporlar`).
- **Response:** Immediately removed `generate_report.py` from public repo, deleted all hardcoded keys from code, enforced environment-only key usage.
- **Verification:** Scanned entire workspace – no hardcoded keys remain. Public repo contains only HTML/CSS/JS.
- **Policy reinforcement:** Added ULTRA-CRITICAL API KEY SECURITY POLICY (above).
