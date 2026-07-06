# 13 — Uydu Uygunluk Matrisi (Açık + Ticari + Türkiye)

> **Amaç:** Dünyadaki ve Türkiye'deki uyduları bizim hasat-zamanı tahmini problemimiz için **kanıt-bazlı** olarak puanlamak; MVP omurgasında ne olacağını ve V2/V3'te neyin doğrulama katmanı olacağını netleştirmek.
> **Kapsam:** Uydu seçim kriterleri, açık veri uyduları, ticari uydular, Türkiye uyduları (RASAT, GÖKTÜRK-1/2, İMECE, TÜRKSAT 6A neden uygun değil), her uydu için tablo (özellik + maliyet + rolümüz + MVP/ticari uygunluk skorları), önerilen veri kombinasyonu.
> **Son güncelleme:** 2026-06-26
> **Uyarı:** Aşağıdaki teknik özellikler `deep_search.md`'den derlenmiştir. Tezde alıntılanmadan önce **resmi kaynak** (ESA, NASA, USGS, TÜBİTAK UZAY, Copernicus, üretici sayfaları) ile birebir doğrulanmalıdır. Belirsiz kalan satırlar **"doğrulanmalı"** ile işaretlenir.

---

## 1. Uydu seçim kriterleri (12 başlık)

Her uydu aşağıdaki kriterlerle puanlanır. Kriterler tarımsal fenoloji ve hasat tahmini için literatürde belirgin olanlardır.

| Kriter | Neden önemli | Not |
|---|---|---|
| Spektral bant zenginliği | NDVI/EVI/NDMI/NDRE için yeterli bant gerekli | NIR + Red + RedEdge + SWIR |
| NIR var mı? | Vejetasyon yansıma çekirdeği | Zorunlu |
| Red-edge var mı? | Geç dönem klorofil hassasiyeti | Tercihen var |
| SWIR var mı? | Kanopi su (NDMI) için gerekli | Tercihen var |
| Optik / radar | Bulut bağımsızlığı için radar | İkisi de istenir |
| Mekânsal çözünürlük | Parsel boyutuna göre ≤ 30 m önerilir | 10-30 m ideal |
| Zamansal tekrar | Sezon-içi sıklık | ≤ 7 gün ideal |
| Açık / kapalı veri | Maliyet ve sürdürülebilirlik | Açık öncelikli |
| API erişimi / GEE varlığı | Pipeline kolaylığı | Var/yok ikili |
| Tarihsel arşiv | Çoklu sezon için | ≥ 5 yıl ideal |
| Türkiye kapsaması | Pilot kapsam | Tüm Türkiye |
| Tarımsal fenolojiye uygunluk | Literatürde kanıt | Yüksek/orta/düşük |

---

## 2. Açık veri uyduları

| Uydu | Sensör / bantlar | Çözünürlük | Tekrar | Erişim | Maliyet | Türkiye kapsaması | Tarihsel arşiv | MVP /10 | Ticari /10 | Bizim rolümüz |
|---|---|---|---|---|---|---|---|---|---|---|
| **Sentinel-2 A/B** | 13 bantlı MSI (Mavi, Yeşil, Kırmızı, 4× RedEdge, NIR, SWIR1, SWIR2 vb.) | 10/20/60 m | 5 gün (kombine) | Copernicus / GEE / AWS Open Data / MS Planetary | Açık ve ücretsiz | Tam | 2015– | **10** | **9** | **Birincil omurga (optik fenoloji)** |
| **Sentinel-1 A/B/C/D** | C-band SAR; VH/VV polarizasyon | 5–40 m (modlara göre) | ~6 gün (çift uydu; 2022–24 tek uyduyla 12 gün, S1C/S1D ile tekrar 6) | Copernicus / GEE / ASF | Açık ve ücretsiz | Tam | 2014– | **9** | **9** | **Bulut sigortası, hasat olayı (VH düşüşü)** |
| **Landsat 8/9** | OLI/TIRS; 11 bant; Pan 15 m | 30 m MS, 15 m Pan | 8 gün (kombine) | USGS / GEE / AWS | Açık ve ücretsiz | Tam | Landsat ailesi 1972– | **7** | **7** | **Tarihsel süreklilik + HLS girdisi** |
| **HLS (Landsat + S2 harmonized)** | Harmonize ürün | 30 m | ~1.6 gün | NASA / GEE | Açık ve ücretsiz | Tam | 2015– | **8** | **8** | **Yoğun zaman serisi (Faz 4)** |
| **MODIS (Aqua/Terra)** | 36 kanal | 250–1000 m | 1–2 gün | NASA / GEE | Açık ve ücretsiz | Tam | 1999/2002– | **5** | **4** | **Bölgesel / mevsimlik bağlam** |
| **VIIRS (Suomi NPP, NOAA-20/21)** | VIS + IR | Orta çözünürlük (~375–750 m) | 1 gün | NOAA / GEE | Açık ve ücretsiz | Tam | 2011– | **4** | **4** | **MODIS sürekliliği** |

---

## 3. Ticari uydular

> Bunlar bütçe gerektirir; akademik MVP'de yer almaz, ancak Faz 4-5'te yüksek çözünürlüklü doğrulama veya premium müşteri katmanı için değerlendirilir.

| Uydu / sağlayıcı | Sensör | Çözünürlük | Tekrar | Maliyet | MVP /10 | Ticari /10 | Bizim rolümüz |
|---|---|---|---|---|---|---|---|
| **PlanetScope (Planet)** | 4–8 bant (SuperDove'da coastal blue, blue, green I/II, yellow, red, red-edge, NIR) | ~3.7–4.1 m | Günlük | Ticari (teklif) | 3 | **8** | Küçük parsel doğrulama; premium ürün |
| **SkySat (Planet)** | RGB + NIR | < 1 m | Görev bazlı | Ticari | 2 | 7 | Çok yüksek çözünürlüklü doğrulama |
| **Maxar WorldView-2** | 8 MS bant (coastal, blue, green, yellow, red, red-edge, NIR1, NIR2) | 0.46 m Pan / 1.84 m MS | < 1 gün (görev) | Ticari | 2 | 7 | Doğrulama / referans |
| **Maxar WorldView-3** | 8 VNIR + 8 SWIR + CAVIS | 0.31 m Pan / 1.24 m MS / 3.7 m SWIR | < 1 gün | Ticari (yüksek) | 1 | 7 | SWIR + ultra çözünürlük doğrulama |
| **Maxar WorldView Legion** | 30 cm sınıfı, MS | 30 cm | Günde çoklu | Ticari (yüksek) | 1 | 6 | İleri ticari katman |
| **Airbus Pléiades / SPOT 6/7** | 4 bant MS | Pléiades 0.5 m, SPOT 1.5 m | 1–3 gün | Ticari | 2 | 6 | Avrupa odaklı doğrulama |
| **ICEYE / Capella (SAR)** | X-band SAR | 0.5–1 m | Yüksek revisit | Ticari | 1 | 5 | Bulutta yüksek çözünürlük SAR |

---

## 4. Türkiye uyduları

> Brief'in 5. kuralı net: **abartmadan**, yetenek ve sınırı birlikte yazılır.

| Uydu / sahip | Sensör / bantlar | Çözünürlük | Tekrar | Erişim modeli | NIR? | Red-edge? | SWIR? | MVP /10 | Ticari /10 | Bizim rolümüz |
|---|---|---|---|---|---|---|---|---|---|---|
| **RASAT** (TÜBİTAK UZAY) | Pan + 3 bant MS (Mavi, Yeşil, Kırmızı) | 7.5 m Pan / 15 m MS | 4 gün | GEZGİN üzerinden ücretsiz arşiv | ❌ Yok | ❌ Yok | ❌ Yok | **3** | **3** | Tarihsel / yerli görünürlük; **NIR olmadığı için fenoloji çekirdeğine uygun değil** |
| **GÖKTÜRK-2** (TUSAŞ + TÜBİTAK UZAY) | Optik EO; kamuya açık bant ayrıntısı sınırlı (doğrulanmalı) | < 2.5 m | ~2.5 gün | Resmî mağaza km² bazlı ücretli | (doğrulanmalı) | (doğrulanmalı) | (doğrulanmalı) | **3** | **5** | Yüksek çözünürlüklü doğrulama / ek örnekleme |
| **GÖKTÜRK-1** (TUSAŞ) | Yüksek çözünürlüklü optik EO | (doğrulanmalı; submetre sınıfı bilgileri) | ~2.5 gün | Açık erişim akışı sınırlı | (doğrulanmalı) | (doğrulanmalı) | (doğrulanmalı) | **2** | **5** | İzin/erişim sürtünmesi nedeniyle V1'e uygun değil |
| **İMECE** (TÜBİTAK UZAY) | Metrealtı PAN + 3.96 m RGBNIR | Pan metrealtı, MS 3.96 m | (doğrulanmalı) | Açık ekosistem henüz belirgin değil | ✅ Var | ❌ Yok | ❌ Yok | **3** | **6** | Yüksek çözünürlüklü yerli optik; V2/V3 doğrulama katmanı |
| **TÜRKSAT 6A** ve diğer haberleşme uyduları | Haberleşme (yer gözlem değil) | — | — | — | — | — | — | **0** | **0** | **EO uydusu değildir** — kapsam dışı |

### 4.1. Türkiye uyduları için özet karar

- **RASAT:** NIR/red-edge/SWIR yokluğu nedeniyle fenoloji ve hasat-hazır oluş takibi için modern Sentinel-2 kadar güçlü değildir; tarihsel ve yerli görünürlük katkısı vardır.
- **GÖKTÜRK-2:** Yüksek uzamsal çözünürlük; ancak kamuya açık band çeşitliliği ve sürekli akış sınırlı görünür → doğrulama / ek örnekleme aracı.
- **GÖKTÜRK-1:** Teknik olarak güçlü; ancak açık erişim/ticarileşme akışı Sentinel-Landsat kadar görünür değil → izin sürtünmesi proje riski.
- **İMECE:** Teknik açıdan en umut veren yerli optik platform; metrealtı PAN ve 3.96 m RGBNIR küçük parsel doğrulama için değerli; **araştırmacı dostu sürekli erişim ekosistemi V1 için yeterince oturmuş değil.**
- **TÜRKSAT 6A:** Haberleşme uydusu — tarımsal görüntüleme için **uygun değildir.**
- **TÜBİTAK BulutTÜBİTAK / hesaplama platformları:** Doğrudan uydu değil, ama yerel pipeline taşırken hesap kaynağı olarak değerlendirilebilir.

---

## 5. Önerilen veri kombinasyonu

### 5.1. MVP ana omurga (Faz 1–3)

| Katman | Uydu | Rol |
|---|---|---|
| Optik fenoloji | **Sentinel-2 A/B** | Birincil |
| Bulut sigortası + hasat olayı | **Sentinel-1 A/B** | İkincil zorunlu |
| Tarihsel süreklilik | **Landsat 8/9** | Yardımcı |
| Yoğun zaman serisi (Faz 4) | **HLS** | Faz 4'te eklenir |
| Bölgesel bağlam | **MODIS / VIIRS** | Tematik harita |

### 5.2. Ticari ölçek (Faz 4–5)

Yukarıdaki MVP ana omurgası **aynen korunur**, ek olarak:

- Premium müşteri için **PlanetScope** (günlük) — küçük parsel doğrulama / abonelik üst katmanı.
- Yerli görünürlük katkısı için **GÖKTÜRK-2 / İMECE** — yıllık doğrulama paketi.
- Yüksek çözünürlüklü tek seferlik doğrulama için **WorldView-2/3** — özel sözleşme.

### 5.3. Faz × uydu çapraz tablo

| Faz | S2 | S1 | Landsat | HLS | MODIS | Planet | GÖKTÜRK-2 | İMECE | WorldView |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ✅ | 🟡 | 🟡 | — | — | — | — | — | — |
| 2 | ✅ | ✅ | 🟡 | — | — | — | — | — | — |
| 3 | ✅ | ✅ | ✅ | 🟡 | — | — | — | — | — |
| 4 | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | — |
| 5 | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ (premium) | 🟡 | 🟡 | 🟡 |

✅ Aktif kullanım • 🟡 Opsiyonel / değerlendirme • — Kapsam dışı

---

## 6. Uydu seçiminin ADR ile bağı

- **ADR-B-011:** Sentinel-2 ana, Sentinel-1 destek.
- **ADR-B-012:** Türkiye uyduları V1 ana kaynak değil; V2/V3 doğrulama katmanı.

Bu iki ADR doğrudan bu dosyanın puanlamasından beslenir.

---

İlgili: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) (uydu kararı gerekçesi) / [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md) (veri katmanları) / [`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md) (uydu kullanılan akademik referanslar) / [`15_MALIYET_VE_IS_PLANI.md`](./15_MALIYET_VE_IS_PLANI.md) (uydu maliyetleri).

---

## Bu dosyada alınan kararlar
- MVP ana omurga: Sentinel-2 + Sentinel-1 + meteoroloji (+ Landsat/HLS Faz 3-4'te).
- Türkiye uyduları V1'de yok; V2/V3'te doğrulama / yüksek çözünürlüklü örnekleme katmanı olarak değerlendirilir.
- TÜRKSAT 6A kapsamdan tamamen dışlanır (haberleşme uydusu).
- Ticari yüksek çözünürlüklü uydular yalnız ödeme gücü olan müşteri katmanlarında devreye girer.

## Açık sorular
- GÖKTÜRK-1/2 ve İMECE için resmi tarımsal araştırma erişim koşulları nedir? — Kuruma resmî yazıyla sorulacak.
- HLS'nin Türkiye kapsamasında veri boşluğu var mı? — Faz 4 başında bir parsel için kapsama testi yapılacak.
- BulutTÜBİTAK kaynağı yerel pipeline taşımada bütçe açısından mantıklı mı? — Faz 4'te değerlendirilecek.

## Sonraki aksiyonlar
- Faz 0 sonu: Sentinel-2 + Sentinel-1 GEE örneklerini doğrulayan tek-parsel notebook hazır olsun.
- Faz 4 başı: HLS koleksiyonu pilot bölgeye yetkin biçimde çekiliyor mu test et.
- Faz 5: GÖKTÜRK-2 fiyatlandırması güncel duruma göre yıllık bütçeye dahil et veya çıkar.