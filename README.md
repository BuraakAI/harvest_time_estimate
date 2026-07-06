# HasadHaber — Hasat Zamanı Karar Destek Sistemi (MVP)

> Uydu zaman serisinden bir tarlanın fenolojik olgunluğunu okuyup parsel bazında
> **"hasada kaç gün kaldı?"** sorusuna ±gün cinsinden cevap üreten karar destek demosu.
> Pilot: **kışlık buğday · Konya / Çumra**. Bu, staj omurgasının (`../staj-omurga/`)
> Faz 2 (MVP-V1) çıktısıdır.

## Hızlı başlangıç

```bash
cd hasat-zamani
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Tarayıcı `http://localhost:8501` adresinde açılır. **Hiçbir kimlik bilgisi gerekmez** —
varsayılan **Demo modu** Çumra için 10 örnek parselde gerçekçi sentetik buğday
fenolojisi üretir (offline demo paketi her zaman hazır; `01_VIZYON` anti-vizyonu).

## Ne yapıyor?

1. Haritada parseller hasat yakınlığına göre renklenir (🟢 zaman var · 🟠 ≤21 gün · 🔴 ≤7 gün).
2. Seçilen parsel için **tahmini hasat tarihi · kalan gün · fenolojik evre · güven skoru** gösterilir.
3. NDVI / NDMI / VH eğrisi, POS–bugün–tahmini hasat işaretleriyle çizilir.
4. "Neden bu tahmin?" paneli kuralı ve sinyalleri doğal dilde açıklar (açıklanabilirlik).
5. "Kooperatif görünümü" sekmesi hasat sırası + haftalık hasat dalgasını verir.

## Mimari (omurga karşılığı)

| Dosya | Rol | Omurga referansı |
|---|---|---|
| `core/datasource.py` | Demo (sentetik) + GEE (gerçek Sentinel-2/S1, tam adaptör) veri kaynağı | `04_TEKNIK_MIMARI §2-3` |
| `core/indices.py` | NDVI/NDMI/NDRE (canlı mod) | `05_VERI §5` |
| `core/phenology.py` | Savitzky-Golay + SOS/POS/EOS + eğim | `05_VERI §4, §6` |
| `core/rules.py` | Kural tabanlı tahmin + 4 bileşenli güven skoru | `05_VERI §7.1`, `04 §7.1` |
| `app.py` | Streamlit arayüzü | `06_URUN §2` |

Model sırası **kural → RF → XGBoost → DL** (`05_VERI §7`). Bu sürüm **kural tabanlı**
ve **etiketsiz** çalışır — dayanağı Sedano 2025 (`12_LITERATUR §3`, doğrulandı ✅).

## Doğruluk ölçümü (backtest)

`📊 Doğruluk` sekmesi ve `ml/evaluate.py`, tahminleri gerçek hasat tarihiyle
karşılaştırır (`05_VERI §8`): **MAE, RMSE, ±3/±7/±14 gün isabet, bias, kapsama,
güven aralığı kapsaması**. Yöntem **lead-time backtest**: her parselin hasat
tarihinden 40/30/20/10/5 gün önce tahmin üretilir; hasada yaklaştıkça MAE düşmelidir.

```bash
python -m ml.evaluate          # CLI özet
```

Etiketler `data/harvest_labels.csv` (`parcel_id, season_year, harvest_date, source,
confidence` — `04 §5` `harvest_labels` tablosu). Şu an **sentetik**; gerçek doğruluk
için bu dosyaya **saha hasat tarihleri** (üretici/kooperatif/biçerdöver) girilir.

> ⚠️ Sentetik etiketle backtest, ölçüm **kodunun** ve motorun davranışını gösterir —
> gerçek tarım doğruluğunu **değil**. Gerçek sayı: saha etiketi + Canlı Sentinel-2.

## Testler

```bash
python -m pytest -q     # 27 test: kural motoru + fenoloji + veri kaynağı + indeksler + değerlendirme
```

## Canlı moda geçiş (gerçek Sentinel-2, GEE)

`GEEDataSource` **yazıldı ve hazır** (`core/datasource.py`); yalnız kimlik bilgisi gerekiyor:

1. **Hesap:** [code.earthengine.google.com](https://code.earthengine.google.com) → Google
   hesabınla kaydol (akademik/araştırma ücretsiz). Bir **Google Cloud projesi** oluştur.
2. **Kurulum:**
   ```bash
   pip install -r requirements-gee.txt
   earthengine authenticate            # tarayıcıda izin
   export EE_PROJECT=<cloud-proje-id>  # GEE artık proje ister
   # veya kalıcı olarak: proje kimliğini data/ee_project.txt dosyasına yazın (gitignore'da)
   ```
3. **Çalıştır:** `streamlit run app.py` → sidebar'dan **"Canlı (GEE)"** seç. Parsel
   poligonu ile `COPERNICUS/S2_SR_HARMONIZED`'dan SCL bulut maskeli NDVI/NDMI +
   `COPERNICUS/S1_GRD` VH çekilir; sezon parsel başına `data/cache/`'e CSV olarak
   önbelleğe alınır (`today`'e göre kesilir → gelecek sızıntısı yok).
4. **Doğruluk:** `📊 Doğruluk` sekmesinde "Backtest çalıştır (gerçek GEE)" butonu.

> Çekirdek mantık veri kaynağından bağımsızdır: Demo → GEE geçişi yalnız adaptör
> değişimidir; `phenology.py`, `rules.py`, `ml/evaluate.py`, `app.py` **değişmez**.
> Gerçek doğruluk için `data/harvest_labels.csv`'ye **gerçek saha hasat tarihleri** girilir.

## Sınırlar (dürüst)

- Demo verisi **sentetiktir**; doğruluk iddiası taşımaz, veri hattını ve UI'yı gösterir.
- Gerçek doğruluk (MAE, ±7/±14 gün isabet) ancak saha hasat etiketleriyle ölçülür (`05_VERI §8`).
- V1 **verim tahmini yapmaz**; yalnız hasat zamanı (`01_VIZYON §6`).
