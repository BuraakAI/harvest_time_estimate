# 02 — Bilimsel Karar Gerekçelendirmesi (Pilot ve Tech Stack)

> **Amaç:** Projedeki en kritik iki kararın — (a) pilot ürün/bölge, (b) teknik altyapı — bilimsel ve operasyonel gerekçesini açıkça ortaya koymak.
> **Kapsam:** Tek ürün/tek bölge stratejisi, hasat zamanı vs verim tahmini ayrımı, kural→ML aşaması, Sentinel-2/Sentinel-1 rolleri, 6 alternatif pilotun karşılaştırılması, tech stack boyut-boyut analiz.
> **Son güncelleme:** 2026-05-10

> Hocaya/jüriye "neden buğday + Konya?", "neden Earth Engine?", "neden bu sıralama?" diye sorulduğunda bu dosya konuşur.

---

## A) Pilot ürün ve bölge seçimi

### A.0. Neden tek ürün + tek bölge ile başlanmalı?

Hasat zamanı tahmini **fizyolojik olarak ürün-spesifiktir**: bir mısır tarlasının senesens dinamiği bir buğday tarlasınınkinden farklı evrelerden geçer; aynı şekilde Konya kurak fenolojisi, Trakya yarı-nemli fenolojisinden saparak tek model genelliğini bozar. Bu nedenle:

1. **Bilimsel zorunluluk:** Aynı algoritma farklı ürün-bölge kombinasyonlarında farklı eşik kalibrasyonu gerektirir. Bunu MVP'de paralel yapmak modelin "her yerde orta kötü" olmasına yol açar.
2. **Etiket ekonomisi:** Etiket en pahalı veridir. Tek pilotta odaklanmak 30–100 etiketi yeterli kılar; çok pilot 300+ etiket ister.
3. **Akademik savunulabilirlik:** Bir ürün-bölgede iyi sonuç üretmek, beş üründe orta sonuç üretmekten daha güçlü tezdir. Tek pilot literatürde de yaygındır (Yue 2024 — kışlık buğday; Liu 2025 — mısır+soya; Cyran 2025 — Nil Deltası küçük parselleri — *kaynaklar deep_search.md'den, doğrulanmalı*).
4. **Operasyonel risk:** Az kaynak (bir staj, bir kişi) çoklu pilotu sürdüremez; kapsam kayması ile her şey yarım kalır (`07_RISKLER_VE_KALITE.md` R-07).

### A.1. Hangi kriterler bir pilotu "iyi" yapar?

Beş ana kriter aday pilotları elimine eder. Her kriter dolaylı olarak bir literatür çerçevesine bağlanır.

| Kriter | Neden önemli | Bu kriter yoksa ne olur? |
|---|---|---|
| **K1. Büyük ve homojen parseller** | Sentinel-2'nin 10–20 m piksel boyutu küçük parsellerde "karışık piksel" sorunu üretir. Büyük parselde parsel-ortalaması anlamlı sinyaldir. | Küçük parsellerde indeks gürültülü olur, MAE 10+ güne çıkar. |
| **K2. Tek baskın ürün** | Pilot bölgede ürün karışıklığı varsa modelin ilk yapması gereken iş "ürün tipi sınıflandırma" olur. | Crop-type classifier zorunluluğu, etiket ihtiyacı, pipeline karmaşıklığı. |
| **K3. Yönetilebilir bulutluluk** | Optik uydu buluttan etkilenir. Bulutlu bölgelerde fenolojinin kritik dönemleri kaçırılır. | Sentinel-1 radar zorunluluğu sezon başında yükselir, model karmaşıklaşır. |
| **K4. Yer doğrulama / etiket erişimi** | Hasat tarihi etiketleri olmadan model değerlendirilemez. | Yalnız kural tabanlı kalırsın, akademik savunma zayıflar. |
| **K5. İstikrarlı ürün takvimi + literatür referansı** | Aynı ürün/bölgede önceki yayınlar varsa benchmarking ve baseline mevcuttur. | Sıfırdan kalibrasyon, kıyas yok, jürinin "neden bu ürün?" sorusu sertleşir. |

### A.2. Aday pilotların karşılaştırma matrisi (genişletilmiş)

Aşağıdaki tablo deep_search.md'deki bölge analizi + bakanlık üretim raporları (2023–2025 aralığı, *doğrulanmalı*) + akademik literatür yoğunluğuna dayanır.

| Aday | Parsel boyutu | Bulut yoğunluğu | Ürün takvimi | Etiket erişimi | Literatür yoğunluğu | Ticari değer | MVP zorluğu | **Sonuç** |
|---|---|---|---|---|---|---|---|---|
| **Konya + kışlık buğday** | Çok büyük, homojen | Düşük-orta | Çok kararlı | Orta-yüksek (bakanlık + ziraat odası + kooperatif) | Yüksek (Yue 2024, Liao 2023, Şimşek 2024 — *doğrulanmalı*) | Yüksek (stratejik ürün, geniş üretici kitle) | Düşük | **🟢 Birincil pilot** |
| **Trakya/Tekirdağ + yağlık ayçiçeği** | Orta-büyük, karışık rotasyon | Orta-yüksek | Kararlı ama daha kısa pencere | Orta (Trakya Birlik) | Orta (mısır/buğdaya göre az) | Yüksek (yağ sanayi) | Orta | **🟡 İkinci pilot** |
| **Çukurova/GAP + dane mısır** | Orta-büyük, sulamaya bağlı değişken | Düşük | Sulu/kuru ayrımı zorlu | Orta-zor | Yüksek (NHPI Liu 2025, ABD literatürü — *doğrulanmalı*) | Yüksek (yem + nişasta sanayi) | Orta-yüksek | **🟠 Üçüncü pilot** |
| **Şanlıurfa/Harran + pamuk** | Büyük ama sulamaya bağlı | Düşük | Uzun sezon, tek hasat | Zor (etiket nadir) | Düşük-orta | Orta-yüksek (tekstil) | Yüksek | ❌ V3+ |
| **Manisa/Denizli + üzüm (sofralık/şaraplık)** | Çok küçük, karışık piksel | Düşük-orta | Karmaşık, çeşit-spesifik | Zor | Düşük (uzaktan algılama açısından) | Yüksek (ihracat) | Çok yüksek | ❌ Bu projede yok |
| **Karadeniz + fındık** | Çok küçük, dağlık | Çok yüksek | Tek hasat ama karmaşık olgunlaşma | Zor | Düşük | Yüksek (FOB ihracat) | Çok yüksek | ❌ Uydu sınırı belirgin |
| **Karadeniz + çay** | Küçük, dik bahçeler | Çok yüksek | Çok hasatlı (3–4 sürgün) | Zor | Çok düşük | Orta | Çok yüksek | ❌ Çok hasatlı + bulut |

**Skor mantığı:** Her aday üst tablodaki K1–K5 kriterlerine göre yeşil/sarı/kırmızı işaretlenir. Konya+buğday tek "tamamı yeşil/sarı" adayı.

### A.3. Konya + kışlık buğday — gerekçe zinciri (resmi)

```
K1 (büyük homojen parsel)        → Konya Ovası ile karşılanır.
K2 (tek baskın ürün)             → Kışlık buğday Konya'da yıllık üretimin baskın bileşeni.
K3 (bulutluluk yönetilebilir)    → Konya yarı kurak; optik gözlem sürekliliği yüksek.
K4 (etiket erişimi)              → İl müdürlüğü + ziraat odası + kooperatif kayıtları erişilebilir.
K5 (literatür)                   → Yue 2024 (kışlık buğday olgunluk), Liao 2023 (saha içi fenoloji),
                                    Şimşek 2024 (Türkiye XGBoost ürün desen) — kaynaklar doğrulanacak.
─────────────────────────────────────────────────────────────
SONUÇ: V1 pilot olarak en düşük riskli ve en yüksek savunulabilir seçim.
```

### A.4. Neden ilk aşamada ürün çeşitlemesi yapılmamalı?

- Çoklu ürün, **çoklu kalibrasyon** demektir; her biri ayrı eşik, ayrı etiket.
- Veri pipeline'ı ürün-spesifik özellikler (ekim tarihi, T_base, sezon uzunluğu) gerektirir; tek ürün üzerinde olgunlaştırılmadan ikinciye geçmek borç üretir.
- Akademik tezler tipik olarak **bir alanda derin** olduğunda güçlüdür; yatay genişleme literatür beklentilerini karşılamaz.
- Ürün çeşitlenmesi **V2 ile** başlar — bu sırada V1 mimarisi tek ürünün rafinasyonunu görür.

### A.5. Neden verim tahmini değil de hasat zamanı tahmini?

Verim tahmini ve hasat zamanı tahmini **yakın akraba ama farklı problemlerdir**. Bu projenin V1 hedefi *yalnız* hasat zamanıdır. Gerekçe:

| Boyut | Hasat zamanı tahmini (V1) | Verim tahmini (V2+) |
|---|---|---|
| Hedef değişken | Tarih veya kalan-gün | Ton/ha veya bağıl verim |
| Etiket ihtiyacı | Bir tek tarih (etiket başına) | Hasat sonrası kantar/biçer logu |
| Hata toleransı | ±gün — operasyonel pencere | %hata — fiyatlamada doğrudan etki |
| Akademik temel | Fenoloji + olgunluk indeksi | Biyofizik + iklim + toprak |
| Kullanıcı kararı | Lojistik (biçer/işçi/kamyon) | Finansal (alım, sigorta, banka) |
| Karmaşıklık | Düşük-orta | Yüksek |
| Pilot için ölçeklenebilirlik | Az etiketle çalışabilir | Etiket ve veri ihtiyacı yüksek |

Verim tahminini V1'e koymak iki problemi paralel çözmek demektir; etiket darboğazı ortak olduğu için **ikisini de yarıda bırakırız**. V1'de hasat zamanı için solid bir altyapı, V2'de aynı altyapı üzerine verim modülü kurulur.

### A.6. Neden önce kural tabanlı model, sonra ML?

Kural tabanlı yaklaşım literatürde "etiket gerektirmeyen, eşik tabanlı, açıklanabilir" olarak konumlanır (Sedano 2025; Yue 2024 — *doğrulanmalı*). Sıralama gerekçesi:

1. **Etiket boşluğunda da çalışır.** Faz 0–2'de elimizde etiket yokken bile sonuç üretebilir.
2. **Açıklanabilirdir.** Kural eşikleri bir zirai mühendise mantıklı gelir; jüriye karşı savunma kolaydır.
3. **ML için baseline'dır.** ML modeli kuralı geçemiyorsa modelden değil özelliklerden ya da etiketten şüpheleniriz.
4. **Veri kalitesi sınamasıdır.** Kural çıktıları manuel doğrulamada saçma çıkarsa veride sorun var demektir.
5. **Ardından ML kademeli ölçeklenir:** RF (baseline) → XGBoost / LightGBM → LSTM/Temporal Fusion Transformer.

### A.7. Neden Sentinel-2 ana, Sentinel-1 destek kaynak?

| Boyut | Sentinel-2 (optik) | Sentinel-1 (radar) |
|---|---|---|
| Fenoloji sinyali zenginliği | Çok yüksek (NDVI, EVI, NDMI, NDRE, SWIR…) | Düşük-orta (VH/VV, doku) |
| Yorumlanabilirlik | Yüksek (zirai mühendis bildiği indeksler) | Düşük (mikrodalga geri saçılım) |
| Bulut etkisi | Var | Yok |
| Tarımsal literatür yoğunluğu | Çok yüksek | Orta |
| Açık veri & API | Var (Copernicus / GEE / AWS Open Data) | Var |
| MVP üzerinde geliştirme hızı | Yüksek | Orta |

Sentinel-2 tek başına çoğu sezon Konya'da yeterli kapsama sağlar. Sentinel-1 **bulutlu dönem sigortası** ve **hasat olayı tespiti** (VH'da ani düşüş) için ikinci kademedir. Bu ayrım Faz 1'de yalnız S2, Faz 4'te S1 füzyonu olarak yapılandırılır (`03_FAZLAR_VE_DURUMLAR.md`).

### A.8. Karşı-iddialar ve cevapları

| Karşı-iddia | Cevap |
|---|---|
| "Mısır daha 'cool' bir ürün, NHPI gibi yeni indeksler var" | Doğru, ama mısır pilotu daha çok etiket ister; V3 pilotu için ideal. NHPI metodolojisine V1'de zaten referans veriyoruz. |
| "Konya çok geniş, küçük bir alan seçmek lazım" | Evet — pilot içinde **2–3 ilçe** seçilecek (örn. Çumra, Karatay, Cihanbeyli), tüm Konya değil. Karar `ADR-017`. |
| "Buğday hep çalışıldı, yenilik nerede?" | Yenilik **hasada kaç gün kaldı** çıktısının Türkiye'ye özel parsel-PWA ürününe paketlenmesi. Bilimsel yenilik orta, uygulamalı yenilik yüksek. |
| "Verim olmadan ticari değeri zayıf" | V1 ticari ürün değil, MVP. Ticarileşme V2+. Hasat zamanı tek başına kooperatif/lojistik için yeterli değer. |
| "Ya hava değişirse — kuraklık, dolu?" | Anomali tespiti V2 modülü. V1 normal sezon varsayımı, aykırı sezon güven skoruyla işaretli. |

### A.9. Eğer pilot elenirse

- **Saha izni alınamazsa** → Trakya/ayçiçeği yedek pilotu (2. öncelik).
- **İl müdürlüğü iletişimi gecikirse** → Açık veri (parsel sınırını kullanıcı çizer) + sentetik etiket (kural tabanlı + uzman görüşü).
- **Etiket toplama gerçekçi olmazsa** → Sedano 2025 stilinde **eğitim verisi gerektirmeyen** kural tabanlı yaklaşıma sıkı bağlanılır; başarı metriği ML değil kapsama+kalibrasyon ile değerlendirilir.

---

## B) Teknik altyapı (tech stack) seçimi

### B.1. deep_search.md ne diyor?

1. **Açık veri ekosistemini omurga yap** — Sentinel-2 + Sentinel-1 + Landsat/HLS. Yerli uydular ikinci faz doğrulama için.
2. **Akademik prototipte Earth Engine + hafif web** en hızlı seçenektir; ticari kullanımda ücretli plan gerekir.
3. **Modelleme sırası:** kural tabanlı → RF/XGBoost → LSTM/Transformer.

Belge **dilden, mobil framework'ten, veri tabanından** bahsetmiyor; bu detaylı seçimler bizim üzerimizde.

### B.2. Tech stack — boyut boyut analiz

#### B.2.1 Programlama dili

| Aday | Artı | Eksi | Karar |
|---|---|---|---|
| **Python** | EO/ML standart dili; rasterio, xarray, GDAL, geopandas, scikit-learn, PyTorch, GEE Python API. | İstemci-tarafı performansta zayıf; mobil geliştirmeye doğal değil. | ✅ Birincil |
| R | İstatistik için güçlü, terra/sf var | EO/ML ekosistemi Python kadar geniş değil | ❌ |
| TypeScript | Frontend zaten gerekiyor | EO server-side için yetersiz | ✅ Sadece frontend |
| Julia | Performans iyi | Topluluk küçük, GEE bağı yok | ❌ |

**Karar:** Backend ve veri Python, frontend TypeScript. (`ADR-002`)

#### B.2.2 Uydu veri kataloğu / hesaplama

İki ana yol: **Earth Engine (GEE)** veya **yerel Python pipeline (rasterio + xarray + dask + STAC + COG)**.

| Boyut | Google Earth Engine | Yerel Python | TÜBİTAK/yerli bulut |
|---|---|---|---|
| Maliyet (akademik) | 0 ₺ | 0 ₺ (disk/CPU senin) | Kredi gerekir |
| Veri indirme | Yok — server-side | Var, GB'larca disk | Var |
| Hız (1 sezon, 100 parsel) | dakikalar | saatler | saatler |
| Ölçeklenebilirlik | Çok yüksek | Disk sınırlı | Bütçe sınırlı |
| Reproducibility (paper) | Orta — GEE script'i dış bağımlı | Yüksek — Docker'a sığar | Düşük (kapalı) |
| Ticari kullanım | Ücretli | Tam serbest | Sözleşmeye bağlı |
| Vendor lock-in | **Yüksek (Google)** | Düşük | Yüksek (sağlayıcı) |
| Öğrenme eğrisi | Düşük (örnek bol) | Orta-yüksek | Yüksek |

**Hibrit karar (`ADR-008`):** Faz 0–2 GEE; Faz 3'ten itibaren kritik adımlar yerel pipeline'a paralel taşınır; Faz 5'te ticari sürüm tamamen yerel.

#### B.2.3 Backend / API

**Karar:** FastAPI. Otomatik OpenAPI, async, Pydantic v2 ile tip güvenli. (`ADR-003`)

#### B.2.4 Veri tabanı

**Karar:** Geliştirmede SQLite + Spatialite, prototipte Supabase (Postgres + PostGIS). (`ADR-004`)

#### B.2.5 Frontend (web)

**Karar:** Faz 2 hızlı demo için **Streamlit**, Faz 3+ ürün için **React + Vite + TypeScript + Tailwind + shadcn/ui**. (`ADR-005`)

#### B.2.6 Harita kütüphanesi

**Karar:** Leaflet + react-leaflet. (`ADR-006`)

#### B.2.7 Mobil

**Karar:** V1 → PWA, V2 → React Native. (`ADR-007`, `ADR-014`)

#### B.2.8 ML / DL

**Karar:** scikit-learn (RF), xgboost, lightgbm, scipy, statsmodels (klasik); PyTorch + Lightning (V4 DL). MLflow ile deney takibi.

#### B.2.9 DevOps

**Karar:** GitHub + Actions, Docker + docker-compose, Vercel (frontend), Render/Fly (backend prototip).

### B.3. Tech stack için anti-örüntüler (yapma)

- ❌ "Hadi her şeyi GEE'de bırakalım" — vendor lock-in derinleşir, ticari geçiş tıkanır.
- ❌ "Mobil önce, web sonra" — mağaza onayları staj süresini tüketir.
- ❌ "Tüm Türkiye için tek model" — V1'de pilot dışı performans gerçekçi değil.
- ❌ "Custom CSS framework" — Tailwind / shadcn kullanılır.
- ❌ "Ham veriyi kendi diskime indireyim" — STAC + COG ile akış üzerinden çek; gerek yoksa indirme.

### B.4. Jüri savunma soruları

- **"Neden Python?"** → EO ve ML için birinci dil; Türkiye akademik EO çalışmaları çoğunlukla Python (Şimşek 2024 — *doğrulanmalı*).
- **"Neden GEE?"** → Akademik kullanımda ücretsiz, server-side, planet-scale arşiv. Ticari geçiş `ADR-008`'de planlandı.
- **"Neden FastAPI?"** → OpenAPI, async, Pydantic. Mikro-servis ölçek için ideal.
- **"Neden React Native değil V1'de?"** → Mağaza onayı staj süresine sığmaz; PWA tarayıcıdan tek tık.
- **"Neden PostGIS?"** → Spatial sorgu (parsel kapsama, alan, mesafe) SQL'de yapılabilir.
- **"Vendor lock-in neyle yönetiliyor?"** → Hibrit karar (GEE + yerel pipeline paralel hazırlığı, `ADR-008`).

---

## C) Bu dosyada alınan kararlar

- **Tek ürün + tek bölge** stratejisi V1 için zorunludur (bilimsel + operasyonel).
- **Pilot:** kışlık buğday + Konya Ovası (Çumra ilçesi öncelik).
- **V1'in hedefi yalnız hasat zamanıdır;** verim tahmini V2+.
- **Modelleme sıralaması:** kural tabanlı → RF → XGBoost/LightGBM → DL.
- **Sentinel-2 ana kaynak, Sentinel-1 destek;** bulutluluk sigortası ve hasat olayı tespiti için.
- **Tech stack:** Python+TypeScript, FastAPI, Postgres+PostGIS, Streamlit→React, Leaflet, PWA→RN, GEE (akademik) → yerel pipeline (ticari).
- **Yerli uydular** V1 ana kaynak değil; V2/V3 doğrulama katmanı (`ADR-012`).

---

## D) Açık sorular

- Pilot ilçe seçimi ÇKS verisinin hangi ilçede daha hızlı erişilebileceğine bağlı (`ADR-017` Faz 0'da).
- GEE akademik plan ticari geçiş anında ne sürede biter? (Resmi politika *doğrulanmalı*.)
- Yerli uydulardan İMECE/GÖKTÜRK akademik kullanım için resmi bir veri talep formu mevcut mu? (TÜBİTAK UZAY ile iletişim, *doğrulanmalı*.)
- Sentinel-1'in VH/VV'si Konya'da hasat olayı için yeterli sinyal taşıyor mu? — Faz 1 analiziyle test edilecek.

---

## E) Sonraki aksiyonlar

1. Pilot kararının yazılı imzası (`ADR-001` + `ADR-010`).
2. Pilot ilçe seçimi (`ADR-017`).
3. Tech stack onayları için kararların `10_KARAR_KAYDI.md`'ye işlenmesi.
4. Konya il müdürlüğü ile veri talep e-postasının gönderilmesi (`T-003`).
5. Yerli uydu erişim politikalarının doğrulanması (TÜBİTAK UZAY iletişimi).

---

İlgili: [`04_TEKNIK_MIMARI.md`](./04_TEKNIK_MIMARI.md) (uygulama detayı) / [`10_KARAR_KAYDI.md`](./10_KARAR_KAYDI.md) (ADR günlüğü) / [`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md) (referansların doğrulanması).
