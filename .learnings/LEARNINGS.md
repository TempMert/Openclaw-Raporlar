## LEARNINGS

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
  2. Commit & push: `git commit -m "Remove old report" && git push`
  3. Regenerate the report fresh (new file created)
  4. Push again: `git add new_report.html && git commit -m "Add updated report" && git push`
- **Why this works:** Removing the file forces GitHub Pages to invalidate the cache entry. When the new file is added, it's treated as a brand new resource, bypassing CDN cache.
- **Automation:** All OpenClaw report generators (`meta_glasses_update_checker.py`, daily_report.sh, etc.) must implement this delete-then-recreate pattern for every update.
- **Verification:** After push, check `curl -I <url>` – the `Last-Modified` header should be recent (within last minute). If not, repeat the delete-recreate cycle.
- **User instruction:** When sharing links, always verify with `curl -I` to ensure the latest version is served. If not, trigger rebuild.

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
