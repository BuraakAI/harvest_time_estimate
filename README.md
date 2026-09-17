# HasadHaber

[![Tests](https://github.com/BuraakAI/harvest_time_estimate/actions/workflows/tests.yml/badge.svg)](https://github.com/BuraakAI/harvest_time_estimate/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

An open, reproducible decision-support prototype that estimates a field's
harvest window from satellite time series. The current pilot models winter
wheat parcels in Çumra, Konya, Türkiye.

HasadHaber combines vegetation indices, phenology signals, and an explainable
rule engine to answer a practical question: **how many days remain until the
estimated harvest date?**

> [!IMPORTANT]
> This is a research prototype, not an agronomic recommendation system. The
> bundled demo data and harvest labels are synthetic. Validate the model with
> local field observations before using its output in operational decisions.

## Why this project exists

Harvest timing affects machinery planning, labor, storage, and crop quality.
Many small agricultural teams do not have a transparent way to combine remote
sensing signals with field observations. This project keeps the full decision
path inspectable and provides an offline demo that anyone can reproduce.

## Features

- Parcel-level estimated harvest date, remaining days, growth stage, and
  confidence score.
- NDVI, NDMI, and Sentinel-1 VH time-series visualization.
- Explainable rules that show which signals influenced each estimate.
- Cooperative view with parcel priority and weekly harvest workload.
- Offline synthetic-data mode with no account or API credentials required.
- Optional live Sentinel-1 and Sentinel-2 ingestion through Google Earth
  Engine.
- Lead-time backtesting with MAE, RMSE, bias, coverage, and tolerance metrics.

## Quick start

Requirements: Python 3.11 or newer.

```bash
git clone https://github.com/BuraakAI/harvest_time_estimate.git
cd harvest_time_estimate
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`. The default demo generates a realistic synthetic
season for ten sample parcels and works completely offline.

## Run the tests

```bash
python -m pytest -q
```

The suite covers data sources, spectral indices, phenology extraction, the
rule engine, and evaluation metrics.

## Optional: live Earth Engine data

The demo requires no credentials. To use real Sentinel data:

```bash
python -m pip install -r requirements-gee.txt
earthengine authenticate
export EE_PROJECT="your-google-cloud-project-id"
streamlit run app.py
```

Alternatively, store the project ID in `data/ee_project.txt`. That file and the
local cache are excluded from Git.

Live mode retrieves cloud-masked `COPERNICUS/S2_SR_HARMONIZED` observations and
`COPERNICUS/S1_GRD` VH data for each parcel. The core phenology and rule modules
remain independent of the selected data source.

## Architecture

```text
harvest_time_estimate/
├── app.py                 # Streamlit application
├── core/
│   ├── datasource.py      # Synthetic and Earth Engine adapters
│   ├── indices.py         # Vegetation-index calculations
│   ├── phenology.py       # Smoothing and SOS/POS/EOS extraction
│   └── rules.py           # Explainable harvest-window rules
├── ml/
│   ├── evaluate.py        # Lead-time backtesting
│   └── validate_t207.py   # Field-validation workflow
├── data/                  # Sample parcels and synthetic labels
└── tests/                 # Pytest suite
```

The current estimator is deliberately rule-based. This makes assumptions and
failure modes visible while a reliable field-labelled dataset is being built.
Random forest, gradient boosting, or deep-learning models should only be added
after sufficient real observations are available.

## Evaluation and data transparency

`python -m ml.evaluate` evaluates predictions at several lead times before the
recorded harvest date. The included `data/harvest_labels.csv` is synthetic and
demonstrates the evaluation pipeline—it does **not** establish field accuracy.

Credible validation requires:

1. Real harvest dates from growers, cooperatives, or machinery records.
2. A documented train/validation split across fields and seasons.
3. Reporting errors by crop, region, season, and observation coverage.
4. Comparison against simple baselines, not only increasingly complex models.

## Project status

The repository is an early-stage research prototype. Near-term priorities are:

- add anonymized, field-validated sample data;
- document agronomic assumptions and supported crop/region boundaries;
- add reproducible notebooks for index and phenology inspection;
- expand tests for missing observations and cloudy seasons;
- package the reusable core separately from the Streamlit interface.

## Contributing

Bug reports, tests, documentation, and agronomy or remote-sensing review are
welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
Please report security issues according to [SECURITY.md](SECURITY.md).

## License

Licensed under the [Apache License 2.0](LICENSE).
