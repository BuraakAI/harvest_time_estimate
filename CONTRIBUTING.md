# Contributing

Thank you for helping improve HasadHaber. Contributions involving agronomy,
remote sensing, Python, testing, documentation, and accessibility are welcome.

## Before you start

- Search existing issues and pull requests first.
- Open an issue before beginning a large feature or model change.
- Never commit Earth Engine credentials, private parcel data, or personal data.
- Clearly label synthetic, simulated, and field-observed datasets.

## Development setup

```bash
git clone https://github.com/BuraakAI/harvest_time_estimate.git
cd harvest_time_estimate
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

## Pull requests

1. Keep each pull request focused on one problem.
2. Add or update tests for behavioral changes.
3. Update the README when installation, inputs, outputs, or assumptions change.
4. Explain the agronomic or technical rationale and cite primary sources when
   introducing a new index, threshold, or model assumption.
5. Confirm that `python -m pytest -q` passes locally.

For data contributions, describe collection date, crop, region, sensor,
processing steps, license, and anonymization method. Do not upload data unless
you have permission to redistribute it.
