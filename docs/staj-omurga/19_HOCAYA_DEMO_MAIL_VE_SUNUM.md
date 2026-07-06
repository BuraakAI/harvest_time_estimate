# Hocaya Demo Paylaşımı — E-posta Taslağı ve Sunum Rehberi

> **Amaç:** Faz 2 MVP demosunu hocaya iletmek için hazır e-posta metni + 15–20 dk
> toplantıda ne anlatılacağı. T-005 (hoca gözden geçirmesi) ve T-208 (ekran kaydı)
> öncesi kullanılır.
> **Son güncelleme:** 2026-07-06

---

## 1. E-posta taslağı

**Konu:** Staj — Hasat Zamanı Karar Destek Sistemi (Faz 2 MVP demo) paylaşımı

---

Sayın Hocam,

Staj kapsamında geliştirdiğim **HasadHaber — Hasat Zamanı Karar Destek Sistemi**nin
Faz 2 (MVP-V1) prototipini paylaşmak istiyorum. Sistem, Sentinel-2 uydu zaman serisinden
parsel bazında *"hasada kaç gün kaldı?"* sorusuna kural tabanlı cevap üreten bir
Streamlit demosudur. Pilot bölge: **Konya / Çumra, kışlık buğday**.

**GitHub:** https://github.com/BuraakAI/harvest_time_estimate

**Yerel çalıştırma (3 komut, kimlik bilgisi gerekmez):**
```bash
git clone https://github.com/BuraakAI/harvest_time_estimate.git
cd hasat-zamani && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && streamlit run app.py
```
Tarayıcıda `http://localhost:8501` açılır. Varsayılan **Demo modu** tamamen offline
çalışır; 10 örnek parselde sentetik buğday fenolojisi gösterir.

**Ne yapıyor (kısa):**
- Haritada parseller hasat yakınlığına göre renklenir
- Parsel seçilince tahmini hasat tarihi, kalan gün, fenolojik evre ve güven skoru gösterilir
- NDVI/NDMI/VH eğrisi + "Neden bu tahmin?" açıklanabilirlik paneli
- Kooperatif görünümü: hasat sırası ve haftalık hasat dalgası
- Backtest sekmesi: lead-time doğruluk ölçüm çatısı (MAE, ±7/±14 gün isabet)

**Teknik özet:**
- Veri: Sentinel-2 (NDVI/NDMI) + Sentinel-1 (VH radar), Google Earth Engine adaptörü hazır
- Motor: kural tabanlı, etiketsiz (Sedano 2025 yaklaşımı); ML Faz 3'te
- Test: 27 birim test geçiyor; gerçek uydu verisiyle uçtan uca akış doğrulandı

**Dürüst sınır (önemli):**
Demo modundaki sayılar sentetiktir; gerçek tarım doğruluğu iddiası taşımaz. Gerçek
Sentinel-2 ile 10 parselde manuel doğrulama tablosu (T-207) ürettik — akış çalışıyor
ancak OSM'den seçilen parsellerin bu sezon büğday deseni göstermediği görüldü (yazlık
ürün olasılığı). Bu nedenle bir sonraki adım: ÇKS/üretici beyanıyla doğrulanmış gerçek
buğday parselleri + saha hasat tarihleri.

Uygun olduğunuzda 20–30 dakikalık kısa bir gözden geçirme toplantısı talep ediyorum.
İsterseniz ekran kaydı da paylaşabilirim.

Saygılarımla,
Burak Taş

**Ekler (isteğe bağlı):**
- `staj-omurga/18_T207_DOGRULAMA_TABLOSU.md` — gerçek uydu verisiyle doğrulama tablosu
- `staj-omurga/16_5N1K_RAPOR.md` — proje özeti

---

## 2. Toplantı sunum akışı (15–20 dk)

### Açılış (1 dk)

> "Hocam, uydu görüntülerinden parsel bazında hasat zamanı tahmini yapan bir karar
> destek sisteminin Faz 2 prototipini göstereceğim. Pilot: kışlık buğday, Çumra.
> Bugün göstereceğim şey bir ürün değil — çalışan bir **kanıt**: veri hattı, kural
> motoru ve arayüz uçtan uca bir arada."

### Demo turu (8–10 dk)

**1. Demo modu (sentetik veri) — 4 dk**

Sidebar'da **"Demo (sentetik)"** seçili olsun. Sarı uyarı bandını göster:

> "Bu mod tamamen offline; kimlik bilgisi yok. Sayılar sentetik — doğruluk iddiası yok,
> ama tüm arayüz ve motor davranışını gösteriyor."

Sırayla göster:
1. **Harita** — 10 parsel, renk kodu (yeşil/turuncu/kırmızı = kalan gün)
2. **Parsel seç** — tahmini hasat, kalan gün, fenolojik evre, veri güveni
3. **"Neden bu tahmin?"** — açılır panel: NDVI düşüşü, NDMI kuruma, takvim önseli
4. **Grafik** — NDVI/NDMI/VH eğrisi, bugün ve tahmini hasat işaretleri
5. **Kooperatif sekmesi** — 10 parselin hasat sırası tablosu + haftalık dalga grafiği
6. **Doğruluk sekmesi** — MAE, ±7/±14 gün isabet (sentetik etiketle; motor testi)

**2. Canlı GEE modu (gerçek uydu) — 3 dk** *(internet + GEE hesabı gerekir)*

Sidebar'dan **"Canlı (GEE)"** seç:

> "Aynı arayüz, gerçek Sentinel-2 verisi. Adaptör değişiyor; fenoloji, kural ve
> backtest kodu aynı kalıyor."

Bir parselde gerçek NDVI eğrisini göster. Demo eğrisinden farklı olduğunu vurgula.

**3. T-207 bulgusu — 2 dk** *(en önemli bilimsel nokta)*

`18_T207_DOGRULAMA_TABLOSU.md` veya grafiği aç:

> "Gerçek uydu verisiyle 10 parseli test ettik. Akış çalışıyor — ama bu parsellerin
> NDVI eğrisi buğday deseni göstermiyor; hasat penceresinde hâlâ yükseliyor. Büyük
> olasılıkla yazlık ürün ekilmiş. OSM'den 'tarla' poligonu almak yetmiyor; ekim
> doğrulaması (ÇKS / üretici beyanı) şart. Bu aslında iyi bir bulgu: sistemin veri
> riskini yakaladığını gösteriyor."

### Teknik özet (3 dk)

| Katman | Ne yaptık | Durum |
|---|---|---|
| Veri hattı | GEE → S2 NDVI/NDMI + S1 VH, SCL bulut maskesi, CSV cache | ✅ |
| Fenoloji | Savitzky-Golay, SOS/POS/EOS, senesens eğimi | ✅ |
| Tahmin | Kural tabanlı (NDVI düşüş + NDMI kuruma + takvim önseli) | ✅ |
| Arayüz | Streamlit: harita, grafik, kooperatif, backtest | ✅ |
| Test | 27 birim test | ✅ |
| Doğruluk | Gerçek saha etiketi | ❌ bekliyor (veri talebi) |

> "ML (RF/XGBoost) Faz 3'te; önce gerçek etiket toplanacak."

### Kapanış ve talep (2 dk)

**Hocadan isteyeceklerin:**
1. Pilot karar onayı (buğday + Konya/Çumra) — ADR-001
2. Çumra Ziraat Odası / İl Tarım'a veri talebi için destek veya tanıştırma
3. Faz 2 → Faz 3 geçişi için yazılı "devam" onayı

**Söylememen gerekenler** (17_HOCAYA_SUNUM_STRATEJISI uyarınca):
- "MAE 6 gün" gibi kesin doğruluk iddiası (sentetik etiketle ölçüldü)
- "Yarın App Store'da" / ticari vaat
- Henüz yapılmamış ML katmanını "yaptık" demek

---

## 3. Sık sorulan sorular — hazır cevaplar

**"Neden kural tabanlı, ML değil?"**
> Etiket darboğazı. Kural tabanlı motor etiketsiz çalışır (Sedano 2025); demo
> edilebilirlik garanti. ML, ≥30 saha hasat tarihi toplandıktan sonra Faz 3'te.

**"Doğruluk ne kadar?"**
> Henüz bilinmiyor — saha etiketi yok. Sentetik etiketle motor davranışı test
> edildi (MAE ~6 gün) ama bu tarımsal doğruluk değil. Gerçek sayı, ÇKS doğrulanmış
> parseller + biçerdöver kayıtları gelince ölçülecek.

**"Neden bu parseller buğday değil?"**
> OSM'den `landuse=farmland` ile aldık; ekim bilgisi yok. Çumra sulu tarımda
> rotasyon yaygın — yazlık ürün olası. T-207 bunu yakaladı; bir sonraki adım
> doğrulanmış buğday parseli listesi.

**"Sentinel-2 yeterli mi, radar neden?"**
> Optik (NDVI/NDMI) birincil sinyal. Radar (VH) bulutlu dönemlerde destek —
> Faz 4'te füzyon. Şu an VH çekiliyor ama kural motorunda ikincil.

**"Bu işi yapan var mı?"**
> Evet — EOSDA, OneSoil, FieldView. Farkımız: Türkiye odaklı, parsel-özel kural
> motoru, açıklanabilirlik, akademik şeffaflık. Detay: `14_REKABET_VE_MEVCUT_SISTEMLER.md`.

---

## 4. Ekran kaydı kontrol listesi (T-208)

Kayıt alırken bu sırayı izle (~5 dk):

- [ ] Demo modu açılış + sarı uyarı bandı
- [ ] Haritada 10 parsel, renk kodu
- [ ] Bir parsel seç → tahmin paneli + "Neden bu tahmin?"
- [ ] NDVI grafiği (POS, bugün, tahmini hasat işaretleri)
- [ ] Kooperatif sekmesi → tablo + bar chart
- [ ] Doğruluk sekmesi → MAE metrikleri
- [ ] (İsteğe bağlı) Canlı GEE moduna geçiş → gerçek eğri farkı
- [ ] Kapanış: "Gerçek doğruluk için saha etiketi bekliyoruz"

---

*Bu dosya `17_HOCAYA_SUNUM_STRATEJISI.md` ile birlikte okunur.*
