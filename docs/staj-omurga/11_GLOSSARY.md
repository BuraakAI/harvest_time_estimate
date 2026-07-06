# 11 — Sözlük (Glossary)

> **Amaç:** Hoca, danışman, ekip ve kullanıcıyla aynı dili konuşmak; yeni gelene 10 dakikada projenin temel terimlerini öğretebilmek; rapor/tez/yayında tutarlı kelime kullanımını garanti etmek.
> **Kapsam:** Uydu/uzaktan algılama (Sentinel, Landsat, HLS, MODIS), spektral indeksler (NDVI, EVI, NDMI, NDRE, SAVI, GCI, VH/VV), fenoloji metrikleri (SOS/POS/EOS/LOS), modelleme (RF, XGBoost, LSTM, TFT, SHAP), mimari (FastAPI, PostGIS, PWA, JWT, Streamlit, Leaflet), Türkiye bağlamı (ÇKS, MGM, MEVBİS, KVKK), proje yönetimi (ADR, Kanban, MVP).
> **Son güncelleme:** 2026-05-10
>
> Yeni terim girdikçe alfabetik sıraya ekle.

---

## A

**ADR (Architecture Decision Record)** — Mimari/stratejik kararı tek sayfada belgeleyen ve gelecekte "neden böyle yapmıştık?" sorusuna cevap veren yazılı kayıt. Bizde `10_KARAR_KAYDI.md`.

**Ablation çalışması** — Bir özelliği veya bileşeni modelden çıkararak performansa etkisini ölçme yöntemi. "İndeks X olmasaydı MAE ne olurdu?" sorusunu yanıtlar.

**Atmosferik düzeltme** — Uydu görüntüsündeki atmosferik etkilerin (su buharı, aerosol) çıkarılarak yüzey yansımasının elde edilmesi. Sentinel-2 L2A ürünü zaten düzeltilmiş gelir.

## B

**Bant (band)** — Uydu sensörünün belirli bir dalga boyu aralığında ölçüm yapan kanalı. Sentinel-2'nin 13 bandı vardır (kıyı aerosol, mavi, yeşil, kırmızı, red-edge, NIR, SWIR vs.).

**Biyofizik parametre** — Bitkinin fiziksel/biyolojik özellikleri (LAI, FAPAR, klorofil) — uydu sinyalinden tahmin edilebilir.

## C / Ç

**Calibration (model kalibrasyonu)** — Modelin verdiği güven aralığı içine düşen gerçek değer oranının %CI ile uyuşması. %80 CI içine olayların %78-82'si düşerse model iyi kalibre demektir.

**COG (Cloud Optimized GeoTIFF)** — Bulut depolamadan parça parça okumaya uygun GeoTIFF varyantı. Yerel pipeline'da S2/HLS ham veri için ideal.

**Crop calendar (ürün takvimi)** — Bir ürünün ekim, çıkış, çiçeklenme, olgunlaşma, hasat tarihlerinin bölgeye özel takvimi.

**Crop type classification** — Bir parselin hangi ürünü taşıdığını uydu zaman serisinden çıkaran sınıflandırma görevi.

**ÇKS (Çiftçi Kayıt Sistemi)** — Türkiye'de çiftçilerin parsel ve üretimlerini Bakanlık'a kaydettiği sistem. Resmi parsel sınırı kaynağıdır.

## D

**Decision gate (karar kapısı)** — Faz sonunda "geçtim mi, geçmedim mi?" kontrolü. Bizde G0–G5.

**DL (Deep Learning)** — Çok katmanlı yapay sinir ağları. Bizde V4'te LSTM/Transformer.

**Domain shift (alan kayması)** — Eğitim verisinin geldiği koşullarla (Konya, 2023-25, kuru sezon) tahmin yapılan ortamın (örn. Trakya, yaş sezon) farklı olması. Modelin pilot dışına genelleme zayıflığının ana nedeni.

**DOY (Day of Year)** — Yılın 1 Ocak'tan itibaren kaçıncı günü. 1 Ocak = 1, 31 Aralık = 365 (artık yıl 366).

## E

**Earth Engine (GEE)** — Google'ın bulut tabanlı uydu/coğrafi analiz platformu. Server-side hesaplama. Akademik kullanım ücretsiz.

**EOS (End of Season)** — Senesensin / sezon sonunun fenoloji tarihi.

**ETL (Extract-Transform-Load)** — Veriyi çek, dönüştür, yükle. Bizde GEE → indeks → parquet → DB.

**EVI (Enhanced Vegetation Index)** — Yoğun kanopide doygunluğa NDVI'dan daha dirençli vejetasyon indeksi. Formül: G * (NIR - Red) / (NIR + C1 * Red - C2 * Blue + L).

## F

**FAPAR (Fraction of Absorbed Photosynthetically Active Radiation)** — Bitki örtüsünün absorbe ettiği fotosentetik ışın oranı (0–1). LAI ile birlikte verim modellerinin temel girdisidir.

**FastAPI** — Python için modern, async, OpenAPI'li web framework.

**Fenoloji** — Bitkinin yıllık yaşam döngüsü olaylarının (çıkış, çiçeklenme, olgunluk, hasat) zamanlama bilimi.

**Field boundary** — Tarla sınırı (poligon).

**Fusion (füzyon)** — Birden fazla sensörün (Sentinel-2 + Landsat, optik + radar) birleştirilmesi.

## G

**GDD (Growing Degree Days)** — Birikimli termal birim. Sigma max(0, T_avg - T_base). Buğdayda T_base genellikle 0°C.

**GeoJSON** — Coğrafi veri için JSON tabanlı format.

**GeoTIFF** — Coğrafi referanslı raster (TIFF) dosyası.

**GroupKFold** — Cross-validation: aynı grup (parsel) hem eğitim hem test'te olmasın.

## H

**Harvest window (hasat penceresi)** — Hasadın yapılabileceği makul tarih aralığı (örn. 12 Temmuz ± 5 gün). Ürünümüzün ana çıktı kavramı.

**HLS (Harmonized Landsat–Sentinel)** — NASA tarafından harmonize edilen Landsat 8/9 + Sentinel-2 ürünü, 30 m, ~1.6 günde bir.

## İ

**İndeks** — Bant kombinasyonundan üretilmiş tek değer (ör. NDVI = (NIR-Red)/(NIR+Red)).

**Imputation** — Eksik tarihlerin yerine değer yerleştirmek (interpolasyon, model tahmini).

## J

**JWT (JSON Web Token)** — Kullanıcı kimlik doğrulama tokeni; HTTP başlığında taşınır.

## K

**Kanban** — Görevlerin durumlar arasında akışını izleyen pano.

**Kapsama (coverage)** — Tahmin yapılabilen parsel oranı; bulutluluk düşürür.

**KVKK** — Kişisel Verilerin Korunması Kanunu. Türkiye'de veri sahipliği ve işleme kuralları.

## L

**LAI (Leaf Area Index)** — Birim toprak alanına düşen tek taraflı yaprak alanı (m²/m²). Vejetatif gelişimin temel biyofizik göstergesi; uydu yansımasından tahmin edilebilir.

**Label noise (etiket gürültüsü)** — Etiketlerin kendisinde bulunan hata payı (yanlış tarih, alan uyumsuzluğu, çapraz kaynak çelişkisi). Bizim sistemde `confidence` skoruyla yönetilir.

**Landsat 8/9** — NASA-USGS uydu serisi; 30 m MS, 16 günde bir tek uydu.

**LSTM (Long Short-Term Memory)** — Zaman serisi öğrenmede güçlü yapay sinir ağı türü.

**L2A** — "Level-2A" — Sentinel-2'de atmosferik düzeltme yapılmış, surface reflectance ürün.

## M

**MAE (Mean Absolute Error)** — Ortalama mutlak hata. Hasat tarihi tahmininde gün cinsinden kritik metrik.

**MGM** — Meteoroloji Genel Müdürlüğü.

**MEVBİS** — MGM'nin meteoroloji veri sunum sistemi.

**ML (Machine Learning)** — Makine öğrenmesi. Bizde RF, XGBoost, LSTM.

**MLflow** — Deney izleme/model paketleme aracı.

**MVP (Minimum Viable Product)** — Asgari kullanılabilir ürün.

## N

**NDMI (Normalized Difference Moisture Index)** — Kanopi nem indeksi. Olgunlaşma fazında düşer.

**NDRE (Normalized Difference Red Edge)** — Klorofil duyarlı red-edge indeksi.

**NDVI (Normalized Difference Vegetation Index)** — En yaygın vejetasyon indeksi. (NIR-Red)/(NIR+Red).

**NHPI** — Liu 2025'te tanıtılan mısır/soya hasat tarihi tespiti için özelleşmiş indeks.

**NIR (Near Infrared)** — Yakın kızılötesi bandı; vejetasyon güçlü yansıtır.

## O / Ö

**OpenAPI** — REST API'ler için spec formatı; FastAPI otomatik üretir.

**Orto-rektifikasyon** — Görüntünün topoğrafik bozulmaları düzeltilerek harita ile uyumlu hale getirilmesi.

**Overfit** — Modelin eğitim verisine aşırı uyum sağlaması, yenide çökmesi.

## P

**Parquet** — Sütun tabanlı ikili veri formatı; zaman serisi için ideal.

**PA (Plant Area)** — Bitki alanı; LAI ile ilişkili.

**Phenological stage (fenolojik evre)** — Bitkinin yaşam döngüsündeki ayrık aşamalar (vejetatif, başaklanma, çiçeklenme, süt olum, hamur olum, sarı olum, hasat). Buğdayda BBCH sınıflandırması yaygındır.

**Phenology metrics** — SOS, POS, EOS, LOS, max NDVI, plateau süresi gibi türetilmiş özellikler.

**POS (Peak of Season)** — Sezon tepe noktasının tarihi.

**PostGIS** — PostgreSQL için coğrafi (spatial) eklenti.

**PWA (Progressive Web App)** — Tarayıcıdan kurulabilen, offline çalışabilen web uygulaması.

## Q

(boş)

## R

**Radar (SAR)** — Synthetic Aperture Radar; aktif mikrodalga gözlem; buluttan etkilenmez.

**Random Forest (RF)** — Karar ağacı topluluğu; tablo verilerde güçlü baseline.

**Re-sampling** — Verinin farklı çözünürlüğe/zaman aralığına çevrilmesi.

**RMSE (Root Mean Square Error)** — Karekök ortalama kare hatası; büyük sapmalara MAE'den daha duyarlı.

## S / Ş

**SAR (Synthetic Aperture Radar)** — Aktif mikrodalga gözlem yöntemi; bulut bağımsız. Sentinel-1 C-band SAR'dır.

**Savitzky-Golay filtresi** — Hareketli pencere içinde polinom uydurarak yapılan smoothing yöntemi.

**STAC (SpatioTemporal Asset Catalog)** — Coğrafi/zamansal veri varlıklarının standart kataloglama API'si. Yerel pipeline'da Sentinel/Landsat sahnelerini sorgulamak için kullanılır.

**Sentinel-1** — ESA C-band SAR; VH/VV polarizasyon; ücretsiz.

**Sentinel-2** — ESA optik MSI; 13 bant; 10/20/60 m; ücretsiz.

**Senesens** — Bitkinin sararma/yaşlanma evresi; hasat habercisi.

**SHAP (SHapley Additive exPlanations)** — ML modellerinin tahminlerini özelliklere atfederek açıklayan yöntem.

**Shapefile (.shp)** — ESRI'nin coğrafi vektör veri formatı.

**SOS (Start of Season)** — Vejetatif başlangıç tarihi.

**Spatial query** — "X parselinin etrafındaki Y parseller" gibi geometrik sorgu.

**SR (Surface Reflectance)** — Yüzey yansıması; atmosferik düzeltme sonrası ürün.

**Streamlit** — Python ile hızlı web demo aracı.

**SWIR (Short-Wave Infrared)** — Kısa dalga kızılötesi; nem ve yapı bilgisi.

## T

**Time series (zaman serisi)** — Aynı yerin zaman içinde alınmış ölçüm dizisi.

**TFT (Temporal Fusion Transformer)** — Çok değişkenli zaman serisi için Transformer mimarisi.

## U / Ü

**U-Net** — Görüntü segmentasyonu mimarisi; tarla sınırı çıkarımında kullanılabilir.

## V

**VH / VV** — Sentinel-1 radar polarizasyonları (vertical-horizontal, vertical-vertical).

**Verim (yield)** — Birim alandan elde edilen ürün miktarı (ton/ha).

**Vejetatif evre** — Bitkinin yapraklı büyüme dönemi.

## W

**Window (smoothing window)** — Düzgünleştirme fonksiyonunun çalıştığı pencere boyu.

## X

**XGBoost** — Gradient boosting tabanlı, tablolar için çok güçlü ML kütüphanesi.

## Y

**Yer doğrulaması (ground truth)** — Sahada toplanan, modelin doğruluğunu ölçmek için kullanılan referans veri.

## Z

**Zaman serisi smoothing** — Gürültü azaltmak için yumuşatma; SG, LOWESS, Whittaker kullanılır.

---

İlgili: [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md) (terimlerin geçtiği yer).

---

## Bu dosyada alınan kararlar
- Sözlük yalnız-ekleme ilkesi: terim çıkarmak yerine açıklamayı revize ederiz (eski rapor/tez metniyle uyum).
- Türkçe terim öncelikli, parantezde İngilizce karşılığı; ortak kullanımda İngilizce kalan terimler aynen yazılır (NDVI, SHAP).
- Marka/sistem isimleri (Sentinel-2, FastAPI, Leaflet) öz isim olarak ayrı maddedir; ürün için "ne yapar" tanımı verilir.

## Açık sorular
- BBCH evre sınıflandırması Türkçe karşılıklarıyla genişletilmeli mi? (Buğday için ek tablo yararlı olabilir.)
- Yerli uydulara ait teknik terimler (PAN, MS, GSD) için ayrı "yerli uydu sözlüğü" alt bölümü açılmalı mı?

## Sonraki aksiyonlar
- Bitirme tezi yazımında kullanılan her yeni terimi buraya da yansıt.
- Kullanıcı arayüzünde geçen terimler (örn. "süt olum", "kalan gün") UI metinleriyle aynı kelimelerle tanımlansın (`design:ux-copy` disiplini).
