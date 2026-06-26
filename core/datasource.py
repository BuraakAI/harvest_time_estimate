"""Veri kaynağı adapteri.

04_TEKNIK_MIMARI.md §2-3: akademik MVP'de GEE birincil; demo modu vendor-bağımsız.
İki uygulama:
  * DemoDataSource  — sentetik ama gerçekçi kışlık buğday fenolojisi (offline, anında).
  * GEEDataSource   — Google Earth Engine ile gerçek Sentinel-2 (kimlik bilgisi gerekir).

Ortak arayüz: get_timeseries(parcel, season_year, today) -> TimeSeries.
01_VIZYON anti-vizyon: "offline demo paketi her zaman hazır olacak" → demo varsayılan.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from . import RANDOM_STATE
from .models import Parcel, TimeSeries


def _stable_seed(text: str) -> int:
    """Süreçten bağımsız sabit tohum (Python hash() randomize olduğu için)."""
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    return RANDOM_STATE + int(digest[:6], 16)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# --- Parsel yükleme -----------------------------------------------------------
def load_parcels(path: Path | None = None) -> list[Parcel]:
    """data/parcels.geojson dosyasından parselleri okur."""
    path = path or (DATA_DIR / "parcels.geojson")
    gj = json.loads(path.read_text(encoding="utf-8"))
    parcels: list[Parcel] = []
    for feat in gj["features"]:
        p = feat["properties"]
        ring = feat["geometry"]["coordinates"][0]      # [[lon, lat], ...]
        lons = [c[0] for c in ring]
        lats = [c[1] for c in ring]
        centroid = (sum(lats) / len(lats), sum(lons) / len(lons))
        planted = p.get("planted_at")
        parcels.append(Parcel(
            id=p["id"], name=p["name"], crop_code=p["crop_code"],
            region_code=p["region_code"], area_ha=float(p["area_ha"]),
            planted_at=date.fromisoformat(planted) if planted else None,
            centroid=centroid, polygon=ring,
            _demo_params=p.get("demo_params", {}),
        ))
    return parcels


# --- Demo (sentetik) kaynak ---------------------------------------------------
class DemoDataSource:
    """Çift-lojistik fenoloji eğrisinden gerçekçi NDVI/NDMI/VH üretir.

    Kışlık buğday: ilkbahar yeşillenmesi → tepe (~Nisan sonu) → senesens →
    sararma/kuruma → hasat (Haziran sonu–Temmuz). Bulut boşlukları NaN olarak
    eklenir; gözlemler `today`'e kadar kesilir.
    """

    name = "Demo (sentetik)"

    NDVI_FLOOR = 0.16   # senesens sonu / çıplak anız taban seviyesi

    def get_timeseries(self, parcel: Parcel, season_year: int, today: date) -> TimeSeries:
        prm = parcel._demo_params
        sos = prm.get("sos_doy", 70)
        pos = prm.get("pos_doy", 120)
        harvest = prm.get("eos_doy", 195)          # senesens-sonu ≈ hasat günü
        ndvi_max = prm.get("max_ndvi", 0.82)
        ndvi_base = prm.get("base_ndvi", 0.15)
        rng = np.random.default_rng(_stable_seed(parcel.id))

        start = date(season_year, 2, 1)
        dates = pd.date_range(start, date(season_year, 8, 15), freq="5D")
        doy = np.array([d.dayofyear for d in dates], float)

        # Yükseliş: lojistik (sos → pos). Senesens: pos'tan hasata ~lineer dik düşüş
        # (buğday drydown'ı uydu NDVI'sinde yaklaşık doğrusaldır).
        rise = 1 / (1 + np.exp(-0.16 * (doy - sos)))
        ndvi = ndvi_base + (ndvi_max - ndvi_base) * rise
        sen_end = harvest + 4
        sen = (doy > pos)
        frac = np.clip((doy[sen] - pos) / max(sen_end - pos, 1), 0, 1.3)
        ndvi[sen] = np.maximum(ndvi_max - (ndvi_max - self.NDVI_FLOOR) * frac, self.NDVI_FLOOR)
        ndvi += rng.normal(0, 0.010, size=ndvi.shape)

        # NDMI: NDVI'yi izler, olgunlaşmada (kuruma) daha hızlı/derin düşer
        ripening = np.clip((doy - (pos - 5)) / max(harvest - pos, 1), 0, 1)
        ndmi = (ndvi * 0.50) - 0.18 * ripening + rng.normal(0, 0.010, size=ndvi.shape)

        # VH (radar, dB): hasat olayında ani düşüş — burada eğilim olarak modellenir
        vh = -14 + 4 * (ndvi - ndvi_base) / max(ndvi_max - ndvi_base, 0.1) \
             + rng.normal(0, 0.4, size=ndvi.shape)

        df = pd.DataFrame({"date": dates, "ndvi": ndvi, "ndmi": ndmi, "vh": vh})

        # Bulut boşlukları: optik gözlemlerin ~%25'i NaN (radar etkilenmez)
        cloud_mask = rng.random(len(df)) < 0.25
        df.loc[cloud_mask, ["ndvi", "ndmi"]] = np.nan

        # Geleceği gizle: yalnız bugüne kadar gözlem var
        today_ts = pd.Timestamp(today)
        df = df[df["date"] <= today_ts].reset_index(drop=True)

        n_obs = int(df["ndvi"].notna().sum())
        cloud_pct = float(100 * df["ndvi"].isna().mean()) if len(df) else 0.0
        return TimeSeries(parcel.id, season_year, df, n_obs, cloud_pct)


# --- GEE (gerçek veri) kaynağı ------------------------------------------------
class GEEDataSource:
    """Google Earth Engine ile gerçek Sentinel-2 (+ Sentinel-1) zaman serisi.

    Pipeline (05_VERI §4 ETL): S2_SR_HARMONIZED → SCL bulut maskesi →
    NDVI=(B8-B4)/(B8+B4), NDMI=(B8-B11)/(B8+B11) → parsel ortalaması (10 m) →
    S1_GRD VH (dB, bulut bağımsız) ile birleştir. Çıktı şeması Demo ile aynıdır
    (date, ndvi, ndmi, vh) → fenoloji/kural/UI/backtest hiç değişmeden çalışır.

    Kurulum (README 'Canlı moda geçiş'):
        pip install earthengine-api
        earthengine authenticate
        export EE_PROJECT=<google-cloud-proje-id>   # GEE artık proje ister

    Sezonun tamamı bir kez çekilip parsel-sezon başına önbelleğe (CSV) alınır;
    `today`'e göre istemci tarafında kesilir (gelecek gözlem sızıntısı olmaz —
    backtest için kritik). Önbellek 04_TEKNIK_MIMARI §2.3 stratejisinin yereli.
    """

    name = "Canlı (GEE)"
    CACHE_DIR = DATA_DIR / "cache"
    # SCL'de maskelenecek sınıflar: 0 nodata,1 doygun,3 bulut gölgesi,
    # 8/9 bulut(orta/yüksek),10 sirüs,11 kar
    SCL_MASK_CLASSES = [0, 1, 3, 8, 9, 10, 11]

    def __init__(self, project: str | None = None) -> None:
        import os
        self.project = project or os.environ.get("EE_PROJECT")
        self._initialized = False
        try:
            import ee  # noqa: F401
            self._available = True
        except Exception:
            self._available = False

    # --- başlatma ---
    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        try:
            import ee
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "earthengine-api kurulu değil. `pip install earthengine-api` çalıştırın."
            ) from exc
        try:
            ee.Initialize(project=self.project) if self.project else ee.Initialize()
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "GEE başlatılamadı. Önce `earthengine authenticate` çalıştırın ve "
                "EE_PROJECT ortam değişkenini Cloud proje id'nizle ayarlayın. "
                f"(Ayrıntı: {exc})"
            ) from exc
        self._initialized = True

    # --- ana giriş ---
    def get_timeseries(self, parcel: Parcel, season_year: int, today: date) -> TimeSeries:
        frame = self._load_cache(parcel.id, season_year)
        if frame is None:
            self._ensure_initialized()
            frame = self._pull_season(parcel, season_year)
            self._save_cache(parcel.id, season_year, frame)

        obs = frame[frame["date"] <= pd.Timestamp(today)].reset_index(drop=True)
        n_obs = int(obs["ndvi"].notna().sum()) if len(obs) else 0
        cloud_pct = float(100 * obs["ndvi"].isna().mean()) if len(obs) else 0.0
        return TimeSeries(parcel.id, season_year, obs, n_obs, cloud_pct)

    # --- GEE'den sezonu çek ---
    def _pull_season(self, parcel: Parcel, season_year: int) -> pd.DataFrame:
        import ee

        geom = ee.Geometry.Polygon([parcel.polygon])
        start, end = f"{season_year}-02-01", f"{season_year}-08-15"

        s2 = self._pull_s2(ee, geom, start, end)
        s1 = self._pull_s1(ee, geom, start, end)

        frame = pd.merge(s2, s1, on="date", how="outer") if not s1.empty else s2.copy()
        for col in ("ndvi", "ndmi", "vh"):
            if col not in frame.columns:
                frame[col] = np.nan
        return frame.sort_values("date").reset_index(drop=True)

    def _pull_s2(self, ee, geom, start, end) -> pd.DataFrame:
        mask_classes = self.SCL_MASK_CLASSES

        def add_indices(img):
            scl = img.select("SCL")
            keep = scl.remap(mask_classes, [0] * len(mask_classes), 1)  # maske dışı=1
            masked = img.updateMask(keep)
            ndvi = masked.normalizedDifference(["B8", "B4"]).rename("ndvi")
            ndmi = masked.normalizedDifference(["B8", "B11"]).rename("ndmi")
            return masked.addBands([ndvi, ndmi])

        col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
               .filterBounds(geom).filterDate(start, end)
               .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 80))
               .map(add_indices))

        def reduce_img(img):
            stats = img.select(["ndvi", "ndmi"]).reduceRegion(
                reducer=ee.Reducer.mean(), geometry=geom, scale=10, maxPixels=int(1e9))
            return ee.Feature(None, {"date": img.date().format("YYYY-MM-dd"),
                                     "ndvi": stats.get("ndvi"), "ndmi": stats.get("ndmi")})

        feats = col.map(reduce_img).getInfo()["features"]
        rows = [f["properties"] for f in feats]
        df = pd.DataFrame(rows)
        if df.empty:
            return pd.DataFrame(columns=["date", "ndvi", "ndmi"])
        df["date"] = pd.to_datetime(df["date"])
        # aynı günde birden çok karo → ortala; geçerli gözlemi olanları tut
        df = df.groupby("date", as_index=False)[["ndvi", "ndmi"]].mean()
        return df

    def _pull_s1(self, ee, geom, start, end) -> pd.DataFrame:
        try:
            col = (ee.ImageCollection("COPERNICUS/S1_GRD")
                   .filterBounds(geom).filterDate(start, end)
                   .filter(ee.Filter.eq("instrumentMode", "IW"))
                   .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH")))

            def reduce_img(img):
                v = img.select("VH").reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=geom, scale=10, maxPixels=int(1e9))
                return ee.Feature(None, {"date": img.date().format("YYYY-MM-dd"),
                                         "vh": v.get("VH")})

            feats = col.map(reduce_img).getInfo()["features"]
            rows = [f["properties"] for f in feats]
            df = pd.DataFrame(rows)
            if df.empty:
                return pd.DataFrame(columns=["date", "vh"])
            df["date"] = pd.to_datetime(df["date"])
            return df.groupby("date", as_index=False)[["vh"]].mean()
        except Exception:
            return pd.DataFrame(columns=["date", "vh"])  # S1 zorunlu değil (Faz 4)

    # --- önbellek (CSV) ---
    def _cache_path(self, parcel_id: str, season_year: int) -> Path:
        return self.CACHE_DIR / f"gee_{parcel_id}_{season_year}.csv"

    def _load_cache(self, parcel_id: str, season_year: int) -> pd.DataFrame | None:
        path = self._cache_path(parcel_id, season_year)
        if not path.exists():
            return None
        df = pd.read_csv(path, parse_dates=["date"])
        return df

    def _save_cache(self, parcel_id: str, season_year: int, frame: pd.DataFrame) -> None:
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        frame.to_csv(self._cache_path(parcel_id, season_year), index=False)
