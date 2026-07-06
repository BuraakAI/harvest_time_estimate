"""T-207 — 10 parsel manuel doğrulama tablosu üretici.

Faz 2 kapı kriteri G2 (03_FAZLAR): "10 parsel manuel doğrulama tablosu var".
Gerçek (GEE, Sentinel-2) veriyle tahmin üretir, demo tahminiyle yan yana koyar,
markdown tablo + parsel başına NDVI karşılaştırma grafiği çıkarır.

ADR-B-015 UYARISI: Saha hasat etiketi OLMADIĞI için bu tablo doğruluk (MAE)
İDDİASI taşımaz. Doğruladığı şey: (1) gerçek uydu verisiyle uçtan uca akışın
çalıştığı, (2) fenolojinin makul olduğu (ilkbahar tepe → Haziran senesens),
(3) tahminlerin bölgesel hasat penceresi içinde kaldığı.

Çalıştırma (repo kökünden, GEE kimliği hazırken):
    python -m ml.validate_t207 [--today YYYY-MM-DD] [--out DIZIN]
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

from core.datasource import DemoDataSource, GEEDataSource, load_parcels
from core.phenology import compute_metrics, smooth_series
from core.rules import REGION_HARVEST_WINDOW, predict

DEFAULT_OUT = Path(__file__).resolve().parent.parent.parent / "staj-omurga"


def build_rows(parcels, gee, demo, season: int, today: date) -> list[dict]:
    rows = []
    for p in parcels:
        ts_g = gee.get_timeseries(p, season, today)
        m_g = compute_metrics(ts_g.frame, pd.Timestamp(today))
        pr_g = predict(m_g, today, p.region_code)

        ts_d = demo.get_timeseries(p, season, today)
        m_d = compute_metrics(ts_d.frame, pd.Timestamp(today))
        pr_d = predict(m_d, today, p.region_code)

        win = REGION_HARVEST_WINDOW.get(p.region_code)
        in_window = win[0] <= pr_g.est_harvest.timetuple().tm_yday <= win[1] + 14

        rows.append({
            "parcel": p, "ts_gee": ts_g, "pred_gee": pr_g, "metrics_gee": m_g,
            "ts_demo": ts_d, "pred_demo": pr_d,
            "in_window": in_window,
        })
    return rows


def _wheat_verdict(m) -> tuple[bool, str]:
    """Eğri kışlık buğday fenolojisine uyuyor mu? (wheat_like, değerlendirme)."""
    if m.slope_last_14d < -0.003 and m.ndvi_now < 0.45:
        return True, "Belirgin senesens — hasat sinyali güçlü, tahmin sinyal ağırlıklı"
    if m.ndvi_now < 0.30 and m.slope_last_14d <= 0.003:
        return True, "NDVI tabana yakın — hasat olmuş/çok yakın olabilir"
    if m.slope_last_14d > 0.005:
        return False, ("❌ NDVI hasat penceresinde hâlâ YÜKSELİYOR — kışlık buğday deseni değil; "
                       "yazlık ürün (mısır/pancar/ayçiçeği) olasılığı yüksek. Tahmin yalnız takvim önseli")
    return True, "Senesens kısmi — tahmin takvim önseli ağırlıklı, izlenmeli"


def render_markdown(rows, season: int, today: date) -> str:
    verdicts = {r["parcel"].id: _wheat_verdict(r["metrics_gee"]) for r in rows}
    n_wheat = sum(1 for ok, _ in verdicts.values() if ok)
    n = len(rows)

    lines = [
        "# T-207 — 10 Parsel Manuel Doğrulama Tablosu (Gerçek Sentinel-2)",
        "",
        f"> **Üretim:** `python -m ml.validate_t207` · veri: GEE `COPERNICUS/S2_SR_HARMONIZED`",
        f"> (SCL bulut maskesi) + `S1_GRD` VH · sezon {season} · tahmin tarihi **{today.isoformat()}**.",
        "> **Kapsam:** Faz 2 kapı kriteri G2 — \"10 parsel manuel doğrulama tablosu var\".",
        "",
        "## ⚠️ Kalibre edilmemiş — doğruluk iddiası yok (ADR-B-015)",
        "",
        "Saha hasat etiketi henüz YOK. Bu tablo **MAE / ±gün isabet iddiası taşımaz**.",
        "Doğruladığı şeyler:",
        "",
        "1. Gerçek uydu verisiyle uçtan uca akış (GEE → fenoloji → kural → tahmin) hatasız çalışıyor.",
        "2. Tahminler bölgesel hasat penceresi (DOY 167–213 + tolerans) içinde kalıyor.",
        "",
        "Sentetik `harvest_labels.csv` GERÇEK veriye kıyas ölçütü değildir; 'demo tahmini' sütunu",
        "yalnız iki veri kaynağının aynı motordan geçtiğini gösterir.",
        "",
        "## 🔴 Ana bulgu: ürün deseni uyuşmazlığı",
        "",
        f"Gerçek NDVI eğrisi kışlık buğday fenolojisine {n_wheat}/{n} parselde uyuyor.",
        "",
    ]
    if n_wheat < n:
        lines += [
            "Uymayan parsellerde NDVI, buğday hasat penceresi içinde hâlâ **yükseliyor** —",
            "kışlık buğdayda bu dönemde eğri düşer. Yorum: Bu OSM `farmland` parselleri bu",
            "sezon büyük olasılıkla **yazlık ürün** (Çumra sulu tarımında yaygın: mısır, şeker",
            "pancarı, ayçiçeği) ekilmiş; `crop_code=WHEAT_WINTER` varsayımı bu parseller için",
            "bu sezon GEÇERLİ DEĞİL. Bu tam da T-207'nin yakalaması gereken türden bir bulgudur",
            "ve kural motorunun neden **ekin doğrulaması** (ÇKS kaydı / üretici beyanı) olmadan",
            "kullanılamayacağını gösterir (07_RISKLER R-02 veri riski).",
            "",
            "**Aksiyon:** Faz 2 kapanışında pilot parsel listesi, ekimi ÇKS/üretici beyanıyla",
            "doğrulanmış GERÇEK buğday parselleriyle değiştirilmeli (T-002/T-003 veri talebi).",
            "Akış ve motor hazır; yalnız doğru parseller + saha etiketi gerekiyor.",
            "",
        ]
    lines += [
        "## Özet tablo",
        "",
        "| Parsel | Alan (ha) | Gözlem (bulutsuz) | Bulut % | POS (DOY) | Evre | Tahmini hasat (GERÇEK S2) | Kalan gün | Veri güveni | Pencere içi? | Demo tahmini (kıyas) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        p, prg, prd, m, ts = r["parcel"], r["pred_gee"], r["pred_demo"], r["metrics_gee"], r["ts_gee"]
        lines.append(
            f"| {p.name} | {p.area_ha} | {ts.n_obs} | {ts.cloud_pct:.0f} | "
            f"{m.pos_doy if m.pos_doy is not None else '—'} | {prg.pheno_phase} | "
            f"**{prg.est_harvest.isoformat()}** | {prg.remaining_days} "
            f"({prg.ci_lower}–{prg.ci_upper}) | %{prg.confidence*100:.0f} | "
            f"{'✅' if r['in_window'] else '❌'} | {prd.est_harvest.isoformat()} |"
        )

    n_ok = sum(r["in_window"] for r in rows)
    lines += [
        "",
        f"**Pencere tutarlılığı:** {n_ok}/{len(rows)} parsel bölgesel hasat penceresi içinde.",
        "",
        "## Manuel kontrol notları (parsel başına)",
        "",
        "Grafikler: `gorseller/t207_ndvi_karsilastirma.png` — yeşil noktalar gerçek S2 NDVI",
        "gözlemi, yeşil çizgi yumuşatılmış eğri, gri kesik çizgi demo (sentetik) eğri,",
        "kırmızı dikey çizgi gerçek-veri tahmini hasat tarihi.",
        "",
        "| Parsel | Gerçek eğri gözlemi | Değerlendirme |",
        "|---|---|---|",
    ]
    for r in rows:
        p, m = r["parcel"], r["metrics_gee"]
        obs_note = (
            f"POS DOY {m.pos_doy}, max NDVI {m.max_ndvi:.2f}, "
            f"son NDVI {m.ndvi_now:.2f}, 14g eğim {m.slope_last_14d:+.4f}"
        )
        verdict = verdicts[p.id][1]
        lines.append(f"| {p.name} | {obs_note} | {verdict} |")

    lines += [
        "",
        "![T-207 NDVI karşılaştırma](gorseller/t207_ndvi_karsilastirma.png)",
        "",
        "## Sonraki adım",
        "",
        "- Gerçek saha hasat tarihleri (üretici/kooperatif/biçerdöver kaydı) `data/harvest_labels.csv`'ye",
        "  `source=field` olarak girildiğinde aynı backtest kodu GERÇEK MAE üretir (≥30 etiket → Faz 4).",
        "",
        "---",
        f"*Üretim tarihi: {date.today().isoformat()} · kod: `hasat-zamani/ml/validate_t207.py`*",
    ]
    return "\n".join(lines)


def render_chart(rows, today: date, out_png: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(rows)
    ncols, nrows = 2, (n + 1) // 2
    fig, axes = plt.subplots(nrows, ncols, figsize=(13, 3.0 * nrows), sharey=True)
    axes = axes.flatten()
    for ax, r in zip(axes, rows):
        p = r["parcel"]
        fg, fd = r["ts_gee"].frame, r["ts_demo"].frame
        sm_g = smooth_series(fg, "ndvi")
        sm_d = smooth_series(fd, "ndvi")
        ax.plot(fg["date"], fg["ndvi"], "o", ms=3, color="#2ca02c", alpha=0.6,
                label="S2 NDVI (gerçek gözlem)")
        ax.plot(sm_g.index, sm_g.values, "-", color="#2ca02c", lw=1.8,
                label="gerçek (yumuşatılmış)")
        ax.plot(sm_d.index, sm_d.values, "--", color="#999", lw=1.2, label="demo (sentetik)")
        ax.axvline(pd.Timestamp(r["pred_gee"].est_harvest), color="#d62728", lw=1.4)
        ax.axvline(pd.Timestamp(today), color="#444", ls=":", lw=1)
        ax.set_title(f"{p.name} → tahmin {r['pred_gee'].est_harvest.isoformat()}", fontsize=10)
        ax.set_ylim(0, 1)
    for ax in axes[n:]:
        ax.set_visible(False)
    axes[0].legend(fontsize=7, loc="upper left")
    fig.suptitle("T-207 — Gerçek Sentinel-2 NDVI vs demo eğrisi (kırmızı: tahmini hasat)", y=1.0)
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=140, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    ap.add_argument("--season", type=int, default=None)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    season = args.season or args.today.year

    gee = GEEDataSource()
    ok, why = gee.check_ready()
    if not ok:
        raise SystemExit(f"GEE hazır değil: {why}")

    parcels = load_parcels()
    rows = build_rows(parcels, gee, DemoDataSource(), season, args.today)

    md_path = args.out / "18_T207_DOGRULAMA_TABLOSU.md"
    png_path = args.out / "gorseller" / "t207_ndvi_karsilastirma.png"
    render_chart(rows, args.today, png_path)
    md_path.write_text(render_markdown(rows, season, args.today), encoding="utf-8")
    print(f"yazıldı: {md_path}")
    print(f"yazıldı: {png_path}")


if __name__ == "__main__":
    main()
