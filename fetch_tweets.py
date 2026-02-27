#!/usr/bin/env python3
"""Fetch recent tweets/topics via Tavily and save JSON for report generation."""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime

TAVILY_KEYS = [
    os.getenv("TAVILY_API_KEY", "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")
]

def search_tavily(query, max_results=5):
    url = "https://api.tavily.com/search"
    for key in TAVILY_KEYS:
        try:
            data = json.dumps({
                "query": query,
                "search_depth": "basic",
                "max_results": max_results,
                "time_range": "week",
                "include_images": False
            }).encode()
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status == 200:
                    resp = json.loads(r.read().decode())
                    return {"success": True, "results": resp.get("results", [])}
        except urllib.error.HTTPError as e:
            if e.code == 403:
                continue
            else:
                return {"success": False, "error": f"HTTP {e.code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return {"success": False, "error": "All keys exhausted"}

# Search queries (one per topic to speed up)
queries = {
    "OpenClaw": "OpenClaw AI assistant latest features",
    "VibeCoding": "vibe coding AI pair programming tools",
    "NanoBanana": "NanoBanana OpenClaw skill features"
}

collected = {}
for cat, q in queries.items():
    res = search_tavily(q, max_results=5)
    if res["success"]:
        collected[cat] = res["results"][:5]
    else:
        collected[cat] = []

# Save
today = datetime.now().strftime("%Y-%m-%d")
out_dir = "/home/openclaw/.openclaw/workspace/raporlar"
os.makedirs(out_dir, exist_ok=True)
out_path = f"{out_dir}/{today}_rapor.json"
with open(out_path, "w") as f:
    json.dump(collected, f, indent=2, ensure_ascii=False)

print(f"Saved {sum(len(v) for v in collected.values())} items to {out_path}")
