"""Fenoloji modülü testleri: yumuşatma, SOS/POS/EOS, kenar durumları.

07_RISKLER_VE_KALITE.md test stratejisi — T-106 (Savitzky-Golay birim test)
ve T-201 (fenoloji metrikleri) karşılığı.
"""
from datetime import date

import numpy as np
import pandas as pd

from core.datasource import DemoDataSource, load_parcels
from core.phenology import _peak, compute_metrics, smooth_series

TODAY = pd.Timestamp(2026, 6, 26)


def _demo_frame(parcel_idx: int = 0) -> pd.DataFrame:
    parcel = load_parcels()[parcel_idx]
    return DemoDataSource().get_timeseries(parcel, 2026, TODAY.date()).frame


# --- smooth_series -------------------------------------------------------------
def test_smooth_fills_cloud_gaps():
    """Bulut NaN'leri interpolasyonla dolar → yumuşatılmış seri NaN içermez."""
    frame = _demo_frame()
    assert frame["ndvi"].isna().any()          # demo %25 bulut boşluğu üretir
    s = smooth_series(frame, "ndvi")
    assert not np.isnan(s.values).any()
    assert len(s) == len(frame)


def test_smooth_reduces_roughness():
    """Yumuşatma, eğrinin pürüzlülüğünü (2. fark karesi) azaltmalı."""
    frame = _demo_frame()
    raw = frame["ndvi"].interpolate(method="linear", limit_direction="both")
    s = smooth_series(frame, "ndvi")
    raw_rough = np.sum(np.diff(raw.values, n=2) ** 2)
    smooth_rough = np.sum(np.diff(s.values, n=2) ** 2)
    assert smooth_rough < raw_rough


def test_smooth_short_series_returns_interpolated():
    """5'ten az geçerli gözlem: Savitzky-Golay atlanır, seri yine döner."""
    frame = pd.DataFrame({
        "date": pd.date_range("2026-03-01", periods=3, freq="5D"),
        "ndvi": [0.3, np.nan, 0.5],
    })
    s = smooth_series(frame, "ndvi")
    assert len(s) == 3
    assert not np.isnan(s.values).any()


# --- _peak (POS) ---------------------------------------------------------------
def test_peak_empty_and_all_nan():
    for vals in (np.array([]), np.array([np.nan, np.nan])):
        max_v, idx = _peak(vals)
        assert idx is None
        assert np.isnan(max_v)


def test_peak_finds_maximum():
    vals = np.array([0.2, 0.4, 0.8, 0.5, 0.3])
    max_v, idx = _peak(vals)
    assert max_v == 0.8
    assert idx == 2


def test_peak_plateau_takes_end():
    """Plato: senesens plato bitiminde başlar → son near-max indeks POS'tur."""
    vals = np.array([0.2, 0.795, 0.80, 0.798, 0.2])
    _, idx = _peak(vals, tol=0.01)
    assert idx == 3


# --- compute_metrics -----------------------------------------------------------
def test_metrics_full_season_detects_phenology():
    """Sezon sonuna yakın: SOS ve POS bulunmalı, POS parametreye yakın olmalı."""
    parcel = load_parcels()[0]                  # cumra-01: pos_doy 119
    frame = DemoDataSource().get_timeseries(parcel, 2026, date(2026, 6, 26)).frame
    m = compute_metrics(frame, TODAY)
    assert m.sos_doy is not None
    assert m.pos_doy is not None
    assert abs(m.pos_doy - 119) <= 15           # yumuşatma kayması payı
    assert m.n_obs > 0
    assert m.max_ndvi > 0.6
    assert m.slope_last_14d < 0                 # senesens: NDVI düşüyor


def test_metrics_partial_season_no_crash():
    """Erken sezonda (henüz tepe yok) metrikler hatasız üretilmeli."""
    parcel = load_parcels()[0]
    early = pd.Timestamp(2026, 3, 15)
    frame = DemoDataSource().get_timeseries(parcel, 2026, early.date()).frame
    m = compute_metrics(frame, early)
    assert m.n_obs >= 0
    assert m.eos_doy is None                    # senesens henüz gözlemlenmedi


def test_metrics_truncates_future():
    """`today` sonrası gözlemler metriklere sızmamalı (backtest kritik)."""
    parcel = load_parcels()[0]
    full = DemoDataSource().get_timeseries(parcel, 2026, date(2026, 8, 15)).frame
    mid = pd.Timestamp(2026, 5, 1)
    m = compute_metrics(full, mid)
    assert m.pos_doy is None or m.pos_doy <= mid.dayofyear


def test_metrics_cloud_gap_days():
    """Son gözlemden bugüne geçen gün doğru sayılmalı."""
    dates = pd.date_range("2026-04-01", periods=10, freq="5D")
    frame = pd.DataFrame({"date": dates, "ndvi": 0.5, "ndmi": 0.3})
    frame.loc[frame.index[-2:], "ndvi"] = np.nan       # son 2 gözlem bulutlu
    today = dates[-1] + pd.Timedelta(days=3)
    m = compute_metrics(frame, today)
    assert m.cloud_gap_days == (today - dates[-3]).days
