# 17 — Hocaya Sunum ve İlk Görüşme Stratejisi

> **Amaç:** Stajın ilk hoca/danışman görüşmesinde **nelerin söyleneceğini**, **hangi dosyaların gösterileceğini**, **hangilerinin gösterilmeyeceğini** ve **hangi onayların alınacağını** önceden netleştirmek; sunum başına gereksiz risk üretmemek.
> **Kapsam:** İlk görüşme akışı, ne anlatılır / ne anlatılmaz, kritik onay listesi, 2-3 haftalık raporlama protokolü, dosyalar arası gösterim sırası, savunma soruları için cep cevap notları.
> **Son güncelleme:** 2026-05-10

---

## 1. İlk görüşmenin amacı

Birinci toplantı **"hocayı projeye ortak etme"** toplantısıdır. Üç şey hedeflenir:

1. **Onay almak** — pilot karar (Konya + buğday), tech stack, faz iskeleti, çıktı paketi.
2. **Bağlantı kurmak** — Çumra Ziraat Odası, KVKK danışmanı, sempozyum çağrı tarihi.
3. **Düzenli ritim kurmak** — 2-3 haftalık ara rapor + Faz sonu G karar kapısı toplantısı.

İlk görüşmede **"her şeyi anlatmak"** hedef değildir; **doğru soruları sordurabilmek** hedeftir.

---

## 2. Görüşme akışı (45 dakika önerisi)

| Dakika | Konu | Hangi dosya açık olsun |
|---|---|---|
| 0–3 | Kendini tanıt + projeyi tek paragrafta özetle | — |
| 3–8 | Problem ve vizyon (Yönetici özeti) | [`16_5N1K_RAPOR.md`](./16_5N1K_RAPOR.md) Bölüm 1 |
| 8–15 | Pilot kararı: neden buğday + Konya | [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) Bölüm A.2-A.3 |
| 15–22 | Tech stack özeti + GEE vendor lock-in farkındalığı | [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) Bölüm B (özet) |
| 22–28 | Faz iskeleti + ölçeklenebilir süre (6 hafta / 3 ay / 6 ay / 12 ay) | [`03_FAZLAR_VE_DURUMLAR.md`](./03_FAZLAR_VE_DURUMLAR.md) Bölüm 1 ve 3 |
| 28–35 | Riskler ve "neden başarısız olabilir?" senaryoları | [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md) Bölüm 9-10 |
| 35–40 | Ara rapor şablonu + ritim önerisi | [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md) Bölüm 9 |
| 40–45 | Hocanın soruları + onay listesi | [`10_KARAR_KAYDI.md`](./10_KARAR_KAYDI.md) ADR-001 imzaya |

---

## 3. Ne anlatmalıyım? (anahtar mesajlar)

### Mesaj 1 — "Bu proje tek seferlik bir akademik çıktı değil"
Faz iskeleti zaten akademik MVP'den ticari prototipe uzanıyor; vizyon dört zaman ufkuna (MVP, POC, ürünleşme, ticari) ayrılmış.

### Mesaj 2 — "Bilimsel çerçevem güçlü"
Literatür taraması yapılmış (`12_LITERATUR_TARAMASI.md`); en yakın referanslar Yue 2024, Liao 2023, Şimşek 2024, Sedano 2025. Bizim farkımız: Türkiye + ürün dikeyi + kalan-gün + açıklanabilir PWA.

### Mesaj 3 — "Riskleri biliyorum ve mitigasyonum var"
Risk kaydı 17 madde, "neden başarısız olabilir?" senaryoları yazılı. Tek kişi tükenmişliği, etiket darboğazı, GEE bağımlılığı en kritikleri.

### Mesaj 4 — "Süre esnek, çıktı paketim ölçeklenebilir"
6 hafta / 3 ay / 6 ay / 12 ay için aynı faz iskeleti farklı derinlikte çalışır. Hoca hangi süreyi tercih ederse plan ona uyacak.

### Mesaj 5 — "Etiketsiz başlangıçta da değerli çıktı üretebilirim"
V1 kural tabanlı (Sedano 2025 stilinde); etiket gelmezse demo hâlâ savunulabilir. Etiketle V2'de kalan-gün regresyonu.

---

## 4. Ne anlatmamalıyım? (ilk görüşmede yapmaması gerekenler)

- ❌ **Detaylı maliyet tablosu sunma** — `15_MALIYET_VE_IS_PLANI.md` ileri faz; ilk görüşmede yatırımcı algısı yaratmaz.
- ❌ **Ticari iş modelini büyük büyük anlatma** — `06_URUN_VE_TICARILESTIRME.md` Bölüm 6-7 ileri faz; ilk hedef akademik onay.
- ❌ **Çoklu ürün ve çoklu bölge konuş** — sürekli "tek ürün, tek bölge" disiplini.
- ❌ **"Hızla ulusal kapsama büyürüz" benzeri abartı** — bunu yapan dünyada bile yok; hocaya "abartılı pazarlama" izlenimi vermez.
- ❌ **Tüm dosyaları aynı anda paylaşma** — bunaltıcı olur; ihtiyaca göre dosya açılır.
- ❌ **Marka tescil, fiyat, gelir** — bunlar Faz 5 konularıdır.

---

## 5. Hangi dosyayı göstermeliyim, hangisini göstermemeliyim?

| Dosya | Birinci görüşmede? | Neden? |
|---|---|---|
| `00_README.md` | ✅ | İndeks olarak yararlı |
| `01_VIZYON.md` | ✅ | Stratejik vizyonu net gösterir |
| `02_NEDEN_SONUC.md` | ✅ | Pilot kararının gerekçesi kritik |
| `03_FAZLAR_VE_DURUMLAR.md` | ✅ | Süre ölçeklemesi önemli |
| `04_TEKNIK_MIMARI.md` | 🟡 sadece üst görünüm | Detay ileri toplantıya |
| `05_VERI_VE_MODELLEME.md` | 🟡 problem 3 form özeti | Tam metni ileri faz |
| `06_URUN_VE_TICARILESTIRME.md` | 🟡 segment tablosu | Ticari iş modeli ileri faz |
| `07_RISKLER_VE_KALITE.md` | ✅ Bölüm 1, 9, 10 | Şeffaflık güven verir |
| `08_TESLIMATLAR.md` | ✅ teslimat haritası + ara rapor şablonu | Düzenli ritim sözü |
| `09_GOREVLER.md` | 🟡 ilk 14/30 gün | Detay liste ezberletme amaçlı değil |
| `10_KARAR_KAYDI.md` | ✅ ADR-001 imzaya | Karar disiplini gösterilir |
| `11_GLOSSARY.md` | 🟡 referans | Soru gelirse |
| `12_LITERATUR_TARAMASI.md` | ✅ Bölüm 5 + tablo özeti | Akademik güven |
| `13_UYDU_UYGUNLUK_MATRISI.md` | 🟡 üst tablo | Detaya gerekirse iner |
| `14_REKABET_VE_MEVCUT_SISTEMLER.md` | 🟡 pozisyonlama tezi (Bölüm 4) | "Yapan var mı?" sorusuna |
| `15_MALIYET_VE_IS_PLANI.md` | ❌ | İlk görüşmede gerek yok |
| `16_5N1K_RAPOR.md` | ✅ tek pdf çıktı olarak | Hocaya bırakılacak doküman |

---

## 6. Hocadan almam gereken kritik onaylar

- [ ] **ADR-001:** Pilot — Konya + kışlık buğday onayı
- [ ] **Faz iskeleti:** Faz 0–5 yapı onayı
- [ ] **Süre senaryosu:** 6 hafta / 3 ay / 6 ay / 12 ay'dan birinin tercihi
- [ ] **Ara rapor ritmi:** 2-3 haftada bir, `08_TESLIMATLAR.md` Bölüm 9 şablonuyla
- [ ] **Veri talebi yazısı:** Hoca'nın Çumra Ziraat Odası'na resmi tanıtım yazısı vermesi
- [ ] **KVKK danışman önerisi**
- [ ] **Bitirme tezi danışmanlığı uyumu** — staj danışmanı + bitirme danışmanı aynı/farklı kişiyi netleştirme
- [ ] **Yayın hedefi:** Ulusal sempozyum mu doğrudan dergi mi
- [ ] **Sonraki toplantı tarihi**

---

## 7. Hocanın muhtemel soruları ve cep cevapları

| Soru | Tek paragraflık cevap | Dayanak |
|---|---|---|
| "Neden buğday?" | Tek ürünle başlamak hasat zamanı tahmini için bilimsel olarak zorunlu; buğday Konya'da baskın, takvimi istikrarlı, literatürde referansı güçlü (Yue 2024). | `02_NEDEN_SONUC.md` A.3 |
| "Neden Konya?" | Büyük homojen parsel, düşük bulutluluk, erişilebilir kurumsal ağ, stratejik buğday üretim bölgesi. | `02_NEDEN_SONUC.md` A.2 |
| "Bunu yapan var mı?" | Evet, akademik literatür var; ticari platformlar (EOSDA, OneSoil) genel sağlık veriyor ama Türkiye + kalan-gün dikeyinde niş açık. | `12_LITERATUR_TARAMASI.md` 5, `14_REKABET_VE_MEVCUT_SISTEMLER.md` 4 |
| "Senin farkın ne?" | Türkiye yerel + ürün dikey + kalan-gün cinsinden çıktı + açıklanabilir + PWA + açık veri tabanlı düşük maliyet. | `14_REKABET_VE_MEVCUT_SISTEMLER.md` 5 |
| "Etiket nereden gelecek?" | 5 kanal paralel: üretici beyanı, kooperatif kaydı, biçerdöver logu, saha fotoğrafı (EXIF), tarihsel takvim+uzman onayı. Çapraz doğrulama ile kalite puanı. | `05_VERI_VE_MODELLEME.md` 3 |
| "Bulutlu sezon olursa?" | Sentinel-1 SAR bulut bağımsız; HLS yoğun zaman serisi; kapsama metrik takibi. | `07_RISKLER_VE_KALITE.md` R-02 |
| "Türkiye uyduları yok mu?" | RASAT NIR'sız fenoloji için yetersiz; GÖKTÜRK-1/2 erişim sürtünmesi; İMECE umut veriyor ama V1 omurgası için ekosistem oturmadı; V2/V3 doğrulama katmanı. TÜRKSAT 6A haberleşme uydusudur, EO değil. | `13_UYDU_UYGUNLUK_MATRISI.md` 4 |
| "GEE'ye bağımlı kalmaz mısın?" | Faz 0-3 GEE; Faz 4'te yerel Python pipeline prototipi (rasterio + xarray + dask + STAC + COG); Faz 5'te ticari geçişte tamamen yerel. ADR-008. | `02_NEDEN_SONUC.md` B.2.2 |
| "Doğruluk hedefin nedir?" | V1 MAE ≤ 10 gün, ±7 gün isabet ≥ %60; V3 stretch MAE ≤ 5, ±7 ≥ %80. Etiket olmadan kesin iddia yapmıyoruz (ADR-B-015). | `05_VERI_VE_MODELLEME.md` 7-8 |
| "Risk listende en kritik nedir?" | Etiket erişim gecikmesi (R-01) ve etiket kalite tutarsızlığı (R-03). Mitigasyon: Faz 0'da paralel kuruma iletişim + çapraz doğrulama. | `07_RISKLER_VE_KALITE.md` 1 |
| "Bitirme tezi konun nedir?" | Bu projenin yöntem + sonuç bölümü doğrudan tez olur; özgün katkı Türkiye/buğday/kalan-gün dikeyi. | `08_TESLIMATLAR.md` 3 |

---

## 8. İlk 2-3 haftalık raporun teslimi

`08_TESLIMATLAR.md` Bölüm 9.2'de "Sprint 0 ara raporu" tam taslak halinde. İlk hoca toplantısının ardından 14 gün içinde aynı şablonla doldurulup teslim edilir. Şablonun 9 başlığı sabit kalır; sadece içerik güncellenir.

Teslim biçimi:
1. **PDF** olarak (1-2 sayfa) — e-posta eki.
2. **Repo `docs/reports/2026-05-26.md`** — versiyonlu.
3. **Kısa toplantı** (15 dk) — sözlü özet.

---

## 9. Etik ve şeffaflık disiplini

- **Belirsizlikleri saklama.** "Doğrulanmalı" işareti olan satırlar hocaya da gösterilir; kapatılana kadar açıkça belirtilir.
- **Pazarlama dili yok.** "Devrim niteliğinde", "tüm Türkiye için", "yapay zeka destekli" gibi içerikten kaçın; somut metrik ve dosya referansıyla konuş.
- **Dürüst rekabet özeti.** "Kimse yapmıyor" iddiası yerine `14_REKABET_VE_MEVCUT_SISTEMLER.md` 4. bölümündeki konumlanmayı kullan.
- **Doğruluk iddiası etikettir.** Etiketsiz "yüksek doğruluk" iddiası yapılmaz (ADR-B-015).

---

İlgili: [`16_5N1K_RAPOR.md`](./16_5N1K_RAPOR.md) (hocaya bırakılan tek belge) / [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md) (ara rapor şablonu) / [`10_KARAR_KAYDI.md`](./10_KARAR_KAYDI.md) (ADR imza listesi).

---

## Bu dosyada alınan kararlar
- İlk görüşme amacı: onay + bağlantı + ritim. Detaylı teknik gösterim değil.
- Maliyet ve ticari iş modeli ilk görüşmede gündeme alınmaz.
- "Bunu yapan var mı?" sorusuna **dürüst evet ama niş açık** cevabı standart söylem.
- Tüm doğrulanmamış rakamlar açık şekilde "doğrulanmalı" işaretiyle hocaya sunulur.
- İlk hocaya bırakılacak dosya `16_5N1K_RAPOR.md`'tir.

## Açık sorular
- Hocanın tercih ettiği iletişim kanalı (e-posta / WhatsApp / Teams)? — İlk toplantıda netleşir.
- Toplantı sıklığı haftalık mı, 2 haftada bir mi? — Hoca kararına göre.
- Sözlü vs. yazılı tercih: hoca uzun rapor mu kısa not mu okuyor? — İlk birkaç sprintten sonra görülecek.

## Sonraki aksiyonlar
- Görüşme öncesi 24 saat: bu dosyayı baştan oku, anahtar mesajları sesli prova et.
- Görüşme sonrası 24 saat: ADR-001'in durumunu güncelle, ara rapor takvimini repo'ya işle.
- 2 hafta sonra ilk ara raporu teslim et (Sprint 0 ara raporu taslağı zaten hazır).