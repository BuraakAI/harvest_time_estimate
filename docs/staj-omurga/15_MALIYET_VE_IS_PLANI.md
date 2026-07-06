# 15 — Maliyet, Operasyon ve İş Planı

> **Amaç:** Projenin akademik MVP'den ticari ölçeğe uzanan yolundaki **maliyet kalemlerini**, **iş modeli alternatiflerini** ve **maliyet azaltma stratejilerini** dürüst aralıklarla belgelemek; "kesin gelir" iddiasından kaçınmak.
> **Kapsam:** Maliyet kalemleri, MVP/POC/ürünleşme/ticari ölçek bütçe aralıkları, maliyet azaltma stratejileri, iş modeli karşılaştırma, fiyatlama (fikir düzeyi), gelir varsayım disiplini.
> **Son güncelleme:** 2026-05-10
> **Uyarı:** **Hiçbir rakam kesin değildir.** Tüm sayılar **aralık** ve **varsayım**dır; Türkiye'deki güncel kurum içi ücret bantları, bulut sağlayıcı fiyatları ve ticari uydu teklifleri **doğrulanmalıdır**. Kesin gelir tahmini bu raporda yapılmaz.

---

## 1. Maliyet kalemleri (12 başlık)

| Kalem | Açıklama | MVP'de var mı? | Ticari ölçekte var mı? |
|---|---|---|---|
| Uydu verisi | Sentinel-2/1, Landsat, HLS açık | ✅ ücretsiz | ✅ ücretsiz; PlanetScope ek |
| Hesaplama | GEE / yerel sunucu / dask | 🟡 GEE ücretsiz | ✅ ücretli |
| Sunucu / API | FastAPI hosting | ✅ düşük | ✅ orta-yüksek |
| Veri tabanı / PostGIS | Supabase Free / Postgres | ✅ ücretsiz tier | ✅ ücretli tier |
| Object storage | parquet / GeoTIFF | 🟡 düşük | ✅ orta |
| Saha doğrulama | gezi + etiket toplama | 🟡 elden ele | ✅ kurumsal |
| Mobil uygulama | PWA (V1) → RN (V2) | ✅ ücretsiz V1 | ✅ store ücretleri |
| Harita servisleri | OpenStreetMap / Leaflet | ✅ ücretsiz | 🟡 trafik artarsa CDN |
| Domain / hosting | landing page + deploy | ✅ düşük | ✅ orta |
| Hukuk / KVKK | sözleşme + danışmanlık | 🟡 minimum | ✅ kurumsal |
| Danışmanlık (zirai uzman) | bölge bilgisi, etiket onayı | 🟡 saatlik | ✅ proje payı |
| Bakım / izleme | Sentry, uptime, model retraining | 🟡 ücretsiz tier | ✅ ücretli + ekip |

---

## 2. Bütçe aralıkları (4 ölçekte)

> **Para birimi:** USD ile yazıldı; TL karşılığı kur tarihine bağlı. Aşağıdaki tüm rakamlar **aralık** ve **varsayım**dır.

### 2.1. MVP — akademik prototip (3 ay)

| Kalem | Aralık (USD/ay) | Not |
|---|---|---|
| Uydu verisi | $0 | Açık veri |
| GEE | $0 | Akademik noncommercial |
| Backend hosting (Render Hobby / Fly.io free) | $0–25 | Streamlit Cloud da ücretsiz |
| Frontend hosting (Vercel Hobby) | $0 | Hobby sınırı yeterli |
| DB (Supabase Free) | $0 | 500 MB sınırı yeterli |
| Domain | $1–2 | .com bazlı |
| **Toplam altyapı** | **$1–30/ay** | |
| İnsan kaynağı | 4.5–6.5 kişi-ay (kurum içi katsayıyla) | Tek kişi staj senaryosunda 0 |

### 2.2. POC — pilot kullanıcılarla (6 ay)

| Kalem | Aralık (USD/ay) | Not |
|---|---|---|
| Backend Pro tier | $7–25 | Render/Fly Pro |
| DB Supabase Pro | $25 | 8 GB + auth |
| Object storage | $5–15 | parquet + GeoTIFF cache |
| Sentry Team | $0–26 | Free tier büyüyebilir |
| Domain + e-posta | $5–10 | |
| Saha gezi (yol + konaklama) | yıllık $500–2000 | aralıklı |
| Zirai danışman saatlik | $20–50/saat × ~10 saat/ay | |
| **Toplam altyapı** | **$50–200/ay** | |
| İnsan kaynağı | 8–12 kişi-ay | |

### 2.3. Ürünleşme (12 ay)

| Kalem | Aralık (USD/ay) |
|---|---|
| Backend (Cloud Run / Fargate küçük) | $50–200 |
| DB (Supabase Pro veya RDS small) | $25–150 |
| Object storage | $20–50 |
| MLflow / model artifaktları | $10–50 |
| Mobil mağaza (Apple $99/yıl + Google $25 tek seferlik) | yıllık $124 |
| Sentry / Grafana / monitoring | $25–100 |
| Domain + e-posta + landing | $20–50 |
| Hukuk / KVKK + sözleşme şablonları | tek seferlik $500–2000 + danışmanlık |
| **Toplam altyapı** | **$150–600/ay** |
| İnsan kaynağı | 12–24 kişi-ay |

### 2.4. Ticari ölçek (yıllık)

| Kalem | Aralık (USD) |
|---|---|
| Bulut altyapı (büyüklüğe göre) | $5k–50k/yıl |
| GEE ticari (gerekirse) veya yerel pipeline operasyonu | $5k–30k/yıl |
| Yüksek çözünürlüklü ticari uydu (Planet/Maxar) — opsiyonel | $10k–100k+/yıl |
| Müşteri destek + satış | ekip maliyeti (kurum içi) |
| Pazarlama | $2k–20k/yıl |
| KVKK + hukuk yıllık | $1k–5k/yıl |
| **Toplam tahmini** | **~$25k–200k+/yıl** ölçeğe bağlı |

> **Yorum:** Bu rakamların bir kısmı kurum içi insan kaynağı ile katlanır. Türkiye bağlamında TL kur değişimleri tahmini bozar; bu yüzden **kesin TL bütçesi** hocaya/yatırımcıya ancak aktif sözleşme döneminde yazılır.

---

## 3. Maliyet azaltma stratejileri

| Strateji | Beklenen kazanç | Risk |
|---|---|---|
| Açık veri (S2/S1/HLS) | Veri maliyeti %0'a yakın | Bulutluluk gibi sınırlar |
| Önbellekleme (parquet + edge cache) | Hesaplama %30-60 düşer | İmplemantasyon emek |
| Tek ürün / tek bölge | Geliştirme maliyeti %50+ düşer | Pazar genişliği sınırlanır |
| Kooperatifle toplu etiket | Etiket maliyeti birim başına %70 düşer | Kooperatif bağımlılığı |
| PWA önce, native sonra | Mağaza maliyeti ve süresi ertelenir | Cihaz API'leri sınırlı |
| GEE → yerel pipeline kademeli | Vendor lock-in azalır, ölçek kontrolü | Geliştirme süresi |
| Açık kaynak kod + ücretli destek | Dağıtım hızı artar | IP/farklılaşma erezyonu |
| Yıllık peşin sözleşme indirimi | Nakit akış güçlenir | Müşteri taahhüdü zorlaşır |

---

## 4. İş modeli alternatifleri (genişletilmiş)

(`06_URUN_VE_TICARILESTIRME.md` Bölüm 7 ile uyumlu — burası maliyet ekseni.)

| Model | Müşteri | Müşteri edinim maliyeti | Ortalama kontrat | Sürdürülebilirlik | Faz |
|---|---|---|---|---|---|
| Freemium | Bireysel çiftçi | Düşük (organik) | Düşük | Yüksek (uzun ömürlü) | 5+ |
| Abonelik (parsel-ay) | Çiftçi / kooperatif / firma | Orta | Orta | Yüksek | 5 |
| Yıllık kurumsal lisans | Bakanlık, büyük firma | Yüksek (ihale) | Yüksek | Yüksek | 5+ |
| API kotası | Tedarik / sigorta / banka | Orta-yüksek | Orta-yüksek | Orta | 5+ |
| Komisyon (hasat fiyatı %) | Çiftçi + alıcı | Çok yüksek (model risk) | Belirsiz | Düşük (Türkiye'de denenmemiş) | — |
| Açık kaynak + destek | Akademik / kurum | Düşük | Değişken | Orta | Faz 5 paralel |

> **Karar (`06_URUN_VE_TICARILESTIRME.md` ile uyumlu):** İlk satış kanalı **kooperatif aboneliği**; bireysel çiftçi **freemium** ile uzun vadeli kullanıcı tabanı; bakanlık/sigorta **API/lisans** ileri faz.

---

## 5. Fiyatlama (yalnız fikir düzeyi)

| Katman | Yaklaşık fiyat aralığı (TL/ay) | Kapsam | Müşteri |
|---|---|---|---|
| Free | 0 | 1 parsel, 1 sezon | Bireysel çiftçi |
| Pro | ~₺50–150 | ~25 parsel, 5 sezon arşivi, push, ihracat | Bireysel çiftçi |
| Cooperative | ~₺500–2.000 | ~250 parsel, çoklu kullanıcı, rapor | Kooperatif |
| Enterprise | yıllık sözleşme | Sınırsız + API + SLA | Bakanlık, büyük firma, sigorta |

> **Uyarı:** Bu rakamlar **fikir düzeyindedir**. Kesin fiyat aralığı ancak Faz 5'te en az 5 pilot kullanıcı görüşmesinden sonra netleşir. Bu raporda kesin gelir tahmini yapılmaz.

---

## 6. Gelir varsayım disiplini

Eğer ileride iş planına gelir tahmini koymak gerekirse aşağıdaki disipline uy:

1. **Müşteri sayısı varsayımları açık yazılır** ("100 kooperatif × 50 parsel × ₺1.000/ay" gibi).
2. **Alt limit / üst limit** verilir; tek nokta tahmin yapılmaz.
3. **Müşteri edinim varsayımları** (CAC, çevirme oranı) ayrı listelenir.
4. **Sezonluk / iklim sapma** etkisi azaltıcı varsayım olarak eklenir.
5. **Doğrulanmadı** ibareli her satır vurgulu yazılır.

---

## 7. Operasyonel maliyet kontrolü

- Aylık fatura takibi: Sentry, Vercel, Supabase, GEE quota.
- Aylık MAU (Monthly Active Users) takibi.
- Sezonluk kapsama metriği (parsel × hafta).
- Yıllık kullanıcı geri bildirimi (NPS / kısa anket) — fiyatın değer önermesiyle uyumunu kontrol eder.

---

İlgili: [`06_URUN_VE_TICARILESTIRME.md`](./06_URUN_VE_TICARILESTIRME.md) (müşteri segmentleri) / [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md) (maliyet riskleri R-05, R-08) / [`13_UYDU_UYGUNLUK_MATRISI.md`](./13_UYDU_UYGUNLUK_MATRISI.md) (uydu maliyetleri).

---

## Bu dosyada alınan kararlar
- Tüm rakamlar aralık + varsayım. Hocaya/yatırımcıya tek nokta gelir tahmini sunulmaz.
- MVP altyapı bütçesi $30/ay üst sınırı; aşılırsa karar gözden geçirilir.
- POC bütçesi $200/ay üst sınırı; saha gezisi yıllık $2k üst sınırı.
- Ürünleşmede mağaza ücretleri yıllık $124 sabit kalemdir.
- Yıllık kurumsal lisans ihaleleri Faz 5'ten önce hedeflenmez.

## Açık sorular
- Türkiye'de KVKK uyumlu hosting tercihi (TR sınırlarında veri saklama) gerekli olur mu? — Müşteri segmentine bağlı.
- Pilot kooperatif sözleşmesinde "ücretsiz pilot + sözleşme süresi sonunda fiyat müzakeresi" uygun mu? — Hukuki danışman görüşü gerek.
- GEE ticari fiyatlandırması güncel olarak ne aralıkta? — Faz 5 başında resmi kaynaktan al.

## Sonraki aksiyonlar
- Faz 0 sonu: MVP altyapı için seçilen sağlayıcıların güncel fiyatlandırmasını bir tabloda doğrula.
- Faz 3 sonu: Pilot kullanıcı görüşmelerinden gelen "ödeme isteği" geri bildirimleri bu dosyaya işlenir.
- Faz 5: Yıllık bütçe planı resmî olarak yazılır; danışmana sunulur.