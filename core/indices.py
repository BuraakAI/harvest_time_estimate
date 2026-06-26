"""Spektral indeks hesaplama (CANLI mod için).

05_VERI_VE_MODELLEME.md §5 indeks paletinin çekirdek alt kümesi.
Demo modunda kullanılmaz; GEE/STAC adapteri bant verisi getirince devreye girer.
"""
from __future__ import annotations

import numpy as np


def ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """(NIR - Red) / (NIR + Red) — genel canlılık."""
    nir, red = np.asarray(nir, float), np.asarray(red, float)
    return _safe_ratio(nir - red, nir + red)


def ndmi(nir: np.ndarray, swir1: np.ndarray) -> np.ndarray:
    """(NIR - SWIR1) / (NIR + SWIR1) — kanopi su içeriği, olgunlaşmada düşer."""
    nir, swir1 = np.asarray(nir, float), np.asarray(swir1, float)
    return _safe_ratio(nir - swir1, nir + swir1)


def ndre(nir: np.ndarray, red_edge: np.ndarray) -> np.ndarray:
    """(NIR - RedEdge) / (NIR + RedEdge) — klorofil/senesens duyarlı."""
    nir, red_edge = np.asarray(nir, float), np.asarray(red_edge, float)
    return _safe_ratio(nir - red_edge, nir + red_edge)


def _safe_ratio(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    out = np.full_like(num, np.nan, dtype=float)
    mask = den != 0
    out[mask] = num[mask] / den[mask]
    return out
