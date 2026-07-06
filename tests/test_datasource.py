"""Veri kaynağı testleri: parsel yükleme, demo üretimi, `today` kesmesi.

Faz 2 kapı kriteri G2: 10 parsel demo hatasız çalışır (03_FAZLAR §Faz2).
"""
from datetime import date

import numpy as np
import pandas as pd

from core.datasource import DemoDataSource, load_parcels

SEASON = 2026


# --- load_parcels --------------------------------------------------------------
def test_ten_parcels_loaded():
    """Faz 2 teslimat kriteri: en az 10 parsel (08_TESLIMATLAR)."""
    parcels = load_parcels()
    assert len(parcels) >= 10
    assert len({p.id for p in parcels}) == len(parcels)   # id benzersiz


def test_parcel_fields_valid():
    for p in load_parcels():
        assert p.crop_code == "WHEAT_WINTER"
        assert p.region_code == "TR-42-Konya-Cumra"
        assert p.area_ha > 0
        assert p.planted_at is not None
        # Çumra civarı koordinat aklı-başındalık kontrolü
        lat, lon = p.centroid
        assert 37.4 < lat < 37.8 and 32.6 < lon < 33.0
        # poligon kapalı halka
        assert p.polygon[0] == p.polygon[-1]
        assert len(p.polygon) >= 4


# --- DemoDataSource ------------------------------------------------------------
def test_demo_truncates_at_today():
    parcel = load_parcels()[0]
    today = date(2026, 5, 10)
    ts = DemoDataSource().get_timeseries(parcel, SEASON, today)
    assert (ts.frame["date"] <= pd.Timestamp(today)).all()


def test_demo_deterministic_per_parcel():
    """Aynı parsel → aynı seri; farklı parsel → farklı seri (sabit seed)."""
    parcels = load_parcels()
    src = DemoDataSource()
    today = date(2026, 6, 26)
    a1 = src.get_timeseries(parcels[0], SEASON, today).frame
    a2 = src.get_timeseries(parcels[0], SEASON, today).frame
    b = src.get_timeseries(parcels[1], SEASON, today).frame
    pd.testing.assert_frame_equal(a1, a2)
    assert not np.allclose(a1["ndvi"].fillna(0), b["ndvi"].fillna(0))


def test_demo_ndvi_range_and_clouds():
    parcel = load_parcels()[0]
    ts = DemoDataSource().get_timeseries(parcel, SEASON, date(2026, 8, 15))
    ndvi = ts.frame["ndvi"].dropna()
    assert ((ndvi > -0.2) & (ndvi < 1.0)).all()
    assert ts.frame["ndvi"].isna().any()            # bulut boşluğu var
    assert ts.n_obs == int(ts.frame["ndvi"].notna().sum())
    assert 0 <= ts.cloud_pct <= 100


def test_demo_seasonal_shape():
    """Yeşillenme → tepe → senesens düşüşü sırası korunmalı."""
    parcel = load_parcels()[0]                       # pos_doy 119, eos_doy 182
    from core.phenology import smooth_series
    frame = DemoDataSource().get_timeseries(parcel, SEASON, date(2026, 8, 15)).frame
    s = smooth_series(frame, "ndvi")
    doy = np.array([d.dayofyear for d in s.index])
    early = s.values[doy < 80].mean()
    peak = s.values[(doy > 105) & (doy < 135)].mean()
    late = s.values[doy > 195].mean()
    assert early < peak and late < peak
