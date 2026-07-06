"""Spektral indeks formül testleri (core/indices.py — canlı mod yardımcıları)."""
import numpy as np

from core.indices import ndmi, ndre, ndvi


def test_ndvi_known_values():
    nir = np.array([0.5, 0.4, 0.3])
    red = np.array([0.1, 0.4, 0.6])
    out = ndvi(nir, red)
    np.testing.assert_allclose(out, [(0.4 / 0.6), 0.0, (-0.3 / 0.9)], atol=1e-12)


def test_ndvi_range_bounded():
    rng = np.random.default_rng(42)
    nir, red = rng.uniform(0.01, 1, 100), rng.uniform(0.01, 1, 100)
    out = ndvi(nir, red)
    assert ((out >= -1) & (out <= 1)).all()


def test_zero_denominator_gives_nan():
    out = ndvi(np.array([0.0]), np.array([0.0]))
    assert np.isnan(out[0])


def test_ndmi_and_ndre_formulas():
    nir = np.array([0.6])
    np.testing.assert_allclose(ndmi(nir, np.array([0.2])), [0.5])
    np.testing.assert_allclose(ndre(nir, np.array([0.3])), [1 / 3])


def test_vegetation_brighter_nir():
    """Sağlıklı bitki: NIR >> Red → NDVI pozitif ve yüksek."""
    assert ndvi(np.array([0.7]), np.array([0.08]))[0] > 0.7
