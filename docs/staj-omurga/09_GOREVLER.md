# 09 — Görevler (Yaşayan Kanban)

> **Amaç:** Her gün ve her hafta "şu an ne yapacağım?" sorusuna 5 saniyede cevap vermek; sprint disiplinini görünür kılmak; görevleri fazlara ve teslimatlara izlenebilir biçimde bağlamak.
> **Kapsam:** Bu hafta sprint odağı, aktif görev, faz fazlandırılmış backlog (Faz 0–5, 80+ görev), engelliler, sprint ritmi, WIP limit, yeni görev ekleme prosedürü.
> **Son güncelleme:** 2026-07-06
>
> Bu dosya **yaşar**: her gün/haftada güncelle. Durum sistemi `03_FAZLAR_VE_DURUMLAR.md` Bölüm 4'te tanımlandı.

---

## Bu hafta (sprint odağı)

> Faz 2 kapanışı — Kod tarafı (`hasat-zamani/`) tamamlandı: 10 parsel, kural motoru, GEE canlı veri, T-207 tablosu, 27 test. Kalan işler insan-tarafı: hoca onayı, demo kaydı, gerçek buğday parseli + saha etiketi temini.

| ID | Görev | Faz | Durum | Sahip | Bitiş |
|---|---|---|---|---|---|
| T-001 | ADR-001'i imzala (buğday + Konya kararı yazılı) | 0 | 🟠 Yapılıyor | Burak | bu hafta |
| T-002 | Konya il müd. ve Çumra Ziraat Odası iletişim listesi çıkar | 0 | 🟡 Bu hafta | Burak | bu hafta |
| T-003 | Veri talep e-postası taslağı (parsel + hasat tarihi) — **T-207 bulgusu gereği acil: ekimi doğrulanmış buğday parselleri iste** | 0 | 🟡 Bu hafta | Burak | bu hafta |
| T-005 | Hocayla 30 dk gözden geçirme toplantısı (Faz 2 demo + T-207 bulgusu) | 0 | 🟡 Bu hafta | Burak | bu hafta |
| T-208 | Faz 2 demo ekran kaydı (5 dk) | 2 | 🟡 Bu hafta | Burak | bu hafta |

---

## Yapılıyor (active)

```
T-001 — ADR-001 yazımı
```

---

## Backlog (henüz başlanmadı, faza göre sıralı)

### Faz 0 — Keşif

- T-004 — GitHub repo aç (lokal git repo var; GitHub'a push + lisans seçimi kaldı)
- T-006 — Veri envanter tablosunu doldur (gerçek kaynak adları)
- T-007 — Etik/KVKK kısa notu (tek sayfa) yaz
- T-009 — `docker-compose.yml` placeholder
- T-010 — Hocadan resmi staj başlangıç tarihi al

### Faz 2 — MVP-V1 kalanlar

- T-202 — Buğday hasat eşiklerini Yue 2024'e göre kalibre et (V1'de NDVI_HARVEST_FLOOR=0.25 sezgisel; literatür kalibrasyonu bekliyor)
- T-209 — Streamlit Cloud üzerinde public yayın

### Faz 3 — MVP-V2 (FastAPI + PWA + ML)

- T-301 — FastAPI iskelet `/health` `/version`
- T-302 — Postgres + PostGIS Docker ile lokal
- T-303 — Alembic migration: `parcels`, `labels`, `predictions`, ...
- T-304 — `/parcels` CRUD
- T-305 — `/parcels/{id}/timeseries` GET
- T-306 — `/parcels/{id}/predict` GET
- T-307 — JWT auth (basit)
- T-308 — React + Vite iskelet, Tailwind, shadcn
- T-309 — MapCanvas + Leaflet + parsel ekleme
- T-310 — TimeSeriesChart komponent
- T-311 — PredictionCard
- T-312 — PWA manifest + service worker (offline cache)
- T-313 — RF baseline eğitim notebook (`03_ml_baseline.ipynb`)
- T-314 — XGBoost kalan-gün eğitim (`04_xgb_remaining_days.ipynb`)
- T-315 — MLflow lokal kurulum + 3 deney kaydı
- T-316 — `evaluate.py`: MAE, ±gün isabet, calibration
- T-317 — Docker compose: api + db + frontend
- T-318 — GitHub Actions CI: lint + test + build
- T-319 — Vercel deploy frontend
- T-320 — Render/Fly deploy backend
- T-321 — Faz 3 demo ekran kaydı

### Faz 4 — Derinleşme

- T-401 — S1+S2 füzyon özellikleri
- T-402 — HLS koleksiyonu entegrasyonu
- T-403 — İkinci pilot bölge: ayçiçeği veri talebi
- T-404 — Saha mobil etiket formu (Google Form veya basit web)
- T-405 — 30 saha etiketi topla
- T-406 — SHAP açıklanabilirlik notebook
- T-407 — Anomali bayrağı (kuraklık/dolu)
- T-408 — Bulutlu sezon kapsama testi raporu
- T-409 — Ablation çalışması (indeks bazında etki)
- T-410 — Faz 4 ara raporu

### Faz 5 — Ticarileşme + tez

- T-501 — React Native iskelet
- T-502 — RN Leaflet köprü (react-native-maps)
- T-503 — RN push bildirim
- T-504 — RN saha foto etiketleme
- T-505 — TestFlight/Internal Track yayın
- T-506 — Bitirme tezi taslak (her bölüm 1 sürüm)
- T-507 — Yayın taslağı (Türkçe)
- T-508 — Pilot kullanıcı görüşmesi 5 adet
- T-509 — İş modeli + fiyatlama dokümanı
- T-510 — Tez savunma sunumu

---

## Engelli (blocked)

| ID | Görev | Engel | Beklenen kalkış |
|---|---|---|---|
| — | — | — | — |

---

## Bitti (sprint sonunda arşivle)

> Not: T-1xx görevleri planda "notebook" olarak tanımlıydı; ADR-B-016 kararıyla
> test edilebilir `core/` modülleri olarak gerçekleşti (`hasat-zamani/`).

| ID | Görev | Bitiş |
|---|---|---|
| T-008 | `requirements.txt` ilk sürüm (+ pytest dev bağımlılığı) | 2026-07-06 |
| T-101 | GEE hesabı + `earthengine authenticate` + `EE_PROJECT` çalışır | 2026-07-06 |
| T-102 | Tek parsel S2 NDVI zaman serisi (`core/datasource.py: GEEDataSource._pull_s2`) | 2026-07-06 |
| T-103 | Bulut maskesi — SCL sınıf maskesi (s2cloudless yerine; yeterli) | 2026-07-06 |
| T-104 | Çoklu indeks: NDVI/NDMI canlı + NDRE fonksiyonu (`core/indices.py`) | 2026-07-06 |
| T-105 | S1 GRD VH zaman serisi (`GEEDataSource._pull_s1`) | 2026-07-06 |
| T-106 | Savitzky-Golay smoothing + birim test (`core/phenology.py`, `tests/test_phenology.py`) | 2026-07-06 |
| T-107 | Düzenli ızgara: demo 5 günlük; canlıda gözlem tarihi bazlı seri | 2026-07-06 |
| T-108 | Lokal cache — parsel-sezon CSV (`data/cache/`; parquet yerine CSV, ADR-B-016) | 2026-07-06 |
| T-109 | 10 parsel pipeline + görsel kontrol (T-207 grafiği) | 2026-07-06 |
| T-110 | ETL son hali — `core/datasource.py` (notebook yerine modül) | 2026-07-06 |
| T-201 | Fenoloji metrikleri SOS/POS/EOS (`core/phenology.py`) | 2026-07-06 |
| T-203 | Tahmin fonksiyonu: kalan-gün + güven (`core/rules.py`) | 2026-07-06 |
| T-204 | Streamlit harita + parsel seçimi (`app.py`, folium) | 2026-07-06 |
| T-205 | Streamlit zaman serisi grafiği (plotly, NDVI/NDMI/VH + CI bandı) | 2026-07-06 |
| T-206 | Streamlit tahmin paneli (+ "Neden bu tahmin?" açıklanabilirlik) | 2026-07-06 |
| T-207 | 10 parsel manuel doğrulama tablosu — `18_T207_DOGRULAMA_TABLOSU.md` (gerçek S2 verisiyle; ürün deseni uyuşmazlığı bulgusu dahil) | 2026-07-06 |

---

## Sprint ritmi

- **Pazartesi:** "Bu hafta" tablosunu temizle, en fazla 5 görev seç.
- **Çarşamba:** mid-sprint check, engel var mı?
- **Cuma:** demo + retro, kapanmamış görevleri taşı.

## WIP limit (yeniden hatırlat)

- `Yapılıyor` ≤ 2
- `İncelemede` ≤ 3

## Nasıl yeni görev eklerim?

```
1. ID ata: T-{faz}{sıra}
2. Faz seç
3. Tahmini süre belirt (S/M/L = 1-2 saat / yarım gün / 1+ gün)
4. Sahip ata
5. Backlog'da fazına ekle
```

---

İlgili: [`03_FAZLAR_VE_DURUMLAR.md`](./03_FAZLAR_VE_DURUMLAR.md) (durum tanımları) / [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md) (görevlerin teslimata bağı).

---

## Kısa horizon planları

### İlk 14 gün (Faz 0 — keşif)

| Gün | Görev | Kabul ölçütü |
|---|---|---|
| 1 | Hoca ile ilk gözden geçirme toplantısı, staj başlangıç tarihi netleşmesi | Yazılı özet + ADR-001 imza onayı |
| 2 | Konya İl Tarım ve Orman Müdürlüğü + Çumra Ziraat Odası iletişim listesi | 5+ kişi/kurum, ad-soyad-rol-iletişim |
| 3 | Veri talep e-postası taslağı (parsel sınırı + hasat tarihi) — KVKK notu dahil | Hocaya iletildi, onay alındı |
| 4 | Bakanlık veri portalı + ÇKS rehberi taraması | `12_LITERATUR_TARAMASI.md`'ye not |
| 5 | E-postalar gönderildi, takip çizelgesi açıldı | Bir Google Sheet veya repo md |
| 6-7 | GitHub repo aç, Apache-2.0 lisans, README iskeleti, CI placeholder | `git push origin main` yeşil CI |
| 8 | GEE servis hesabı (akademik) | İlk `ee.Initialize()` çalışıyor |
| 9 | Çumra/Karatay'da örnek 3 parsel için demo poligon (manuel) | `parcels/demo.geojson` |
| 10 | Tek parsel için S2 NDVI zaman serisi notebook (T-102 başlangıcı) | `notebooks/01_extract_timeseries.ipynb` ilk grafik |
| 11 | Hoca ara toplantısı: 14 gün özeti, sonraki sprint için teyit | Toplantı notu + güncellenmiş `09_GOREVLER.md` |
| 12 | Bulut maskesi entegrasyonu | Bulutlu tarihler temizleniyor |
| 13 | 10 parsele genişletme | Pipeline 10 parselde çalışıyor |
| 14 | Faz 0 → Faz 1 karar kapısı (G0) | Tüm G0 maddeleri yeşil |

### İlk 30 gün

İlk 14 günün üstüne:
- Sentinel-1 VH/VV pipeline (T-105)
- Savitzky-Golay smoothing + ızgaraya yeniden örnekleme (T-106, T-107)
- Parquet ihracı (T-108)
- 10 parsel için fenoloji metrikleri (SOS/POS/EOS) hesaplandı
- Faz 1 → Faz 2 karar kapısı (G1) yeşil
- İlk hoca ara raporu (`08_TESLIMATLAR.md` Bölüm 9 şablonu) teslim

### İlk 90 gün

İlk 30 günün üstüne:
- Faz 2 tam tamam: kural tabanlı tahmin + Streamlit demo (T-201–T-209)
- 10+ parselde manuel doğrulama tablosu
- Streamlit Cloud üzerinde public demo
- Faz 2 → Faz 3 karar kapısı (G2) yeşil
- FastAPI iskelet ve PostGIS şema oturmuş (T-301–T-303)
- React + Vite frontend iskelet (T-308)
- 6 ay senaryosunda: Faz 3 ortası — RF baseline ilk eğitim sonucu

### Literatür ve karşılaştırma görevleri (paralel akış)

| Süre | Görev | Çıktı |
|---|---|---|
| Hafta 1-2 | `12_LITERATUR_TARAMASI.md` makale tablosunu doldurmaya başla | 5+ makale notu |
| Hafta 3-4 | `13_UYDU_UYGUNLUK_MATRISI.md` puanlamasını kendi ölçütlerinle revize et | Tüm puanlar gerekçeli |
| Hafta 5-6 | `14_REKABET_VE_MEVCUT_SISTEMLER.md` için EOSDA, OneSoil, FieldView demo kayıt videolarını izle ve not düş | Her sistem için 1 paragraf |

---

## Bu dosyada alınan kararlar
- WIP limit (tek kişilik): `Yapılıyor` ≤ 2, `İncelemede` ≤ 3.
- Sprint uzunluğu: 1-2 hafta. Sprint sonunda kısa retro yazılır.
- Görev ID şeması: `T-{faz}{sıra}` (T-102 = Faz 1, görev 02).
- Her sprint başında "Bu hafta" tablosu ≤ 5 göreve indirilir.

## Açık sorular
- Hoca onayı gerekli görevler ayrı bir `🔵 Onayda` durumuna mı gitmeli? (Şimdilik `İncelemede` yeterli.)
- Görev → ADR bağı zorunlu olmalı mı? Şimdilik tavsiye düzeyinde.

## Sonraki aksiyonlar
- T-001 imzalandığında `ADR-001` durumunu `🟡 Öneri` → `✅ Kabul` çek.
- Sprint sonunda kapanan görevleri haftalık `Bitti` arşivine taşı (büyürse ay bazlı kategorize et).
