# 14 — Rekabet ve Mevcut Sistemler

> **Amaç:** "Bu işi yapan var mı?" sorusuna **dürüst** ve **kanıt-bazlı** cevap vermek; mevcut sistemleri sınıflandırarak bizim ürünün konumunu netleştirmek; jürinin "neden başka birisi değil de sen?" sorusuna cevap üretmek.
> **Kapsam:** Dünyada ve Türkiye'de uydu tabanlı tarım izleme platformlarının özeti, her sistemin hedef kullanıcı/veri/özellik/Türkiye uygunluk değerlendirmesi, rekabet matrisi (özellik bazlı), pozisyonlama tezi, niş açıklığının kanıtı.
> **Son güncelleme:** 2026-05-10
> **Uyarı:** Aşağıdaki sistem özelliklerinin önemli kısmı `deep_search.md`'den ve sağlayıcı resmi sayfalarından alınmıştır. Tezde alıntılanmadan önce **resmi kaynaklarla** birebir doğrulanmalıdır.

---

## 1. "Bu işi yapan var mı?" — dürüst kısa cevap

- **Evet**, uydu tabanlı tarım izleme sistemleri var.
- **Evet**, bazıları NDVI, ürün sağlığı, hava verisi, risk analizi, saha notu sunuyor.
- **Ancak** çoğu **doğrudan Türkiye'ye özel**, **parsel bazlı**, **kalan-gün cinsinden hasat tahmini** veren ve **çiftçi/kooperatif PWA arayüzüne sokulmuş** bir niş üründe yoğunlaşmamıştır.
- Türkiye'deki kamu sistemleri (TARBİL gibi) operasyonel tarımsal bilgi sistemi olarak değerli ama **ürün-spesifik kalan-gün dikeyi** olarak konumlanmamıştır.

Sonuç: **Bilimsel rekabet yoğun, ürün dikeyinde Türkiye için niş açık.**

---

## 2. Sistemler — özet

### 2.1. Uluslararası kamu / araştırma çerçeveleri

| Sistem | Geliştiren | Amaç | Veri | Özellik | Hasat tahmini? | Türkiye uygunluğu | Bizim farkımız |
|---|---|---|---|---|---|---|---|
| **GEOGLAM Crop Monitor** | GEO + çoklu uluslararası kuruluş | Küresel ürün durumu izleme | Sentinel/Landsat/MODIS | Aylık küresel ürün durumu raporu, gıda güvenliği | ❌ Doğrudan değil; sezon durumu | Bölgesel kapsama var ama çiftçi düzeyi yok | Parsel düzeyi + kalan gün + PWA |
| **Copernicus MARS / EU yield** | Avrupa Komisyonu JRC | AB ürün büyüme koşulları, verim tahmini | Sentinel ailesi + meteoroloji | Resmi, operasyonel, yüksek güven | 🟡 Verim odaklı | AB merkezli; Türkiye düzenli kapsam dışı | Türkiye odak + kalan gün dikeyi |
| **CAP Area Monitoring Services** | EU CAP Pillar | Parsel/faaliyet takibi, ekiliş denetim | Sentinel | Uyum/denetim odaklı | ❌ | Türkiye'de paralel sistem TARBİL/ÇKS | Çiftçi karar destek tarafı |
| **Sen2-Agri / Sen4Stat** | ESA | Sentinel-2 tarım algoritmaları açık altyapı | Sentinel-2 | Algoritmik referans, açık bilim | 🟡 | Açık kullanılabilir; tek başına ürün değil | Ürünleştirilmiş, kullanıcı dostu |

### 2.2. Ticari tarım izleme platformları

| Sistem | Geliştiren | Hedef kullanıcı | Veri | Özellik | Hasat tahmini? | Türkiye uygunluğu | Bizim farkımız |
|---|---|---|---|---|---|---|---|
| **EOSDA Crop Monitoring** | EOS Data Analytics | Çiftçi, agronomist | Sentinel + hava + saha notları | NDVI, hava, saha izleme, alan yönetimi | 🟡 Genel saha sağlığı; spesifik kalan-gün net değil | İngilizce; Türkiye yerelleştirme sınırlı | Türkçe + ürün dikeyi |
| **OneSoil** | OneSoil | Çiftçi | Sentinel | NDVI, parsel sınırı (otomatik), scouting | ❌ Doğrudan değil | İngilizce; popülasyon küçük | Türkiye + kalan gün + güven skoru |
| **Climate FieldView** (Bayer) | Bayer Crop Science | Büyük çiftçi (donanım entegre) | Çoklu (uydu + makina) | Tüm sezon planlama, hasat verisi | 🟡 Hasat **kayıt** ana; tahmin değil | Türkiye'de kullanım sınırlı; donanım bağı | Açık veri + donanımsız PWA |
| **Cropwise (Syngenta)** | Syngenta | Çiftçi, danışman | Sentinel + reçete | NDVI, reçeteleme, ekim takvimi | 🟡 Genel | Türkiye dağıtım sınırlı | Hasat dikeyi netliği |
| **John Deere Operations Center** | John Deere | Büyük makina sahibi | Makina telemetri + uydu | Filo + tarım operasyon | 🟡 Hasat lojistiği var ama tahmin değil | Donanım bağımlılığı | Donanımsız + tahmin odaklı |
| **Planet Crop Biomass / Planet Agriculture** | Planet | Kurumsal | PlanetScope + Sentinel | Günlük biyokütle, anomali | 🟡 Biyokütle proxy | Ticari, kurum odaklı | Açık veri + ürün düşük maliyetli |
| **EarthDaily Agro** | EarthDaily | Kurumsal | Çoklu kaynak harmonize | Anomali, hava, agronomi | 🟡 | Türkiye'de kısıtlı erişim | Türkiye odak |

### 2.3. Türkiye yerel sistemler

| Sistem | Geliştiren | Amaç | Bizim farkımız |
|---|---|---|---|
| **TARBİL** (Tarımsal İzleme ve Bilgi Sistemi) | T.C. Tarım ve Orman Bakanlığı | Kamu çapında bitkisel üretim izleme | Operasyonel kamu; çiftçi seviyesinde mobil + kalan gün dikeyi yok |
| **ÇKS / Parsel Sorgulama** | Bakanlık | Çiftçi parsel kayıtları | Operasyon değil veri sistemi; tahmin yok |
| **Türkiye Uzaktan Algılama Birimi / TÜBİTAK BİLGEM, TÜBİTAK UZAY projeleri** | TÜBİTAK | Araştırma + servis | Ürün-müşteri arayüzü çoğu zaman yok |
| **Üniversite spin-off / akademik prototipler** | Akademi | Araştırma | Sürekli ürün değil |
| **Yerli AgTech start-uplar** (varsa) | Çeşitli | Çoğunlukla saha sensörü, hava, akıllı sulama | Hasat-zamanı dikeyinde belirgin oyuncu yok (taramamızda) |

> **Not:** "Yerli yeni ürün var mı?" sorusunu Faz 0-1'de bizzat doğrulamak gerekir; AgTech ekosistemi hızlı değişiyor.

---

## 3. Rekabet matrisi (özellik bazlı)

| Özellik | Bizim ürün | EOSDA | OneSoil | FieldView | Cropwise | TARBİL | GEOGLAM |
|---|---|---|---|---|---|---|---|
| NDVI / bitki sağlığı | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ |
| Parsel çizimi | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Hava verisi | 🟡 (V2) | ✅ | 🟡 | ✅ | ✅ | ✅ | ✅ |
| Fenoloji metrikleri | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| **Hasat penceresi (gün)** | ✅ **çekirdek** | 🟡 dolaylı | ❌ | 🟡 dolaylı | 🟡 | ❌ | ❌ |
| **Kalan gün tahmini** | ✅ **çekirdek** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Mobil PWA | ✅ V1 | ✅ | ✅ | ✅ | ✅ | 🟡 | ❌ |
| Türkçe yerelleştirme | ✅ | 🟡 | 🟡 | ❌ | 🟡 | ✅ | 🟡 |
| Açık veriyle çalışma | ✅ | 🟡 | 🟡 | ❌ donanım bağı | 🟡 | ✅ | ✅ |
| Açıklanabilirlik (SHAP / "neden") | ✅ V3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| KVKK / veri sahipliği netliği | ✅ | (kurum politika) | (kurum politika) | (kurum politika) | (kurum politika) | (kamu) | (kamu) |
| Türkiye'ye özel ürün dikeyi (buğday Konya) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 4. Pozisyonlama tezi

> **HasadHaber, "genel tarım izleme platformu" değildir.**
>
> **HasadHaber, "Türkiye'ye özel, ürüne dikey, hasat zamanlama karar destek sistemi"dir.**
>
> İlk sürüm Konya/kışlık buğday hasat penceresi tahmini üzerinde çalışır; ikinci sürümde Trakya/ayçiçeği, üçüncü sürümde sulu mısır eklenir.

Bu pozisyon, mevcut platformların eksik bıraktığı **dört kesişimde** yer alır:
1. Türkiye yerelleştirmesi
2. Ürün dikeyliği (genel değil özel)
3. Kalan-gün cinsinden çıktı
4. Açık veriyle düşük maliyet + güven skoru/açıklanabilirlik

---

## 5. Niş açıklığının kanıtı

Aşağıdaki üç boyut **birlikte** karşılayan başka bir sistem taramamızda yer almadı:

| Boyut | Mevcut sistemlerde durum |
|---|---|
| Türkiye odak + Türkçe + Türkiye veri kaynakları (ÇKS, MGM) | Sınırlı (TARBİL var ama dikey değil) |
| Kalan-gün cinsinden hasat penceresi tahmini, parsel düzeyinde | Akademik literatürde çalışıldı (Liu 2025, Yue 2024) ama operasyonel ürün olarak Türkiye'de yok |
| Çiftçi/kooperatif PWA arayüzü + KVKK uyumu | Mevcut sistemler ya çok genel ya yabancı yönelim |

**Bu üçünün kesişimi şu an itibarıyla boştur** — projemiz bu boşluğa konumlanır.

---

İlgili: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) (pilot kararı) / [`06_URUN_VE_TICARILESTIRME.md`](./06_URUN_VE_TICARILESTIRME.md) (müşteri segmentleri ve B2B/B2C/B2G) / [`12_LITERATUR_TARAMASI.md`](./12_LITERATUR_TARAMASI.md) (akademik benzeri çalışmalar) / [`15_MALIYET_VE_IS_PLANI.md`](./15_MALIYET_VE_IS_PLANI.md) (rakip fiyatlama referansı).

---

## Bu dosyada alınan kararlar
- Konum: "Genel tarım izleme platformu" değil; "hasat zamanlama karar destek sistemi". Bu cümle pazarlama metinlerinde sabit kalır.
- Dört kesişim (Türkçe yerel + dikey ürün + kalan gün + açıklanabilir/PWA) bizim ürün metnimizin temel söylemi.
- Mevcut sistemlere açıkça atıf yapılır; "yapan yok" iddiası yerine "biz şu kesişimde varız" iddiası kurulur.

## Açık sorular
- TARBİL'in son 2 yıldaki ürün özelliklerinde değişiklik var mı? — Resmî kaynaktan teyit gerek.
- Yerli AgTech start-uplarda (Tarla.io, AgrowTech, vb. — taramada doğrulanmadı) hasat-zamanı dikeyi ile çıkmış oyuncu var mı?
- EOSDA'nın "harvest readiness" alt modülü oluştu mu? — Faz 4'te tekrar kontrol.

## Sonraki aksiyonlar
- Hafta 3-4: Her rakip sistem için 5-10 dakikalık demo videosu izle, kısa not düş.
- Faz 5: Pozisyonlama tezini bir landing page metnine çevir.
- Yıllık: Rekabet matrisini güncel tut; yeni oyuncu çıkarsa eklemek.