"""Fenoloji metrikleri ve zaman serisi işleme.

05_VERI_VE_MODELLEME.md §4 (ETL adımları 8-11) ve §6 (fenoloji metrikleri)
karşılığı: yumuşatma (Savitzky-Golay), SOS/POS/EOS, senesens eğimi vb.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


@dataclass
class PhenoMetrics:
    """Bir parsel-sezonun gözlem-gününe kadarki fenoloji özeti."""

    pos_doy: int | None          # tepe noktası (Peak of Season)
    sos_doy: int | None          # sezon başlangıcı (Start of Season)
    eos_doy: int | None          # senesens sonu (gözlemlendiyse)
    max_ndvi: float
    ndvi_now: float              # bugünkü (son) yumuşatılmış NDVI
    ndmi_now: float
    days_since_pos: int | None
    slope_last_14d: float        # NDVI/gün, son 14 gün doğrusal eğim
    ndmi_drop_last_14d: float    # son 14 günde NDMI düşüşü (pozitif = düşüyor)
    n_obs: int
    cloud_gap_days: int          # son gözlemden bugüne geçen gün


def _doy(d: pd.Timestamp) -> int:
    return int(d.dayofyear)


def smooth_series(frame: pd.DataFrame, col: str) -> pd.Series:
    """NaN'leri zaman-interpolasyonuyla doldurup Savitzky-Golay uygular.

    05_VERI §4 adım 8: Savitzky-Golay (window~15, order 3). Gözlem azsa
    pencere otomatik küçültülür.
    """
    s = frame.set_index("date")[col].astype(float)
    s = s.interpolate(method="time", limit_direction="both")
    valid = s.dropna()
    if len(valid) < 5:
        return s
    window = min(15, len(valid) if len(valid) % 2 == 1 else len(valid) - 1)
    window = max(5, window if window % 2 == 1 else window - 1)
    poly = min(3, window - 1)
    smoothed = savgol_filter(s.values, window_length=window, polyorder=poly)
    return pd.Series(smoothed, index=s.index, name=col)


def compute_metrics(frame: pd.DataFrame, today: pd.Timestamp) -> PhenoMetrics:
    """Gözlemleri `today`'e kadar kesip fenoloji metriklerini çıkarır."""
    obs = frame[frame["date"] <= today].copy()
    n_obs = int(obs[["ndvi"]].notna().sum().iloc[0])

    ndvi_s = smooth_series(obs, "ndvi")
    ndmi_s = smooth_series(obs, "ndmi")

    max_ndvi, pos_idx = _peak(ndvi_s.values)
    pos_date = ndvi_s.index[pos_idx] if pos_idx is not None else None
    pos_doy = _doy(pos_date) if pos_date is not None else None
    days_since_pos = int((today - pos_date).days) if pos_date is not None else None

    # SOS: tepenin %20'sine ilk ulaşma; EOS: tepeden %30 seviyesine iniş (gözlemlendiyse)
    sos_doy = _first_cross_doy(ndvi_s, level=0.20 * max_ndvi, rising=True)
    eos_doy = None
    if pos_date is not None:
        post = ndvi_s[ndvi_s.index >= pos_date]
        eos_doy = _first_cross_doy(post, level=0.30 * max_ndvi, rising=False)

    ndvi_now = float(ndvi_s.iloc[-1]) if len(ndvi_s) else float("nan")
    ndmi_now = float(ndmi_s.iloc[-1]) if len(ndmi_s) else float("nan")

    slope_last_14d = _slope_per_day(ndvi_s, today, days=14)
    ndmi_drop_last_14d = _drop_last(ndmi_s, today, days=14)

    last_obs_date = obs["date"][obs["ndvi"].notna()].max()
    cloud_gap_days = int((today - last_obs_date).days) if pd.notna(last_obs_date) else 99

    return PhenoMetrics(
        pos_doy=pos_doy, sos_doy=sos_doy, eos_doy=eos_doy,
        max_ndvi=max_ndvi, ndvi_now=ndvi_now, ndmi_now=ndmi_now,
        days_since_pos=days_since_pos, slope_last_14d=slope_last_14d,
        ndmi_drop_last_14d=ndmi_drop_last_14d, n_obs=n_obs,
        cloud_gap_days=cloud_gap_days,
    )


def _peak(vals: np.ndarray, tol: float = 0.01) -> tuple[float, int | None]:
    """Yumuşatılmış serideki tepe (POS) — boş/tümü-NaN girdiye ve platoya dayanıklı.

    Kışlık buğdayda NDVI tepede platolaşır; senesens platonun bitişinde başlar.
    Bu yüzden maksimuma `tol` içinde kalan bölgenin SON indeksi POS sayılır —
    tek noktalık erken gürültü sıçraması POS'u öne çekmez, `days_since_pos`
    senesens süresini ölçer (kural motoru bunun üzerine kuruludur).
    """
    vals = np.asarray(vals, float)
    if vals.size == 0 or np.all(np.isnan(vals)):
        return float("nan"), None
    max_v = float(np.nanmax(vals))
    near = np.flatnonzero(vals >= max_v - tol)
    return max_v, int(near[-1])


def _first_cross_doy(series: pd.Series, level: float, rising: bool) -> int | None:
    vals = series.values
    for i in range(1, len(vals)):
        if rising and vals[i - 1] < level <= vals[i]:
            return _doy(series.index[i])
        if not rising and vals[i - 1] > level >= vals[i]:
            return _doy(series.index[i])
    return None


def _slope_per_day(series: pd.Series, today: pd.Timestamp, days: int) -> float:
    window = series[series.index >= today - pd.Timedelta(days=days)]
    if len(window) < 2:
        return 0.0
    x = np.array([(d - window.index[0]).days for d in window.index], float)
    y = window.values.astype(float)
    slope = np.polyfit(x, y, 1)[0]
    return float(slope)


def _drop_last(series: pd.Series, today: pd.Timestamp, days: int) -> float:
    window = series[series.index >= today - pd.Timedelta(days=days)]
    if len(window) < 2:
        return 0.0
    return float(window.iloc[0] - window.iloc[-1])  # pozitif => düşüyor
