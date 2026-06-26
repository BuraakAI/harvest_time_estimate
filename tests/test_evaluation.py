"""Değerlendirme çatısı testleri.

Amaç: ölçüm KODUNUN doğru olduğunu kanıtlamak (model doğruluğunu değil).
"""
import numpy as np
import pandas as pd

from core.datasource import DemoDataSource, load_parcels
from ml.evaluate import _summarize, backtest, load_labels


def test_backtest_runs_and_metrics_in_range():
    res = backtest(load_parcels(), load_labels(), DemoDataSource())
    assert res.n > 0
    assert np.isfinite(res.mae) and res.mae >= 0
    for h in (res.hit3, res.hit7, res.hit14, res.coverage, res.ci_coverage):
        assert 0.0 <= h <= 1.0
    assert res.hit3 <= res.hit7 <= res.hit14          # iç tutarlılık
    assert set(res.per_lead_mae)                       # lead kırılımı dolu


def test_accuracy_improves_near_harvest():
    """Hasada yakın (kısa lead) tahmin, uzak tahminden daha iyi olmalı."""
    res = backtest(load_parcels(), load_labels(), DemoDataSource())
    leads = sorted(res.per_lead_mae)
    assert res.per_lead_mae[leads[0]] <= res.per_lead_mae[leads[-1]]


def test_perfect_predictions_give_zero_mae():
    """Saf metrik mantığı: hata=0 olduğunda MAE=0, isabet=%100."""
    rows = pd.DataFrame([
        {"parcel": "x", "lead": 10, "producible": True, "hata_gün": 0,
         "mutlak_hata": 0, "ci_içinde": True},
        {"parcel": "y", "lead": 10, "producible": True, "hata_gün": 0,
         "mutlak_hata": 0, "ci_içinde": True},
    ])
    res = _summarize(rows)
    assert res.mae == 0 and res.hit7 == 1.0 and res.ci_coverage == 1.0
