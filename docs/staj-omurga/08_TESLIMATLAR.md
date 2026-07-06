# 08 — Teslimatlar: Rapor, Bitirme Tezi, Repo, Demo, Sunum, Yayın

> **Amaç:** Stajın çıktılarını akademik (rapor + tez + makale), teknik (repo + model + demo) ve operasyonel (sunum + video + sözleşme) düzeyde standardize etmek; her teslimatın iskeletini, kabul ölçütünü ve hangi fazda olgunlaşacağını netleştirmek.
> **Kapsam:** Teslimat haritası, staj raporu iskeleti (sayfa hedefli), bitirme tezi iskeleti, sunum slayt planı (18 dk), repo README iskeleti, yayın stratejisi (kongre + dergi), model kartı şablonu, faz × teslimat çapraz tablo.
> **Son güncelleme:** 2026-05-10

---

## 1. Teslimat haritası

| Teslimat | Format | Faz başlangıç | Faz tamamlama | Sahip | Kabul ölçütü |
|---|---|---|---|---|---|
| Staj raporu | .docx + .pdf | 0 | 4 | Burak | Üniversite formatı, 30+ sayfa |
| Bitirme tezi taslağı | .docx + .pdf | 2 | 5 | Burak + danışman | Giriş+yöntem+sonuç tam |
| Çalışan repo | GitHub | 0 | 5 | Burak | README + reproducible |
| Web demo (Streamlit) | URL + ekran kaydı | 2 | 2 | Burak | 10 parsel + hata yok |
| PWA | URL | 3 | 4 | Burak | Mobil tarayıcı çalışır |
| Mobil RN V0 | TestFlight / Internal Track | 5 | 5 | Burak | iOS+Android build |
| Sunum (slayt) | .pptx | 2 | 5 | Burak | 15-20 dk + soru |
| Posteri (akademik) | .pdf 1xA0 | 4 | 5 | Burak | Konuya 1 bakışta hâkim |
| Yayın taslağı | .docx | 4 | 5 | Burak | Ulusal kongre / açık erişim dergi |
| Veri sözleşmesi şablonları | .docx | 0 | 3 | Burak + hukuk danışmanı | İmzalanabilir |
| Final video (60 sn) | .mp4 | 4 | 5 | Burak | Demo + ses |

---

## 2. Staj raporu — taslak iskeleti

```
KAPAK
ÖZET (TR + EN)
İÇİNDEKİLER

1.  GİRİŞ
    1.1 Problem ve motivasyon
    1.2 Amaç ve kapsam
    1.3 Raporun yapısı

2.  LİTERATÜR
    2.1 Uydu temelli tarımsal izleme
    2.2 Fenoloji ve hasat tarihi tahmini
    2.3 Türkiye bağlamı ve önceki çalışmalar

3.  YÖNTEM
    3.1 Pilot bölge ve ürün seçimi
    3.2 Veri kaynakları (Sentinel-2/1, meteoroloji, etiket)
    3.3 Ön işleme ve indeksler
    3.4 Modelleme (kural tabanlı + ML)
    3.5 Değerlendirme metrikleri

4.  UYGULAMA
    4.1 Sistem mimarisi
    4.2 ETL hattı
    4.3 Web ve PWA arayüzü
    4.4 Mobil yol haritası

5.  SONUÇLAR
    5.1 Pilot parsel sonuçları
    5.2 Hata analizleri
    5.3 Açıklanabilirlik (SHAP)

6.  TARTIŞMA
    6.1 Sınırlar ve riskler
    6.2 İyileştirme alanları
    6.3 Ticarileşme potansiyeli

7.  SONUÇ ve İLERİDE YAPILACAKLAR

KAYNAKÇA
EKLER
  A. Veri envanter tablosu
  B. Eşik kalibrasyonları
  C. Model deney kayıtları
  D. Kullanıcı görüşme notları
```

**Sayfa hedefleri:** Giriş 4, Lit 6, Yöntem 8, Uygulama 6, Sonuç 4, Tartışma 3, Sonuç 1, Ekler 5+.

---

## 3. Bitirme tezi — taslak iskeleti

(Üniversiteye göre değişebilir; klasik 60-100 sayfa varsayımı.)

```
1.  GİRİŞ
2.  LİTERATÜR TARAMASI
    2.1 Uzaktan algılama
    2.2 Tarımsal fenoloji
    2.3 Hasat tarihi tahmini
    2.4 Türkiye'de uydu tabanlı tarım çalışmaları
3.  KAVRAMSAL ÇERÇEVE
    3.1 Spektral indeksler
    3.2 Fenoloji metrikleri
    3.3 Makine öğrenmesi yaklaşımları
4.  MATERYAL ve YÖNTEM
    4.1 Çalışma alanı
    4.2 Veri seti
    4.3 Yazılım altyapısı
    4.4 Modelleme yaklaşımı
    4.5 Doğrulama yöntemi
5.  BULGULAR
    5.1 Veri keşfi
    5.2 Kural tabanlı sonuçlar
    5.3 ML model sonuçları
    5.4 Karşılaştırma ve hata analizi
6.  TARTIŞMA
7.  SONUÇ ve ÖNERİLER
KAYNAKÇA
EKLER
```

**Bitirme tezi vs. staj raporu farkı:**
- Tez **akademik üslup**, staj raporu **uygulama günlüğü** ağırlıklı.
- Tez **derin literatür**, staj raporu **kısa lit + kapsamlı uygulama**.
- Tez **özgün katkı** beklenir, staj raporu **çalışmayı öğrenme** beklenir.

---

## 4. Sunum (slayt) iskeleti — 18 dakika

| # | Slayt | Süre | Not |
|---|---|---|---|
| 1 | Başlık + isim + tarih | 30 sn | |
| 2 | "Üç cümle problem" | 1 dk | Çiftçi acısı, mevcut açıklık |
| 3 | Vizyon ekranı (mockup) | 1 dk | Telefon görseli |
| 4 | Pilot: buğday + Konya — neden | 2 dk | Eleme tablosu |
| 5 | Veri kaynakları haritası | 1 dk | S2 + S1 + MGM + ÇKS |
| 6 | Mimari diyagramı | 1.5 dk | `04_TEKNIK_MIMARI.md` |
| 7 | Modelleme: kural → ML → DL | 2 dk | Üç kademe |
| 8 | Demo (canlı / kayıt) | 4 dk | Streamlit veya PWA |
| 9 | Sonuçlar: MAE, ±7/14, kapsama | 1.5 dk | Tablo + grafik |
| 10 | Açıklanabilirlik (SHAP) | 1 dk | Bir parselin gerekçesi |
| 11 | Riskler ve sınırlar | 1 dk | Şeffaf |
| 12 | Yol haritası: V2-V3 | 1 dk | Trakya, mısır, mobil |
| 13 | Teşekkür + soru | — | |

**Demo öncesi yedek:** ekran kaydı `.mp4` slaytın içinde gömülü.

---

## 5. Repo / GitHub README iskeleti

```
# HasadHaber — Uydu Görüntüleri ile Hasat Zamanı Tahmini

[badges: ci, license, python, model card]

## TL;DR
Tek cümle proje + ekran görüntüsü.

## Hızlı başlangıç
git clone ...
docker compose up
http://localhost:8000/docs

## Mimari
[link → docs/ARCHITECTURE.md]

## Veri
[link → data/README.md]

## Notebook'lar
01 → ETL
02 → Fenoloji kuralları
03 → ML baseline
04 → XGBoost kalan-gün
05 → Validasyon

## Sonuçlar
| Sürüm | Pilot | MAE | ±7 |
|...|...|...|...|

## Atıf
@thesis{burak2026hasadhaber, ...}

## Lisans
Apache-2.0 (kod) — CC-BY-4.0 (raporlar)
```

---

## 6. Yayın stratejisi

| Yer | Tür | Süre | Hedef faz |
|---|---|---|---|
| Türkiye Tarımsal Uzaktan Algılama Sempozyumu | Bildiri | 1 ay yazım | Faz 4 sonu |
| Türk Tarımsal Bilimler Dergisi | Makale | 3 ay yazım | Faz 5 |
| Remote Sensing (MDPI, açık erişim) | Makale | 3-6 ay (review) | Faz 5+ |
| ArXiv | Önbaskı | 1 hafta | Faz 4 sonu (paralel) |
| GitHub Discussions / Hugging Face | Repo + dataset card | 1 hafta | Faz 4-5 |

---

## 7. Veri / model kartı (model card)

Yayınla birlikte yayınlanacak transparan dosya:

```
Model: rules-v1, xgb-v0.3
Eğitim verisi: 50 parsel × 3 sezon, Çumra-Konya, 2023-2025
Hedef: kalan-gün, sınıf: kışlık buğday
Performans: MAE 6.4 gün (test), ±7 gün isabet 0.71
Sınırlar: pilot dışı bölgelerde test edilmedi
Etik: yalnız tavsiye amaçlı; karar destek
İletişim: [email]
```

---

## 8. Faz × teslimat çapraz tablo

| Teslimat | F0 | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|
| Repo iskeleti | ✅ | | | | | |
| Veri envanteri | ✅ | | | | | |
| ETL notebook | | ✅ | | | | |
| Streamlit demo | | | ✅ | | | |
| FastAPI | | | | ✅ | | |
| PWA | | | | ✅ | ✅ | |
| RF baseline | | | | ✅ | | |
| XGBoost | | | | ✅ | ✅ | |
| Radar füzyonu | | | | | ✅ | |
| Saha doğrulama | | | | | ✅ | |
| Mobil RN V0 | | | | | | ✅ |
| Staj raporu (taslak) | | | ✅ | ✅ | ✅ | |
| Staj raporu (final) | | | | | ✅ | |
| Bitirme tezi (taslak) | | | | ✅ | ✅ | ✅ |
| Bitirme tezi (final) | | | | | | ✅ |
| Sunum slaytları | | | ✅ | | | ✅ |
| Yayın taslağı | | | | | ✅ | ✅ |

---

İlgili: [`03_FAZLAR_VE_DURUMLAR.md`](./03_FAZLAR_VE_DURUMLAR.md) (faz akışı) / [`09_GOREVLER.md`](./09_GOREVLER.md) (görev karşılığı).

---

## 9. Hocaya 2-3 haftalık ara rapor şablonu

Hoca her ara raporda aynı yapıyla aynı yerde aynı bilgiyi bulsun. Bu hem okuma süresini düşürür hem de "ilerleme var mı?" sorusunu net cevaplar.

### 9.1. Şablon

```
# Ara Rapor — Sprint #N — [Tarih aralığı]

## 1. Tek paragraf özet
Bu sprintte X yapıldı, Y blokajıyla karşılaşıldı, Z sonraki sprintte hedeftir.

## 2. Tamamlanan (kabul ölçütü ile)
- T-XXX — kısa açıklama — kabul ölçütü "..."
- ...

## 3. Yapılıyor / yarım kalan
- T-XXX — neden bitmedi, ne kadar kaldı

## 4. Bulgular ve kararlar
- Yeni gözlem 1
- Yeni gözlem 2
- Açık karar (ADR'a girdi mi?)

## 5. Engeller
- Veri/izin/teknik/zaman engelleri

## 6. Metrikler (varsa)
- Pipeline kapsama: %X
- MAE (henüz erkense): N/A
- Gözden geçirilen literatür: N

## 7. Sonraki sprint hedefi
- T-YYY — tahmini bitiş tarihi
- T-ZZZ — tahmini bitiş tarihi

## 8. Hocadan ricalar
- Onay gereken karar
- Tanıtım gereken kişi
- Erişim gereken kaynak

## 9. Eklerin
- Demo URL (varsa)
- Notebook PDF (varsa)
- Veri envanteri güncellemesi
```

### 9.2. İlk rapor taslağı (Sprint 0 — Faz 0 ilk 2 hafta)

```
# Ara Rapor — Sprint 0 — [12 Mayıs – 26 Mayıs 2026]

## 1. Tek paragraf özet
Konya + kışlık buğday pilotu için keşif fazı tamamlandı: literatürden alınan
beş kritik kriter (parsel büyüklüğü, tek ürün baskınlığı, bulutluluk, etiket
erişimi, literatür yoğunluğu) Konya bölgesinde karşılanıyor. İl Tarım
Müdürlüğü ve Çumra Ziraat Odası ile ilk iletişim açıldı; veri talep
e-postaları gönderildi. Repo iskeleti ayağa kaldırıldı, Earth Engine
akademik hesabı aktif. Sonraki sprintte Faz 1 — veri hattı başlıyor.

## 2. Tamamlanan
- T-001 — ADR-001 (Konya+buğday) yazılı imza — kabul "yazılı, hocaya iletildi"
- T-002 — Paydaş iletişim listesi — kabul "5+ kişi/kurum"
- T-003 — Veri talep e-postaları — kabul "3 kuruma gönderildi"
- T-004 — GitHub repo + Apache-2.0 lisans — kabul "CI yeşil"
- T-006 — Veri envanter tablosu ilk sürüm — kabul "9 katman, sahip atandı"

## 3. Yapılıyor
- T-007 — KVKK kısa notu (yarım, %60)

## 4. Bulgular ve kararlar
- Konya'da büyük homojen parsel oranı, Trakya/ayçiçeğine kıyasla net
  şekilde yüksek (sahaya bakmadan parsel veritabanı üzerinden bile gözle
  ayırt edilebiliyor) — ADR-001 desteklenmiş.
- Yerli uydulardan veri çekmek için imece/göktürk açık erişim portallarının
  araştırma erişim koşulları belirsiz; ADR-B-012 ile V1 ana kaynak
  konumundan dışlandı.

## 5. Engeller
- Çumra Ziraat Odası iletişimi — yanıt bekleniyor (3 iş günü).
- KVKK metni için hukuk danışmanı önerisi (henüz alınmadı).

## 6. Metrikler
- Pipeline kapsama: N/A (Faz 1 başlamadı)
- MAE: N/A
- Gözden geçirilen literatür: 12 makale (Sedano 2025, Liu 2025, Mimić 2025,
  Liao 2023, Cyran 2025, Yue 2024, Şimşek 2024 dahil)
- Repo: tek dal, MIT yerine Apache-2.0; CI: lint + nbsmoke yeşil

## 7. Sonraki sprint hedefi
- T-101 — GEE servis hesabı + tek parsel S2 zaman serisi (T-102) — 5 gün
- T-103 — Bulut maskesi entegrasyonu — 3 gün
- T-104 — Çoklu indeks (NDVI/EVI/NDMI/NDRE) — 3 gün
- 10 parsele genişletme — 2 gün
- G1 karar kapısı denemesi

## 8. Hocadan ricalar
- Çumra Ziraat Odası başkanına resmi tanıtım yazısı (bir tek paragraf yeter)
- KVKK ön incelemesi için danışman önerisi
- Türkiye Tarımsal Uzaktan Algılama Sempozyumu çağrı tarihinin teyidi

## 9. Eklerin
- Repo: github.com/.../hasat-zamani
- Veri envanter tablosu: data/README.md
- ADR-001 imzalı: docs/adr/001.md
```

---

## Bu dosyada alınan kararlar
- 18 dakikalık sunum standardı (13 slayt) tüm sprint demo'larında ve final savunmada aynı kalır.
- Staj raporu ve bitirme tezi farkı: rapor uygulama günlüğü, tez akademik yapı + özgün katkı.
- Repo lisansı: Apache-2.0 (kod), CC-BY-4.0 (dokümantasyon).
- Ara rapor şablonu yukarıdaki 9 başlıkta sabittir; 2-3 haftada bir teslim edilir.

## Açık sorular
- Üniversitenin staj raporu formatı .docx şablon zorunluluğu var mı? — Faz 0'da öğren.
- Bitirme tezi danışmanı ile staj danışmanı aynı kişi mi? — Aynıysa rapor entegrasyonu kolaylaşır.
- Yayın stratejisinde önce ulusal sempozyum mu, doğrudan açık erişim dergi mi? — Faz 4 sonu karar.

## Sonraki aksiyonlar
- Faz 0 sonunda yukarıdaki "Sprint 0 ara raporu" hocaya teslim edilir (taslak şu an hazır).
- Her faz sonu G kapısının yeşil yandığı maddeler raporda kanıt olarak eklenir.
