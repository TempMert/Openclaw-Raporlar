# Cooder-Agent Skill

Bu skill, Cooder agent'ına şu rolleri ekler:

- **developer** – Kod yazma, debug, API entegrasyonu
- **data-analyst** – Veri analizi, CSV/Excel işlemleri
- **devops** – Docker, CI/CD, infrastructure as code
- **content-writer** – Blog yazısı, dokümantasyon, içerik üretimi
- **designer** – HTML/CSS tasarım, grafik oluşturma

## Kurulum

```bash
clawhub link /path/to/cooder-agent
```

## Kullanım

```
/developer <code description>
/data-analyst <csv file path>
/devops <dockerfile instructions>
/content-writer <topic>
/designer <html/css spec>
```

Her komut, ilgili role göre işlem yapar ve sonuç döndürür.