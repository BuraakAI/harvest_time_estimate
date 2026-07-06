# Staj Omurgası — Uydu Görüntüleri ile Hasat Zamanı Tahmini

> **Amaç:** Stajın akademik, teknik, ürünsel ve operasyonel tüm boyutlarını birbirine bağlı, yaşayan bir bilgi tabanında toplamak; "neden böyle yapıyoruz?" ve "şu an ne yapacağım?" sorularına tek tıkla cevap vermek.
> **Kapsam:** İndeks, dosya rolleri, kullanım akışı, kabul ettiğimiz temel varsayımlar, hızlı yönlendirme tabloları, versiyonlama disiplini.
> **Tek cümlede proje:** Uydu zaman serisinden bir tarlanın fenolojik olgunluğunu okuyup parsel bazında "hasada kaç gün kaldı?" sorusuna ±gün cinsinden cevap üreten ve bunu mobil-uyumlu prototip arayüze taşıyan karar destek sistemi.
> **Son güncelleme:** 2026-05-10

Bu klasör (`staj-omurga/`) stajın **kalıcı beynidir**. Her dosya tek bir konuya odaklı, birbirine bağlı ve yaşayan dokümandır. Yeni bilgi geldikçe ilgili dosya güncellenir; yeni karar alındıkça `10_KARAR_KAYDI.md`'ye satır eklenir; yeni iş çıktıkça `09_GOREVLER.md` güncellenir.

## Kullanım sırası (yeni okuyan için ideal akış)

### A) Strateji ve gerekçe katmanı
1. **`01_VIZYON.md`** — Vizyon (4 zaman ufku), problem, 5N1K, başarı ölçütleri
2. **`02_NEDEN_SONUC.md`** — Pilot ve tech stack seçimlerinin bilimsel gerekçesi (kritik okuma)
3. **`03_FAZLAR_VE_DURUMLAR.md`** — Faz 0–5, durum sistemi, karar kapıları, sprint disiplini

### B) Teknik ve bilim katmanı
4. **`04_TEKNIK_MIMARI.md`** — Akademik MVP ve ticari ölçek mimarisi (iki seviye)
5. **`05_VERI_VE_MODELLEME.md`** — Problem formları, etiket stratejisi, modelleme, açıklanabilirlik

### C) Ürün ve operasyon katmanı
6. **`06_URUN_VE_TICARILESTIRME.md`** — Müşteri segmentleri, ekosistem girişi, B2C/B2B/B2G, iş modeli
7. **`07_RISKLER_VE_KALITE.md`** — Risk kaydı, kalite kapıları, test ve etik
8. **`08_TESLIMATLAR.md`** — Staj raporu + bitirme tezi + kod + demo + sunum + yayın matrisi

### D) Yaşayan operasyon katmanı
9. **`09_GOREVLER.md`** — Yaşayan kanban (sprint, WIP limiti, görev kayıtları)
10. **`10_KARAR_KAYDI.md`** — Mimari/stratejik kararların ADR-stili kaydı
11. **`11_GLOSSARY.md`** — Terim sözlüğü (NDVI, fenoloji, S1/S2, HLS, ÇKS, KVKK…)

### E) Akademik ve rekabet katmanı
12. **`12_LITERATUR_TARAMASI.md`** — Akademik literatür: anahtar makale tablosu, farklılaşma, kaynakça
13. **`13_UYDU_UYGUNLUK_MATRISI.md`** — Açık + ticari + Türkiye uyduları puanlı matris
14. **`14_REKABET_VE_MEVCUT_SISTEMLER.md`** — "Yapan var mı?" — dürüst rekabet matrisi ve pozisyonlama
15. **`15_MALIYET_VE_IS_PLANI.md`** — MVP/POC/ürünleşme/ticari maliyet aralıkları + iş modeli

### F) Hocaya teslim katmanı
16. **`16_5N1K_RAPOR.md`** — **Tek pdf çıktı** — hocaya/jüriye bırakılan ana rapor
17. **`17_HOCAYA_SUNUM_STRATEJISI.md`** — İlk görüşme akışı, ne anlat / ne anlatma, onay listesi, cep cevapları
18. **`18_T207_DOGRULAMA_TABLOSU.md`** — Faz 2 kapı çıktısı: 10 parsel gerçek Sentinel-2 doğrulama tablosu (T-207; `hasat-zamani/ml/validate_t207.py` üretir)

## Dosya rolleri ve sahiplik

| Dosya | Rol | Güncelleme tetikleyicisi | Sahip |
|---|---|---|---|
| `00_README.md` | İndeks ve gezinme | Dosya yapısı değişirse | Burak |
| `01_VIZYON.md` | Kuzey yıldızı (4 zaman ufku) | Sezon başı / büyük strateji değişimi | Burak |
| `02_NEDEN_SONUC.md` | Pilot + stack için bilimsel gerekçe | Pilot/stack kararı revize edilirse | Burak |
| `03_FAZLAR_VE_DURUMLAR.md` | Süreç + sprint çerçevesi | Yeni faza geçince, sprint sonunda | Burak |
| `04_TEKNIK_MIMARI.md` | Akademik + ticari sistem mimarisi | Mimari karar / ADR | Burak |
| `05_VERI_VE_MODELLEME.md` | Bilim defteri (problem + veri + model) | Haftalık (deney sonrası) | Burak |
| `06_URUN_VE_TICARILESTIRME.md` | Müşteri + iş modeli | Ayda bir + müşteri görüşmesi sonrası | Burak |
| `07_RISKLER_VE_KALITE.md` | Risk + QA + etik defter | Yeni risk / faz sonu / olay sonrası | Burak |
| `08_TESLIMATLAR.md` | Çıktı kontrol listesi + ara rapor şablonu | Faz sonu / sprint sonu | Burak |
| `09_GOREVLER.md` | Yaşayan kanban + 14/30/90 gün planı | Günlük | Burak |
| `10_KARAR_KAYDI.md` | ADR — yalnız ekleme | Her büyük karar | Burak |
| `11_GLOSSARY.md` | Terim sözlüğü | Yeni terim girdikçe | Burak |
| `12_LITERATUR_TARAMASI.md` | Akademik literatür defteri | Yeni makale / DOI doğrulama | Burak |
| `13_UYDU_UYGUNLUK_MATRISI.md` | Uydu seçim matrisi | Uydu envanteri değişirse | Burak |
| `14_REKABET_VE_MEVCUT_SISTEMLER.md` | Rekabet ve pozisyonlama | Yeni oyuncu / pazar değişimi | Burak |
| `15_MALIYET_VE_IS_PLANI.md` | Maliyet + iş modeli aralıkları | Çeyreklik / pilot kullanıcı sonrası | Burak |
| `16_5N1K_RAPOR.md` | Hocaya tek pdf çıktı | Faz sonu / büyük revizyon | Burak |
| `17_HOCAYA_SUNUM_STRATEJISI.md` | Görüşme protokolü + cep cevapları | Hoca toplantısı öncesi | Burak |

## Temel kabuller (bu omurganın üzerine kurulduğu varsayımlar)

- **Süre esnek**, bu yüzden plan **6 hafta / 3 ay / 6 ay / 12 ay** ölçeklerine çoklu açıdan uyacak biçimde modüler tasarlandı.
- **Pilot adayı:** kışlık buğday + Konya Ovası (gerekçesi `02_NEDEN_SONUC.md` içinde tam zincir olarak verildi). Karar kapısı `Faz 0 sonu` olarak işaretlendi — alternatif kabul edilebilir.
- **Tech stack:** Python + Google Earth Engine (akademik) + FastAPI + PWA (React + Leaflet) + Supabase/Postgres. Mobil için ilk fazda **Progressive Web App**, ticari dikeyde **React Native / Flutter**. Detaylı gerekçe `02_NEDEN_SONUC.md` ve `04_TEKNIK_MIMARI.md` içinde.
- **Çıktı paketi:** çalışan prototip (web + PWA) + repo + staj raporu + bitirme tezi taslağı + sunum + (opsiyonel) makale.

## "Nereden başlamalıyım?" hızlı yönlendirme

| Senaryo | İlk açacağın dosya |
|---|---|
| Konuyu yeni öğreniyorum | `01_VIZYON.md` |
| Niye buğday + Konya seçildi anlamadım | `02_NEDEN_SONUC.md` |
| Bu hafta ne yapacağım? | `09_GOREVLER.md` |
| Hangi kütüphane / ortam? | `04_TEKNIK_MIMARI.md` |
| Bana NDVI ne demek lazım? | `11_GLOSSARY.md` |
| Hocam "neden Sentinel-2?" diye soracak | `02_NEDEN_SONUC.md` + `10_KARAR_KAYDI.md` |
| Hocaya yarın toplantım var, ne diyeceğim? | `17_HOCAYA_SUNUM_STRATEJISI.md` |
| Hocaya bir tek dosya verebilsem hangisi? | `16_5N1K_RAPOR.md` |
| "Bunu yapan var mı?" sorusuna nasıl cevap vereyim? | `14_REKABET_VE_MEVCUT_SISTEMLER.md` |
| Hangi makale, kim, hangi yıl? | `12_LITERATUR_TARAMASI.md` |
| Hangi uyduyu MVP'ye koyalım? | `13_UYDU_UYGUNLUK_MATRISI.md` |
| Maliyet ne kadar tutar? | `15_MALIYET_VE_IS_PLANI.md` |
| Staj raporunda hangi başlık ne kadar yer kaplar? | `08_TESLIMATLAR.md` |
| Ara rapor şablonu nerede? | `08_TESLIMATLAR.md` Bölüm 9 |
| Ürün ne satacak? | `06_URUN_VE_TICARILESTIRME.md` |
| Bu proje nerede başarısız olur? | `07_RISKLER_VE_KALITE.md` Bölüm 10 |

## Versiyonlama

Her dosyanın tepesinde son güncelleme tarihi tutulur. Büyük revizyon olunca:
- `10_KARAR_KAYDI.md`'ye yeni ADR satırı eklenir.
- Etkilenen dosyaların tepesindeki tarih güncellenir.

---

## Bu dosyada alınan kararlar
- Tüm omurga 17 dosya altında, 6 katmana ayrılır: (A) strateji-gerekçe, (B) teknik-bilim, (C) ürün-operasyon, (D) yaşayan operasyon, (E) akademik-rekabet, (F) hocaya teslim.
- Hocaya tek belge olarak teslim edilen dosya `16_5N1K_RAPOR.md`'tir; tek başına okunabilir tutulur.
- İlk hoca toplantısı için "ne anlat / ne anlatma" protokolü `17_HOCAYA_SUNUM_STRATEJISI.md`'tedir; toplantı öncesi okunur.
- Her dosyanın sonunda **Bu dosyada alınan kararlar / Açık sorular / Sonraki aksiyonlar** üçlüsü standarttır.

## Açık sorular
- Kullanıcı arayüzünde gerekecek bir "Help / Sözlük" linki için `11_GLOSSARY.md`'nin web sürümü gerekir mi? — Faz 3'te değerlendirilecek.
- Repo `docs/` altında bu omurga dosyaları "live wiki" olarak yayımlansın mı (MkDocs / Docusaurus)? — Faz 3'te.
- Hoca toplantısı sonrası bu README "yeni okuyana onay verilmiş kuzey yıldızı" olarak güncellenir mi?

## Sonraki aksiyonlar
- Faz 0 sonu: hoca onayıyla `01_VIZYON.md` "Final v0.1" işaretlenir; gerekirse README de versiyonlanır.
- Her büyük revizyon sonrası README'nin "Kullanım sırası" tablosunu güncel tut.
- Yeni dosya eklenirse README'ye katman ataması, dosya rolleri tablosu, hızlı yönlendirme tablosu güncellenir.

---
*Son güncelleme: 2026-05-10*

[[01_VIZYON]][[02_NEDEN_SONUC]][[03_FAZLAR_VE_DURUMLAR]][[04_TEKNIK_MIMARI]]
[[05_VERI_VE_MODELLEME]]
[[06_URUN_VE_TICARILESTIRME]]
[[07_RISKLER_VE_KALITE]]
[[08_TESLIMATLAR]]
[[09_GOREVLER]]
[[10_KARAR_KAYDI]]
[[11_GLOSSARY]]
[[12_LITERATUR_TARAMASI]]
[[13_UYDU_UYGUNLUK_MATRISI]]
[[14_REKABET_VE_MEVCUT_SISTEMLER]]
[[15_MALIYET_VE_IS_PLANI]]
[[16_5N1K_RAPOR]]
[[17_HOCAYA_SUNUM_STRATEJISI]]
