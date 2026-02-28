## ERRORS

### 2026-02-28: Translate batch did not populate summaries
- **Symptom:** `generate_report.py` ran without exception, but `summary_tr` fields remained empty (still English).
- **Cause:** `translate_batch()` returned the original list when translation failed or response parsing didn't match indices.
- **Fix:** Check translation results length; if shorter, fall back to English for missing items. Also ensure batch prompt format matches expected response numbering.
- **Next steps:** Implement robust fallback and log which items failed translation.

### 2026-02-28: GitHub Pages 404 after push (meta_glasses report)
- **Symptom:** Pushed HTML file to public repo `Openclaw-Raporlar`, but GitHub Pages returned 404 at expected URL.
- **Cause:** GitHub Pages build delay or path mismatch. The file exists in repo (`raporlar/meta_glasses/...`) but Pages not yet built or wrong base path.
- **Fix:** After push, wait 30-60 seconds, then validate URL with `curl -I`. If 404, trigger rebuild with empty commit and re-check. Do not send link until verified.
- **Policy added:** "Before sharing any link, verify it returns HTTP 200. If not, rebuild and retry up to 3 times."
