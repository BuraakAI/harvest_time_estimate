# 12 — Literatür Taraması ve Akademik Konumlanma

> **Amaç:** Hocaya/jüriye "bu konuda kim çalıştı, sen ne ekliyorsun?" sorusuna **kanıt ve kaynakla** cevap verebilmek; tezde literatür bölümünün omurgasını oluşturmak.
> **Kapsam:** Literatür arama stratejisi, anahtar makale karşılaştırma tablosu, konu başlıklarına göre referanslar, "yapan var mı?" özeti, farklılaşma noktaları, literatürdeki boşluklar, kaynakça (DOI/yıl/yazar bilgili).
> **Son güncelleme:** 2026-06-26
> **Uyarı:** Aşağıdaki kaynakların önemli bir kısmı `deep_search.md` derin tarama belgesinden alınmıştır. Her makaleyi DOI ile **kendin de doğrulamalısın**; staj raporuna girmeden önce her satır bir kez "doğrulanmıştır" işaretiyle kapatılmalıdır.

---

## 1. Literatür taramasının amacı

Bu projenin akademik savunulabilirliği üç soruya dayanıyor:

1. **Yapan var mı?** — Evet, dünyada ve kısmen Türkiye'de var. Bunu örtmek değil, açıkça yazmak gerekir.
2. **Bizim farkımız ne?** — Bölge/ürün dikeyliği, açık veri MVP yaklaşımı, parsel-PWA odağı, "kalan-gün" çıktısının Türkiye'ye yerelleştirilmesi.
3. **Boşluk nerede?** — Etiket erişimi, parsel düzeyi doğruluk raporlanmış değer, çiftçi-uygulamasına dönüşme, çoklu sezon kararlılığı.

Literatür taraması bu üç soruya dayanak üretir.

---

## 2. Literatür arama stratejisi

### 2.1. Anahtar terim setleri

| Set | Anahtar kelimeler | Hedef |
|---|---|---|
| **Hasat tarihi tahmini** | "harvest date", "harvest detection", "harvest readiness", "remaining days to harvest", Sentinel-2, SAR, time series | Çekirdek metodoloji |
| **Fenoloji** | "crop phenology", "phenological metrics", "SOS POS EOS", NDVI, EVI, Savitzky-Golay | Özellik mühendisliği |
| **Uydu füzyonu** | "Sentinel-1 Sentinel-2 fusion", "optical SAR", HLS, harmonization | Bulut sigortası |
| **ML / DL** | "Random Forest crop", "XGBoost phenology", LSTM crop yield, transformer time series | Modelleme |
| **Türkiye bağlamı** | "Türkiye uzaktan algılama", "buğday Sentinel-2", Konya, Şanlıurfa, ÇKS | Yerel literatür |
| **Operasyonel ürünler** | GEOGLAM, Sen2-Agri, EOSDA, OneSoil | Rekabet |

### 2.2. Veri tabanları

- **Birincil:** Google Scholar, Scopus, Web of Science.
- **İkincil:** ResearchGate (yazardan PDF talebi), Semantic Scholar (alıntı zinciri).
- **Türkçe:** TR Dizin, ULAKBİM, DergiPark, YÖK Tez merkezi.
- **Açık erişim:** MDPI Remote Sensing, ISPRS, IEEE Xplore (kurum erişimi varsa).

### 2.3. Tarama disiplini

- Her makale için tek satırlık "alıntı olarak ne kullanırım?" notu.
- DOI yoksa "doğrulanmalı" etiketi.
- Yıl ≥ 2020 öncelikli; klasik referanslar (Tucker NDVI 1979 vb.) sadece teorik bölüm için.

---

## 3. Anahtar makale karşılaştırma tablosu

| Yazar / Yıl | Ülke / Bölge | Ürün | Uydu / Veri | Yöntem | Tahmin hedefi | Metrik | Sonuç | Bizim projeye katkısı |
|---|---|---|---|---|---|---|---|---|
| **Sedano et al. 2025** ✅ | İspanya (Castilla y León) | Tahıllar (buğday vb.) | Sentinel-2 zaman serisi | Eğitim verisi gerektirmeyen kural tabanlı | Hasat tarihi tespiti | Operasyonel kapsama | Geniş ölçekte etiketsiz hasat tespiti mümkün | V1 kural tabanlı çekirdeğin **doğrudan dayanağı** |
| **Liu et al. 2025 (NHPI)** ✅ | ABD Mısır Kuşağı | Mısır, soya | Landsat + Sentinel-2 | NHPI (özel hasat indeksi) + ML | Hasat tarihi (tarla düzeyi) | MAE 4 gün, R² 0.85 | Tarla düzeyinde yüksek doğruluk | Kalan-gün modelinde "harvest-specific" indeks fikri |
| **Mimić et al. 2025** | Sırbistan | Tahıllar | Sentinel-1 SAR (VH/VV) | ML (RF, SVM) | Hasat tarihi | Bulut bağımsız doğruluk | SAR ile tek başına başarılı | Bulutlu sezonlarda S1'i çekirdeğe alma kararının kanıtı |
| **Liao et al. 2023** | Çin | Kışlık buğday, mısır | Sentinel-2 | Saha içi fenoloji + NRT tahmin | Fenolojik evre + erken tahmin | Evre isabet | Saha içi fenoloji üretilebilir | Fenoloji çıkarımı pipeline'ımızın metodolojik altyapısı |
| **Cyran et al. 2025** | Mısır (Nil Deltası) | Karma küçük parseller | Sen2Like (S2 + Landsat 8/9) | Füzyon + sezon tespiti | Sezon tarihleri | Tek S2'ye karşı iyileşme | Küçük parsellerde HLS füzyonu değerli | İkinci pilot bölge (küçük parseller) için yol gösterici |
| **Yue et al. 2024** ✅ | Çin | Kışlık buğday | Sentinel-2 + eşik | Çok zamanlı + dinamik eşik | Olgunluk tahmini | Eşik kalibrasyonu | Buğdayda olgunluk eşiklenebilir | **Konya pilotu için en yakın referans** |
| **Garcia-Perez et al. 2026** | İspanya | Çeşitli | Sentinel-2 | Unsupervised + fenoloji | Crop calendar türetimi | Tekrarlanabilirlik | Ürün takvimi otomatik üretilebilir | Bölgesel takvim önseli için referans |
| **Qin et al. 2024** | Çin | Mısır | Sentinel-2 | Savitzky-Golay + dinamik eşik | Mısır fenolojik evreleri | Evre isabet | 10 m'de hassas evre tespiti | V3 mısır pilotu için yol gösterici |
| **Şimşek 2024** | Türkiye | Çeşitli | Sentinel-1 + Sentinel-2 | XGBoost | Ürün desen tespiti | Sınıflandırma doğruluğu | Türkiye bağlamında optik+radar+ML çalışıyor | **Türkiye yerel referans** (yöntem ve veri seçimi) |
| **Buğday ekim alanlarının S2A ile belirlenmesi 2024** | Türkiye | Buğday | Sentinel-2A | Bant analizi | Ekim alanı | Sınıflandırma | Buğdayda B2/B3/B4/B8 etkili | İndeks paletinin sadeliği (NDVI omurga) için destek |
| **Radočaj et al. 2025 (suitability)** | Hırvatistan | Çeşitli | Sentinel-2 | İndeks ablation | Ekilebilirlik proxy | İndeks kıyas | WDRVI/EVI2 bazı ürünlerde NDVI'dan iyi | İndeks paletinin çoğullanması (sadece NDVI değil) |
| **Fuentes et al. 2026 (field-aware, explainable)** | Karma | Çeşitli | Fenoloji + iklim reanalysis | Açıklanabilir ML | Erken sezon verim | MAE + SHAP | Açıklanabilirlik feasible | V3 SHAP paneli için yöntem dayanağı |
| **Jiang et al. 2024 (Field Rover)** | Çin | Mısır vb. | Saha rover + uydu | Yer doğrulama yöntemi | Hasat tarihi etiketi | Etiket kalitesi | Etiket darboğazı çözümü | Saha etiket kanalı tasarımının önemi |
| **Parreiras et al. 2025 (HLS + ensemble ML)** | Brezilya | Çeşitli | HLS | Yoğun zaman serisi + ensemble | Ürün özellikleri | İyileşme | HLS yoğunluk fark eder | Faz 4 HLS entegrasyonunun gerekçesi |
| **Rivas et al. 2024 (PROBA-V country-scale)** | Karma | Çeşitli | PROBA-V | Disagregasyon | Crop-specific phenomap | Ülke ölçeği | Çoklu çözünürlük dengesi şart | Türkiye ölçek uyarısı |

> **Not:** Bu satırların büyük kısmı `deep_search.md` derin tarama belgesinden gelmiştir. Tezde alıntılanmadan önce **DOI ile bire bir doğrulanmalıdır**. Eksik veya yanlış DOI durumunda satır kayıttan çıkarılır veya "doğrulanmalı" işaretiyle bekletilir.

---

## 4. Konu başlıklarına göre literatür özeti

### 4.1. Uydu tabanlı tarımsal izleme (genel çerçeve)

Tarımsal uzaktan algılama 1980'lerden bu yana NDVI ekseninde gelişti; 2010 sonrası Sentinel-2'nin operasyonel hâle gelmesiyle parsel düzeyine indi. Son 5 yılda fenoloji **tek başına izleme** olmaktan çıkıp **operasyonel karar destek** girdisine dönüştü. Üst çerçeve referansları: Radočaj 2026 review, Kumhálová 2026, Zhang 2025 crop mapping review.

### 4.2. Fenoloji çıkarımı

Fenoloji metrikleri (SOS, POS, EOS, LOS) 2000'lerden beri MODIS üzerinde çalışılır; Sentinel-2 ile parsel ölçeğine indirilebildi. Düzgünleştirme yöntemleri: Savitzky-Golay (Qin 2024), Whittaker, double-logistic. Türetilen metrikler kalan-gün modeli için ana özelliklerdir.

### 4.3. Hasat tarihi tahmini

Üç yaklaşım hâkim:
1. **Eşik tabanlı** (Yue 2024, Sedano 2025): NDVI/NDMI'nin sezon-içi davranışına göre kural.
2. **Özel indeks** (Liu 2025 NHPI): Hasada özel formülasyon.
3. **ML/DL** (Mimić 2025, Fuentes 2026): RF/XGBoost ya da DL ile regresyon.

MAE 3-4 gün düzeyine inebilen çalışmalar (Liu 2025) çok kaliteli etiket altyapısıyla birlikte gelmektedir.

### 4.4. Buğday olgunluk / hasat çalışmaları

Yue 2024 doğrudan kışlık buğday olgunluğu üzerinde çalışır ve eşik tabanlı yöntem önerir. Türkiye'de buğday için doğrudan **hasat-zamanı tahminine** odaklanan, parsel düzeyinde yayınlanmış bir çalışma sınırlıdır; çoğu Türkçe çalışma "ekim alanı tespiti" veya "verim tahmini"ne odaklanır (Şimşek 2024 ürün deseni; "Buğday ekim alanlarının S2A ile" 2024 alan tespiti).

### 4.5. Sentinel-2 optik zaman serileri

Sentinel-2 13 bantı, 10/20/60 m çözünürlüğü ve 5 günlük tekrarı ile fenoloji çalışmalarının baz omurgasıdır. L2A SR ürünü atmosferik düzeltmeyi içerir. Bulut maskesi için s2cloudless veya QA60+SCL kullanılır.

### 4.6. Sentinel-1 radar zaman serileri

Sentinel-1 C-band SAR, VH/VV polarizasyonları; iki uydu konfigürasyonunda ~6 günlük tekrar. **Önemli not:** S1B Aralık 2021'de arızalandı (görev Ağustos 2022'de resmen sonlandı), 2022–2024 arası tek uyduyla revisit 12 güne çıktı; S1C (Aralık 2024) ve S1D (Kasım 2025) ile tekrar ~6 güne dönüyor. Bulutlardan bağımsız olduğu için hasat olayı tespitinde (VH ani düşüş) güçlü (Mimić 2025).

### 4.7. Optik–radar füzyonu

Optik fenolojik dinamiği, radar olayı yakalar. Nduku 2024 buğdayda S1+S2 kombinasyonunun biyofizik parametre çıkarımında etkin olduğunu gösterir. Faz 4'te ana derinleştirme yönü.

### 4.8. Makine öğrenmesi yöntemleri

Klasik ML (RF, XGBoost, LightGBM) tablo verilerde standart baseline. DL (LSTM, Temporal Fusion Transformer) çok değişkenli zaman serisi için tercih edilir ama daha çok etiket gerektirir. Demissie 2026 PRISMA taraması Akdeniz koşullarında RF/XGBoost'un operasyonel olduğunu, LSTM/CNN'in yükseldiğini gösterir.

### 4.9. Türkiye bağlamı

Türkiye bağlamlı uzaktan algılama yayınları çoğunlukla:
- Ürün desen ve alan tespiti (Şimşek 2024, "Buğday ekim alanlarının S2A ile" 2024)
- Verim tahmini ve kuraklık (TÜBİTAK projeleri)
üzerinedir. **Doğrudan hasat-zamanı tahminine odaklı, parsel düzeyinde, mobil-arayüzlü Türkçe yayın** taramamızda az sayıda — bu da projenin **özgün katkı** alanıdır.

---

## 5. "Yapan var mı?" — dürüst cevap

| Soru | Cevap |
|---|---|
| Akademik olarak hasat tarihi tahmini yapıldı mı? | Evet, geniş literatür mevcut (yukarıdaki tablo). |
| Genel tarım izleme ürünleri var mı? | Evet (GEOGLAM, EOSDA, OneSoil, FieldView, Cropwise vb.). Bkz. `14_REKABET_VE_MEVCUT_SISTEMLER.md`. |
| Türkiye/Konya/buğday/parsel/PWA dikeyinde özel sistem var mı? | Taramamızda yaygın bir muadil bulamadık. Kamu tarafında TARBİL gibi bilgi sistemleri var ama hasat-zamanı + mobil PWA dikeyi farklı bir konum. |

Sonuç: **Bilimsel olarak yenilik orta düzey; uygulama-ürün dikeyinde Türkiye için niş açık.**

---

## 6. Bizim farklılaşma noktalarımız

1. **Ürün/bölge dikeyliği** — tek ürün (kışlık buğday) + tek bölge (Konya) ile derinlik.
2. **Açık veri tabanlı düşük maliyetli MVP** — Sentinel-2 + Sentinel-1 + GEE; ticari uydu bağımlılığı yok.
3. **Hasat-zamanı odaklı çıktı** — verim tahmini değil, **kalan gün** ve **hasat penceresi**.
4. **Parsel + PWA** — ürün-pazar uyumu açısından Türkiye'de boş alan.
5. **Açıklanabilirlik** — SHAP + güven skoru; her tahminle "neden" gelir.
6. **KVKK ve veri sahipliği bilinciyle inşa** — kullanıcı haklarının operasyonel karşılığı tasarımdan itibaren.
7. **Ölçeklenebilir akademik → ticari yol** — V1 GEE; V3 yerel pipeline; V5 mobil + ticari.

---

## 7. Literatürdeki boşluklar

- **Etiket erişimi** — neredeyse tüm ML çalışması zayıf etiketle veya simulasyonla yetiniyor (Jiang 2024 bu boşluğu açıkça yazıyor).
- **Çoklu sezon kararlılığı** — modeller tek-iki sezonla raporlanıyor; iklim kayması durumunda davranış belirsiz.
- **Pilot dışı genelleme** — ülke ya da tek bölgede çalışan model başka bölgede çökme örnekleri tartışılmıyor.
- **Çiftçi uygulamasına dönüşüm** — akademik çalışmaların çoğu "demo" düzeyinde kalıyor; gerçek kullanıcı görüşmeleri raporlanmıyor.
- **Türkçe akademi** — hasat-zamanı odaklı parsel düzeyi yayın eksik.

Bu boşlukların her biri tezde **tartışma** ve **gelecek çalışma** olarak kullanılır.

---

## 8. Kaynakça (yıl • yazar • başlık • doğrulama durumu)

> **Disiplin:** Aşağıdaki kayıtların DOI'leri `deep_search.md`'den geliyor; tez yazımında her satır **DOI doğrulanıp** kaynakçaya geçirilecek. "Doğrulanmalı" işareti olan satırlar hocaya gösterilmeden önce kontrol edilir.

| Yıl | Yazar(lar) | Başlık (kısa) | Yer / Dergi | Doğrulama |
|---|---|---|---|---|
| 2026 | Radočaj et al. | Satellite RS for Crop Yield Prediction (review) | (doğrulanmalı) | 🟡 |
| 2026 | Kumhálová et al. | Monitoring of Agricultural Crops by RS in Central Europe | (doğrulanmalı) | 🟡 |
| 2026 | Demissie et al. | AI + RS in Mediterranean agroecosystems (PRISMA review) | (doğrulanmalı) | 🟡 |
| 2026 | Garcia-Perez et al. | Deriving crop calendars from satellite phenology | (doğrulanmalı) | 🟡 |
| 2026 | Fuentes et al. | Field-aware explainable yield modelling | (doğrulanmalı) | 🟡 |
| 2025 | Sedano et al. | Harvest Date Monitoring in Cereal Fields at Large Scale (Sentinel-2, RTK doğrulamalı) | *Agriculture* 15(18):1984 · DOI 10.3390/agriculture15181984 | ✅ (2026-06-26) |
| 2025 | Liu et al. | NHPI for corn and soybean harvesting date detection (GEE) | *Remote Sens. Environ.* · ScienceDirect PII S0034425725004201 | ✅ (2026-06-26) |
| 2025 | Mimić et al. | ML-Based Harvest Date Detection Using SAR | (doğrulanmalı) | 🟡 |
| 2025 | Cyran et al. | Retrieving crop phenology in the Nile Delta | (doğrulanmalı) | 🟡 |
| 2025 | Parreiras et al. | Dense Time Series of HLS and Ensemble ML | (doğrulanmalı) | 🟡 |
| 2025 | Radočaj et al. | Phenology-Based Maize/Soybean Yield Potential | (doğrulanmalı) | 🟡 |
| 2025 | Radočaj et al. | Optimal proxy for cropland suitability from S2 | (doğrulanmalı) | 🟡 |
| 2025 | Zhang et al. | Remote sensing for crop mapping (review) | (doğrulanmalı) | 🟡 |
| 2025 | Zhang et al. | Crop yield estimation on pixel and field scales (review) | (doğrulanmalı) | 🟡 |
| 2024 | Yue et al. | Winter Wheat Maturity Prediction via Sentinel-2 MSI Images | *Agriculture* 14(8):1368 · DOI 10.3390/agriculture14081368 | ✅ (2026-06-26) |
| 2024 | Qin et al. | Extraction of maize phenological stages | (doğrulanmalı) | 🟡 |
| 2024 | Nduku et al. | Synergetic Use of S1/S2 for wheat biophysical parameters | (doğrulanmalı) | 🟡 |
| 2024 | Jiang et al. | Field Rover ground-truth approach for harvesting dates | (doğrulanmalı) | 🟡 |
| 2024 | Rivas et al. | Country-scale crop-specific phenology from PROBA-V | (doğrulanmalı) | 🟡 |
| 2024 | Şimşek | Optik ve radar görüntüleri ile XGBoost ile ürün desen tespiti (Türkçe) | (doğrulanmalı) | 🟡 |
| 2024 | (yazar eksik) | Buğday ekim alanlarının Sentinel-2A ile belirlenmesi (Türkçe) | (doğrulanmalı) | 🟡 |
| 2023 | Liao et al. | Near real-time detection of within-field phenology | (doğrulanmalı) | 🟡 |
| 2023 | Wei et al. | Early Crop Mapping Based on Sentinel-2 and RF | (doğrulanmalı) | 🟡 |

**Klasik teorik referanslar** (giriş/yöntem bölümünde):
- Tucker 1979 — NDVI'nin orijinal tanımı.
- Huete 1988 — SAVI ve toprak etkisi.
- Huete et al. 2002 — EVI orijinali.
- Jönsson & Eklundh 2002, 2004 — TIMESAT, fenoloji metrikleri.
- Savitzky & Golay 1964 — düzgünleştirme filtresi.
- Lundberg & Lee 2017 — SHAP.
- Breiman 2001 — Random Forest.
- Chen & Guestrin 2016 — XGBoost.
- Hochreiter & Schmidhuber 1997 — LSTM.
- Lim et al. 2021 — Temporal Fusion Transformer.

> **Doğrulama prosedürü:** Tezi yazmaya başlamadan önce her satır şu şartla geçer: (a) DOI doğru, (b) yazar/yıl/başlık tutarlı, (c) makale gerçekten erişilebilir, (d) bizim atıfımıza uyan iddia içeriyor. Bu disiplin "deep_search.md"'den otomatik kopya/yapıştır riskini önler.

---

## 9. Doğrulama günlüğü

> Bu bölüm, "atıfları gerçekten kontrol ettim" kanıtıdır; jüri/hoca "şu kaynağa baktın mı?" diye sorduğunda doğrudan cevap verir. Her satır: tarih, atıf, nasıl doğrulandı, sonuç.

| Tarih | Atıf | Doğrulama yöntemi ve bulgu | Sonuç |
|---|---|---|---|
| 2026-06-26 | **Sedano et al. 2025** — Harvest Date Monitoring | DOI 10.3390/agriculture15181984 açıldı. İspanya/Castilla y León, kırmızı bant (~665 nm) yansımasıyla; **RMSE 9.5 gün, %90.5 ±10 gün, eğitim verisi gerektirmiyor.** "Etiketsiz kural tabanlı V1" dayanağımızla birebir örtüşüyor. | ✅ Doğru |
| 2026-06-26 | **Yue et al. 2024** — Winter Wheat Maturity Prediction | DOI 10.3390/agriculture14081368 açıldı. *Agriculture* 14(8):1368. NDVI+NDRE+NDII1/2 + eşik + box-plot ile buğday olgunluğu/hasat ilerlemesi. "Eşik tabanlı buğday olgunluğu" referansımız. | ✅ Doğru |
| 2026-06-26 | **Liu et al. 2025 (NHPI)** — corn/soybean hasat tarihi | ScienceDirect PII S0034425725004201 (*Remote Sens. Environ.*). Tarla düzeyi **MAE 4 gün, R² 0.85**, USDA crop progress'e karşı MAE 3 gün. Dosyadaki rakamlarla birebir. | ✅ Doğru |
| — | Diğer ~18 satır (Mimić, Liao, Qin, Nduku, Cyran, Şimşek 2024, "Buğday ekim alanları S2A" 2024 vb.) | DOI doğrulaması bekliyor; özellikle Türkçe yayınlar TR Dizin/DergiPark/YÖK Tez'de tek tek aranacak. | 🟡 Bekliyor |

**Ek teknik doğrulamalar (2026-06-26, resmi kaynaklarla):**
- **Sentinel-1 revisit:** S1B Aralık 2021'de arızalandı (görev Ağustos 2022'de sonlandı, ESA) → 2022–2024 arası tek uyduyla 12 gün; S1C (Aralık 2024) + S1D (Kasım 2025) ile tekrar ~6 gün. → İlgili tüm dosyalarda düzeltildi.
- **Sentinel-2:** çift uyduyla (S2A+S2B, ayrıca S2C) 5 gün; 13 bant, 10/20/60 m (ESA). ✅ Doğru.
- **Konya/Çumra buğday hasadı:** Haziran sonu – Temmuz; sulu alanda Ağustos başına sarkabilir (Konya Ovası hububat hasadı haberleri). Önceki "15 Haziran" başlangıcı erken bulunduğu için düzeltildi; İl Tarım Müdürlüğü ürün takvimiyle resmî bağ hâlâ gerekli.
- **TARBİL:** Tarım Bakanlığı + İTÜ + TÜİK ortaklı kamu tarımsal izleme sistemi (`tarbil.gov.tr`). ✅ Doğru.

> **Sonraki tur:** Yukarıdaki 🟡 satırlar için aynı disiplinle (DOI aç → yazar/yıl/başlık/iddia kontrol) bu tabloya satır eklenir.

---

İlgili: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) (gerekçe) / [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md) (yöntemler) / [`13_UYDU_UYGUNLUK_MATRISI.md`](./13_UYDU_UYGUNLUK_MATRISI.md) (uydu kaynakları) / [`14_REKABET_VE_MEVCUT_SISTEMLER.md`](./14_REKABET_VE_MEVCUT_SISTEMLER.md) (operasyonel ürünler).

---

## Bu dosyada alınan kararlar
- Her literatür satırı kullanılmadan önce DOI ile bire bir doğrulanır.
- Türkçe yayınlar ayrıca taranır (TR Dizin, DergiPark, YÖK Tez); ulusal akademiye atıf disiplini korunur.
- Bizim farklılaşma argümanımız: Türkiye + tek dikey + açık veri + parsel-PWA. Bu argüman tezde tek paragrafta sabit kalır.
- Klasik referanslar (Tucker NDVI, SHAP, RF, XGBoost) yöntem bölümünün giriş paragrafında bir kez geçer.

## Açık sorular
- Türkçe doğrudan "hasat tarihi tahmini" yayını başka var mı? — TR Dizin + YÖK Tez taraması derinleştirilmeli.
- Akdeniz bağlamlı PRISMA tarama bizim Konya pilotu için uyarlanabilir mi? — Demissie 2026'yı yakından oku.

## Sonraki aksiyonlar
- Hafta 1-2: tablonun ilk 5 satırını tam DOI doğrulamasından geçir.
- Hafta 3-4: Türkçe literatürü ekle (en az 5 yeni satır).
- Faz 3 sonu: tezde literatür bölümünün ilk taslağı bu dosyadan üretilir.