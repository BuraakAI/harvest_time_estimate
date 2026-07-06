# 03 — Fazlar, Durumlar, Karar Kapıları ve Sprint Disiplini

> **Amaç:** Süreyi ve belirsizliği yönetmek; ilerlemeyi 2–3 haftalık sprintlerle ölçmek; her fazın "minimum başarı" ve "ideal başarı" çubuklarını net koymak.
> **Kapsam:** Faz 0–5 tanımları, süre ölçeklemesi (6 hafta / 3 ay / 6 ay / 12 ay), durum sistemi, karar kapıları (gates), sprint çıktıları, ara rapor formatı.
> **Son güncelleme:** 2026-07-06
> **Mevcut faz: FAZ 2 (kapanış aşamasında).** Kod tarafı (`hasat-zamani/`) Faz 1 ve Faz 2'nin teknik maddelerini tamamladı; kapılarda kalan maddeler insan-tarafı (hoca onayı, demo videosu, gerçek buğday parseli listesi). Kapı durumları aşağıda işaretli.

---

## 1. Faz haritası — özet

```
FAZ 0 — KEŞİF        Pilot ve veri sözleşmesi netleşene kadar
FAZ 1 — VERİ HATTI   Çalışan ETL + ham fenoloji eğrisi
FAZ 2 — MVP-V1       Kural tabanlı çekirdek + Streamlit demo
FAZ 3 — MVP-V2       FastAPI + PWA + RF/XGBoost kalan-gün
FAZ 4 — DERİNLEŞME   Radar füzyonu + 2. pilot bölge + saha doğrulama
FAZ 5 — TİCARİLEŞME  Mobil + iş modeli + pilot müşteri + tez
```

Her faz **bir karar kapısıyla (gate)** biter. Kapıdan geçemezsen sonraki faza başlamazsın; geri dönüp eksiği kapatırsın.

---

## 2. Süre ölçeklemesi (aynı fazlar, farklı içerik derinliği)

| Faz | 6 hafta (zorunlu staj) | 3 ay | 6 ay | 12 ay |
|---|---|---|---|---|
| **Faz 0** | 3 gün | 1 hafta | 2 hafta | 2 hafta |
| **Faz 1** | 1 hafta | 2 hafta | 3 hafta | 3 hafta |
| **Faz 2** | 2 hafta | 3 hafta | 4 hafta | 4 hafta |
| **Faz 3** | sadece taslak | 4 hafta | 6 hafta | 6 hafta |
| **Faz 4** | yok | yok | 4 hafta | 8 hafta |
| **Faz 5** | yok | tez taslağı | 4 hafta | 12+ hafta |
| **Çıktı kalitesi** | Demo + sunum | POC + rapor | MVP + bitirme taslağı | Mobil + tez + makale |

> **Pratik tavsiye:** Süre netleşinceye kadar **3 ay senaryosu** baseline kabul edilir. Süre kesinleşince Faz 3 ve sonrası yeniden ölçeklenir.

### 2.1. Senaryo özetleri

| Senaryo | Hedef çıktı | Hocaya teslim noktası | Risk |
|---|---|---|---|
| 6 hafta | Streamlit demo + 8–10 parsel + kısa rapor | 6. hafta sonu sunum | ML hiç olmaz |
| 3 ay | + FastAPI + PWA + RF baseline | 13. hafta sunum + ara rapor | ML modeli sığ olabilir |
| 6 ay | + XGBoost + radar füzyonu + saha etiketi | 13. ve 24. hafta ara raporlar | İkinci pilot zaman alır |
| 12 ay | + ikinci pilot + bitirme tezi + mobil V0 | Çeyrek bazlı raporlar | Mobil mağaza onay riski |

---

## 3. Faz tanımları (genişletilmiş, min/ideal başarı + sprint çıktıları + go/no-go)

### FAZ 0 — Keşif ve sözleşme

**Amaç:** Pilot ürün/bölge kararı, veri/etiket erişim izinleri, repo iskeleti, ekip rolleri.

**Sprint çıktıları (her 2 hafta):**
- Sprint 0.1: Pilot karar imzası (ADR-001/010), repo açılışı, hocayla onay.
- Sprint 0.2: Veri envanter tablosu, izin formu taslağı, iletişim listesi.

**Minimum başarı:**
- Pilot kararı yazılı (ADR imzalı).
- Repo açık, README var, lisans seçildi.
- Veri kaynaklarının en az biri için resmi talep gönderilmiş.

**İdeal başarı:**
- Tüm hedef veri sahipleriyle iletişim açık.
- Tech stack onaylı, geliştirme ortamı çalışır.
- Hocadan yazılı onay (e-posta).

**Go/no-go (G0 → Faz 1):** *(durum: 2026-07-06)*
- [ ] ADR-001/010 yazılı ve onaylı *(yazılı; imza/onay bekliyor — T-001)*
- [x] En az 1 fenoloji sezonu için veri ulaşılabilir *(GEE ile 2026 sezonu S2/S1 çekildi)*
- [x] Repo iskeleti CI yeşil *(lokal git repo + 27 test geçiyor; GitHub push T-004)*
- [ ] Hocayla onay alındı *(T-005)*

---

### FAZ 1 — Veri hattı (ETL)

**Amaç:** Tek bir parselin Sentinel-2 zaman serisini ham bir notebook'ta gösterebilmek.

**Sprint çıktıları:**
- Sprint 1.1: GEE servis hesabı + tek parsel S2 NDVI eğrisi.
- Sprint 1.2: Bulut maskesi + S1 VH/VV + smoothing + 10 parsele genişleme.

**Minimum başarı:**
- Tek parselin son 1 sezon NDVI eğrisi pürüzsüz çiziliyor.
- Bulut tarihleri temizleniyor.
- Notebook tekrar üretilebilir.

**İdeal başarı:**
- 10+ parsel için 5 sezon NDVI/EVI/NDMI/VH eğrisi var.
- Parquet ihracı + lokal cache çalışıyor.
- Ön-fenoloji metrikleri (POS, EOS) hesaplanabiliyor.

**Go/no-go (G1 → Faz 2):** *(durum: 2026-07-06 — teknik olarak GEÇİLDİ)*
- [x] Tek parsel uçtan uca işliyor *(GEE → fenoloji → kural → tahmin)*
- [x] Bulut maskesi doğru çalışıyor *(SCL sınıf maskesi; ADR-B-016)*
- [x] Notebook tekrar üretilebilir *(notebook yerine test edilebilir `core/` modülleri; ADR-B-016)*
- [x] 10 parsele genişletme yapıldı *(cache + T-207 tablosu 10 parselde üretildi)*

---

### FAZ 2 — MVP-V1 (kural tabanlı + Streamlit)

**Amaç:** Hocaya/jüriye gösterilebilir, parsel seçimi → fenolojik evre + tahmini hasat tarihi üreten **demo**.

**Sprint çıktıları:**
- Sprint 2.1: Fenoloji metrikleri + buğday eşik kalibrasyonu (Yue 2024 — *doğrulanmalı*).
- Sprint 2.2: Streamlit harita + tahmin paneli + 10 parsel manuel doğrulama.

**Minimum başarı:**
- Streamlit demo lokal olarak < 30 sn açılıyor.
- 10 parselden 5+'sında tahmin ±14 gün içinde.
- Demo videosu kayıtlı.

**İdeal başarı:**
- 10 parselden 7+'sında ±14 gün, 5+'sında ±7 gün.
- Streamlit Cloud üzerinden public yayın.
- Hocadan yazılı "devam" onayı.

**Go/no-go (G2 → Faz 3):** *(durum: 2026-07-06)*
- [x] Demo açılıyor ve hata vermiyor *(10 parsel, demo + canlı GEE modu, duman testi geçti)*
- [x] 10 parselde manuel doğrulama tablosu var *(`18_T207_DOGRULAMA_TABLOSU.md` — dikkat: ürün deseni uyuşmazlığı bulgusu; gerçek buğday parseli listesi gerekiyor)*
- [ ] Hocanın onayı var *(T-005 toplantısında T-207 bulgusuyla birlikte sunulacak)*

> ⚠️ **"±14 gün isabet" başarı çubuğu hakkında:** Sentetik etiketle ölçülen isabet
> (backtest: MAE 6.2 gün, ±14 %92) motorun davranışını gösterir, tarımsal doğruluğu
> DEĞİL (ADR-B-015). Gerçek isabet ölçümü, ekimi doğrulanmış buğday parselleri +
> saha hasat tarihleri geldiğinde aynı kodla yapılacak.

---

### FAZ 3 — MVP-V2 (FastAPI + PWA + ML)

**Amaç:** Streamlit demo'yu modüler bir mimariye taşımak; etiketli veri toplandıkça kalan-gün regresyon modelini eğitmek.

**Sprint çıktıları:**
- Sprint 3.1: FastAPI iskelet + Postgres+PostGIS + parsel CRUD.
- Sprint 3.2: PWA (React+Vite+Leaflet) + auth + tahmin akışı.
- Sprint 3.3: RF baseline + XGBoost + MLflow.
- Sprint 3.4: Docker compose + CI yeşil + lokal e2e.

**Minimum başarı:**
- API uçları curl ile test ediliyor.
- PWA mobil tarayıcıda çalışıyor.
- RF baseline kural tabanlı çekirdeği geçiyor (MAE iyileşmesi ≥ %15).

**İdeal başarı:**
- XGBoost MAE'si ≤ 7 gün, ±7 isabet ≥ %75.
- 3+ MLflow deneyi kayıtlı.
- Docker compose ile herkes için reproducible.

**Go/no-go (G3 → Faz 4):**
- [ ] API smoke test geçiyor
- [ ] ML baseline'ı geçti (≥ %15 iyileşme)
- [ ] PWA test cihazda çalışıyor
- [ ] Docker compose ile reproducible

---

### FAZ 4 — Derinleşme

**Amaç:** Bulut sigortası, ikinci pilot, saha doğrulama, açıklanabilirlik.

**Sprint çıktıları:**
- Sprint 4.1: S1+S2 füzyon + HLS koleksiyonu.
- Sprint 4.2: 30+ saha etiketi + ikinci pilot bölge talebi.
- Sprint 4.3: SHAP açıklanabilirlik + anomali bayrakları.
- Sprint 4.4: Ablation çalışması + ara rapor.

**Minimum başarı:**
- 20+ saha etiketi.
- Bulutlu sezonda kapsama ≥ %75.
- SHAP paneli en az 5 parsel için yorumlu.

**İdeal başarı:**
- 50+ saha etiketi.
- Kapsama ≥ %95.
- İkinci pilot ürün için ilk sonuçlar.

**Go/no-go (G4 → Faz 5):**
- [ ] Bulutlu sezon kapsama ≥ %80
- [ ] 30+ saha etiketi
- [ ] SHAP/açıklanabilirlik panel demosu çalışıyor
- [ ] İkinci pilot çıktısı raporda yer aldı

---

### FAZ 5 — Ticarileşme ve tez

**Amaç:** Bitirme tezi yazımı, mobil native taşıma, pilot müşteri görüşmesi, makale taslağı.

**Sprint çıktıları:**
- Sprint 5.1: React Native iskelet + Leaflet köprüsü.
- Sprint 5.2: Push bildirim + saha foto etiketi.
- Sprint 5.3: TestFlight/Internal Track yayın.
- Sprint 5.4: Bitirme tezi taslakları + 5 pilot kullanıcı görüşmesi.
- Sprint 5.5: Yayın taslağı + tez savunma sunumu.

**Minimum başarı:**
- Tez taslağı danışmana iletildi.
- En az 3 pilot kullanıcı görüşmesi yazılı.
- React Native build (en az iOS veya Android) çalışıyor.

**İdeal başarı:**
- 5 pilot kullanıcı + 1 kooperatif gerçek kullanım.
- Bitirme tezi tam taslak + jüri onayı.
- Mobil store (TestFlight/Internal) yayında.
- Makale taslağı ulusal kongre veya açık erişim dergiye gönderildi.

**Go/no-go (G5):**
- [ ] Mobil V0 store-ready
- [ ] Tez taslağı danışmana sunuldu
- [ ] 5+ pilot kullanıcı görüşmesi
- [ ] İş modeli yazılı

---

## 4. Durum sistemi (kanban)

| Durum | Anlam | Eylem |
|---|---|---|
| 🔵 `Backlog` | Fikir/varsayım | Sahip belirlenecek |
| 🟡 `Bu hafta` | Aktif sprint'e seçildi | Sahip atandı |
| 🟠 `Yapılıyor` | Aktif çalışma | Sahip çalışıyor |
| 🟣 `İncelemede` | Çıktı var, review bekliyor | Reviewer |
| 🟢 `Bitti` | Kabul ölçütü karşılandı | Arşivlenir |
| 🔴 `Engelli` | Bağımlılık/izin/veri eksiği | Engel kaldıran |
| ⚪ `İptal` | Artık gerek yok | — |

### Geçiş kuralları

```
Backlog → Bu hafta → Yapılıyor → İncelemede → Bitti
                ↓         ↓           ↓
              Engelli ← Engelli ← Engelli
                ↓
              Backlog (engel kalkınca)
```

**WIP limit:** `Yapılıyor` ≤ 2, `İncelemede` ≤ 3.

---

## 5. Sprint ritmi (2 hafta)

| Gün | Aktivite |
|---|---|
| Pzt (sprint başı) | Backlog'dan en fazla 5 görev seç → "Bu hafta" |
| Çar | Mid-sprint check; engel var mı? |
| Cum | Mini demo (kendine veya hocaya) + retro |
| Pzt (sonraki sprint) | Önceki sprint çıktısı arşiv → yeni planlama |

### Sprint çıktısı şablonu

Her sprint sonunda yazılır (kendi notlarına veya `09_GOREVLER.md` arşivine):

```markdown
## Sprint X.Y — [tarih]
**Hedef:** [tek cümle]
**Tamamlanan:** T-001, T-002, ...
**Yapılmadı (sebep):** T-003 (saha izni gecikti)
**Demo:** [bağlantı]
**Engelli görevler:** ...
**Sonraki sprint için:** ...
**Ders / retro notu:** ...
```

---

## 6. Hocaya 2–3 haftalık ara rapor formatı

> **Amaç:** Hocanın 1–2 sayfada projenin nerede olduğunu, ne yapıldığını, ne kaldığını, hangi karara ihtiyaç duyulduğunu görmesi.

```markdown
# Ara Rapor — [Sprint X.Y, tarih aralığı]

## 1. Bu dönemde ne yapıldı?
- Madde 1
- Madde 2
- Madde 3 (en fazla 5 madde, somut çıktıyla)

## 2. Sayısal/teknik ilerleme
| Metrik | Önceki | Şimdi | Hedef |
|---|---|---|---|
| MAE (gün) | — | 9.4 | ≤ 10 |
| Test parsel | 8 | 12 | 30 |
| ... |

## 3. Demo / ekran görüntüleri
- 1–2 ekran görüntüsü veya demo bağlantısı.

## 4. Engelli kalan / yardım istenen
- Veri izni X kurumdan gelmedi.
- Tech karar Y için hocadan onay bekleniyor.

## 5. Sonraki 2 hafta planı
- Sprint hedefi: ...
- Beklenen çıktılar: ...

## 6. Riskler ve dikkat
- R-XX yükseldi (sebep, mitigasyon).

## Ekler
- Karar kayıtlarındaki yenilikler (`10_KARAR_KAYDI.md`)
- Görev listesi durumu (`09_GOREVLER.md`)
```

Bu format hocaya yorgunluk vermeden özet, gerekirse derine inilebilir bağlantı sunar.

---

## 7. Risk × faz haritası

| Risk | En yüksek olduğu faz | Mitigasyon fazı |
|---|---|---|
| Veri/etiket erişim izni | 0–1 | Faz 0 paralel başlatma |
| Bulutluluk düşüklüğü | 2–3 | Faz 4 radar füzyonu |
| Model overfitting | 3 | Faz 3 cross-val + Faz 4 ek pilot |
| Demo kararsızlığı | 2–3 | Faz 2 offline paket |
| Kapsam kayması | 3–4 | Faz başı backlog dondurma |
| Tek kişi tükenmişlik | 4–5 | Süre ölçeklemesi yeniden gözden geçirme |

Detay: `07_RISKLER_VE_KALITE.md`.

---

## 8. Bu dosyada alınan kararlar

- Süreden bağımsız aynı faz iskeleti, derinlik ölçeklenir.
- Her faz **min/ideal başarı** ile çift çubuklu değerlendirilir.
- Sprint 2 hafta, çıktı şablonu standart.
- Hocaya 2–3 haftalık ara rapor 6 başlıklı sabit format.
- Her faz sonunda go/no-go checklist.

---

## 9. Açık sorular

- Hocanın resmi staj başlangıç tarihi ve süre kararı? (Senaryo seçimi buna bağlı.)
- Ara rapor sıklığı 2 mi 3 hafta mı tercih edilir? (Hocayla ilk toplantıda netleşecek.)
- 6 haftalık zorunlu staj senaryosunda Faz 3 hangi sınırla taslak kalır? — Hocadan kapsamsız onay alınmalı.

---

## 10. Sonraki aksiyonlar

1. Hocayla süre senaryosu netleştirilecek.
2. İlk sprint (Sprint 0.1) `09_GOREVLER.md`'de tanımlanacak.
3. Ara rapor şablonu `08_TESLIMATLAR.md`'ye kopyalanacak.
4. Sprint takvimi (2 hafta × N) takvime girilecek.

---

İlgili: [`09_GOREVLER.md`](./09_GOREVLER.md) — durumların yaşadığı yer / [`07_RISKLER_VE_KALITE.md`](./07_RISKLER_VE_KALITE.md) — risk detayı / [`08_TESLIMATLAR.md`](./08_TESLIMATLAR.md) — ara rapor uzun şablonu.
