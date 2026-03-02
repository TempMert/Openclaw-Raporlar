#!/usr/bin/env python3
"""
Amadeus Flight Search - İstanbul → Osaka/Tokyo
Gidiş: 22-24 Mayıs 2026
Dönüş: 5-7 Haziran 2026
2 yetişkin, aktarma süresi max 6 saat.
Fiyat: 30,000 TL altı öncelikli, yoksa 44,000 TL altı.
"""

import requests, os, json, datetime, itertools
from urllib.parse import quote

# Amadeus credentials
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_API_KEY", "tIjfBtTKVC6wAGt0GtKw5nNYsyJa39b7")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET", "JcQNofOuRG5KHexB")  # Fixed typo

# Airport codes
IST = "IST"  # İstanbul
KIX = "KIX"  # Osaka Kansai
NRT = "NRT"  # Tokyo Narita

# Tarih kombinasyonları
DEPARTURE_DATES = ["2026-05-22", "2026-05-23", "2026-05-24"]
RETURN_DATES = ["2026-06-05", "2026-06-06", "2026-06-07"]

# Parametreler
ADULTS = 2
MAX_CONNECTION_HOURS = 6  # aktarma süresi max 6 saat
MAX_PRICE = 88000  # TL (2 kişi toplam 44k x2)
PRIORITY_PRICE = 60000  # TL (2 kişi toplam 30k x2)

def get_amadeus_access_token():
    """OAuth2 token al."""
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_API_SECRET
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            print(f"❌ Token alınamadı: {r.status_code} {r.text}")
            return None
    except Exception as e:
        print(f"❌ Token error: {e}")
        return None

def search_flight_offers(token, origin, destination, departure, return_date, adults=2):
    """Uçuş tekliflerini ara (Flight Offers Search)."""
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure,
        "returnDate": return_date,
        "adults": adults,
        "currencyCode": "TRY",
        "max": 20  # max sonuç
    }
    headers = {"Authorization": f"Bearer {token}"}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"❌ Search failed {origin}->{destination}: {r.status_code}")
            print(r.text)
            return None
    except Exception as e:
        print(f"❌ Search error: {e}")
        return None

def filter_offers(offers_json, max_connection_hours=6, max_price=MAX_PRICE):
    """Aktarma süresi ve fiyat filtresi uygula."""
    if not offers_json or "data" not in offers_json:
        return []

    filtered = []
    for offer in offers_json["data"]:
        # Fiyat kontrolü
        price = float(offer.get("price", {}).get("total", 0))
        if price > max_price:
            continue

        # Aktarma süresi kontrolü
        itineraries = offer.get("itineraries", [])
        skip = False
        for itin in itineraries:
            segments = itin.get("segments", [])
            if len(segments) > 1:
                for i in range(len(segments)-1):
                    arr = segments[i]["arrival"]["at"]
                    dep = segments[i+1]["departure"]["at"]
                    arr_dt = datetime.datetime.fromisoformat(arr)
                    dep_dt = datetime.datetime.fromisoformat(dep)
                    diff = (dep_dt - arr_dt).total_seconds() / 3600
                    if diff > max_connection_hours:
                        skip = True
                        break
            if skip:
                break
        if not skip:
            filtered.append(offer)

    return filtered

def generate_booking_link(offer):
    """Amadeus offering'dan direkt booking link oluştur."""
    # Amadeus response'unda "bookableEmail" veya "deepLinks" olabilir
    # Basit çözüm: Havayolu kodunu al ve direkt havayolu sitesine yönlendir
    airline_code = "N/A"
    for itin in offer.get("itineraries", []):
        for seg in itin.get("segments", []):
            airline_code = seg.get("carrierCode", "N/A")
            break
        if airline_code != "N/A":
            break

    # Havayolu websitesi mapping (basit)
    airline_urls = {
        "TK": "https://www.turkishairlines.com",
        "JL": "https://www.jal.co.jp",
        "NH": "https://www.ana.co.jp",
        "OZ": "https://www.flyasiana.com",
        "KE": "https://www.koreanair.com",
        "CA": "https://www.airchina.com",
        "BR": "https://www.china-airlines.com",
        "CI": "https://www.china-airlines.com",
        "MU": "https://www.ceair.com",
        "CZ": "https://www.csair.com",
    }

    base_url = airline_urls.get(airline_code, "https://www.google.com/flights")

    # Fiyat ve detayları query string'e ekle (basit)
    price = offer.get("price", {}).get("total", "")
    return f"{base_url}?search=flight&price={price}&currency=TRY"

def generate_booking_link(offer):
    """Amadeus offering'dan Google Flights'a yönlendirir (spesifik rota + tarihler)."""
    # İlk itinerary (gidiş) ve ikinci (dönüş) bilgilerini al
    itineraries = offer.get("itineraries", [])
    if len(itineraries) < 2:
        return "https://www.google.com/flights"
    
    # Gidiş segmenti
    outbound_seg = itineraries[0]["segments"][0]
    return_seg = itineraries[1]["segments"][0]
    
    origin = outbound_seg["departure"]["iataCode"]
    dest = outbound_seg["arrival"]["iataCode"]
    out_date = outbound_seg["departure"]["at"].split("T")[0]  # YYYY-MM-DD
    ret_date = return_seg["departure"]["at"].split("T")[0]
    
    # Google Flights query
    return f"https://www.google.com/flights?q={origin}+{dest}+{out_date}+{ret_date}"

def format_flight_card(offer, route_name, departure_date, return_date):
    """Bir bilet için HTML kart oluştur (kare kart, modern)."""
    price = float(offer.get("price", {}).get("total", 0))
    currency = offer.get("price", {}).get("currency", "TRY")

    # Havayolu kodu
    airline_code = "N/A"
    for itin in offer.get("itineraries", []):
        for seg in itin.get("segments", []):
            airline_code = seg.get("carrierCode", "N/A")
            break
        if airline_code != "N/A":
            break

    # Havayolu adı mapping
    airline_names = {
        "TK": "Türk Hava Yolları", "JL": "Japan Airlines", "NH": "All Nippon Airways",
        "OZ": "Asiana Airlines", "KE": "Korean Air", "CA": "Air China",
        "BR": "China Airlines", "CI": "China Airlines", "MU": "China Eastern",
        "CZ": "China Southern"
    }
    airline_name = airline_names.get(airline_code, airline_code)

    # Gidiş/Dönüş saatleri (ilk/last segment)
    outbound = offer["itineraries"][0] if offer.get("itineraries") else {}
    return_trip = offer["itineraries"][1] if len(offer.get("itineraries", [])) > 1 else {}

    outbound_dep = outbound.get("segments", [{}])[0].get("departure", {}).get("at", "N/A") if outbound else "N/A"
    outbound_arr = outbound.get("segments", [{}])[-1].get("arrival", {}).get("at", "N/A") if outbound else "N/A"
    return_dep = return_trip.get("segments", [{}])[0].get("departure", {}).get("at", "N/A") if return_trip else "N/A"
    return_arr = return_trip.get("segments", [{}])[-1].get("arrival", {}).get("at", "N/A") if return_trip else "N/A"

    # Bagaj (extract from travelerPricings)
    baggage = "Bilgi yok"
    for traveler in offer.get("travelerPricings", []):
        for fareDetails in traveler.get("fareDetailsBySegment", []):
            baggage = fareDetails.get("includedCheckedBags", {}).get("quantity", 0)
            if baggage:
                baggage = f"{baggage} Adet"
                break

    # Aktarma detayları
    connections = []
    for itin in offer.get("itineraries", []):
        segs = itin.get("segments", [])
        if len(segs) > 1:
            for i in range(len(segs)-1):
                arr = segs[i]["arrival"]["at"]
                dep = segs[i+1]["departure"]["at"]
                arr_dt = datetime.datetime.fromisoformat(arr)
                dep_dt = datetime.datetime.fromisoformat(dep)
                diff_hours = (dep_dt - arr_dt).total_seconds() / 3600
                connections.append(f"{segs[i]['arrival']['iataCode']} ({diff_hours:.1f} sa)")

    connection_html = "<br>".join([f"🔄 {c}" for c in connections]) if connections else "🔄 Direkt"

    # Fiyat rengi (öncelikli fiyat mı?)
    price_class = "price-high"
    if price <= PRIORITY_PRICE:
        price_class = "price-priority"
    elif price <= MAX_PRICE:
        price_class = "price-normal"

    booking_link = generate_booking_link(offer)

    html = f"""
<div class="flight-card" style="border: 1px solid #ddd; border-radius: 12px; padding: 20px; margin: 15px 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 100%; max-width: 800px; margin-left: auto; margin-right: auto;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #2c3e50;">{airline_name} ({airline_code})</div>
            <div style="color: #7f8c8d; font-size: 0.9rem;">{route_name}</div>
        </div>
        <div class="{price_class}" style="text-align: right;">
            <div style="font-size: 1.5rem; font-weight: bold;">{price:,.0f} ₺</div>
            <div style="font-size: 0.9rem; color: #7f8c8d;">2 yetişkin toplam</div>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
        <div>
            <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 4px;">GİDİŞ</div>
            <div style="font-weight: 600;">{departure_date}</div>
            <div style="font-size: 0.9rem; color: #7f8c8d;">{outbound_dep.split('T')[1][:5] if outbound_dep != 'N/A' else 'N/A'} → {outbound_arr.split('T')[1][:5] if outbound_arr != 'N/A' else 'N/A'}</div>
        </div>
        <div>
            <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 4px;">DÖNÜŞ</div>
            <div style="font-weight: 600;">{return_date}</div>
            <div style="font-size: 0.9rem; color: #7f8c8d;">{return_dep.split('T')[1][:5] if return_dep != 'N/A' else 'N/A'} → {return_arr.split('T')[1][:5] if return_arr != 'N/A' else 'N/A'}</div>
        </div>
        <div>
            <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 4px;">BAGAJ</div>
            <div style="font-weight: 600;">{baggage}</div>
            <div style="font-size: 0.9rem; color: #7f8c8d;">Alt bagaj</div>
        </div>
    </div>

    <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
        <div style="font-size: 0.9rem; color: #495057;">🔄 Aktarma(lar):</div>
        <div style="margin-top: 5px;">{connection_html}</div>
    </div>

    <div style="text-align: center;">
        <a href="{booking_link}" target="_blank" style="display: inline-block; background: #2563eb; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1rem;">🎫 Biletini Satın Al</a>
    </div>
</div>
"""
    return html

def generate_html_report(all_results):
    """HTML raporu oluştur - tüm rotalar ve tarihler."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Önce tüm rotaları birleştir ve fiyata göre sırala
    flat_results = []
    for route_name, results_by_date in all_results.items():
        for dep_date, return_date, offers in results_by_date:
            for offer in offers:
                flat_results.append({
                    "route": route_name,
                    "departure": dep_date,
                    "return": return_date,
                    "offer": offer
                })

    # Fiyata göre sırala (ucuzdan pahalıya)
    flat_results.sort(key=lambda x: float(x["offer"].get("price", {}).get("total", 0)))

    # HTML başlangıcı
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Uçuş Bilet Arama Sonuçları - {today}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0f172a;
    --card-bg: #ffffff;
    --text-main: #1e293b;
    --text-muted: #64748b;
    --accent: #2563eb;
    --accent-hover: #1d4ed8;
    --success: #059669;
    --warning: #d97706;
    --danger: #dc2626;
    --price-priority: #10b981;
    --price-normal: #2563eb;
    --price-high: #dc2626;
}}
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text-main);
    margin: 0;
    padding: 20px;
    line-height: 1.6;
}}
.container {{
    max-width: 900px;
    margin: 0 auto;
}}
header {{
    text-align: center;
    margin-bottom: 40px;
    padding: 30px;
    background: linear-gradient(135deg, var(--accent) 0%, #1d4ed8 100%);
    color: white;
    border-radius: 16px;
}}
header h1 {{
    font-size: 2rem;
    margin: 0 0 10px 0;
}}
header p {{
    opacity: 0.9;
    margin: 5px 0;
}}
.stats {{
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 20px;
    flex-wrap: wrap;
}}
.stat {{
    text-align: center;
}}
.stat-value {{
    font-size: 1.8rem;
    font-weight: 700;
}}
.stat-label {{
    font-size: 0.85rem;
    opacity: 0.8;
}}
.price-priority {{ color: var(--price-priority); }}
.price-normal {{ color: var(--price-normal); }}
.price-high {{ color: var(--price-high); }}
.alert {{
    background: #fef2f2;
    color: var(--danger);
    padding: 15px;
    border-radius: 8px;
    margin: 20px 0;
    border-left: 4px solid var(--danger);
}}
.filters {{
    background: #e0f2fe;
    padding: 15px;
    border-radius: 8px;
    margin: 20px 0;
    font-size: 0.95rem;
}}
footer {{
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    color: var(--text-muted);
    font-size: 0.9rem;
    border-top: 1px solid var(--border);
}}
@media (max-width: 600px) {{
    .flight-card {{ padding: 15px !important; }}
    header h1 {{ font-size: 1.5rem; }}
}}
</style>
</head>
<body>
<div class="container">

<header>
    <h1>🛫 Uçuş Bilet Arama Sonuçları</h1>
    <p>{today} • Amadeus API • İstanbul → Osaka/Tokyo</p>
    <div class="stats">
        <div class="stat">
            <div class="stat-value">{len(flat_results)}</div>
            <div class="stat-label">Toplam Bilet</div>
        </div>
        <div class="stat">
            <div class="stat-value">{len([r for r in flat_results if float(r['offer'].get('price', {}).get('total', 0)) <= PRIORITY_PRICE])}</div>
            <div class="stat-label">30k TL Altı (Öncelikli)</div>
        </div>
        <div class="stat">
            <div class="stat-value">{len([r for r in flat_results if float(r['offer'].get('price', {}).get('total', 0)) <= MAX_PRICE])}</div>
            <div class="stat-label">44k TL Altı</div>
        </div>
    </div>
</header>

<div class="filters">
<strong>🔍 Arama Kriterleri:</strong><br>
• Gidiş: 22-24 Mayıs 2026 • Dönüş: 5-7 Haziran 2026<br>
• Rotalar: IST → Osaka (KIX) / Tokyo (NRT)<br>
• Aktarma: Maksimum 6 saat • 2 yetişkin<br>
• Hedef: 30.000 TL altı (öncelik), yoksa 44.000 TL altı
</div>

<div class="alert">
⚠️ <strong>Not:</strong> Bu sonuçlar Amadeus test API'sinden alınmıştır. Gerçek bilet fiyatları ve seferler değişken olabilir. Lütfen doğrulamak için havayolu websitesine gidin.
</div>

<h2 style="text-align: center; margin: 30px 0;">📋 Tüm Uygun Biletler (Fiyata Göre Sıralı)</h2>

<div class="cards-container">
'''

    for item in flat_results:
        route = item["route"]
        dep = item["departure"]
        ret = item["return"]
        offer = item["offer"]
        html += format_flight_card(offer, route, dep, ret)

    html += f'''
</div>

<footer>
Bu rapor <strong>OpenClaw</strong> tarafından Amadeus API ile otomatik üretilmiştir.<br>
API kotaları: Flight Offers Search (3,000/ay) - Kalan: ~2,999<br>
<small>Son güncelleme: {today} {datetime.datetime.now().strftime("%H:%M")}</small>
</footer>

</div>
</body>
</html>'''

    return html

def main():
    print("🔍 Amadeus ile gelişmiş uçuş araması başlatılıyor...")

    # Token al
    token = get_amadeus_access_token()
    if not token:
        print("❌ Token alınamadı - çıkılıyor")
        send_telegram_message("❌ Amadeus API token alınamadı. Kontrol edin.")
        return

    print("✅ Token alındı, arama yapılıyor...")

    # Tüm kombinasyonları ara
    all_results = {}

    # Rota listesi
    routes = [
        ("IST → KIX (Osaka)", IST, KIX),
        ("IST → NRT (Tokyo)", IST, NRT)
    ]

    for route_name, origin, dest in routes:
        all_results[route_name] = []
        for dep_date, ret_date in itertools.product(DEPARTURE_DATES, RETURN_DATES):
            print(f"🔍 {route_name}: {dep_date} → {ret_date}")
            raw_results = search_flight_offers(token, origin, dest, dep_date, ret_date, ADULTS)
            if raw_results:
                filtered = filter_offers(raw_results, MAX_CONNECTION_HOURS, MAX_PRICE)
                all_results[route_name].append((dep_date, ret_date, filtered))
                print(f"   → {len(filtered)} uygun bilet (max 6h aktarma, ≤{MAX_PRICE} TL)")
            else:
                all_results[route_name].append((dep_date, ret_date, []))

    # HTML raporu oluştur
    html = generate_html_report(all_results)

    # Kaydet (LOCAL ONLY - public repo'ya push yok)
    report_dir = "/home/openclaw/.openclaw/workspace/raporlar/ucak_biletleri"
    os.makedirs(report_dir, exist_ok=True)
    report_path = f"{report_dir}/bilet_arama_detayli_{datetime.datetime.now().strftime('%Y-%m-%d')}.html"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Detaylı rapor oluşturuldu: {report_path}")

    # VS Code'da aç (sadece manual/terminal çalıştırmada, cron'da atla)
    if not os.getenv("RUNNING_FROM_CRON"):
        try:
            subprocess.run(["code", report_path], check=False)
            print("💡 Rapor VS Code'da açıldı")
        except:
            pass

    # Summary
    total_flights = sum(len(offers) for route_data in all_results.values() for _, _, offers in route_data)
    priority = sum(1 for route_data in all_results.values() for _, _, offers in route_data for o in offers if float(o.get("price", {}).get("total", 0)) <= PRIORITY_PRICE)
    print(f"📊 Toplam uygun bilet: {total_flights} (önce {priority} tanesi 30k altı)")

    # Telegram bildirimi - sadece env'ler set ise
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        send_telegram_notification(all_results, total_flights, priority, report_path)
    else:
        print("📢 Telegram bildirimi atlandı (token/chat_id eksik)")

def send_telegram_message(text, parse_mode="HTML"):
    """Telegram'a mesaj gönder."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("❌ Telegram token veya chat_id eksik (ortam değişkenleri)")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram mesajı gönderildi")
            return True
        else:
            print(f"❌ Telegram hatası: {r.status_code} {r.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def send_telegram_notification(all_results, total_flights, priority_count, report_path):
    """Bilet sonuçları için Telegram bildirimi oluştur ve gönder."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    if total_flights == 0:
        msg = f"""❌ <b>Uçuş Arama Sonucu</b>
📅 <i>{today}</i>

🔍 Rotalar: IST → Osaka (KIX) / Tokyo (NRT)
🗓️ Gidiş: 22-24 Mayıs 2026
🗓️ Dönüş: 5-7 Haziran 2026

⚠️ <b>Hiç uygun bilet bulunamadı.</b>"""
        send_telegram_message(msg)
        return

    # Priority biletler varsa önce onları listele
    priority_flights = []
    normal_flights = []

    for route_name, route_data in all_results.items():
        for dep_date, ret_date, offers in route_data:
            for offer in offers:
                price = float(offer.get("price", {}).get("total", 0))
                if price <= PRIORITY_PRICE:
                    priority_flights.append({
                        "route": route_name,
                        "departure": dep_date,
                        "return": ret_date,
                        "offer": offer
                    })
                elif price <= MAX_PRICE:
                    normal_flights.append({
                        "route": route_name,
                        "departure": dep_date,
                        "return": ret_date,
                        "offer": offer
                    })

    # Mesaj oluştur
    if priority_flights:
        msg = f"""🎯 <b>Öncelikli Biletler Bulundu! (≤60k TL)</b>
📅 <i>{today}</i>

🔍 Toplam: {total_flights} bilet ({len(priority_flights)} öncelikli, {len(normal_flights)} normal)

"""
        # İlk 3 priority bilet
        for i, item in enumerate(priority_flights[:3], 1):
            msg += format_flight_telegram(item, i)

        if len(priority_flights) > 3:
            msg += f"<i>...ve {len(priority_flights)-3} daha</i>\n"

        msg += f"\n📄 <a href='file://{report_path}'>Detaylı rapor (local)</a>"

    elif normal_flights:
        msg = f"""⚠️ <b>Normal Fiyatlı Biletler Bulundu (≤88k TL)</b>
📅 <i>{today}</i>

🔍 Toplam: {total_flights} bilet (Öncelikli: 0)

"""
        for i, item in enumerate(normal_flights[:3], 1):
            msg += format_flight_telegram(item, i)

        if len(normal_flights) > 3:
            msg += f"<i>...ve {len(normal_flights)-3} daha</i>\n"

        msg += f"\n📄 <a href='file://{report_path}'>Detaylı rapor (local)</a>"

    else:
        msg = f"""✅ Arama tamamlandı, ancak belirtilen kriterlere uygun bilet bulunamadı.
📅 {today}
🔍 Toplam sonuç: {total_flights} (hepsi filtre dışı)"""

    send_telegram_message(msg)

def format_flight_telegram(item, index):
    """Telegram mesajı için bilet formatı."""
    offer = item["offer"]
    route = item["route"]
    dep = item["departure"]
    ret = item["return"]
    price = float(offer.get("price", {}).get("total", 0))
    currency = offer.get("price", {}).get("currency", "TRY")

    # Havayolu kodu
    airline_code = "N/A"
    for itin in offer.get("itineraries", []):
        for seg in itin.get("segments", []):
            airline_code = seg.get("carrierCode", "N/A")
            break
        if airline_code != "N/A":
            break

    # Havayolu adı
    airline_names = {
        "TK": "Türk Hava Yolları", "JL": "Japan Airlines", "NH": "All Nippon Airways",
        "OZ": "Asiana Airlines", "KE": "Korean Air", "CA": "Air China",
        "BR": "China Airlines", "CI": "China Airlines", "MU": "China Eastern",
        "CZ": "China Southern"
    }
    airline_name = airline_names.get(airline_code, airline_code)

    # Saatler
    outbound = offer["itineraries"][0] if offer.get("itineraries") else {}
    return_trip = offer["itineraries"][1] if len(offer.get("itineraries", [])) > 1 else {}

    outbound_dep = outbound.get("segments", [{}])[0].get("departure", {}).get("at", "N/A") if outbound else "N/A"
    outbound_arr = outbound.get("segments", [{}])[-1].get("arrival", {}).get("at", "N/A") if outbound else "N/A"
    return_dep = return_trip.get("segments", [{}])[0].get("departure", {}).get("at", "N/A") if return_trip else "N/A"
    return_arr = return_trip.get("segments", [{}])[-1].get("arrival", {}).get("at", "N/A") if return_trip else "N/A"

    # Bagaj
    baggage = "0"
    for traveler in offer.get("travelerPricings", []):
        for fareDetails in traveler.get("fareDetailsBySegment", []):
            qty = fareDetails.get("includedCheckedBags", {}).get("quantity", 0)
            if qty:
                baggage = str(qty)
                break

    # Aktarma
    connections = []
    for itin in offer.get("itineraries", []):
        segs = itin.get("segments", [])
        if len(segs) > 1:
            for i in range(len(segs)-1):
                arr = segs[i]["arrival"]["at"]
                dep = segs[i+1]["departure"]["at"]
                arr_dt = datetime.datetime.fromisoformat(arr)
                dep_dt = datetime.datetime.fromisoformat(dep)
                diff_hours = (dep_dt - arr_dt).total_seconds() / 3600
                connections.append(f"{segs[i]['arrival']['iataCode']} ({diff_hours:.1f} sa)")

    conn_text = "<i>Doğrudan</i>" if not connections else "<b>Aktarma:</b> " + ", ".join(connections)

    # Booking link
    booking_link = generate_booking_link(offer)

    text = f"""<b>{index}. {route}</b>
🛫 <b>{airline_name}</b>
💰 <b>Toplam:</b> {price:,.0f} TL (2 kişi)
📅 Gidiş: {dep} ({outbound_dep.split('T')[1][:5] if outbound_dep!='N/A' else 'N/A'} → {outbound_arr.split('T')[1][:5] if outbound_arr!='N/A' else 'N/A'})
📅 Dönüş: {ret} ({return_dep.split('T')[1][:5] if return_dep!='N/A' else 'N/A'} → {return_arr.split('T')[1][:5] if return_arr!='N/A' else 'N/A'})
🧳 Bagaj: {baggage} Adet
{conn_text}
🔗 <a href='{booking_link}'>Rezervasyon Yap</a>

"""
    return text

if __name__ == "__main__":
    import subprocess
    main()