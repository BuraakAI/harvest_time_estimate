# 05 — Veri Bilimi: Problem Formları, Etiket Stratejisi, Modelleme ve Açıklanabilirlik

> **Amaç:** Hasat zamanı tahmini probleminin bilimsel olarak doğru tanımını yapmak; veri tabanını, etiketleme stratejisini ve modelleme yol haritasını akademik bir defter gibi yazmak.
> **Kapsam:** 3 problem formu (sınıflandırma / regresyon / fenoloji evresi), veri katmanları, etiket kaynakları + kalite puanı, indeks paleti, fenoloji metrikleri, baseline + ML + DL adımları, değerlendirme metrikleri, açıklanabilirlik, reproducibility.
> **Son güncelleme:** 2026-06-26

---

## 1. Problem üç farklı şekilde formüle edilebilir

Hasat zamanı tahmini görünüşte tek problem ama akademik literatürde **üç farklı form**da çalışılır. Hangisini ne zaman seçeceğimiz önemli.

### 1.1. Form A — Sınıflandırma: "hasada hazır mı / hazır değil mi?"

- **Çıktı:** ikili etiket (`ready` / `not_ready`) veya çok sınıflı (`weeks_ahead`: 0, 1, 2, 3+).
- **Avantaj:** Az etiketle çalışabilir; jüriye anlatılması kolay.
- **Dezavantaj:** "Tarih" granülerliği yok; lojistik planlamada kaba.
- **MVP uygunluk:** Yüksek (Faz 2 kural tabanlı çekirdek bu forma yakındır).
- **Tez/ticari uygunluk:** Düşük-orta.

### 1.2. Form B — Regresyon: "hasada kalan gün"

- **Çıktı:** sürekli sayı (gün), ± güven aralığı.
- **Avantaj:** Lojistik karar için doğrudan, akademik literatürde standart hedef.
- **Dezavantaj:** Daha çok ve daha kaliteli etiket ister.
- **MVP uygunluk:** Orta (Faz 3'te RF/XGBoost ile başlar).
- **Tez/ticari uygunluk:** **Yüksek — birincil hedef.**

### 1.3. Form C — Fenolojik evre tahmini: "şu an süt olum / hamur olum / sarı olum"

- **Çıktı:** ayrık evre etiketi.
- **Avantaj:** Zirai mühendise tanıdık, açıklanabilir.
- **Dezavantaj:** Evre sınırları belirsiz, etiket gürültülü olabilir.
- **MVP uygunluk:** Yüksek (yardımcı çıktı).
- **Tez/ticari uygunluk:** Orta (B'nin yardımcı katmanı).

### 1.4. Stratejimiz

| Faz | Birincil form | Yardımcı form |
|---|---|---|
| 1–2 | Form A (kural tabanlı) + Form C (evre etiketleme) | — |
| 3 | **Form B** (RF/XGBoost regresyon) | Form C (evre paneli) |
| 4 | Form B (radar+meteoroloji füzyonu) | Form C |
| 5 | Form B (DL) | Form A (basit kullanıcı uyarısı) |

V1 demo'da kullanıcı her üçünü görür: "süt olum (Form C) → hasada 22 gün (Form B) → bu hafta hazır değil (Form A)".

---

## 2. Veri katmanları (zorunlu vs. opsiyonel)

| Katman | Zorunlu | Birincil kaynak | Yedek | Erişim formu | Notlar |
|---|---|---|---|---|---|
| Parsel sınırı | ✅ | ÇKS / kullanıcı shapefile | OneSoil benzeri delineation, U-Net | Yazılı izin | Pilot 30–100 parsel |
| Ürün tipi etiketi | ✅ | Üretici beyanı / ÇKS | Sezon başı RF/XGB sınıflandırma | Yazılı izin | V1 yalnız buğday |
| Hasat tarihi etiketi | ✅ (V2) | Üretici / kooperatif / biçerdöver | Mobil saha formu, foto-EXIF | İzin + KVKK | En kritik darboğaz |
| Sentinel-2 zaman serisi | ✅ | Copernicus / GEE / AWS Open Data | Microsoft Planetary | Açık | 5 günde bir |
| Sentinel-1 zaman serisi | ✅ (Faz 4) | Copernicus / GEE | ASF | Açık | ~6 gün (çift uydu); 2022–2024 tek uyduyla 12 gün, S1C/S1D ile tekrar 6 gün; bulut bağımsız |
| Landsat 8/9 / HLS | 🟡 | NASA / GEE | USGS | Açık | Süreklilik için |
| Meteoroloji | ✅ | MGM / MEVBİS | ERA5-Land | Kayıt | Sıcaklık, yağış, GDD |
| Toprak | 🟡 | SoilGrids | ESDAC | Açık | V2 özelliği |
| Tarihsel takvim | ✅ | Bakanlık il müd. | Akademik raporlar | Açık | Önsel |

---

## 3. Etiket toplama stratejisi (5 kanal)

Etiket kalitesi MVP'nin sınırlayıcısıdır. Beş paralel kanal kullanılır.

| Kanal | Açıklama | Kalite (0–1) | Hız |
|---|---|---|---|
| **Üretici beyanı** | Telefonla / forma "tarlamı X tarihinde biçtim" | 0.6–0.8 | Hızlı |
| **Kooperatif kaydı** | Kantar/depo defteri tarihi | 0.7–0.9 | Orta |
| **Biçerdöver logu** | GPS+tarih CSV/GPX (varsa) | 0.9–1.0 | Yavaş (cihaz bağımlı) |
| **Saha fotoğrafı (EXIF)** | Tarih+GPS+görsel "biçildi" | 0.7–0.9 | Hızlı (sezon içi) |
| **Tarihsel takvim + uzman onayı** | Bölgesel ortalama + ziraat odası onayı | 0.4–0.6 | Çok hızlı |

### 3.1. Çapraz doğrulama

İki bağımsız kaynak ≥ 7 gün uyuşmazsa etiket **şüpheli** işaretlenir; eğitimde ya çıkarılır ya da `confidence` ile düşük ağırlıkla kullanılır.

### 3.2. Veri kalitesi puanlama (parsel-sezon başına)

```
quality_score =
    0.30 * has_parcel_boundary
  + 0.20 * cloud_free_obs_score   # n_clear / n_nominal
  + 0.20 * label_source_score     # max(label_quality_per_source)
  + 0.15 * temporal_alignment     # etiket ile son gözlem arası gün
  + 0.15 * meteorology_completeness
```

Eşikler:
- `quality_score ≥ 0.70` → eğitim ve test için tam ağırlık.
- `0.40 ≤ quality_score < 0.70` → eğitim için yarım ağırlık, test için dışla.
- `< 0.40` → tamamen dışlanır.

### 3.3. KVKK ve sahiplik kuralı

- Kullanıcı parselini eklerken etiket girişi için **opt-in** onayı verir.
- Etiket sahibi kullanıcıdır; çıktı tahminleri kullanıcı izni ile anonim toplulaştırılır.
- 30 gün içinde silme talebi karşılanır.

---

## 4. ETL adımları (uçtan uca)

```
1. Parsel kaydı (geojson)
        ↓
2. Sentinel-2 sahne sorgusu (cloud_pct < 80, season aralığı)
        ↓
3. Bulut maskesi (s2cloudless veya QA60 + SCL)
        ↓
4. Atmosferik düzeltme (L2A SR varsayılan)
        ↓
5. Parsel istatistiği (mean/median per band)
        ↓
6. İndeks hesaplama (NDVI, EVI, EVI2, NDMI, NDRE, SAVI, GCI)
        ↓
7. Sentinel-1 paralel akış (VH/VV, Lee filter, dB)
        ↓
8. Smoothing (Savitzky-Golay window=15, order=3)
        ↓
9. Düzenli ızgaraya yeniden örnekleme (5 günde bir interpolasyon)
        ↓
10. Meteoroloji birleştirme (GDD, kümülatif yağış)
        ↓
11. Fenoloji metrikleri (SOS, POS, EOS, max, slope_decay)
        ↓
12. Parquet'e yaz (parcel_id, season, indeks)
        ↓
13. timeseries_summary tablosuna URI'yi kaydet
```

---

## 5. İndeks paleti

| İndeks | Formül kabaca | Hangi sinyali yakalar | Buğday için rolü |
|---|---|---|---|
| NDVI | (NIR-Red)/(NIR+Red) | Genel canlılık | Baseline; geç dönem doygunluk |
| EVI / EVI2 | toprak/atmosfer düzeltilmiş | Yoğun kanopi vigor | Olgunluk öncesi kararlı |
| NDMI | (NIR-SWIR1)/(NIR+SWIR1) | Kanopi su içeriği | Olgunlaşma + kuruma → düşer |
| NDRE | (NIR-RedEdge)/(NIR+RedEdge) | Klorofil | Senesens duyarlı |
| SAVI | toprak parametreli | Seyrek örtü | Erken dönem |
| MSAVI | modifiye SAVI | Toprak çıplak alan | Erken vejetatif |
| GCI | NIR/Green-1 | Yeşil klorofil | Stres tespiti |
| VH (S1, dB) | radar geri saçılım | Kanopi yapısı + nem | Hasat olayı (ani düşüş) |
| VV (S1, dB) | radar geri saçılım | Yapraklı kütle | Destek |
| VH/VV oranı | normalize | Yön bağımsız doku | Sezon dinamiği |

**Pratik kural:** V1'de NDVI + NDMI + VH yeterli. Diğerleri Faz 4 ablation çalışmasıyla eklenir.

---

## 6. Fenoloji metrikleri

| Metrik | Anlamı | Hesabı |
|---|---|---|
| SOS (Start of Season) | Vejetatif başlangıç | NDVI baseline'a göre %20 yükseliş |
| POS (Peak of Season) | Tepe noktası | smoothed NDVI argmax |
| EOS (End of Season) | Senesens sonu | NDVI tepeden %30'a iniş |
| LOS | Sezon uzunluğu | EOS - SOS |
| Max NDVI | Tepe seviyesi | smoothed max |
| Plateau süresi | Tepede kalış | NDVI > 0.85*max gün sayısı |
| Senescence slope | Kuruma hızı | linregress(POS..EOS) |
| GDD-cumulative | Termal birikim | Σ max(0, T_avg - T_base) |
| Bulut boşluk oranı | Kapsama | gözlem / nominal gün |
| VH minimum tarihi | Hasat olayı proxy | argmin(VH son 30 gün) |

---

## 7. Modelleme yol haritası (kademeli)

### 7.1. Baseline (V1, Faz 2) — kural tabanlı

Üç bileşen birleşir:

#### Bileşen 1 — Bölgesel takvim önseli
Konya buğdayında tarihsel hasat penceresi: Haziran sonu – Temmuz; sulu alanda (Çumra) Temmuz ağırlıklı, Ağustos başına sarkabilir (*İl Tarım Müdürlüğü ürün takvimiyle bağlanmalı*).

#### Bileşen 2 — NDVI tepe sonrası düşüş kuralı
```
Eğer days_since_pos ≥ 28 ve ndvi_now < 0.45 ve slope_last_14d < -0.005:
    pheno_phase = "olgun"
    est_harvest = bugün + 0..7 gün
```

#### Bileşen 3 — NDMI kuruma sinyali
```
Eğer ndmi_drop_last_14d > 0.15 ve vh_min_last_14d düşüyor:
    pheno_phase = "olgun-hasat"
    est_harvest = bugün + 0..5 gün
    confidence += 0.1
```

Eşikler Yue 2024 + Liao 2023 + Sedano 2025 referansından (*doğrulanacak*) Konya verisinde kalibre edilir.

### 7.2. Random Forest baseline (V2, Faz 3)

**Özellikler:**

| Özellik | Tip | Not |
|---|---|---|
| max_ndvi | float | Tepe seviyesi |
| pos_doy | int | Yılın günü |
| eos_doy | int | Senesens sonu DOY |
| los_days | int | Sezon uzunluğu |
| senescence_slope | float | Kuruma hızı |
| ndmi_at_pos | float | POS'ta NDMI |
| ndmi_min_last30 | float | Son 30 gün NDMI min |
| vh_min_last30 | float | Son 30 gün VH min |
| gdd_cumulative_at_pos | float | POS'ta GDD |
| precip_last30 | float | Son 30 gün yağış |
| crop_code (ohe) | category | V1'de tek değer |
| region_code (ohe) | category | İlçe kodu |

**Hedef:** `remaining_days = harvest_date - prediction_date`.

**Validasyon:** GroupKFold (parcel_id) — aynı parsel hem train hem test'te olmasın. Ayrıca **temporal split** (önceki sezonlar train, son sezon test).

### 7.3. XGBoost / LightGBM (V3, Faz 3 sonu)

- Lag özellikleri (NDVI t-7, t-14, t-21).
- GDD lag ve kümülatif yağış lag.
- Hyperparam: Optuna 50–100 deneme.
- Quantile loss (P10, P50, P90) → güven aralığı çıktısı.
- SHAP ile açıklanabilirlik.
- LightGBM XGBoost'a alternatif; ikisini ablation karşılaştırmalı.

### 7.4. LSTM / Temporal Transformer (V4, Faz 4)

- Girdi: çok değişkenli zaman serisi (NDVI/EVI/NDMI/VH × T).
- Çıktı: kalan-gün regresyon + güven aralığı (kuantil regresyon).
- Mimari adayları: BiLSTM, TFT (Temporal Fusion Transformer), Informer.
- Veri yetersizse: transfer öğrenme (önceden eğitilmiş model üzerinde fine-tuning).

> **Önemli kısıt:** DL modelinin RF/XGB baseline'ını anlamlı şekilde geçemediği durum **erken sinyaldir**: sorun büyük olasılıkla etikettedir, modelde değil.

---

## 8. Değerlendirme metrikleri

| Metrik | Formül | Hedef V1 | Hedef V3 |
|---|---|---|---|
| MAE (gün) | mean(|y - ŷ|) | ≤ 10 | ≤ 5 |
| RMSE (gün) | sqrt(mean((y-ŷ)²)) | ≤ 14 | ≤ 7 |
| ±3 gün isabet | |y-ŷ|≤3 oranı | ≥ %30 | ≥ %55 |
| ±7 gün isabet |  | ≥ %60 | ≥ %80 |
| ±14 gün isabet |  | ≥ %90 | ≥ %97 |
| Kapsama | tahmin yapılabilen parsel oranı | ≥ %85 | ≥ %95 |
| Bias | mean(ŷ - y) | |bias|≤2 | |bias|≤1 |
| ECE (kalibrasyon) | Expected Calibration Error | < 0.15 | < 0.08 |
| Reliability diagram | %80 CI içine düşen oran | %75–85 | %78–82 |

Kalibrasyon: kuantil regresyon çıktıları + Platt scaling veya Isotonic regression sonrası ECE düşürülür.

---

## 9. Açıklanabilirlik

### 9.1. Üç katmanlı sunum

1. **Sinyal panel** — `reason_signals` JSON → kullanıcıya doğal dilde özet ("POS'tan 21 gün geçti, NDMI hızlı düşüyor").
2. **SHAP / feature importance** — tek tahmin için en güçlü 5 özellik bar grafik.
3. **Eğri yorumu** — NDVI/NDMI/VH üzerinde işaretli SOS/POS/EOS + tahmin tarihi.

### 9.2. Global önem

- Permutation importance ve SHAP global özet — modelin genel davranışını gösterir.
- Region/ürün bazlı bakış — domain shift'i erken yakalar.

### 9.3. Fail-safe yorumu

Model güveni düşükse (≤ 0.4) UI:
- "Bu tahmin düşük güvenli"
- Sebep listesi: "son 14 günde 9 günlük bulutluluk", "etiket havuzu küçük", "yıl dışı meteoroloji".
- Kullanıcı "neden hesabımdan farklı?" dediğinde açıklama bu üç madde üzerinden verilir.

---

## 10. Veri kalitesi kontrol listesi

Her sezon başlangıcında:

- [ ] Parsel poligonları geçerli (ST_IsValid)
- [ ] Parsel alanları 0.5–1000 ha aralığında
- [ ] Ürün etiketi izinli sözlükten
- [ ] Sentinel-2 son 30 gün ≥ 4 bulutsuz gözlem
- [ ] Bulut yüzdesi parselin %50+ kapatıyorsa S1'e düş
- [ ] Aynı parsele aynı sezon birden fazla etiket yok
- [ ] Etiket alanı sapması > %20 → işaretle
- [ ] Meteoroloji eksik tarih oranı < %5
- [ ] Region_code beyaz listede
- [ ] Tahmin sonuçlarında `confidence` boş değil

---

## 11. Reproducibility

- Notebook'lar `papermill` ile head-to-tail çalışır.
- `RANDOM_STATE = 42` her yerde.
- Veri sürümleme: DVC (S3 backend).
- Model artifaktları MLflow `runs/` ile.
- `pyproject.toml` lock'ta sabit.
- Docker compose ile lokal stack.
- README'de "git clone → docker compose up → http://localhost:8000/docs".

---

## 12. Bu dosyada alınan kararlar

- Hasat zamanı problemi **üç formda** ifade edilebilir; V1 birincil form **regresyon (kalan-gün)**, yardımcı **fenoloji evresi**.
- Etiket toplama 5 paralel kanaldan (üretici, kooperatif, biçer logu, saha foto EXIF, tarihsel takvim).
- Veri kalitesi puanı 0–1 arası ağırlıklı; eğitim/test eşikleri belli.
- Modelleme **kural → RF → XGB/LGBM → DL** sırasıyla.
- Değerlendirmede tek metrik değil, **çoklu metrik + kalibrasyon** ölçütü.
- Açıklanabilirlik üç katmanlı (sinyal panel, SHAP, eğri yorumu).

---

## 13. Açık sorular

- Konya buğday için ürün-spesifik T_base hangi değerle alınacak (literatürde 0°C yaygın ama bölge spesifik *doğrulanmalı*)?
- HLS ürününün Konya bölgesi için kapsama yoğunluğu sezonluk olarak nedir?
- Kalibrasyon için Platt vs Isotonic seçimi hangi MSE/MAE'de daha iyi?
- Domain shift testi (Konya → Trakya) hangi metriği baz alacak?

---

## 14. Sonraki aksiyonlar

1. Faz 1: tek parselde indeks + smoothing + fenoloji metrik fonksiyonları yazılacak.
2. Faz 2 başında Yue 2024 + Liao 2023 eşiklerinin Konya verisine kalibrasyonu.
3. Veri kalitesi puanlama fonksiyonu `ml/quality.py` olarak kodlanacak.
4. SHAP entegrasyonu Faz 3 sonu / Faz 4 başı.

---

İlgili: [`04_TEKNIK_MIMARI.md`](./04_TEKNIK_MIMARI.md) (sistemde yer) / [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md) (kalite kapıları) / [`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md) (yöntem kaynakları).
