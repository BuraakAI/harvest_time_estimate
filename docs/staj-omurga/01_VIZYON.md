# 01 — Vizyon, Problem ve Başarı Ölçütleri

> **Amaç:** Projenin uzun ve kısa erimli hedeflerini, paydaşlara göre değer önermesini ve "MVP'den ticari sisteme" yolculuğunu tek belgede sabitlemek.
> **Kapsam:** Stratejik vizyon (4 katman), problem tanımı, 5N1K özeti, kapsam (V1 yapar/yapmaz), başarı ölçütleri, anti-vizyon.
> **Son güncelleme:** 2026-05-10

---

## 1. Stratejik vizyon — dört zaman ufku

Bu proje **tek seferlik bir akademik çıktı** değil, kademeli olarak büyüyebilecek bir karar destek sistemidir. Bu nedenle vizyonu dört zaman ufkuna ayırarak yönetiyoruz.

### 1.1. MVP vizyonu (0–3 ay)

**Tek cümle:** *Konya Ovası'nda seçilmiş 30–100 buğday parselinde, son 5 sezonun uydu zaman serisi üzerinden "hasada kalan gün" ± gün cinsinden hesaplanır ve tarayıcıda demo edilir.*

- Tek ürün (kışlık buğday), tek bölge (Konya, Çumra ilçesi öncelik).
- Açık veri (Sentinel-2 ana, Sentinel-1 destek) ve kural tabanlı bir motor.
- Hocaya gösterilebilir bir Streamlit demosu + tekrar üretilebilir notebook seti.
- Etiket sayısı az olabilir; bu yüzden "doğruluk yüzdesi" yerine "kapsama + güven skoru + örnek üzerinde gerekçe" gösterilecektir.

### 1.2. POC vizyonu (3–6 ay)

**Tek cümle:** *Aynı pilotta 30+ saha etiketiyle Random Forest / XGBoost kalan-gün regresyon modeli kurulur, bir FastAPI + PWA arayüzünde gerçek bir kullanıcının seçtiği parsele tahmin döner.*

- Etiket koleksiyonu kuralı (üretici beyanı + kooperatif kaydı + biçerdöver logu) yerleşmiş.
- Bulutluluk için Sentinel-1 füzyonu eklenmiş.
- API + PWA mimarisi çalışıyor; tek kullanıcı tek parsel akışı 30 saniyenin altında.
- "Neden bu tahmin?" panelinin ilk sürümü (NDVI/NDMI/VH eğrileri + en güçlü 3 sinyal).

### 1.3. Bitirme/ürün vizyonu (6–12 ay)

**Tek cümle:** *İkinci pilot ürün (ayçiçeği) eklenir, bitirme tezi yazılır, en az 1 kooperatif gerçek sezonda sistemi kullanır ve mobil uygulama (React Native V0) test paketinde dağıtılır.*

- Açıklanabilirlik (SHAP) entegrasyonu son kullanıcı arayüzünde.
- Domain shift (Konya → Trakya) sorununa açık testler.
- Bitirme tezi taslağı + 1 ulusal kongre bildirisi taslağı.
- KVKK uyumu, kullanıcı sözleşmesi, veri sahipliği politikası yazılı.

### 1.4. Ticari/kurumsal vizyon (12–36 ay)

**Tek cümle:** *Türkiye'de en az 3 ürün (buğday, ayçiçeği, dane mısır), 3 bölgeyi (İç Anadolu, Trakya, Çukurova/GAP) kapsayan, kooperatif ve alım firması müşterilerine abonelik + API ile satılan bir hasat penceresi karar destek platformu.*

- GEE bağımlılığından çıkış: yerel pipeline (rasterio + xarray + dask + STAC + COG + object storage).
- Kurumsal entegrasyonlar: il müdürlükleri, alım firmaları, sigorta.
- Ölçeklenebilir mimari (asenkron jobs, önbellek, çok kiracılı veri tabanı).
- Bitirme sonrası bağımsız bir ürün/şirket dönüşümü için temel hazır.

> **Önemli ayrım:** "Büyük vizyon" 36 ay konuşur; **MVP yalnız 0–3 ayı taahhüt eder**. Hocaya sunarken bu ayrım net tutulur — büyük vizyon ilham, MVP iddia.

---

## 2. Problem cümlesi

Türkiye'de hasat tarihi planlaması büyük ölçüde **yerel deneyim + iklim hissi** ile yapılır. Bu;

- biçerdöver / işçi / kamyon planlamasında **boş gün veya çakışma** yaratır,
- kalite kaybı (geç hasat → dane dökülmesi, erken hasat → düşük randıman) doğurur,
- alıcı–satıcı arası **bilgi asimetrisi** ile fiyat baskısına yol açar,
- ürün kayıtları (ÇKS) ile gerçek hasat zamanı arasında **veri boşluğu** üretir.

Mevcut yabancı tarım izleme platformlarının çoğu **genel ürün sağlığı / NDVI** odaklıdır; doğrudan **parsel düzeyinde "hasada kalan gün"** çıktısı veren, Türkiye ürün takvimine kalibre, açık veri tabanlı, mobil-erişilebilir bir sisteme yer vardır.

---

## 3. "Bu proje yalnız bir NDVI grafiği değildir"

Çünkü:

| NDVI grafiği uygulaması | Bu projenin iddiası |
|---|---|
| Tek bir indeks zaman serisi gösterir | Çok değişkenli (NDVI/EVI/NDMI/NDRE/VH) zaman serisi + meteoroloji + parsel sınırı |
| Yorumu kullanıcıya bırakır | Fenolojik evre + tahmini hasat tarihi + güven skoru + gerekçe sinyalleri çıktısı |
| Bulutlu sezonda sessizleşir | Sentinel-1 radar ve HLS füzyonuyla kapsama korunur |
| Statik | Sezon ilerledikçe güncellenen tahmin + etiket öğrenmesi |
| Anonim | Kullanıcı parselleri kayıt altında, KVKK uyumlu sahiplik |
| Akademik gösterim | MVP sonrası kooperatif/alım/sigorta kullanıcıları için iş modeli |

NDVI bizim girişimizin yalnız **bir bandı**dır. Çıktımız bir karardır: **"Bu hafta mı, gelecek hafta mı, iki hafta sonra mı?"**

---

## 4. 5N1K (özet, detaylı yorum `16_5N1K_RAPOR.md`'da)

| Soru | Cevap |
|---|---|
| **Ne** | Parsel bazında tahmini hasat tarihi + kalan gün + güven skoru üreten karar destek sistemi |
| **Neden** | İş gücü/lojistik planlama, kalite kaybı önleme, dijital tarımın eksik halkasını kapatma |
| **Kim için** | Birincil: çiftçi, ziraat mühendisi, kooperatif. İkincil: alım firmaları, sigorta, banka, bakanlık |
| **Nerede** | Pilot: Konya Ovası — kışlık buğday. Genişleme: Trakya/ayçiçeği, sulu mısır bölgeleri |
| **Ne zaman** | Tek görüntüyle değil, **zaman serisi** ile çalışılır; senesens–olgunluk–hasat döneminde sık gözlem kritik |
| **Nasıl** | Sentinel-2 (optik) + Sentinel-1 (radar) + meteoroloji + parsel sınırı + kural tabanlı fenoloji → ML kalan-gün regresyonu |

---

## 5. Paydaş bazlı değer önermeleri

Aynı sistem farklı paydaşlara farklı şeyler söyler. Sunumda ve ürün arayüzünde bu segment ayrımı net tutulur.

### 5.1. Çiftçi (B2C — bireysel üretici)

- **Acı:** "Bu sezon biçerdöver kıt; ne zaman ararsam yer ayırırlar, bilemiyorum."
- **Değer:** "Tarlanız 12–18 Temmuz arası hasada uygun; ±5 gün güvenle planlayın."
- **Tetik:** mobil push bildirim 7 gün önce, 3 gün önce.
- **Dikkat:** Türkiye'de bireysel çiftçi düşük ödeme isteklidir; "freemium" katman gerekli.

### 5.2. Ziraat mühendisi / agronomist

- **Acı:** "20 üreticiye danışıyorum, hangisinin tarlası önce olur, hangisi sonra — kafamda tutamıyorum."
- **Değer:** Çoklu parsel görünümü, sıralı hasat sırası listesi, tarla ziyareti rotası önerisi.
- **Dikkat:** Profesyonel kullanıcı; gerekçe ister ("neden bu tarla daha geç?").

### 5.3. Kooperatif

- **Acı:** "Üyelerin hasat tarihleri çakışıyor; biçerdöver / kamyon / depo / kantarda darboğaz oluyor."
- **Değer:** Bölgesel ısı haritası, hafta hafta hasat dalgası tahmini, üye uyarı paneli.
- **Dikkat:** *İlk müşteri segmenti aday adayı.* Tek noktadan çoklu üreticiye değer aktarır → düşük müşteri edinim maliyeti.

### 5.4. Alım firması (un fabrikası, yağ üreticisi, yem fabrikası)

- **Acı:** "Tedarik kayması fiyatları ve kapasite kullanımını bozuyor; bölgesel hasat dalgasını önceden bilmek istiyorum."
- **Değer:** Bölgesel/havza bazlı tahmin → tedarik planlama; çoklu kooperatif/üretici tahminlerinin agregasyonu.
- **Dikkat:** Yıllık kurumsal lisans modeli mantıklı; veri gizliliği hassas.

### 5.5. Banka / sigorta (insurtech)

- **Acı:** "Tarım kredisi / sigorta riskini doğru fiyatlamak için sahaya inmem gerekiyor; uydu temelli hızlı sinyal lazım."
- **Değer:** Hasat zamanı + verim proxy + anomali bayrağı (kuraklık, dolu) → risk skorlama girdisi.
- **Dikkat:** **Verim tahmini bu projenin V1'i değildir**; bu paydaşa V2'de hitap edilir.

### 5.6. Bakanlık / il-ilçe tarım müdürlükleri (B2G)

- **Acı:** "Üretim planlaması, destekleme, alan uyumu denetimi için saha verisi istiyorum."
- **Değer:** Ulusal/il/ilçe ölçeğinde hasat dalgası tahmini, ekiliş doğrulama, anomali izleme.
- **Dikkat:** Yıllık ihale veya kurumsal pilot; veri paylaşımında karşılıklılık (parsel sınırı verisi karşılığında tahmin servisi).

> **Erken hedefleme önceliği:** **Kooperatif > alım firması > banka/sigorta > bakanlık > bireysel çiftçi.** Gerekçesi: kooperatif tek sözleşmede çoklu kullanıcıya erişim, hızlı geri bildirim, makul ödeme isteği.

---

## 6. Kapsam — V1 ne **yapar**, ne **yapmaz**

### V1 yapar
- Bir parselin (shapefile / harita üzerinde çizilen poligon) son 90 günlük NDVI / EVI / NDMI / VH eğrisini gösterir.
- Mevcut fenolojik evreyi etiketler (vejetatif / başaklanma / süt olum / hamur olum / sarı olum / hasat).
- Kural tabanlı motorla "tahmini hasat tarihi" + "kalan gün" + güven skoru üretir.
- Bulutluluk, eksik gözlem, anomali gibi gerekçe sinyallerini raporlar.
- Web ve mobil-uyumlu PWA arayüzünde 10+ örnek parsel üzerinde demo eder.

### V1 yapmaz
- **Verim tahmini** yapmaz (V2 yol haritası).
- **Otomatik tarla sınırı çıkarımı** yapmaz; kullanıcı şekil yükler veya çizer.
- **Çoklu ürün** desteklemez; yalnız buğday (V2 ayçiçeği, V3 mısır).
- **Sigorta / hasar tespiti** yapmaz.
- **Operasyonel ticari SLA** vermez; staj kapsamında "gösterilebilir prototip" hedefi.
- **Yüksek doğruluk taahhüdü** vermez — etiket yetersizliği şeffafça paylaşılır.

---

## 7. Başarı ölçütleri — minimum ve ideal

### 7.1. Bilimsel başarı

| Metrik | Minimum (savunma) | İdeal (yayın) |
|---|---|---|
| Hasat tarihi MAE (gün) | ≤ ±10 | ≤ ±5 |
| ±7 gün isabet oranı | ≥ %60 | ≥ %80 |
| Bulutlu sezonda kapsama | ≥ %80 | ≥ %95 |
| Test parsel sayısı | ≥ 30 | ≥ 100 |
| Tekrarlanabilirlik (notebook + repo) | %100 | %100 |
| Güven skoru kalibrasyonu (ECE) | < 0.15 | < 0.08 |

### 7.2. Ürün başarısı

| Metrik | Minimum | İdeal |
|---|---|---|
| Web demo açılış süresi | < 5 sn | < 3 sn |
| Bir parsel için sonuç üretme süresi | < 30 sn | < 10 sn |
| Kullanıcı testinde "anladım, kullanırım" oranı | ≥ %50 (3 görüşme) | ≥ %70 (5 görüşme) |
| PWA mobilde çalışma | ✅ | ✅ + offline cache |

### 7.3. Akademik/staj başarısı

| Çıktı | Minimum kabul | İdeal kabul |
|---|---|---|
| Çalışan prototip | Lokal Streamlit + 10 demo parsel | Public PWA + 30+ parsel |
| Repo + dokümantasyon | README + reproducible | + Docker compose + CI yeşil |
| Staj raporu | 30 sayfa, üniversite formatı | + EK olarak veri envanteri ve karar kayıtları |
| Bitirme tezi taslağı | Konu + yöntem netleşmiş | Ön sonuçlar + tartışma |
| Sunum | 15 dk + soru | + 60 sn demo videosu |

---

## 8. Öncelik sıralaması (anlaşmazlık çıkarsa)

1. **Bilimsel doğrulanabilirlik** — sonuçlar tekrar üretilebilir olmalı.
2. **Açıklanabilirlik** — "neden bu tahmin?" sorusu cevaplanmalı.
3. **Demo edilebilirlik** — en geç Faz 3 sonunda hocaya canlı gösterilebilmeli.
4. **Tekrar kullanılabilirlik** — kod/veri/karar kayıtları yeniden kullanılabilir olsun.
5. **Genel kullanıcı deneyimi** — V1'de "şık olmasın, anlaşılır olsun".
6. **Performans optimizasyonu** — V2 ve sonrası.

---

## 9. Anti-vizyon (asla olmaması gereken)

- "Çok güzel görünen ama içi boş NDVI haritası uygulaması" olmayacak.
- "Yalnız Sentinel-2 ortalaması alınmış basit bir grafik" olmayacak.
- "Hocaya 'demo şu an çalışmıyor' deme noktasına" gelmeyecek; offline demo paketi her zaman hazır olacak.
- "Veri izni kâğıdı imzalanmadan başlanan" sahaya gerçek etiket toplama olmayacak.
- "Az etiketle yüksek doğruluk" iddiası yapılmayacak; belirsizlik ürünün ön yüzünde.

---

## 10. Bu dosyada alınan kararlar

- Vizyon dört zaman ufkunda yönetilir (MVP / 6 ay / 12 ay / 36 ay).
- Erken müşteri hedefi **kooperatif** segmentidir.
- V1 kesinlikle **verim tahmini** yapmaz; yalnız hasat zamanı.
- Başarı tek bir "doğruluk yüzdesi" ile değil, çoklu metrikle (MAE + kapsama + kalibrasyon + ±gün isabet) değerlendirilir.
- "Yalnız NDVI" projesi olmadığı arayüzde ve raporda görünür kalır.

---

## 11. Açık sorular

- Hocanın bitirme tezi konu sınırlaması var mı? (V1 hasat zamanı yeterli mi, verim de istenir mi?)
- Konya il müdürlüğünden ÇKS parsel verisi resmî olarak ne sürede gelir?
- Kooperatif iletişim için Çumra mı, Karatay mı öncelikli? (`ADR-017` çözecek)
- Etiket kıtlığında "düşük doğruluk" iddiasını arayüzde nasıl ifade edeceğiz? (UX kararı, Faz 3)

---

## 12. Sonraki aksiyonlar

1. Hocayla 30 dk vizyon onay toplantısı (T-005).
2. Pilot karar imzası (ADR-001 + ADR-010).
3. Konya il müdürlüğü/Çumra Ziraat Odası iletişim listesi (T-002).
4. Veri talep e-postası taslağı (T-003).
5. Repo iskeleti açılışı (T-004).

---

İlgili: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) — bu vizyonun arkasındaki nedenler / [`16_5N1K_RAPOR.md`](./16_5N1K_RAPOR.md) — hocaya sunulacak ana rapor.
