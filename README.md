# Advertising Revenue Intelligence — Streamlit Dashboard

## Live dashboard

**[Open the interactive Streamlit dashboard](https://advertising-revenue-intelligence-e6kkqr5kh9rrdg3fnwqmmu.streamlit.app/)**


**Live interactive BI portfolio app** built with Streamlit, Plotly and Pandas. All data is **synthetic** and does not represent a real publisher or SME.

## Dashboard pages
- **Revenue Overview** — booked revenue, campaign count, active advertisers, monthly target comparison and revenue by product
- **Campaign Performance** — digital impressions, clicks, conversions, CTR and click-to-conversion rate
- **Advertiser Intelligence** — top accounts, revenue contribution, and an illustrative cross-sell ranking
- **Data Explorer** — searchable campaign records, multi-select filters and CSV export

## Launch locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

On first launch, the app generates **500 deterministic synthetic campaigns** from `src/generate_data.py`. No API keys or paid accounts required.

## Deploy free to Streamlit Community Cloud
1. Go to https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app** → **Deploy a public app from GitHub**.
3. Select repository `chandralekharavikanti/advertising-revenue-intelligence`, branch `main`, main file `streamlit_app.py`.
4. Click **Deploy**. Share the generated public URL with recruiters.

## KPI definitions
- **Booked revenue** = sum of campaign bookings, not recognized revenue.
- **CTR** = digital clicks / digital impressions × 100, excluding print.
- **Click-to-conversion rate** = digital conversions / digital clicks × 100.
- **Target attainment** = filtered monthly bookings / full-month synthetic target; segment filters do not adjust the target.
- **Opportunity score** = 50 × normalized account spend + 30 × normalized campaign count + 20 × (1 − products used / 4). A descriptive heuristic, **not** a trained model.

## Additional materials
`src/analyze.py` and `sql/revenue_analysis.sql` contain the original reporting workflow and SQL examples. The Streamlit app is the primary interactive presentation.

## Limitations
All data and insights are illustrative. Print circulation is not equivalent to digital impressions; the application excludes print from digital CTR metrics. The app does not use Power BI or Tableau.
