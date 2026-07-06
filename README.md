# HasadHaber — Hasat Zamanı Karar Destek Sistemi (MVP)

> Uydu zaman serisinden bir tarlanın fenolojik olgunluğunu okuyup parsel bazında
> **"hasada kaç gün kaldı?"** sorusuna ±gün cinsinden cevap üreten karar destek demosu.
> Pilot: **kışlık buğday · Konya / Çumra**. Staj omurgasının Faz 2 (MVP-V1) çıktısıdır.

## Gereksinimler

- **Python 3.11+** (3.11 önerilir)
- macOS / Linux / Windows
- İnternet (yalnız **Canlı GEE** modu için; Demo modu tamamen offline çalışır)

## Kurulum ve çalıştırma

### 1. Repoyu klonla

```bash
git clone https://github.com/BuraakAI/harvest_time_estimate.git
cd harvest_time_estimate
```

### 2. Sanal ortam oluştur ve bağımlılıkları kur

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

> **Not:** `streamlit` global PATH'te olmayabilir. Komutları **her zaman** sanal ortam
> aktifken (`source .venv/bin/activate`) veya `.venv/bin/` önekiyle çalıştırın.

### 3. Uygulamayı başlat

```bash
# Sanal ortam aktifken:
streamlit run app.py

# veya sanal ortam açmadan (macOS/Linux):
.venv/bin/streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılır.

**`zsh: command not found: streamlit` hatası** alırsanız → sanal ortamı aktifleştirmediniz
veya `pip install` yapmadınız. Yukarıdaki adım 2'yi tekrarlayın.

### 4. (İsteğe bağlı) Canlı uydu verisi — Google Earth Engine

Demo modu kimlik bilgisi gerektirmez. Gerçek Sentinel-2 için:

```bash
source .venv/bin/activate
pip install -r requirements-gee.txt
earthengine authenticate              # tarayıcıda Google hesabıyla izin ver
echo "<cloud-proje-id>" > data/ee_project.txt   # örn. vault-501610
streamlit run app.py
```

Sidebar'dan **"Canlı (GEE)"** seçin. İlk çalıştırmada 10 parsel için veri çekilir ve
`data/cache/` altına önbelleğe alınır (sonraki açılışlar hızlıdır).

### 5. Testler ve CLI araçları

```bash
source .venv/bin/activate

python -m pytest -q                    # 27 birim test
python -m ml.evaluate                  # backtest özeti (demo veri)
python -m ml.validate_t207             # T-207 doğrulama tablosu (GEE gerekir)
```

## Proje yapısı

```
harvest_time_estimate/
├── app.py                 # Streamlit arayüzü (giriş noktası)
├── core/                  # Veri kaynağı, fenoloji, kural motoru
├── ml/                    # Backtest ve doğrulama
├── data/                  # Parseller, etiketler, GEE cache
└── tests/                 # pytest suite
```

## Hızlı başlangıç (özet)

```bash
git clone https://github.com/BuraakAI/harvest_time_estimate.git && cd harvest_time_estimate
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Varsayılan **Demo modu** Çumra için 10 örnek parselde gerçekçi sentetik buğday
fenolojisi üretir — **hiçbir kimlik bilgisi gerekmez**.

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
