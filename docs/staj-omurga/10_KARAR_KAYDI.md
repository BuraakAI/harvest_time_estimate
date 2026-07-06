# 10 — Karar Kaydı (ADR — Architecture Decision Records)

> **Amaç:** Projedeki her stratejik ve mimari kararın gerekçesini, alternatiflerini ve sonuçlarını yalnız-ekleme bir günlükte tutmak; gelecekteki "neden böyle yapmıştık?" sorusuna kayıt göstermek; jüri/danışman önünde kararları savunulabilir kılmak.
> **Kapsam:** ADR formatı, ADR-001 ile ADR-020 arası karar günlüğü (pilot, dil, framework, DB, harita, mobil, GEE, modelleme yol haritası, lisans, ilçe, dev ortamı, CI, test, hata izleme, repo strateji, auth, dil i18n, veri sürümleme, kullanıcı sözleşmesi), kapatılmış (superseded) ADR bölümü, yeni ADR yazma protokolü.
> **Son güncelleme:** 2026-07-06
>
> Her büyük karar bu dosyaya **yalnız ekleme** olarak yazılır. Eski kararı geri almak için yeni bir ADR yazılır ve eskisi `Superseded` işaretlenir.

ADR formatı: **ID • Başlık • Durum • Bağlam • Karar • Sonuçlar • Alternatifler.**

---

## ADR-001 — Pilot ürün ve bölge: kışlık buğday + Konya Ovası

**Durum:** ✅ Kabul (öneri — Faz 0 sonunda imzalanacak)
**Tarih:** 2026-05-10
**Bağlam:** Türkiye'de pilot için 7'ye yakın ürün/bölge kombinasyonu var. Süre kısıtlı, etiket toplama darboğaz.
**Karar:** İlk pilot kışlık buğday + Konya Ovası (Çumra ilçesi öncelik). İkinci pilot Trakya/ayçiçeği, üçüncü pilot sulu mısır.
**Sonuçlar:**
- Veri kaynakları: ÇKS (Konya), Çumra Ziraat Odası, MGM, Sentinel-2/1.
- Literatür ile uyumlu (Yue 2024, Liao 2023, Şimşek 2024).
- Faz 1-2 düşük risk.
**Alternatifler:** Mısır+Çukurova (yüksek etiket maliyeti — V3); ayçiçeği+Trakya (daha karışık rotasyon — V2).
**Detay:** `02_NEDEN_SONUC.md` Bölüm A.

---

## ADR-002 — Birincil dil: Python (backend), TypeScript (frontend)

**Durum:** ✅ Kabul
**Bağlam:** EO/ML için Python birinci dil; web ürün için TypeScript tip güvenliği gerekli.
**Karar:** Backend Python 3.11; frontend React + TypeScript.
**Sonuçlar:** Tek paketleme (poetry/uv) ve tek lint kurulumu (ruff + mypy + eslint + tsc).
**Alternatifler:** R (EO ekosistemi zayıf), JS (EO server-side için yetersiz), Julia (topluluk küçük).

---

## ADR-003 — Web framework: FastAPI

**Durum:** ✅ Kabul
**Bağlam:** API'nin OpenAPI ile otomatik dokümante olması, Pydantic ile tip güvenli, async olması gerekiyor.
**Karar:** FastAPI.
**Sonuçlar:** `/docs` ve `/redoc` ücretsiz. Pydantic v2 + SQLAlchemy 2.0 modern stack.
**Alternatifler:** Django+DRF (ağır), Flask (modernlik el işi), Node.js (EO ekosistemi Python'da).

---

## ADR-004 — Veri tabanı: PostgreSQL + PostGIS (Supabase hosted)

**Durum:** ✅ Kabul
**Bağlam:** Spatial sorgu (parsel kapsama, alan, mesafe) gerek; auth + storage entegre olsun isteniyor.
**Karar:** Geliştirmede SQLite+Spatialite, prototipte Supabase (Postgres+PostGIS).
**Sonuçlar:** Faz 3'te hızlı kurulum; Faz 5'te kendi Postgres'e taşıma seçeneği saklı.
**Alternatifler:** MongoDB (spatial zayıf), TimescaleDB (V2'de değerlendirilebilir).

---

## ADR-005 — Frontend: V1 Streamlit, V2+ React + Vite

**Durum:** ✅ Kabul
**Bağlam:** V1'de hocaya hızlı demo gerek; V2'de ürünleşme.
**Karar:** Faz 2'de Streamlit (hız), Faz 3+'da React + Vite + TypeScript + Tailwind + shadcn/ui.
**Sonuçlar:** İki farklı arayüz var, ama veri katmanı paylaşılır.
**Alternatifler:** Yalnız React (Faz 2 için yavaş), Vue (ekosistem küçük).

---

## ADR-006 — Harita kütüphanesi: Leaflet

**Durum:** ✅ Kabul
**Karar:** Leaflet + react-leaflet.
**Alternatifler:** Mapbox (lisans/maliyet), MapLibre (V2 değerlendirme), Cesium (3D gereksiz).

---

## ADR-007 — Mobil: V1 PWA, V2 React Native

**Durum:** ✅ Kabul
**Bağlam:** Mağaza onayı staj süresine sığmaz; PWA tarayıcıdan tek tık.
**Karar:** Faz 3-4 PWA, Faz 5 React Native V0.
**Sonuçlar:** İki kod tabanı yerine tek (PWA), sonra RN'ye geçiş.
**Alternatifler:** Flutter (Dart ek yük), native Kotlin/Swift (iki ekip).

---

## ADR-008 — Uydu veri hesaplama: GEE (akademik) + sonradan yerel pipeline

**Durum:** ✅ Kabul
**Bağlam:** GEE noncommercial ücretsiz, ticarileşmede ücretli; vendor lock-in riski.
**Karar:** Faz 0-3 GEE üzerinden; Faz 4'te yerel Python pipeline (rasterio + xarray + dask) prototip; Faz 5'te ticari geçişte tamamen yerel.
**Sonuçlar:** Erken hız + ileride bağımsızlık. Hibrit kabul edilir.
**Alternatifler:** Tamamen yerel başlangıç (yavaş), AWS Open Data only (manuel ETL).

---

## ADR-009 — Modelleme yol haritası: kural → RF → XGBoost → DL

**Durum:** ✅ Kabul
**Bağlam:** Etiket darboğazı; literatürde kural tabanlı yöntem (Sedano 2025) etiketsiz çalışıyor.
**Karar:** V1 kural tabanlı, V2 RF baseline, V3 XGBoost, V4 LSTM/TFT.
**Sonuçlar:** Etiket sayısına göre artan karmaşıklık.
**Alternatifler:** Doğrudan LSTM (etiket yetersiz), yalnız ARIMA (temsil zayıf).

---

## ADR-010 — Lisans: Apache-2.0 (kod), CC-BY-4.0 (dokümantasyon)

**Durum:** ✅ Kabul (öneri — Faz 0)
**Karar:** Kod Apache-2.0 (atıf + patent koruması), dokümantasyon ve raporlar CC-BY-4.0.
**Sonuçlar:** Akademik ve ticari kullanım açık; ileride çatallanma kontrol edilebilir.
**Alternatifler:** MIT (patent koruması yok), GPL (ticari iş ortaklığı zorlaşır).

---

## ADR-011 — Pilot içinde ilçe seçimi: Çumra (Konya)

**Durum:** 🟡 Öneri (Faz 0'da onaylanacak)
**Bağlam:** Konya çok büyük; pilot için 1 ilçe seçilmeli.
**Karar:** Çumra ilçesi (büyük homojen parseller, sulu+kuru karışımı az, ziraat odası iletişimi olası).
**Sonuçlar:** 30-100 parsel hedefi gerçekçi. Genişleme: Karatay, Cihanbeyli.
**Alternatifler:** Karatay (daha şehirsel), Cihanbeyli (daha geniş ama uzak).

---

## ADR-012 — Geliştirme ortamı: Docker compose + uv

**Durum:** ✅ Kabul
**Karar:** Docker compose lokal stack için; Python ortamı `uv` ile (hızlı, lock).
**Sonuçlar:** Reproducibility yüksek; CI/CD basit.
**Alternatifler:** poetry (yavaş), pipenv (eski), conda (büyük).

---

## ADR-013 — CI/CD: GitHub Actions

**Durum:** ✅ Kabul
**Karar:** Lint + test + build her PR'da; main'e merge sonrası staging deploy.
**Alternatifler:** GitLab CI (kullanılmıyor), CircleCI (free tier yetersiz).

---

## ADR-014 — Test çerçevesi

**Durum:** ✅ Kabul
**Karar:** Backend pytest, frontend vitest, E2E Playwright, notebook nbsmoke.
**Alternatifler:** unittest (eski), Cypress (Playwright tercih edildi).

---

## ADR-015 — Hata izleme: Sentry

**Durum:** ✅ Kabul (Faz 3+)
**Karar:** Sentry free tier; PII filtresi aktif.
**Alternatifler:** Rollbar, custom log analiz.

---

## ADR-016 — Repo strateji: monorepo

**Durum:** ✅ Kabul
**Karar:** Tek repo: `backend/`, `frontend/`, `notebooks/`, `ml/`, `ops/`, `docs/`.
**Sonuçlar:** Kod gezinmesi kolay, sürüm tutarlılığı garanti.
**Alternatifler:** Polyrepo (3 repo) — koordinasyon yükü artar.

---

## ADR-017 — Kullanıcı kimliği: e-posta + parola → Supabase Auth

**Durum:** 🟡 Öneri
**Karar:** Faz 3'te basit JWT; Faz 4'te Supabase Auth.
**Alternatifler:** Auth0 (maliyetli), Firebase Auth (Google bağı).

---

## ADR-018 — Çoklu dil: TR öncelik, EN ikinci

**Durum:** ✅ Kabul
**Karar:** UI i18n: tr-TR varsayılan, en-US opsiyonel. Backend hata mesajları İngilizce, kullanıcı mesajları çift dilli.

---

## ADR-019 — Veri sürümleme

**Durum:** 🟡 Faz 1'de karar
**Aday:** DVC (data version control) ile S3 backend.
**Alternatif:** git-lfs (büyük dosyalarda zayıf).

---

## ADR-020 — Lisanslama formu (kullanıcı)

**Durum:** 🟡 Faz 3'te yazılacak
**Bağlam:** Kullanıcı parsel verisini sisteme yüklerken hangi onayı verir?
**Karar şablonu:** "Tahmin amaçlı kullanım, anonim toplulaştırma izinli, satış yasak, geri alma hakkı 30 gün."

---

---

## Brief uyumlu konsolide ADR'lar (ADR-010 → ADR-015)

`revize.md` brief'i altı tematik karara ad-hoc isim verilmesini istiyor. Aşağıdaki ADR'lar yukarıdaki mevcut kararlar ile **çakışmaz**; mevcut detayların özet/konsolide karşılığıdır ve hocaya tek paragrafta savunulabilir formdadır.

### ADR-B-010 — MVP başlangıç hedefi: Konya + kışlık buğday
**Durum:** ✅ Kabul (ADR-001 ve ADR-011 ile uyumlu)
**Karar:** İlk MVP yalnız kışlık buğdayda ve Konya Ovası'nda çalıştırılır. Diğer ürün/bölgeler V2+'ya bırakılır.
**Gerekçe özeti:** Tek ürün/tek bölge tek modeli ürün ve coğrafya bazlı varyanstan korur (`02_NEDEN_SONUC.md` A.0).
**Sonuç:** Yalnız bir crop_code ve bir region_code grubu için validasyon raporlanır. Pilot dışı bölgelerde tahmin "guard rail" mesajıyla kapatılır.

### ADR-B-011 — Ana veri kaynağı: Sentinel-2; destek kaynağı: Sentinel-1
**Durum:** ✅ Kabul
**Karar:** Optik fenoloji omurgası Sentinel-2; bulutlu dönem ve hasat olayı sigortası Sentinel-1.
**Gerekçe özeti:** Sentinel-2 5 günlük tekrar + 13 bant ile fenoloji için literatür standardı; Sentinel-1 buluttan bağımsız ve hasat olayını VH düşüşüyle yakalar (Mimić 2025, Liao 2023).
**Sonuç:** Her iki katman zorunlu; eksikse `quality_score` düşer.

### ADR-B-012 — Türkiye uyduları V1 ana kaynak değildir
**Durum:** ✅ Kabul
**Karar:** RASAT, GÖKTÜRK-1/2, İMECE V1 omurgasında yer almaz; doğrulama/yüksek çözünürlüklü örnekleme/yerli görünürlük katkısı olarak V2/V3'te eklenir.
**Gerekçe özeti:** Açık veri sürekliliği, fenoloji-uygun bant zenginliği ve araştırmacı dostu API ekosistemi Sentinel/Landsat seviyesinde değil; brief 5. kuralla bu sınır açıkça çizilmiştir.
**Sonuç:** TÜRKSAT 6A bir EO uydusu olmadığı için kapsamdan tamamen dışlanır.

### ADR-B-013 — İlk model kural tabanlıdır; ML ikinci aşamadır
**Durum:** ✅ Kabul (ADR-009 ile uyumlu)
**Karar:** Faz 2 V1 kural tabanlı çekirdek (Sedano 2025 stilinde eğitim verisi gerektirmeyen yaklaşım). Faz 3'ten itibaren RF→XGBoost ile kalan-gün regresyonu.
**Gerekçe özeti:** Etiket darboğazı varken kural tabanlı yöntem demo edilebilirliği garanti altına alır.
**Sonuç:** Faz 2 demo, etiket toplanmadan da raporlanabilir.

### ADR-B-014 — İlk uygulama PWA/web demo; native mobil sonraki aşama
**Durum:** ✅ Kabul (ADR-007 ile uyumlu)
**Karar:** V1'de tek kod tabanlı PWA; Faz 5'te React Native V0.
**Gerekçe özeti:** Mağaza onayı staj süresine sığmaz; PWA tarayıcıdan tek tık çalışır.
**Sonuç:** App Store/Play Store yayını V1 hedefi değildir.

### ADR-B-015 — Etiket erişimi olmadan ticari doğruluk iddiası yapılmaz
**Durum:** ✅ Kabul
**Karar:** Sahada doğrulanmış hasat etiketi olmadan kullanıcıya/yatırımcıya kesin "MAE x gün" iddiası iletilmez. Tahminler `confidence` ve "kalibre edilmemiş" işareti ile sunulur.
**Gerekçe özeti:** Etiket gürültüsü tahmin sapmasını maskeler; bilimsel ve etik açıdan zorunlu sınır (Jiang 2024).
**Sonuç:** İlk gerçek MAE raporu Faz 4 sonu (≥30 saha etiketli) sonrası.

### ADR-B-016 — ETL notebook yerine test edilebilir `core/` modülleri; parquet yerine CSV cache; s2cloudless yerine SCL maskesi
**Durum:** ✅ Kabul (fiili durum kaydı)
**Tarih:** 2026-07-06
**Bağlam:** Plan (04_TEKNIK_MIMARI, 09_GOREVLER T-102/T-108/T-103) ETL'yi Jupyter notebook + parquet + s2cloudless olarak öngörüyordu. Prototip yazılırken üç sapma yapıldı.
**Karar:**
1. ETL, notebook yerine `hasat-zamani/core/datasource.py` içinde **modül** olarak yazıldı; birim testle korunuyor (`tests/test_datasource.py`).
2. Sezon önbelleği parquet yerine **CSV** (`data/cache/gee_{parsel}_{sezon}.csv`) — küçük veri hacminde ek bağımlılık (pyarrow) gerekmez.
3. Bulut maskesi s2cloudless yerine S2'nin kendi **SCL bandı** (sınıflar 0,1,3,8,9,10,11) — ek koleksiyon join'i olmadan yeterli kalite.
**Sonuç:** Faz 1 görevleri (T-101–T-110) bu biçimde kapandı; notebook'lar yalnız keşif/rapor görseli gerekirse eklenir. Veri büyürse (çok sezon × çok bölge) parquet'e geçiş yeni ADR ister.
**Alternatifler:** Notebook-önce yaklaşım (tekrar üretilebilirliği zayıf, test edilemez); s2cloudless (daha hassas ama Faz 2 için gereksiz karmaşıklık).

### ADR-B-017 — Faz 2 pilot parselleri OSM'den alındı; ekim doğrulaması zorunlu bulundu
**Durum:** ✅ Kabul (T-207 bulgusu)
**Tarih:** 2026-07-06
**Bağlam:** T-207 doğrulama tablosu gerçek Sentinel-2 verisiyle üretildiğinde, OSM `landuse=farmland` üzerinden seçilen 10 Çumra parselinin 2026 sezonunda kışlık buğday fenolojisi GÖSTERMEDİĞİ görüldü (NDVI hasat penceresinde hâlâ yükseliyor → yazlık ürün olasılığı).
**Karar:** OSM parselleri yalnız **akış doğrulaması** için kullanılır; doğruluk çalışması ancak ÇKS kaydı / üretici beyanıyla **ekimi doğrulanmış** buğday parselleriyle yapılır. T-002/T-003 veri talebine "ekim beyanı" alanı eklendi.
**Sonuç:** `18_T207_DOGRULAMA_TABLOSU.md` bu bulguyu kayıt altına alır; motor ve akış hazır, doğru parsel listesi insan-tarafı bekleyen iştir. Bu bulgu 07_RISKLER R-02 (veri riski) örneği olarak rapora girer.
**Alternatifler:** ESA WorldCereal / Dynamic World gibi ürün sınıflandırma katmanıyla otomatik buğday filtresi (Faz 4'te değerlendirilebilir).

---

## Kapatılmış / superseded ADR'lar

(şu an boş)

---

## Yeni ADR nasıl yazılır?

```
1. Sıra ID al (önceki + 1)
2. Tek cümlede başlık
3. Durum: 🟡 Taslak → ✅ Kabul → ❌ Red
4. Bağlam: 2-3 cümle
5. Karar: tek paragraf
6. Sonuçlar: nelerin değişeceği
7. Alternatifler: ne elendi, neden
8. İlgili dosyalara link
```

---

İlgili: [`02_NEDEN_SONUC.md`](./02_NEDEN_SONUC.md) (gerekçe) / [`04_TEKNIK_MIMARI.md`](./04_TEKNIK_MIMARI.md) (uygulama).

---

## Bu dosyada alınan kararlar
- ADR formatı: ID • Başlık • Durum • Bağlam • Karar • Sonuçlar • Alternatifler. Tüm ADR'lar bu formata uyar.
- Yalnız ekleme ilkesi: eski ADR silinmez; geri çekilirse `Superseded` etiketi ile yeni ADR'a referans verir.
- ADR'lar iki seride yaşar: detay (ADR-001 → ADR-020) ve brief uyumlu konsolide (ADR-B-010 → ADR-B-015). İkisi birbirini tamamlar.

## Açık sorular
- ADR'lara dijital imza/blokzincir benzeri bir denetim izi eklenmeli mi? (Tez kapsamı dışı.)
- Hocadan gelen sözlü kararlar buraya nasıl alınmalı? — Önerim: yazılı özet + ADR'a refere etme.

## Sonraki aksiyonlar
- Faz 0 sonunda "🟡 Öneri" ADR'lar (ADR-001, ADR-011, ADR-017, ADR-019, ADR-020) imzaya açılır.
- Her büyük PR/karar toplantısı sonrası en geç 24 saat içinde yeni ADR yazılır.
