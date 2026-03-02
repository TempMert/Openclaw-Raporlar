# Securi-Agent Skill

Bu skill, Securi güvenlik agent'ına şu yetenekleri ekler:

- **self-improvement**: Kendini analiz et, güçlendir, yeni kontroller öner
- **ontology**: Güvenlik terimleri, CVE'ler, sistem bileşenleri arası ilişkileri öğren
- **answeroverflow**: İnternetten güvenlik forumları, CVE database'leri, OpenClaw güvenlik rehberleri

## Kurulum

```bash
clawhub link /path/to/securi-agent
# veya
npm link /path/to/securi-agent
```

## Kullanım

Agent üzerinden:

```
/self-improve
/ontology
/answeroverflow
```

Her komut, güvenlik bilgisi toplar ve raporlar.