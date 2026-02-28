#!/usr/bin/env python3
"""
Context & Memory Manager – Summarize old conversations to keep context fresh.
Runs every 3 days (with gateway test). Keeps last 7 days of conversations in memory/conversations/,
summarizes older ones into memory/summary/.
"""

import os, json, re, subprocess, datetime, sys
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
CONVERSATIONS_DIR = MEMORY_DIR / "conversations"
SUMMARY_DIR = MEMORY_DIR / "summaries"

# Create dirs if missing
CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

def get_old_conversations(days=7):
    """Return conversation files older than N days."""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    old_files = []
    for f in CONVERSATIONS_DIR.glob("*.md"):
        # Parse date from filename: YYYY-MM-DD.md
        try:
            file_date = datetime.datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date < cutoff:
                old_files.append(f)
        except ValueError:
            continue
    return old_files

def summarize_conversation(file_path):
    """Read a conversation file and generate a summary using OpenRouter."""
    try:
        with open(file_path) as f:
            content = f.read()
        # Skip if too short
        if len(content) < 200:
            return None
        # Use OpenRouter API for summarization (NVIDIA Nemotron)
        import requests
        OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "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")
        OPENROUTER_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
        prompt = f"""Aşağıdaki konuşma günlüğünü Türkçe kısa bir özet haline getir. Ana konular, kararlar, ve önemli bilgileri vurgula. 3-5 cümle. Konuşma:

{content[:4000]}"""
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
                          json={
                              "model": OPENROUTER_MODEL,
                              "messages": [{"role":"user","content":prompt}],
                              "temperature": 0.3,
                              "max_tokens": 500
                          }, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            summary = resp["choices"][0]["message"]["content"].strip()
            return summary
        else:
            print(f"⚠️ Summarization API error {r.status_code} for {file_path.name}")
            return None
    except Exception as e:
        print(f"⚠️ Summarization failed for {file_path.name}: {e}")
        return None

def move_to_summary(file_path, summary):
    """Move old conversation to summaries with metadata."""
    date_str = file_path.stem
    summary_file = SUMMARY_DIR / f"{date_str}.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"# Conversation Summary – {date_str}\n\n")
        f.write(f"**Original file:** {file_path.name}\n")
        f.write(f"**Summarized at:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Summary\n\n")
        f.write(summary + "\n\n")
        f.write("## Full original (truncated)\n\n```\n")
        # Truncate original to 2000 chars
        with open(file_path) as orig:
            content = orig.read()
        f.write(content[:2000])
        f.write("\n... (truncated)\n```\n")
    # Remove original conversation file
    file_path.unlink()
    print(f"✅ Summarized and archived: {file_path.name} -> {summary_file.name}")

def main():
    print("🔍 Context & Memory Manager starting...")
    old_convos = get_old_conversations(days=7)
    print(f"Found {len(old_convos)} old conversation(s) to summarize")
    for conv in old_convos:
        print(f"📝 Summarizing: {conv.name}")
        summary = summarize_conversation(conv)
        if summary:
            move_to_summary(conv, summary)
        else:
            print(f"⚠️ Skipped (summary failed): {conv.name}")
    print("✅ Context cleanup complete")

if __name__ == "__main__":
    main()
