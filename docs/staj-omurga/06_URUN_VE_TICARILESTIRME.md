# 06 — Ürün, Müşteri Segmentleri ve Türkiye Tarım Ekosistemine Giriş

> **Amaç:** Akademik MVP'nin bir ürüne, ürünün de Türkiye tarım ekosisteminde sürdürülebilir bir hizmete dönüşmesi için müşteri seçimini, dağıtım kanalını ve iş modelini iş planı düzeyinde belgelemek.
> **Kapsam:** Ürün çekirdeği, mobil/masaüstü/PWA ayrımı, müşteri segmentleri ve hedefleme önceliği, B2C/B2B/B2G karşılaştırması, Türkiye ekosistem giriş yolu, ücretsiz–pilot–lisans seviyeleri, fiyatlama (fikir düzeyi), rekabet pozisyonu özeti.
> **Son güncelleme:** 2026-05-10
> **Uyarı:** Bu dosya kesin gelir tahmini içermez; rakamlar **aralık** ve **varsayım** olarak işaretlenir.

---

## 1. Ürün adı (çalışma)

**HasadHaber** (yer tutucu) — *"Tarlanız size hasada kaç gün kaldığını söyler."*

Alternatif çalışma adları: HasatRota, FenoTakvim, EkiPlan, BiçerSaat. Marka tescil değerlendirmesi Faz 5.

---

## 2. Ürün çekirdeği (V1)

**Bir ekran cümlesi:** *"Tarlamı çiz veya seç → bana 7 günlük ve 14 günlük hasat penceremi söyle."*

V1 ekran hiyerarşisi:

```
┌────────────────────────────────────────────────────┐
│  HasadHaber          [Profil]  [Ayarlar]           │
├────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐  │
│  │              [HARİTA — Leaflet]              │  │
│  │       parseller renk: yeşil/sarı/kırmızı     │  │
│  │              [+ Yeni parsel]                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  Seçili: Çumra-12 (4.7 ha, kışlık buğday)          │
│  ┌──────────────────────────────────────────────┐  │
│  │  Tahmini hasat:  19 Temmuz 2026  ±5 gün       │  │
│  │  Kalan gün:      48                          │  │
│  │  Fenoloji:       Süt olum                    │  │
│  │  Güven:          ●●●●○ (78%)                 │  │
│  │  [Eğriyi göster] [Etiket gir] [Paylaş]       │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

**V1 başarı kriteri:** kullanıcı uygulamayı ilk açtığında 30 saniye içinde **bir parsel için tahmin** görüyor.

---

## 3. PWA, web panel, mobil uygulama ayrımı

| Sürüm | Hedef kullanıcı | Ana güç | Sınır |
|---|---|---|---|
| **PWA (V1, Faz 3-4)** | Saha + ofis kullanıcısı (tek kişi) | Tek kod tabanı, anında erişim, App Store gerekmez | Cihaz API'lerine sınırlı erişim |
| **Web panel (V2)** | Kooperatif/firma yöneticisi (büyük ekran) | Çoklu parsel, rapor ihracı, yönetici görünümü | Mobil saha kullanımı için uygun değil |
| **React Native mobil (V2)** | Çiftçi + agronomist (saha) | Push, kamera (etiket foto), GPS, offline | Mağaza onay süreci, store ücretleri |
| **Masaüstü (Electron)** | — | — | **Gerek yok**; web responsive yeterli |

**Karar:** V1 yalnız PWA. V2'de aynı backend üzerinde web panel + RN mobil. Electron yok.

---

## 4. Müşteri segmentleri

| Segment | Ne acısı? | Değer önermesi | Ödeme isteği | Erişim zorluğu |
|---|---|---|---|---|
| **Bireysel çiftçi** | İşçi/biçerdöver bul, kalite kaybı | Hasat haftası önceden bilinir | Düşük | Orta |
| **Büyük üretici** (200+ ha) | Çoklu parsel filo planlama | Tek ekranda tüm filo | Orta | Yüksek (B2B satış) |
| **Kooperatif** | Üye koordinasyonu, biçer/kantar darboğazı | Toplu görünüm + üye uyarıları | Orta-yüksek | **Düşük (1 sözleşme = N kullanıcı)** |
| **Alım firması** (un/yağ/yem fabrikası) | Tedarik kayması | Bölgesel hasat dalgası tahmini | Yüksek | Yüksek (uzun satış döngüsü) |
| **Sigorta / banka** | Risk modeli | Hasat zamanı + verim proxy | Yüksek (kurumsal) | Çok yüksek (uzun döngü) |
| **Bakanlık / il müdürlüğü** | Üretim planlama, ekiliş doğrulama | Bölgesel ısı haritası | Yıllık ihale | Çok yüksek (bürokrasi) |

### 4.1. Neden ilk müşteri **çiftçi değil de kooperatif** olabilir?

| Boyut | Çiftçi (B2C) | Kooperatif (B2B) |
|---|---|---|
| Müşteri edinim maliyeti | Yüksek (her birey ayrı satış) | Düşük (tek sözleşme = onlarca üye) |
| Ödeme isteği | Düşük | Orta-yüksek |
| Veri erişimi (etiket) | Zor (her üreticiyle ayrı muhatap) | Kolay (kooperatif kayıtları zaten merkezi) |
| Geri bildirim hızı | Yavaş (parça parça) | Hızlı (toplantıda kollektif) |
| Marka güveni | Bağımsız çiftçi temkinli yaklaşır | Kooperatif tavsiyesi yüksek güven sinyali |
| Akademik pilot uygunluk | Düşük | Yüksek |

**Sonuç:** İlk müşteri segmenti olarak **kooperatif** önerilir. Bireysel çiftçi freemium katmanla kazanılır.

### 4.2. Önceliklendirme

```
1) Kooperatif (öncelik #1)
2) Alım firması (orta vadeli)
3) Bireysel çiftçi freemium (uzun vadeli kullanıcı tabanı)
4) Bakanlık / il müdürlüğü (kurumsal değer + veri karşılığı)
5) Sigorta / banka (V2+ verim modülü açıldıktan sonra)
6) Büyük üretici (genelde kooperatif aracılığıyla erişilir)
```

---

## 5. B2C / B2B / B2G karşılaştırma

| Boyut | B2C (çiftçi) | B2B (kooperatif, alım firması) | B2G (bakanlık, il müd.) |
|---|---|---|---|
| Satış döngüsü | 1-2 hafta | 1-3 ay | 6-12 ay |
| Ortalama sözleşme değeri | Düşük | Orta-yüksek | Yüksek |
| Müşteri sayısı | Çok | Orta | Az |
| Ödeme tahsilat zorluğu | Yüksek (vadeli, kayıp) | Orta | Düşük (resmi) |
| KVKK / sözleşme yükü | Düşük | Orta | Yüksek |
| Pazara çıkış sürtünmesi | Düşük (app store, organic) | Orta (satış görüşmesi) | Yüksek (ihale) |
| Akademik referans değeri | Düşük | Orta | Çok yüksek |

**Strateji:** V1 kooperatif (B2B) odaklı; B2C freemium ile destekle; B2G ihale fırsatlarına Faz 5'te girilebilir.

---

## 6. Türkiye tarım ekosistemine giriş yolu

| Kanal | Eylem | Kaynak |
|---|---|---|
| **Ziraat odaları** | Çumra/Karatay Ziraat Odası tanışma toplantısı | Düşük maliyet, yüksek itibar |
| **Kooperatifler** | Konya Çumra Tarımsal Kalkınma Kooperatifi pilot | Düşük maliyet, hızlı geri bildirim |
| **İl/ilçe tarım müdürlükleri** | Veri talep + işbirliği önerisi | Resmi temas, veri ekosistemi |
| **Un/yem/yağ sanayi** | Bölgesel agronomist toplantıları | Orta maliyet, uzun döngü |
| **Sigorta / banka** | TARSİM / Ziraat Bankası tarım birimi | V2'de değerlendirilmeli |
| **Akademik camia** | Türkiye Tarımsal Uzaktan Algılama Sempozyumu sunum | Düşük maliyet, itibar + öğrenme |
| **Sosyal medya** | LinkedIn (B2B), Instagram/YouTube (B2C eğitim videoları) | Düşük-orta maliyet |
| **Tarım fuarları** | TÜYAP, GAPSHOW, AgroExpo | Yüksek maliyet (stand) |

**Ön ihtiyaçlar:**
- Tek sayfa ürün anlatımı (landing page) — Faz 3.
- 60 saniye demo video — Faz 4.
- Vaka çalışması: "Çumra'daki üretici X için sezon raporu" — Faz 4-5.

---

## 7. İş modeli alternatifleri

| Model | Mantık | Uygunluk |
|---|---|---|
| **Freemium** | İlk parsel ücretsiz, ek parseller ücretli | ✅ Bireysel çiftçi edinmek için |
| **Abonelik (parsel-ay)** | Aylık X parsel = Y ₺ | ✅ Kooperatif/firma |
| **API kotası** | Aylık X tahmin = Y ₺ | ✅ Tedarik/sigorta |
| **Yıllık kurumsal lisans** | Sabit ücret + SLA | ✅ Bakanlık, büyük firma |
| **Komisyon** | Hasat sonrası fiyat üzerinden % | ❌ Türkiye'de denenmemiş |
| **Açık kaynak + ücretli destek** | Kod açık, eğitim/entegrasyon ücretli | 🟡 Akademik damar için iyi |

### 7.1. Önerilen karma model (Faz 5, fikir düzeyi)

```
Free          : 1 parsel, 1 sezon
Pro           : ~25 parsel, 5 sezon arşivi, push, ihracat
Cooperative   : ~250 parsel, çoklu kullanıcı, rapor
Enterprise    : sınırsız parsel + API + SLA, yıllık sözleşme
```

> **Uyarı:** Yukarıdaki kademeler **fikir düzeyindedir**. Kesin fiyat aralığı ancak Faz 5'te 5+ pilot kullanıcı görüşmesinden sonra netleşir. Kesin gelir tahmini bu raporda yapılmaz.

### 7.2. Tüm seviyelerde değişmez ilkeler

- **Veri sahipliği kullanıcının** — gizlilik politikası birinci sayfada.
- **Tahmin tavsiye, karar değil** — UI'da güven skoru ve sınırlar belirgin.
- **Bağımsız ölçüm dışlanmaz** — kullanıcı kendi etiketini girebilir, modelin yanılmasını işaretleyebilir.

---

## 8. Rakipler ve pozisyonlama (özet)

> Detaylı analiz `14_REKABET_VE_MEVCUT_SISTEMLER.md`'de.

| Rakip | Türkiye uygunluk | Bizden ana fark |
|---|---|---|
| EOSDA Crop Monitoring | Var ama lokalizasyonsuz | Hasat zamanı odaklı değil |
| OneSoil | Var | Sınır çıkarımı + NDVI; hasat tarihi yok |
| FieldView | Donanım bağımlı | Çekirdek değil |
| Cropwise (Syngenta) | Sınırlı | Çekirdek değil |
| GEOGLAM Crop Monitor | Bölgesel | Parsel düzeyi değil |
| Sen2-Agri / Sen4Stat | Akademik / kamu | Açık kaynak; bizim ürüne entegre kullanılabilir |
| Yerli dijital tarım sistemleri | TARBİL benzeri (*doğrulanmalı*) | Genelde sağlık/operasyon, hasat tahmini değil |

**Pozisyon:** "Genel tarım izleme platformu" değil; **"Hasat zamanlama karar destek sistemi"**. İlk ürün: Konya/kışlık buğday hasat penceresi. Sonra çok ürünlü fenoloji motoru.

---

## 9. Hukuki / etik kontrol listesi

| Kalem | Durum |
|---|---|
| KVKK uyumu (kullanıcı verisi) | Faz 3 zorunlu |
| Veri sahipliği sözleşmesi | Faz 3 |
| Açık kaynak lisansı (kod) | Faz 0'da seç (`ADR-016`) |
| Veri lisansı (üretilen tahminler) | Faz 4'te belirle |
| Sentinel / Landsat / HLS lisansları | Açık, atıf zorunlu |
| GEE ToS — ticari kullanım | Faz 5'te ücretli plan veya yerel pipeline |
| Marka tescili | Faz 5 |
| KVK Kurulu kayıt | Ticari faaliyetle birlikte (Faz 5) |

---

## 10. Anti-örüntüler (ürün tarafı)

- ❌ "100 özellik koyalım" — V1 yalnız 3 işlevle çıkar (parsel ekle, eğri gör, tahmin gör).
- ❌ "Çiftçinin internetine güvenelim" — offline cache zorunlu.
- ❌ "Bedavadan herkese her şey" — pilot dışında değer kaybı.
- ❌ "Önce iOS, sonra Android" — eşit zamanlı tek kod tabanıyla çık (RN).
- ❌ "Tahminler yanılırsa kullanıcı suçumuz olmaz" — güven skoru ve sınır şartları her zaman görünür.

---

## 11. Bu dosyada alınan kararlar

- **İlk müşteri segmenti** kooperatif; bireysel çiftçi freemium ile destek.
- V1 yalnız **PWA**; web panel ve RN mobil V2; Electron yok.
- İş modeli karması: freemium + abonelik (parsel-ay) + API + yıllık lisans.
- Kesin gelir tahmini bu raporda yapılmaz; varsayımlar açık.
- Pozisyon: "hasat zamanlama karar destek sistemi" (genel tarım izleme değil).

---

## 12. Açık sorular

- Konya'da öncelikli kooperatif kim? (Çumra Tarımsal Kalkınma Kooperatifi vs alternatifler — *doğrulanacak*.)
- TARSİM ile temas Faz 5'te mi V2'de mi?
- KVKK için müşterinin parsel verisi ne süre saklanmalı?
- B2G ihale çalışmaları için destek programları (KOSGEB, TÜBİTAK 1512, vs.) hangisi uygun?

---

## 13. Sonraki aksiyonlar

1. Çumra Ziraat Odası iletişim kişisi belirlenecek (T-002).
2. Faz 4'te 60 sn demo video çekimi.
3. Faz 5'te 5 pilot kullanıcı görüşmesi (kooperatif yöneticisi + üretici karması).
4. Landing page taslağı Faz 3'te.
5. KVKK/sözleşme taslakları için bir hukuk danışmanı kontağı (üniversite hukuk fakültesi vb.).

---

İlgili: [`04_TEKNIK_MIMARI.md`](./04_TEKNIK_MIMARI.md) (uygulama bağı) / [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md) (akademik çıktı bağı) / [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md) (ürün riskleri) / [`14_REKABET_VE_MEVCUT_SISTEMLER.md`](./14_REKABET_VE_MEVCUT_SISTEMLER.md) (rakip detay) / [`15_MALIYET_VE_IS_PLANI.md`](./15_MALIYET_VE_IS_PLANI.md) (maliyet detay).
