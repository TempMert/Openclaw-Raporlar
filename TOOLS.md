# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Environment

- **Host:** HP 840 G8
- **CPU:** Intel i5
- **RAM:** 16GB
- **OS:** Ubuntu Desktop
- **Network:** Tailscale VPN (100.91.79.25)
- **Package managers:** apt, npm, pip, brew

### Runtime Rules

1. Web apps bind to `0.0.0.0` (never `127.0.0.1`)
2. Install missing tools via apt/npm/pip/brew
3. After 3 consecutive failures, STOP and report
4. Always announce port numbers when starting servers
5. Prefer Node.js for web applications

### Reminders

- **2026-02-26 11:00** → Yeni Google Cloud projesi (notional-cirrus-488607-i6) ve client ID (1088750391678-punto3ake7m9s9pc5095dng19bobdqmg) ile gog auth setup. Mail adresi: **mertshp5@gmail.com**. Yetkilendirme kaldı.

Add whatever helps you do your job. This is your cheat sheet.
