# 16 — 5N1K Ana Raporu (Hoca / Yönetici / Jüri için Tek Belge)

> **Amaç:** Tüm omurganın okunabilir, savunulabilir ve hocaya/jüriye/şirket yöneticisine teslim edilebilir tek belge halinde özetlenmesi. Bu dosya stajın "tek pdf çıktısı" rolündedir.
> **Kapsam:** Yönetici özeti, 5N1K, problem, literatür özeti, pilot seçimi, veri kaynakları, uydu uygunluk analizi, yöntem, MVP planı, çıktılar, sorunlar/çözümler, maliyet, riskler, yol haritası, sonuç, ekler.
> **Son güncelleme:** 2026-06-26
> **Üslup:** Akademik ama okunabilir; pazarlama dili yok; bilimsel belirsizlikler dürüstçe işaretli; kanıt-tabanlı.

---

# Uydu Görüntüleri ve Görüntü İşleme ile Tarımsal Hasat Zamanı Tahmini

## *MVP'den Ölçeklenebilir Karar Destek Sistemine*

---

## 1. Yönetici Özeti

**Proje nedir?** Uydu zaman serisinden (Sentinel-2 + Sentinel-1) bir tarlanın fenolojik olgunluğunu okuyup parsel bazında **"hasada kaç gün kaldı?"** sorusuna ±gün cinsinden cevap üreten ve bunu mobil-uyumlu prototip arayüze (PWA) taşıyan karar destek sistemi.

**Neden önemlidir?** Türkiye'de hasat planlaması büyük ölçüde yerel deneyim ve iklim hissi ile yapılır; bu durum işçi/biçerdöver/lojistik darboğazı, kalite kaybı ve alıcı–satıcı arası bilgi asimetrisi yaratır. Açık veri tabanlı, ürün-dikey, Türkiye'ye özel bir sistemin alanı boştur.

**Nasıl başlanacak?** Tek ürün + tek bölge ile dar bir MVP: **kışlık buğday + Konya Ovası (Çumra)**. Çekirdek veri Sentinel-2 (optik fenoloji) + Sentinel-1 (bulut sigortası). İlk sürüm **kural tabanlı** (etiketsiz çalışabilir), sonraki sürüm **ML kalan-gün regresyonu** (RF → XGBoost → DL).

**İlk pilot nedir?** Çumra ilçesinde 30–100 buğday parselinde çalışan, son 5 sezonun zaman serisini tarayan, parsel başına "tahmini hasat tarihi", "kalan gün" ve "güven skoru" üreten Streamlit/PWA demo.

**Beklenen çıktı nedir?**
- Çalışan prototip (Web demo + PWA)
- Tekrar üretilebilir kod tabanı (GitHub repo)
- Akademik staj raporu + bitirme tezi taslağı
- Ulusal sempozyum / açık erişim dergi yayını taslağı
- En az 1 pilot kullanıcı (kooperatif) görüşmesi

**Büyük vizyon nedir?** Türkiye ölçeğinde, çok ürünlü (buğday → ayçiçeği → mısır), kooperatif/B2B odaklı, açık veri omurgalı, açıklanabilir ve KVKK uyumlu bir hasat zamanlama karar destek platformu.

---

## 2. 5N1K

### Ne?
Parsel bazında **hasada kalan gün** ve **hasat penceresi** tahmini; yardımcı çıktı olarak fenolojik evre etiketi ve güven skoru.

### Neden?
Lojistik (işçi + biçerdöver + kantar + nakliye), kalite kaybı önleme, alım planlama, çiftçi karar desteği, kurumsal tarımsal görünürlük (kooperatif, alım firması, sigorta, banka, bakanlık).

### Kim için?
- **Birincil:** çiftçi, ziraat mühendisi, kooperatif.
- **İkincil:** alım firması (un/yem/yağ), sigorta (TARSİM), banka (Ziraat Bankası), bakanlık (T.C. Tarım ve Orman Bakanlığı).

### Nerede?
- **MVP:** Konya Ovası — Çumra ilçesi — kışlık buğday.
- **Genişleme:** Trakya/Tekirdağ ayçiçeği (V2), Çukurova/GAP sulu mısır (V3), Şanlıurfa pamuk (değerlendirilebilir).

### Ne zaman?
Tek görüntü ile değil, **sezon boyunca zaman serisi** ile. Kritik dönem: **vejetatif gelişim → tepe dönem → senesens → olgunluk → hasat öncesi**. Sentinel-2 5 günde bir, Sentinel-1 ~6 günde bir gözlem (S1B arızası nedeniyle 2022–2024 arası 12 gün; S1C/S1D ile tekrar 6 güne döndü).

### Nasıl?
Sentinel-2 + Sentinel-1 + meteoroloji + parsel sınırı + fenoloji metrikleri (SOS/POS/EOS) + **kural tabanlı** mantık (V1) → **ML kalan-gün regresyonu** (V2-V3) → PWA arayüzü (V1) → React Native mobil (V2-V3).

---

## 3. Problem Tanımı

### 3.1. Hasat zamanı neden kritiktir?
Buğdayda hasat **sarı olum**dan sonra kısa bir pencerede yapılmalıdır:
- **Erken hasat** → düşük randıman, yüksek nem, dane kalitesi düşer.
- **Geç hasat** → dane dökülmesi, hava risk faktörü (yağmur, dolu).

### 3.2. Yanlış hasat zamanı neye mal olur?
- Verim kaybı (literatürde tahminler değişken; bölge ve sezona bağlı).
- Kalite primi kaybı (alım fiyatı düşer).
- Lojistik sırada kaymalar (biçerdöver, depo, kantar).
- Sigorta hasar değerlendirmesinde belirsizlik.

### 3.3. Türkiye'de neden bu sorun önemli?
- Buğday Türkiye'nin **stratejik** ürünüdür; Konya Ovası ülke üretiminin önemli kısmını taşır.
- Üretici-alıcı arasındaki bilgi asimetrisi sözleşmeli üretim ve depolama planlamasında darboğaz yaratır.
- Dijital tarım vizyonu (T.C. Tarım ve Orman Bakanlığı) uydu temelli karar destek sistemlerini destekliyor.

### 3.4. Mevcut pratikler neden sınırlı?
- Karar büyük ölçüde **deneyim + iklim hissi** ile veriliyor.
- Mevcut uydu izleme platformları **genel sağlık** (NDVI) gösteriyor; **kalan-gün cinsinden hasat tahmini** dikeyinde Türkiye'ye özel sistem yok (`14_REKABET_VE_MEVCUT_SISTEMLER.md`).

---

## 4. Literatür Özeti

(Detay: [`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md))

### 4.1. Akademik çalışmaların özeti
- **Sedano 2025** — Sentinel-2 ile eğitim verisi gerektirmeyen kural tabanlı tahıl hasadı tespiti.
- **Liu 2025 (NHPI)** — Mısır/soya için tarla düzeyinde MAE 4 gün, R² 0.85.
- **Mimić 2025** — SAR ile bulut bağımsız hasat tarihi tespiti.
- **Liao 2023** — Sentinel-2 ile saha içi fenoloji tespiti.
- **Yue 2024** — Sentinel-2 ile kışlık buğday olgunluk tahmini (bizim pilot için en yakın referans).
- **Şimşek 2024 (Türkiye)** — Optik+radar+XGBoost ile ürün desen tespiti.

### 4.2. Benzer sistemler (operasyonel)
GEOGLAM, Sen2-Agri, EOSDA Crop Monitoring, OneSoil, Climate FieldView, Cropwise. Çoğu **genel tarım izleme**; doğrudan kalan-gün dikeyi yok.

### 4.3. Bizim projenin farkı
1. Türkiye yerelleştirmesi
2. Ürün dikeyliği (kışlık buğday)
3. Kalan-gün cinsinden çıktı
4. Açık veriyle düşük maliyetli MVP
5. Açıklanabilirlik (SHAP + güven skoru)
6. Parsel + PWA arayüzü

---

## 5. Pilot Seçimi

(Detay: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) Bölüm A)

### 5.1. Neden Konya?
- Büyük ve homojen parseller (Sentinel-2'nin 10-20 m piksel boyutuyla uyumlu).
- Yarı kurak iklim → düşük bulutluluk → optik gözlem süreklidir.
- Bakanlık + İl Müdürlüğü + Çumra Ziraat Odası iletişim ağı erişilebilir.
- Konya Ovası, Türkiye'nin buğday üretiminin önemli bölgesi.

### 5.2. Neden kışlık buğday?
- Yıllık tek baskın ürün (ürün karışıklığı az).
- Tarihsel hasat penceresi: Haziran sonu – Temmuz, sulu alanda (Çumra) Ağustos başına sarkabilir (*İl Tarım Müdürlüğü ürün takvimiyle doğrulanmalı*).
- Literatür ve metodolojik altyapı güçlü (Yue 2024).

### 5.3. Neden tek ürün/tek bölge?
Hasat zamanı tahmini **fizyolojik olarak ürün-spesifiktir**: bir mısır tarlasının senesens dinamiği bir buğday tarlasınınkinden farklı evrelerden geçer. Tek model her yere uymaz; **derin tek dikey** > yüzeysel çok dikey.

### 5.4. Alternatiflerin neden sonraya bırakıldığı
- **Ayçiçeği + Trakya:** karışık rotasyon, daha bulutlu — V2.
- **Mısır + Çukurova/GAP:** sulu/kuru farkı, daha çok etiket gereksinimi — V3.
- **Pamuk + Şanlıurfa, Üzüm + Manisa, Çay/Fındık + Karadeniz:** parsel/iklim/etiket koşulları zor — kapsam dışı.

---

## 6. Veri Kaynakları

(Detay: [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md))

| Katman | Birincil | Yedek | Erişim |
|---|---|---|---|
| Parsel sınırı | ÇKS / kullanıcı shapefile | Otomatik delineation (U-Net) | Yazılı izin |
| Ürün tipi | Üretici beyanı / ÇKS | Sezon başı RF/XGB | Yazılı izin |
| Hasat tarihi | Üretici / kooperatif / biçerdöver | Mobil saha formu, foto-EXIF | İzin + KVKK |
| Sentinel-2 | Copernicus / GEE / AWS Open Data | MS Planetary | Açık |
| Sentinel-1 | Copernicus / GEE | ASF | Açık |
| Landsat / HLS | NASA / GEE | USGS | Açık |
| Meteoroloji | MGM / MEVBİS | ERA5-Land | Kayıt |
| Türkiye uyduları | RASAT, GÖKTÜRK-2, İMECE | — | V2/V3 doğrulama |

---

## 7. Uydu Uygunluk Analizi

(Detay: [`13_UYDU_UYGUNLUK_MATRISI.md`](./13_UYDU_UYGUNLUK_MATRISI.md))

### 7.1. MVP ana omurga
- **Sentinel-2** (10/20/60 m, 5 gün, açık) — birincil
- **Sentinel-1** (C-band SAR, ~6 gün — S1B arızasıyla 2022–24 arası 12 gün, S1C/S1D ile tekrar 6; bulut bağımsız) — bulut sigortası + hasat olayı
- **Meteoroloji** (MGM)

### 7.2. Yardımcı / V2-V3
- **Landsat 8/9 + HLS** — tarihsel süreklilik, yoğun zaman serisi.
- **PlanetScope** — ticari, küçük parsel doğrulama / premium katman.
- **GÖKTÜRK-2 / İMECE** — yerli yüksek çözünürlük doğrulama.

### 7.3. Türkiye uyduları konumlanması (dürüst)
- **RASAT** NIR/red-edge/SWIR yokluğu nedeniyle fenoloji çekirdeğine uygun değildir; tarihsel/yerli görünürlük.
- **GÖKTÜRK-2** yüksek uzamsal çözünürlük; sürekli akış sınırlı → doğrulama.
- **GÖKTÜRK-1** açık erişim akışı sınırlı; izin sürtünmesi var.
- **İMECE** teknik açıdan en umut veren; araştırmacı dostu açık ekosistem henüz oturmadı.
- **TÜRKSAT 6A** haberleşme uydusudur; tarımsal görüntüleme için **uygun değildir**.

### 7.4. Uzun vadeli veri stratejisi
V1 ana omurga açık veriyle (Sentinel + Landsat/HLS + meteoroloji); V2/V3'te yerli uydular doğrulama; V5'te ticari premium uydular yalnız ödeme gücü olan müşteri katmanlarında.

---

## 8. Yöntem

(Detay: [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md))

### 8.1. Ön işleme
- Sentinel-2 L2A SR varsayılan kullanılır.
- Bulut maskesi: s2cloudless veya QA60 + SCL.

### 8.2. İndeks hesaplama
NDVI, EVI/EVI2, NDMI, NDRE, SAVI, MSAVI, GCI; radar tarafında VH/VV ve oranı.

### 8.3. Zaman serisi
Parsel istatistiği (mean/median per band) → smoothing (Savitzky-Golay) → düzenli ızgaraya yeniden örnekleme (5 günde bir).

### 8.4. Fenoloji metrikleri
SOS, POS, EOS, LOS, max NDVI, plateau süresi, senescence slope, GDD-cumulative, bulut boşluk oranı, VH minimum tarihi.

### 8.5. Kural tabanlı tahmin (V1)
NDVI tepe sonrası düşüş + NDMI kuruma sinyali + bölgesel takvim önseli birleşir; hasada hazır oluşu yaklaşık eşiklerle saptar.

### 8.6. ML tahmin (V2-V3)
Random Forest baseline → XGBoost ile kalan-gün regresyonu → opsiyonel LSTM/TFT (V4 derinleştirme).

### 8.7. Güven skoru
`quality_score` (parsel-sezon başına 0–1) + model belirsizliği + bulut boşluk oranı birleşerek kullanıcıya tek skor olarak sunulur.

### 8.8. Açıklanabilirlik
SHAP / feature importance; her tahmin için "neden bu tarih?" panelinde NDVI/NDMI/VH eğrisi referans verir.

---

## 9. MVP Prototip Planı

(Detay: [`06_URUN_VE_TICARILESTIRME.md`](./06_URUN_VE_TICARILESTIRME.md) Bölüm 2-3)

### 9.1. İlk demo ne yapacak?
Kullanıcı PWA'da haritada parsel seçer; sistem o parsel için son 90 günlük indeks eğrisini, mevcut fenolojik evreyi, tahmini hasat tarihini (±N gün), kalan günü ve güven skorunu gösterir.

### 9.2. Kullanıcı ne görecek?
- Harita (Leaflet) + parsel renk kodu (yeşil / sarı / kırmızı)
- Seçili parsel paneli: tahmin tarihi, ±gün, kalan gün, fenoloji etiketi, güven skoru
- Eğri görünümü (NDVI/NDMI/VH son 90 gün)
- Etiket girişi (üretici onaylı hasat tarihi)

### 9.3. Teknik olarak ne çalışacak?
- Backend: FastAPI + PostgreSQL/PostGIS (geliştirmede SQLite/Spatialite)
- Veri: GEE üzerinden S2/S1 zaman serisi
- Model: kural tabanlı çekirdek (Faz 2) → RF baseline (Faz 3)
- Frontend: V1 Streamlit (hız), V2 React + Vite + Leaflet + Tailwind PWA

### 9.4. Hangi şeyler V1 dışında kalacak?
- Verim tahmini (V2)
- Otomatik tarla sınırı çıkarımı (V3)
- Çoklu ürün desteği (V2/V3)
- Sigorta / hasar tespiti (gelecek dikey)
- Operasyonel ticari SLA (Faz 5)
- Native mobil (Faz 5)

---

## 10. Çıktılar

| Çıktı | Format | Faz |
|---|---|---|
| Staj raporu | .docx + .pdf | 4 |
| Bitirme tezi taslağı | .docx + .pdf | 5 |
| Çalışan repo (GitHub) | Apache-2.0 | 5 |
| Web demo (Streamlit) | URL + ekran kaydı | 2 |
| PWA | URL | 4 |
| Mobil RN V0 | TestFlight / Internal Track | 5 |
| Sunum slaytları | .pptx | 5 |
| Akademik poster | A0 .pdf | 5 |
| Yayın taslağı | .docx | 5 |
| Veri sözleşme şablonları | .docx | 3 |
| Final video (60 sn) | .mp4 | 5 |

(Detay: [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md))

---

## 11. Sorunlar ve Çözümler

| Sorun | Etkisi | Çözüm | MVP'ye etki | Uzun vadeye etki |
|---|---|---|---|---|
| **Etiket yokluğu** | Kalan-gün modeli kalibre edilemez | Faz 1: kural tabanlı; Faz 3+: çoklu kanal etiket toplama (üretici/kooperatif/biçer/foto) | Modelin yerine demo gösterilir | Ticari doğruluk iddiası geri çekilir |
| **Bulutluluk** | S2 boşluğu, fenoloji eksilir | S1 ağırlığı + HLS füzyonu | Kapsama < %70 | Müşteri "boşluk" şikayeti |
| **Küçük parseller** | Karışık piksel, sinyal bozulur | V1'de Konya'da büyük parsel; V2'de PlanetScope ek | Pilot dışı bölge zayıf | Ölçek genişlemesi yavaşlar |
| **Ürün farklılığı** | Tek model her yere uymuyor | Tek dikey, sonra ayrı modeller | V1 yalnız buğday | Çoklu dikey gelişimi planlanır |
| **Model genellemesi (domain shift)** | Konya'da iyi, Trakya'da çöker | Tahmin "guard rail" mesajı; ikinci pilotla yeniden kalibrasyon | Demo bölgeyle sınırlı | Genişleme uzun sürer |
| **Veri maliyeti** | Ticari uydu pahalı | Açık veri omurgası; ticari yalnız premium | Etkisiz | Ticari katmanın opsiyonelliği |
| **GEE bağımlılığı** | Vendor lock-in, ticari maliyet | Faz 4'te yerel pipeline prototipi (rasterio/xarray/dask/STAC/COG) | Etkisiz | Ticari geçişte risk azalır |
| **KVKK** | Kişisel veri ve sözleşme yükü | Faz 3'te yazılı politika; opt-in; 30 gün silme | KVKK metni Faz 3 | Yıllık denetim hazırlığı |
| **Ticarileşme zorluğu** | Tek başına fonlama yetersiz | Kooperatif odaklı satış + akademik referans + kademeli geçiş | V1 etkisiz | Yıllık 1 pilot kullanıcı zorunlu |

---

## 12. Maliyet

(Detay: [`15_MALIYET_VE_IS_PLANI.md`](./15_MALIYET_VE_IS_PLANI.md). Tüm rakamlar **aralık** ve **varsayım**.)

| Faz | Altyapı (USD/ay) | İnsan kaynağı |
|---|---|---|
| MVP (3 ay) | $1–30 | 4.5–6.5 kişi-ay |
| POC (6 ay) | $50–200 | 8–12 kişi-ay |
| Ürünleşme (12 ay) | $150–600 | 12–24 kişi-ay |
| Ticari ölçek (yıllık) | $25k–200k+/yıl | ekip büyür |

**Maliyet azaltma stratejileri:** açık veri, önbellekleme, tek dikey, kooperatif aracılığıyla toplu etiket, PWA önce native sonra, GEE → yerel pipeline kademeli.

---

## 13. Riskler

(Detay: [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md))

| Tip | En kritik 3 risk | Mitigasyon özeti |
|---|---|---|
| **Teknik** | R-04 overfit, R-13 S2 A/B harmonizasyon | GroupKFold + sabit kalibrasyon |
| **Akademik** | R-15 yön değişikliği, R-08 tek kişi | ADR disiplin + süre ölçeklemesi |
| **Veri** | R-01 izin, R-03 etiket kalitesi | Faz 0 paralel başlat + çapraz doğrulama |
| **Saha** | R-11 saha ziyareti yapılamaz | Yerel ortakla mobil saha formu |
| **Ticari** | R-17 kullanıcı geri bildirimi yok, R-10 mağaza | İlk 3 görüşme zorunlu, PWA önce |
| **Hukuki** | R-09 KVKK | Faz 3 yazılı politika, opt-in, silme |
| **Operasyonel** | R-05 GEE quota, R-06 demo down | Yerel pipeline, offline yedek |

**Bu proje neden başarısız olabilir?** 5 senaryo: (1) demo var ama doğruluk yok, (2) tek bölge başardı genişletilemiyor, (3) teknik var kullanıcı yok, (4) akademik tamam ticari sıfır, (5) GEE çekildi hiçbir şey çalışmıyor. (Detay: `07_RISKLER_VE_KALITE.md` Bölüm 10.)

---

## 14. Yol Haritası

(Detay: [`03_FAZLAR_VE_DURUMLAR.md`](./03_FAZLAR_VE_DURUMLAR.md))

| Süre | Hedef |
|---|---|
| **İlk 2 hafta** | Faz 0 keşif: pilot kararı, veri talebi, repo iskeleti, GEE hesabı |
| **İlk 1 ay** | Faz 1 veri hattı: tek parsel S2/S1 zaman serisi, smoothing, ETL |
| **İlk 3 ay** | Faz 2 MVP-V1: kural tabanlı + Streamlit demo + 10 parsel |
| **İlk 6 ay** | Faz 3 MVP-V2: FastAPI + PWA + RF/XGBoost kalan-gün |
| **İlk 12 ay** | Faz 4-5: radar füzyonu + 2. pilot + saha doğrulama + mobil V0 + tez |
| **3 yıllık vizyon** | Çok ürün dikeyi, kooperatif/B2B sözleşmeleri, kurumsal lisans, açıklanabilir karar destek platformu |

---

## 15. Sonuç

### 15.1. Bu proje yapılabilir mi?
**Evet** — açık veri ekosistemi, modern Python yığını ve var olan literatür altyapısı bu projeyi akademik ve teknik olarak mümkün kılar.

### 15.2. Hangi şartlarla yapılabilir?
- Pilot bölgede (Çumra/Konya) **veri ve etiket erişiminin** Faz 0 sonunda yazılı taahhüde bağlanması.
- Geliştiricinin **dar ürün/dar bölge** disiplinini sürdürmesi (kapsam kayması olmaması).
- Açık veri omurgasının ana kaynak olarak korunması (yerli uyduların V1'e zorlanmaması).
- Etiketsiz başlangıçta **kural tabanlı** çekirdeğin kabul edilmesi.

### 15.3. MVP için başarı tanımı nedir?
- 30+ parselde çalışan, hocaya canlı demo edilebilir prototip.
- ±14 gün isabet ≥ %60 (V1), stretch ±7 gün isabet ≥ %60 (V2).
- Tekrar üretilebilir kod tabanı.
- Hocadan resmi onay.

### 15.4. Büyük vizyon için gerekenler nelerdir?
- En az 1 gerçek kooperatif pilotu (Faz 5).
- Yerel Python pipeline'a kademeli geçiş (vendor lock-in azaltma).
- KVKK uyumlu sözleşme şablonları.
- Çoklu sezon kararlılığını gösteren çok yıllık veri.
- Açık kaynak + ücretli destek hibrit iş modeli.

---

## 16. Ekler

### A. Kavram sözlüğü
[`11_GLOSSARY.md`](./11_GLOSSARY.md)

### B. Veri tablosu
[`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md) Bölüm 2.

### C. Uydu matrisi
[`13_UYDU_UYGUNLUK_MATRISI.md`](./13_UYDU_UYGUNLUK_MATRISI.md)

### D. Literatür tablosu
[`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md) Bölüm 3.

### E. Görev planı
[`09_GOREVLER.md`](./09_GOREVLER.md)

### F. Karar kayıtları (ADR)
[`10_KARAR_KAYDI.md`](./10_KARAR_KAYDI.md)

### G. Hocaya sunum stratejisi
[`17_HOCAYA_SUNUM_STRATEJISI.md`](./17_HOCAYA_SUNUM_STRATEJISI.md)

---

İlgili: bu rapor **omurganın özetidir**; her bölümün arkasındaki ayrıntı kendi özel dosyasındadır.

---

## Bu dosyada alınan kararlar
- Bu rapor "tek pdf çıktı" rolündedir; staj sunumu öncesinde tek başına okunabilir olacak şekilde tutulur.
- Belirsizlikler (özellikle hasat takvimi ve maliyet rakamları) "doğrulanmalı" işaretiyle gösterilir.
- Pazarlama dili kullanılmaz; pozitif iddia varsa bir kanıt referansıyla gelir.
- Her bölüm en fazla 1 sayfaya sığacak şekilde sade tutulur; ayrıntı için diğer dosyalara bağlantı verilir.

## Açık sorular
- Hocanın tercih ettiği rapor formatı .docx mi .pdf mi? — İlk toplantıda netleşir.
- Bu raporun bitirme tezi yapısına dönüştürülmesi için kaç haftalık ek emek gerekli? — Faz 5'te plan.
- "Yönetici özeti" hangi tek paragraflık biçimde sunum açılışı olarak da kullanılabilir? — `17_HOCAYA_SUNUM_STRATEJISI.md`'ye taşı.

## Sonraki aksiyonlar
- Faz 0 sonu: Bu rapor v0.1 olarak hocaya iletilir.
- Faz 2 sonu: Demo eklenmiş v0.5.
- Faz 4 sonu: MAE sonuçları eklenmiş v0.9.
- Faz 5: Final sürüm v1.0; bitirme tezi yapısına dönüştürülür.