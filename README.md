# Advertising Revenue & Sales Intelligence

**Portfolio project with deterministic synthetic data. Not SME company data.**

Analyze booked advertising revenue, digital campaign CTR, monthly sales target attainment, and advertiser cross-sell opportunities across print, display, newsletters, and sponsored content.

## Quick start
Python 3.10+, no external packages.

```bash
python -m src.generate_data
python -m src.analyze
python -m unittest discover -s tests -v
```

Open `dashboard/index.html` after running analysis. Reports are generated in `reports/`.

## KPI definitions
- Booked revenue: sum of campaign booking amounts; **not** recognized revenue.
- CTR: digital clicks divided by digital impressions, excluding print.
- Target attainment: monthly booked revenue divided by synthetic sales target.
- Opportunity score: illustrative heuristic based on advertiser spend, campaign frequency, and product coverage. It is **not** a predicted renewal probability.

## Architecture
Synthetic CSV campaign and advertiser exports → Python KPI aggregation → monthly CSV reports + HTML business dashboard.

## Limitations
Synthetic figures are for demonstration only. Print circulation is not comparable with digital impressions. A production system would reconcile booked and recognized revenue and use CRM/ad-server data.
