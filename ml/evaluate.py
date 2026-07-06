"""Doğruluk değerlendirme çatısı — lead-time backtest.

05_VERI_VE_MODELLEME.md §8 metrikleri: MAE, RMSE, ±3/±7/±14 gün isabet, bias,
kapsama, güven aralığı kapsaması. Veri kaynağından BAĞIMSIZdır: demo (sentetik
etiket) ile bugün, canlı Sentinel-2 + saha etiketi ile yarın aynı kodla çalışır.

DÜRÜSTLÜK NOTU: Sentetik etiketle çalıştırıldığında bu, MOTORUN davranışını ve
ölçüm kodunun doğruluğunu gösterir — gerçek tarım doğruluğunu DEĞİL. Gerçek MAE
ancak saha hasat tarihleri + gerçek uydu verisiyle elde edilir.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from core.datasource import DATA_DIR
from core.phenology import compute_metrics
from core.rules import predict

# Hasat tarihinden kaç gün önce tahmin denenecek (sezon ilerledikçe doğruluk artar)
DEFAULT_LEADS = [40, 30, 20, 10, 5]

# Tez hedefleri (05_VERI §8) — UI'da kıyas için
TARGETS = {"mae": 10.0, "hit7": 0.60, "hit14": 0.90}


@dataclass
class EvalResult:
    n: int                       # üretilebilen tahmin sayısı
    mae: float                   # ortalama mutlak hata (gün)
    rmse: float
    bias: float                  # mean(ŷ - y); + => geç tahmin eğilimi
    hit3: float
    hit7: float
    hit14: float
    coverage: float              # tahmin üretilebilen oran (kapsama)
    ci_coverage: float           # gerçek hasadın güven aralığına düşme oranı
    per_lead_mae: dict           # {lead_gün: MAE}
    rows: pd.DataFrame           # parsel-bazlı ham kayıtlar


def load_labels(path: Path | None = None, min_confidence: float = 0.0) -> pd.DataFrame:
    """Etiketleri okur; `confidence` alanı düşük (belirsiz) kayıtları elemeye yarar.

    Saha etiketi geldiğinde kaynak güvenilirliği (üretici beyanı vs biçerdöver
    kaydı) bu alanla ifade edilir; `min_confidence` ile eşiklenir (05_VERI §3).
    """
    path = path or (DATA_DIR / "harvest_labels.csv")
    df = pd.read_csv(path, parse_dates=["harvest_date"])
    if "confidence" not in df.columns:
        df["confidence"] = 1.0
    return df[df["confidence"] >= min_confidence].reset_index(drop=True)


def backtest(parcels, labels: pd.DataFrame, source,
             leads: list[int] = DEFAULT_LEADS) -> EvalResult:
    """Her etiketli parsel-sezon için, her lead süresinde tahmin üretip hatayı ölçer."""
    pmap = {p.id: p for p in parcels}
    records = []
    for _, lab in labels.iterrows():
        parcel = pmap.get(lab["parcel_id"])
        if parcel is None:
            continue
        true_h = lab["harvest_date"].date()
        season = int(lab["season_year"])
        for lead in leads:
            today = true_h - timedelta(days=lead)
            ts = source.get_timeseries(parcel, season, today)
            if ts.n_obs < 3:                       # kapsama başarısız
                records.append({"parcel": parcel.id, "lead": lead, "producible": False})
                continue
            m = compute_metrics(ts.frame, pd.Timestamp(today))
            pr = predict(m, today, parcel.region_code)
            err = (pr.est_harvest - true_h).days   # işaretli: + => geç
            in_ci = (today + timedelta(days=pr.ci_lower)
                     <= true_h <= today + timedelta(days=pr.ci_upper))
            records.append({
                "parcel": parcel.id, "lead": lead, "producible": True,
                "gerçek_hasat": true_h.isoformat(),
                "tahmin": pr.est_harvest.isoformat(),
                "hata_gün": err, "mutlak_hata": abs(err),
                "veri_güveni": round(pr.confidence, 2), "ci_içinde": in_ci,
            })
    rows = pd.DataFrame(records)
    return _summarize(rows)


def _summarize(rows: pd.DataFrame) -> EvalResult:
    prod = rows[rows.get("producible", False) == True]  # noqa: E712
    n = len(prod)
    if n == 0:
        return EvalResult(0, float("nan"), float("nan"), float("nan"),
                          float("nan"), float("nan"), float("nan"),
                          0.0, float("nan"), {}, rows)
    abs_err = prod["mutlak_hata"].to_numpy(float)
    err = prod["hata_gün"].to_numpy(float)
    per_lead = {int(L): round(float(prod.loc[prod["lead"] == L, "mutlak_hata"].mean()), 2)
                for L in sorted(prod["lead"].unique())}
    return EvalResult(
        n=n,
        mae=round(float(np.mean(abs_err)), 2),
        rmse=round(float(np.sqrt(np.mean(err ** 2))), 2),
        bias=round(float(np.mean(err)), 2),
        hit3=round(float(np.mean(abs_err <= 3)), 3),
        hit7=round(float(np.mean(abs_err <= 7)), 3),
        hit14=round(float(np.mean(abs_err <= 14)), 3),
        coverage=round(float((rows.get("producible", False) == True).mean()), 3),  # noqa: E712
        ci_coverage=round(float(prod["ci_içinde"].mean()), 3),
        per_lead_mae=per_lead,
        rows=rows,
    )


if __name__ == "__main__":  # hızlı CLI: python -m ml.evaluate
    from core.datasource import DemoDataSource, load_parcels

    res = backtest(load_parcels(), load_labels(), DemoDataSource())
    print(f"n={res.n}  MAE={res.mae} gün  RMSE={res.rmse}  bias={res.bias}")
    print(f"±3:{res.hit3:.0%}  ±7:{res.hit7:.0%}  ±14:{res.hit14:.0%}  "
          f"kapsama:{res.coverage:.0%}  CI-kapsama:{res.ci_coverage:.0%}")
    print("lead→MAE:", res.per_lead_mae)
