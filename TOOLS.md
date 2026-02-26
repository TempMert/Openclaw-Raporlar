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

- **2026-02-26 15:50** → GitHub repo oluşturuldu: `Openclaw-in-Reposu`. Tüm workspace başarıyla push edildi.
- **2026-02-26** → Gmail send eklemek için OAuth consent screen'e `gmail.send` scope'u eklendi, yeni credentials indirildi. Token alındı. Calendar testi başarılı. Drive/Sheets testi başarılı.

Add whatever helps you do your job. This is your cheat sheet.

Add whatever helps you do your job. This is your cheat sheet.
