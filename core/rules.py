"""Kural tabanlı hasat tahmini motoru (V1).

05_VERI_VE_MODELLEME.md §7.1 üç bileşeni birleştirir:
  1) Bölgesel takvim önseli (Konya kışlık buğday)
  2) NDVI tepe-sonrası düşüş kuralı
  3) NDMI kuruma sinyali
Güven skoru 04_TEKNIK_MIMARI.md §7.1'deki 4 bileşenli ağırlıklı toplamdır.

Bu motor ETİKETSİZ çalışır (Sedano 2025 ✅ — eğitim verisi gerektirmeyen
kural tabanlı tahıl hasadı tespiti; bkz. 12_LITERATUR §3).
"""
from __future__ import annotations

import calendar
from datetime import date, timedelta

import numpy as np
import pandas as pd

from .models import Prediction
from .phenology import PhenoMetrics

# --- Bölgesel önsel: Konya/Çumra kışlık buğday hasat penceresi -----------------
# 12_LITERATUR §9 doğrulama: Haziran sonu – Temmuz, sulu alanda Ağustos başı.
# (İl Tarım Müdürlüğü ürün takvimiyle resmî bağ hâlâ gerekli.)
REGION_HARVEST_WINDOW = {
    "TR-42-Konya-Cumra": (167, 213),   # ~16 Haziran – ~1 Ağustos (yıl-günü)
}
DEFAULT_WINDOW = (167, 213)

# NDVI'nin hasat olgunluğunda yaklaştığı taban seviye (senesens sonu).
NDVI_HARVEST_FLOOR = 0.25

# Güven skoru ağırlıkları (04 §7.1 — V1 heuristik; V2'de kalibre edilir).
W_COVERAGE, W_QUALITY, W_TEMPORAL, W_MODEL = 0.30, 0.20, 0.20, 0.30
NOMINAL_OBS = 18  # bir sezonda beklenen bulutsuz gözlem (~5 günde bir, kabaca)


def predict(metrics: PhenoMetrics, today: date, region_code: str) -> Prediction:
    """Fenoloji metriklerinden hasat tahmini üretir."""
    today_ts = pd.Timestamp(today)
    win_start, win_end = REGION_HARVEST_WINDOW.get(region_code, DEFAULT_WINDOW)

    phase = _phenology_phase(metrics)

    # --- Bileşen 1: bölgesel takvim önseli (penceredeki orta noktaya kalan gün)
    win_mid_doy = (win_start + win_end) // 2
    prior_harvest = _doy_to_date(today.year, win_mid_doy)
    rem_prior = (prior_harvest - today).days

    # --- Bileşen 2+3: sinyal tabanlı kalan gün (senesens eğimini ileri projekte et)
    rem_signal, signal_ok = _signal_remaining_days(metrics)

    # --- Birleştirme: sinyal güvenilirse ağırlığı yüksek, değilse önsele yaslan
    if signal_ok:
        remaining = int(round(0.6 * rem_signal + 0.4 * rem_prior))
    else:
        remaining = int(round(rem_prior))
    remaining = int(np.clip(remaining, 0, 120))

    # Bölgesel pencereyle tutarlılık: tahmin pencerenin çok dışındaysa kenara çek
    est_doy = today.timetuple().tm_yday + remaining
    est_doy = int(np.clip(est_doy, win_start, win_end + 14))
    est_harvest = _doy_to_date(today.year, est_doy)
    remaining = (est_harvest - today).days

    confidence, conf_parts = _confidence(metrics, signal_ok)

    # Güven aralığı: model belirsizliğiyle genişler (04 §7.1 model_uncertainty)
    half = int(round(3 + (1 - conf_parts["model_uncertainty_score"]) * 12))
    ci_lower, ci_upper = max(0, remaining - half), remaining + half

    reason_signals = {
        "ndvi_now": round(metrics.ndvi_now, 3),
        "ndmi_now": round(metrics.ndmi_now, 3),
        "ndvi_at_peak": round(metrics.max_ndvi, 3),
        "days_since_peak": metrics.days_since_pos,
        "slope_ndvi_last_14d": round(metrics.slope_last_14d, 4),
        "ndmi_drop_last_14d": round(metrics.ndmi_drop_last_14d, 3),
        "cloud_gap_days": metrics.cloud_gap_days,
        "n_obs": metrics.n_obs,
        "region_window": f"DOY {win_start}-{win_end}",
        "rule_fired": _which_rule(metrics),
        "confidence_parts": {k: round(v, 3) for k, v in conf_parts.items()},
    }

    return Prediction(
        parcel_id="",
        predicted_at=today,
        pheno_phase=phase,
        est_harvest=est_harvest,
        remaining_days=remaining,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        confidence=round(confidence, 3),
        reason_signals=reason_signals,
    )


# --- Fenolojik evre etiketi (01_VIZYON §6 evre listesi) ------------------------
def _phenology_phase(m: PhenoMetrics) -> str:
    pre_peak = m.days_since_pos is None or m.days_since_pos < 5
    if pre_peak and m.ndvi_now > 0.55:
        return "başaklanma" if m.ndvi_now < m.max_ndvi * 0.97 else "tepe dönem"
    if pre_peak:
        return "vejetatif"
    # tepe sonrası: NDVI seviyesine göre olgunlaşma evreleri
    n = m.ndvi_now
    if n >= 0.60:
        return "süt olum"
    if n >= 0.45:
        return "hamur olum"
    if n >= 0.32:
        return "sarı olum"
    return "olgun / hasat"


def _which_rule(m: PhenoMetrics) -> str:
    """05_VERI §7.1 hangi kuralın tetiklendiğini raporlar (açıklanabilirlik)."""
    fired = []
    if (m.days_since_pos or 0) >= 28 and m.ndvi_now < 0.45 and m.slope_last_14d < -0.005:
        fired.append("ndvi_decline")
    if m.ndmi_drop_last_14d > 0.15:
        fired.append("ndmi_drying")
    return "+".join(fired) if fired else "calendar_prior"


def _signal_remaining_days(m: PhenoMetrics) -> tuple[float, bool]:
    """Senesens eğimini NDVI tabanına kadar ileri projekte eder."""
    if m.slope_last_14d >= -0.001 or m.days_since_pos is None or m.days_since_pos < 10:
        # Henüz belirgin düşüş yok → sinyal güvenilmez, önsele bırak.
        return 60.0, False
    days = (m.ndvi_now - NDVI_HARVEST_FLOOR) / (-m.slope_last_14d)
    return float(np.clip(days, 0, 90)), True


# --- Güven skoru (04_TEKNIK_MIMARI.md §7.1) ------------------------------------
def _confidence(m: PhenoMetrics, signal_ok: bool) -> tuple[float, dict]:
    coverage = np.clip(m.n_obs / NOMINAL_OBS, 0, 1)
    data_quality = np.clip(1 - m.cloud_gap_days / 21, 0, 1)
    temporal = np.clip(1 - m.cloud_gap_days / 14, 0, 1)
    # model belirsizliği: net senesens sinyali varsa yüksek güven
    model_unc = 0.75 if signal_ok else 0.35
    parts = {
        "coverage_score": float(coverage),
        "data_quality_score": float(data_quality),
        "temporal_distance_score": float(temporal),
        "model_uncertainty_score": float(model_unc),
    }
    conf = (W_COVERAGE * coverage + W_QUALITY * data_quality
            + W_TEMPORAL * temporal + W_MODEL * model_unc)
    return float(np.clip(conf, 0, 1)), parts


def _doy_to_date(year: int, doy: int) -> date:
    max_doy = 366 if calendar.isleap(year) else 365
    doy = int(np.clip(doy, 1, max_doy))
    return date(year, 1, 1) + timedelta(days=doy - 1)
