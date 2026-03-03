# Son Uçuş Bilet Raporu Linki
2026-03-01

GitHub Pages: https://tempMert.github.io/Openclaw-Raporlar/raporlar/ucak_biletleri/bilet_arama_detayli_2026-03-01.html

Özellikler:
- 79 bilet bulundu (3 tanesi ≤60k TL öncelikli)
- Kare kart formatı
- "Biletini Satın Al" butonları → Google Flights'a direkt yönlendirir
- Filtreler: 6 saat maks aktarma, 2 kişi toplam ≤88k TL
- Cron: Her gün 09:10 ve 13:00'te otomatik güncellenir

---
# Kullanılabilir Scriptler
- amadeus_flight_search.py – ana arama scripti
- meta_glasses_update_checker.py – Meta Glasses raporu

# API Kredentials
- Amadeus: AMADEUS_API_KEY, AMADEUS_API_SECRET (ortam değişkenleri)
- Telegram: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (opsiyonel)

# Workflow
1. Script çalıştır → lokal HTML oluştur
2. Git add/commit/push → GitHub Pages otomatik deploy
3. Link paylaş

# Revizyonlar
- 2026-03-01: Booking linkler Google Flights'a yönlendirilerek iyileştirildi

---
# Komunikasyon Politikası (2026-03-03)
- Telegram cevapları: **çok kısa, öz, net** (max 2-3 satır). HTML kodları asla gönderilmez.
- Web tasarımları: sadece **bitmiş GitHub Pages linki** ve kısa bir özet paylaşılır.
- Cooder designer: **uzay tema + altın/gümüş çerçeve** özelliği eklendi.
- Cooder-code skill entegrasyonu planlı.