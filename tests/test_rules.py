"""Kural motoru için duman (smoke) + tutarlılık testleri.

Çalıştırma:  python -m pytest -q
(07_RISKLER_VE_KALITE.md test stratejisi: ML metrik regresyon, sabit seed.)
"""
from datetime import date

import pandas as pd

from core.datasource import DemoDataSource, load_parcels
from core.phenology import compute_metrics
from core.rules import predict

TODAY = date(2026, 6, 26)


def _pred_for(parcel):
    ts = DemoDataSource().get_timeseries(parcel, 2026, TODAY)
    m = compute_metrics(ts.frame, pd.Timestamp(TODAY))
    return predict(m, TODAY, parcel.region_code)


def test_all_parcels_produce_valid_prediction():
    for p in load_parcels():
        pred = _pred_for(p)
        assert 0 <= pred.remaining_days <= 120
        assert pred.ci_lower <= pred.remaining_days <= pred.ci_upper
        assert 0.0 <= pred.confidence <= 1.0
        assert pred.est_harvest >= TODAY
        assert pred.pheno_phase


def test_earlier_eos_means_fewer_remaining_days():
    """Daha erken EOS'lu parsel (cumra-01) daha geç olandan (cumra-06) önce hasat."""
    parcels = {p.id: p for p in load_parcels()}
    early = _pred_for(parcels["cumra-01"])   # eos_doy 182
    late = _pred_for(parcels["cumra-06"])    # eos_doy 206
    assert early.remaining_days <= late.remaining_days


def test_determinism():
    """Aynı seed → aynı sonuç (05_VERI §11 tekrarlanabilirlik)."""
    p = load_parcels()[0]
    assert _pred_for(p).remaining_days == _pred_for(p).remaining_days
