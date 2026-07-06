# 07 — Risk Kaydı, Kalite Kapıları, Test ve Etik

> **Amaç:** Akademik ve ticari ölçekte projenin sürdürülebilirliğini tehdit eden riskleri sürekli görünür kılmak; her fazın "geçti / kaldı" kararını ölçülebilir kapılara bağlamak; kullanıcıya, veriye ve kuruma karşı etik sorumlulukları yazılı sözleşme haline getirmek.
> **Kapsam:** 17 maddelik yaşayan risk kaydı (etki × olasılık skoru), risk × faz ısı haritası, kalite kapıları G0–G5 için pratik kontrol komutları, veri kalitesi kontrol listesi, test piramidi, sürüm yönetimi (SemVer), olay (incident) müdahale matrisi, etik prensipleri ve kullanıcı haklarının operasyonel karşılığı.
> **Son güncelleme:** 2026-05-10

---

## 1. Risk kaydı (yaşayan tablo)

Her risk **etki × olasılık** ile derecelendirilir; mitigasyon ve sahip atanır.

| ID | Risk | Etki (1-5) | Olasılık (1-5) | Skor | Faz | Mitigasyon | Sahip |
|---|---|---|---|---|---|---|---|
| R-01 | Veri/etiket erişim izni gecikir veya alınamaz | 5 | 3 | 15 | 0-1 | Faz 0'da paralel başlat: bakanlık + il müd. + kooperatif. Yedek: kural tabanlı + sentetik etiket | Burak |
| R-02 | Sentinel-2 bulutluluk pilot bölgede beklenmedik yüksek | 4 | 3 | 12 | 2-3 | S1 radar entegrasyonu Faz 4'te kesin; kapsama metriği takip | Burak |
| R-03 | Hasat tarihi etiketleri tutarsız / düşük kaliteli | 4 | 4 | 16 | 3-4 | Çapraz doğrulama (kooperatif + üretici), `confidence` alanı, eğitim örnek ağırlığı | Burak |
| R-04 | Model overfit (az parsel, çok özellik) | 4 | 3 | 12 | 3 | GroupKFold (parsel id), regularization, en az 30 parsel kuralı | Burak |
| R-05 | GEE kotası dolar / akademik plan biter | 3 | 2 | 6 | 3-5 | Yerel Python pipeline'a taşıma planı (Faz 4); önbellek katmanı | Burak |
| R-06 | Streamlit demo sunum günü patlar | 5 | 2 | 10 | 2-3 | Offline paket: yerel notebook + ekran kaydı yedek | Burak |
| R-07 | Kapsam kayması (mısır + ayçiçeği + verim hepsi V1'e) | 4 | 4 | 16 | 2-4 | Faz başında backlog dondurma; yeni istek `Backlog → V2` | Burak |
| R-08 | Tek kişi tükenmişlik / hastalık | 5 | 3 | 15 | hepsi | Süre ölçeklemesi, dokümantasyon disiplini, faz sonu mola | Burak |
| R-09 | KVKK / veri paylaşım hatası | 5 | 2 | 10 | 3-5 | Faz 3'te yazılı politika; PII anonim; sözleşme şablonu | Burak |
| R-10 | Mobil store onayı gecikir | 3 | 4 | 12 | 5 | PWA önce, native sonra; TestFlight Internal | Burak |
| R-11 | Sahaya çıkamamak (uzaklık/iklim/zaman) | 4 | 3 | 12 | 3-4 | Yerel ortakla mobil saha formu kullanımı; uzaktan onay | Burak |
| R-12 | Pilot dışı bölgede model çökmesi | 4 | 4 | 16 | 4 | Modelin "guard rails" içinde çalışması — pilot dışı dış kabul | Burak |
| R-13 | Eski Sentinel-2 sahnelerinde kalibrasyon farkı | 2 | 3 | 6 | 1 | Yalnız L2A SR; uydunun A/B harmonizasyonu | Burak |
| R-14 | Yerli uydu (GÖKTÜRK/İMECE) erişim belirsizliği | 3 | 4 | 12 | 4-5 | İlk omurgayı açık veride kur; yerli veri bonus | Burak |
| R-15 | Hocanın yön değiştirme isteği | 4 | 2 | 8 | hepsi | ADR ile kararları belgele; haftalık kısa demo | Burak |
| R-16 | Repo'da gizli anahtar sızması | 5 | 2 | 10 | 0-3 | Pre-commit (gitleaks), .env şablonu, secret scanning | Burak |
| R-17 | Kullanıcı geri bildirimi olmadan ürün yapımı | 4 | 4 | 16 | 3-5 | Faz 3 sonu en az 3 kullanıcı görüşmesi | Burak |

### Risk yönetim ritmi

- **Haftalık:** R skoru ≥ 12 olanlar gözden geçirilir.
- **Faz sonu:** Tüm risk kaydı revize edilir.
- **Yeni risk:** Tabloya eklenir; ilgili `09_GOREVLER.md` mitigasyon görevi açılır.

---

## 2. Risk × faz ısı haritası

| Faz | En kritik 3 risk |
|---|---|
| 0 — Keşif | R-01, R-15, R-16 |
| 1 — Veri hattı | R-02, R-13, R-05 |
| 2 — MVP-V1 | R-06, R-07, R-04 |
| 3 — MVP-V2 | R-03, R-09, R-17 |
| 4 — Derinleşme | R-12, R-11, R-02 |
| 5 — Ticarileşme | R-08, R-10, R-14 |

---

## 3. Kalite kapıları (gates) — özet

`03_FAZLAR_VE_DURUMLAR.md` Bölüm 5'in üst metni; burası operasyonel kontrol listeleri.

### G2 (Faz 2 → 3) — pratik kontrol

```bash
# repo/scripts/check_g2.sh
pytest backend/  -q                       # API smoke
streamlit run app.py --server.headless 1  # demo açılış
nbsmoke run notebooks/02_phenology_rules.ipynb
python ml/evaluate.py --model rules-v1 --split test  # MAE rapor
```

Çıktı: tüm yeşil + manuel onay (5 dk gözden geçirme).

### G3 (Faz 3 → 4) — pratik kontrol

```bash
docker compose up -d
curl http://localhost:8000/health         # 200
pytest backend/ ml/ -q                    # tüm testler
playwright test                            # E2E parsel akışı
mlflow ui                                  # son 3 deney görünür
```

---

## 4. Veri kalitesi kontrol listesi (her sezon)

- [ ] Parsel poligonları geçerli (`ST_IsValid`)
- [ ] Parsel alanları 0.5–1000 ha aralığında (anomali yakala)
- [ ] Ürün etiketi yalnız izinli sözlükten (`crop_code IN (...)`)
- [ ] Sentinel-2 son 30 gün ≥ 4 bulutsuz gözlem
- [ ] Bulut yüzdesi parselin %50+'sını kapatıyorsa S1'e düş
- [ ] Aynı parsele aynı sezon birden fazla etiket yok
- [ ] Etiketteki alan sapması > %20 → işaretle
- [ ] Meteoroloji eksik tarih oranı < %5
- [ ] Region_code beyaz listede
- [ ] Tahmin sonuçlarında `confidence` boş değil

---

## 5. Test piramidi

```
        ┌──────────────┐
        │     E2E      │   az, kritik akışlar (parsel ekle → tahmin gör)
        ├──────────────┤
        │ Entegrasyon  │   API + DB + GEE mock (orta sayı)
        ├──────────────┤
        │    Birim     │   yoğun (services/, models/)
        ├──────────────┤
        │ Statik analiz│   ruff, mypy, eslint, tsc (en geniş ağ)
        └──────────────┘
```

| Katman | Hedef kapsama | Ne test eder |
|---|---|---|
| Statik | %100 dosya | Hata sınıfları sızdırmasın |
| Birim | ≥ %70 satır | İndeks fonksiyonları, kural mantığı, smoothing |
| Entegrasyon | en kritik 10 senaryo | API → DB, GEE mock |
| ML regresyon | sabit seed test | "Aynı veride MAE değişmesin" |
| E2E | en kritik 3 akış | Parsel ekle → tahmin |

---

## 6. Sürüm yönetimi (versioning)

`vMAJOR.MINOR.PATCH` (SemVer)

- `0.1.0` Faz 1 — ETL hattı çalışıyor
- `0.2.0` Faz 2 — Streamlit demo
- `0.3.0` Faz 3 — FastAPI + PWA + RF
- `0.4.0` Faz 3 sonu — XGBoost
- `0.5.0` Faz 4 — Radar füzyonu + 2. pilot
- `0.9.0` Faz 5 başı — Mobil V0
- `1.0.0` Faz 5 sonu — Tez savunması yapıldı, ilk gerçek kullanıcı

Her sürümde:
- Changelog güncellenir (`CHANGELOG.md`)
- Tag atılır
- Eğer model değişti: `model_runs.id` eski sürümle uyum testi

---

## 7. Olay (incident) müdahale

| Senaryo | İlk eylem | Kim | İletişim |
|---|---|---|---|
| Demo sunum öncesi API down | Yerel Streamlit yedeğine geç | Burak | Hocaya 5 dk önce haber |
| GEE kota aşıldı | Önbellekten servis et | Burak | İçinde kalır |
| DB veri kaybı | Supabase point-in-time restore | Burak | Kullanıcıya yazılı bildirim |
| Modeller hatalı tahmin (anomali) | "Düşük güven" modu otomatik | Burak | Sonraki sürümde düzelt |
| KVKK ihlali şüphesi | Aktif servisi durdur, log al | Burak | Hocaya + kuruma bildirim |

---

## 8. Etik prensipleri ve kullanıcı hakları

### 8.1. Çekirdek prensipler
- Kullanıcı onayı olmadan parsel verisi paylaşılmaz.
- Tahminler **karar değil tavsiye**dir; arayüzde her zaman güven skoru ve hata aralığı vardır.
- Yanılma payı (MAE, ±gün) ürün ekranında "küçük yıldız" değil, ana paneldedir.
- Veri sahipliği kullanıcıya aittir; istek üzerine 30 gün içinde silinir.
- Modelin nasıl çalıştığı açık literatür ve repo aracılığıyla erişilebilir (yayın + model card).

### 8.2. Kullanıcı haklarının operasyonel karşılığı (KVKK uyumlu)

| Hak | Operasyonel karşılık | Sürüm |
|---|---|---|
| Bilgi alma hakkı | Profil sayfasında "verim nasıl kullanılıyor?" linki | Faz 3 |
| Erişim hakkı | "Verilerimi indir" → JSON+geoparquet | Faz 4 |
| Düzeltme hakkı | Etiket düzenleme + parsel sınırı revize | Faz 3 |
| Silme hakkı | "Hesabımı sil" → 30 gün içinde tüm veri silinir | Faz 4 |
| İşleme itiraz | Etiket paylaşımı opt-out anahtarı | Faz 3 |
| Veri taşınabilirliği | Standart format ihracı | Faz 4 |

### 8.3. Yapay zekâ etiği (model özelinde)

- **Hata yanlılığı şeffaflığı:** Pilot dışı bölgelerde modelin çalışmadığı arayüzde yazılır.
- **Açıklanabilirlik:** SHAP veya feature importance her tahminle birlikte sunulur (Faz 4).
- **Geri bildirim döngüsü:** Kullanıcı "yanlış" diyebilir; bu sinyal model retraining'e girer.
- **Otomatik karar yok:** Hiçbir biçerdöver/satım sistemi modele bağlı otomatik tetiklenmez; insan onayı zorunlu.

---

## 9. Genişletilmiş risk değerlendirme (erken uyarı + MVP/ticari etki)

Aşağıdaki tablo Bölüm 1'in 17 maddelik risk kaydını **savunma açısından** zenginleştirir: her risk için (a) erken uyarı sinyali, (b) çözüm planı, (c) MVP'ye etkisi, (d) ticari ölçeğe etkisi.

| ID | Erken uyarı sinyali | Çözüm planı | MVP etkisi | Ticari ölçek etkisi |
|---|---|---|---|---|
| R-01 | İlk 7 günde kuruma yanıt yok | Yedek kanal: kooperatif + ÇKS açık veri | Demo ertelenir (1-2 hafta) | Müşteri edinimi yavaşlar |
| R-02 | Bir aylık bulutsuz S2 < 4 sahne | S1 ağırlığını artır, HLS füzyonu zorunlu | Kapsama < %70 | Müşteri "boşluk" şikayeti |
| R-03 | İki bağımsız etiket arasında ≥ 7 gün sapma | `confidence` ile düşük ağırlık, etiket revize | MAE büyür | Doğruluk iddiasını geri çek |
| R-04 | Train/test MAE farkı > %30 | GroupKFold + regularization + daha çok parsel | V2 modeli ertelenir | Sözleşme öncesi blokaj |
| R-05 | GEE quota uyarısı / latency | Yerel pipeline'a kademeli geçiş | Hesaplama yavaşlar | Aylık altyapı maliyeti +%30 |
| R-06 | Demo öncesi 24 saat içinde "API down" | Offline ekran kaydı + lokal Streamlit yedek | Sunum kurtulur | Demo SLA itibar kaybı |
| R-07 | Sprint sonu yarım iş > 2 | Backlog dondurma + faz başı yeniden tartı | Faz kapısı kapanmaz | Yol haritası kayar |
| R-08 | 2 ardışık sprintte 0 demo | Süreyi ölçeklendir, ölçeği daralt | Bitirme süresi kayar | Tek kişiye bağımlılık riski netleşir |
| R-09 | Veri sahibi kullanıcıdan şikayet | Veri silme + olay raporu, KVKK kuruluna bildirim hazırlığı | Yetkili otorite incelemesi | Ticari faaliyet askıya alınabilir |
| R-10 | TestFlight / Internal Track reddi | PWA üzerinden devam, native sürümü gözden | Mağaza yayını gecikir | Kullanıcı edinimi yavaşlar |
| R-11 | 3 hafta saha ziyareti planlanamaz | Yerel ortakla mobil saha formu | Doğrulama veri kalitesi düşer | Ticari doğruluk iddiası zayıflar |
| R-12 | Pilot dışı parselde MAE > 14 gün | Tahmin "guard rail" mesajı + bölge kapsamı | Demo bölgeyle sınırlı | Genişleme yavaşlar |
| R-13 | Sentinel A/B harmonizasyon farkı > %3 | İki uydu için ayrı kalibrasyon | İndeks gürültüsü artar | Çoklu sezon kıyası bozulur |
| R-14 | İMECE/GÖKTÜRK için resmi yanıt yok | V2'ye ertele; sadece açık veriyle ilerle | Yerli görünürlük kaybı | Kamu ihalesinde dezavantaj |
| R-15 | Hocadan beklenmeyen yön değişikliği | Mevcut ADR'larla geri dönüş maliyeti hesapla; yeni ADR önerisi | Sprint kayar | Ticari pivot maliyeti büyür |
| R-16 | Pre-commit/secret scan uyarısı | Anahtarı iptal et, history'den temizle (BFG) | Repo geçici kapanır | Güvenlik denetimi başlar |
| R-17 | İlk demo sonrası kullanıcı "anlamadım" oranı > %50 | UX iterasyonu, copy revize, mockup test | V2 ürün kabul gecikir | Kooperatif sözleşme döngüsü uzar |

---

## 10. Bu proje neden başarısız olabilir? (dürüst senaryolar)

Bir projenin başarısız olduğu yerler genellikle riskler değil, **risk bileşkeleridir**. Aşağıda 5 olası başarısızlık senaryosu ve her birinin ne tür bir bileşkeden doğduğu açıklanır.

### Senaryo 1 — "Demo var ama doğruluk yok"
**Bileşke:** R-01 + R-03 + R-15. Veri/etiket gecikir, modeller etiketsiz kalır, hoca da yön değiştirir; sonuç: güzel görünen Streamlit demosu var, ama gerçek MAE bilinmiyor.
**Erken sinyaller:** Faz 2 sonunda "manuel doğrulama tablosu" boş kalıyor.
**Çözüm:** Faz 0'da etiket erişim taahhüdü yazılı al; alınamazsa tez konusunu **kural tabanlı sistem ablation çalışması** olarak yeniden çerçevele.

### Senaryo 2 — "Tek bölge başardı, hiçbir yere genişletilemiyor"
**Bileşke:** R-12 + R-04 + R-13. Konya'da %75 isabet, Trakya'da %20. Domain shift sertçe çarpıyor.
**Erken sinyaller:** Faz 4'te ikinci pilotta MAE iki katına çıkar.
**Çözüm:** V1 söyleminde "tek bölge demo" sınırını açıkça koruyup ticari söylemi çoklu bölge yerine **derin tek-bölge** olarak konumla.

### Senaryo 3 — "Teknik var, kullanıcı yok"
**Bileşke:** R-17 + R-11 + R-15. Hiç kullanıcı görüşmesi yapılmadığı için ürün arayüzü çiftçinin ihtiyacını karşılamıyor.
**Erken sinyaller:** Faz 3 sonunda hiç pilot kullanıcı görüşmesi yapılmamış.
**Çözüm:** Faz 3 başında **ilk 3 kullanıcı görüşmesi** zorunlu; demo bu görüşmelerden sonra.

### Senaryo 4 — "Akademik tamam, ticari sıfır"
**Bileşke:** R-08 + R-10 + R-15. Tez yazıldı, makale çıktı; ama kullanıcı yok, gelir yok, ekip dağıldı.
**Erken sinyaller:** Faz 5'te pilot kullanıcı sayısı 0.
**Çözüm:** Bitirme tezi yazımı ile paralel olarak **en az 1 kooperatif pilotu** çalıştır; tezde gerçek pilotun verilerini kullan.

### Senaryo 5 — "GEE çekildi, hiçbir şey çalışmıyor"
**Bileşke:** R-05 + R-08. GEE akademik kullanım koşulları değişti, herhangi bir ticari kullanımda blokajla karşılaşıyoruz; yerel pipeline hiç hazırlanmamış.
**Erken sinyaller:** GEE quota uyarıları, ToS güncellemeleri.
**Çözüm:** Faz 4'te **yerel Python pipeline** prototipini en azından "tek parsel uçtan uca" çalıştır; lock-in'i ileride hafifletme planını yaz.

---

İlgili: [`03_FAZLAR_VE_DURUMLAR.md`](./03_FAZLAR_VE_DURUMLAR.md) (kapı içerikleri) / [`10_KARAR_KAYDI.md`](./10_KARAR_KAYDI.md) (risk kararları) / [`05_VERI_VE_MODELLEME.md`](./05_VERI_VE_MODELLEME.md) (etiket kalite puanı).

---

## Bu dosyada alınan kararlar
- Risk skoru (etki × olasılık) ≥ 12 olan riskler haftalık gözden geçirilir; ≥ 16 olanlar bir sonraki sprintte mitigasyon görevi açar.
- Etik prensipleri arasında "otomatik karar yok" kuralı kırmızı çizgidir; hiçbir entegrasyonla esnetilmez.
- "Bu proje neden başarısız olabilir?" senaryoları her faz sonunda revize edilir; yeni bileşke ortaya çıkarsa eklenir.
- KVKK ihlali şüphesinde ilk eylem servis durdurmadır, soru sormak değil.

## Açık sorular
- Bağımsız bir akademik etik incelemesi (üniversite etik kurulu) gerekli mi? — Veri sahipliği yapısına göre Faz 3'te değerlendirilecek.
- "Yanlış tahmin nedeniyle çiftçi zarar etti" senaryosunda hukuki sorumluluk nasıl sınırlandırılır? — Kullanıcı sözleşmesinde "tavsiye amaçlıdır" ifadesi yeterli mi, hukuki danışman görüşü gerek.
- Pre-commit secret scanning aracı için tercih: gitleaks mi trufflehog mu? — Faz 0'da seç.

## Sonraki aksiyonlar
- T-007 (KVKK kısa notu) tamamlandığında bu dosyaya link eklenir.
- Her sprint sonu retro'da risk kaydı revize edilir; yeni risk eklenir, kapatılan işaretlenir.
- Faz 3 başında etik kurul başvurusu hazırlığı başlatılır (gerekirse).