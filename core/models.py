"""Veri modelleri (dataclass).

04_TEKNIK_MIMARI.md §5 veritabanı şemasının hafif, bellek-içi karşılığıdır.
Faz 3'te bu yapılar SQLAlchemy/Pydantic modellerine taşınır.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import pandas as pd


@dataclass
class Parcel:
    """Bir tarla parseli. Şemada `parcels` tablosuna karşılık gelir."""

    id: str
    name: str
    crop_code: str            # 'WHEAT_WINTER'
    region_code: str          # 'TR-42-Konya-Cumra'
    area_ha: float
    planted_at: Optional[date]
    centroid: tuple[float, float]          # (lat, lon)
    polygon: list[list[float]]             # [[lon, lat], ...] (GeoJSON sırası)
    # Demo modunda sentetik eğri üretmek için fenoloji parametreleri:
    _demo_params: dict = field(default_factory=dict, repr=False)


@dataclass
class TimeSeries:
    """Bir parsel-sezon için indeks zaman serisi.

    `frame` sütunları: date, ndvi, ndmi, vh  (eksik gözlem = NaN, bulut boşluğu).
    """

    parcel_id: str
    season_year: int
    frame: pd.DataFrame
    n_obs: int
    cloud_pct: float


@dataclass
class Prediction:
    """predictions tablosunun karşılığı (04_TEKNIK_MIMARI.md §5)."""

    parcel_id: str
    predicted_at: date
    pheno_phase: str
    est_harvest: date
    remaining_days: int
    ci_lower: int
    ci_upper: int
    confidence: float                # 0..1
    reason_signals: dict             # JSONB karşılığı (04 §8.1)
