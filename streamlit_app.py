"""Streamlit Advertising Revenue Intelligence — synthetic portfolio data."""
from pathlib import Path
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Advertising Revenue Intelligence", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    if not (ROOT / "data" / "campaigns.csv").exists():
        subprocess.run([sys.executable, "-m", "src.generate_data"], cwd=ROOT, check=True)
    campaigns = pd.read_csv(ROOT / "data" / "campaigns.csv")
    advertisers = pd.read_csv(ROOT / "data" / "advertisers.csv")
    targets = pd.read_csv(ROOT / "data" / "sales_targets.csv")
    campaigns["start_date"] = pd.to_datetime(campaigns["start_date"])
    campaigns["month"] = campaigns["start_date"].dt.strftime("%Y-%m")
    campaigns = campaigns.merge(advertisers, on="advertiser_id", how="left", validate="many_to_one")
    return campaigns, targets

df, targets = load_data()
st.title("Advertising Revenue Intelligence")
st.caption("Interactive publisher advertising analytics | Synthetic demonstration data, not real company performance")

st.sidebar.header("Explore the data")
products = sorted(df["product"].dropna().unique())
industries = sorted(df["industry"].dropna().unique())
chosen_products = st.sidebar.multiselect("Advertising products", products, default=products)
chosen_industries = st.sidebar.multiselect("Advertiser industries", industries, default=industries)
months = sorted(df["month"].unique())
chosen_months = st.sidebar.multiselect("Months", months, default=months)
filtered = df[df["product"].isin(chosen_products) & df["industry"].isin(chosen_industries) & df["month"].isin(chosen_months)].copy()
if filtered.empty:
    st.warning("No campaigns match these filters. Adjust the sidebar selections.")
    st.stop()

money = lambda n: f"${n:,.0f}"
revenue = filtered["booked_revenue"].sum()
digital = filtered[filtered["product"] != "Print"]
impressions = digital["impressions"].sum()
clicks = digital["clicks"].sum()
conversions = digital["conversions"].sum()
ctr = 100 * clicks / impressions if impressions else 0
conversion_rate = 100 * conversions / clicks if clicks else 0

page = st.sidebar.radio("Dashboard page", ["Revenue Overview", "Campaign Performance", "Advertiser Intelligence", "Data Explorer"])
if page == "Revenue Overview":
    st.subheader("Revenue Overview")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Booked revenue", money(revenue))
    c2.metric("Campaigns", f"{len(filtered):,}")
    c3.metric("Active advertisers", filtered["advertiser_id"].nunique())
    c4.metric("Digital CTR", f"{ctr:.2f}%")
    monthly = filtered.groupby("month",as_index=False)["booked_revenue"].sum()
    monthly = monthly.merge(targets, on="month", how="left")
    monthly["attainment_pct"] = 100 * monthly["booked_revenue"] / monthly["target_revenue"]
    left,right=st.columns([1.6,1])
    with left:
        fig=px.line(monthly,x="month",y=["booked_revenue","target_revenue"],markers=True,title="Monthly booked revenue vs sales target",labels={"value":"USD","variable":"Measure","month":"Month"})
        st.plotly_chart(fig,use_container_width=True)
    with right:
        by_product=filtered.groupby("product",as_index=False)["booked_revenue"].sum().sort_values("booked_revenue")
        st.plotly_chart(px.bar(by_product,x="booked_revenue",y="product",orientation="h",title="Booked revenue by product",labels={"booked_revenue":"USD","product":""}),use_container_width=True)
    st.subheader("Monthly sales performance")
    st.dataframe(monthly.rename(columns={"booked_revenue":"Booked revenue","target_revenue":"Target revenue","attainment_pct":"Target attainment (%)"}),use_container_width=True,hide_index=True)
    st.info("Targets are synthetic full-month benchmarks. Filtering by industry/product makes attainment a segment-to-total-target comparison, not an adjusted segment target.")
elif page == "Campaign Performance":
    st.subheader("Campaign Performance")
    a,b,c,d=st.columns(4)
    a.metric("Digital impressions",f"{impressions:,.0f}")
    b.metric("Digital clicks",f"{clicks:,.0f}")
    c.metric("Digital conversions",f"{conversions:,.0f}")
    d.metric("Click-to-conversion rate",f"{conversion_rate:.2f}%")
    by_product=digital.groupby("product",as_index=False)[["impressions","clicks","conversions"]].sum()
    by_product["CTR (%)"]=100*by_product["clicks"]/by_product["impressions"].replace(0,float("nan"))
    l,r=st.columns(2)
    with l:st.plotly_chart(px.bar(by_product,x="product",y="CTR (%)",title="Digital CTR by product"),use_container_width=True)
    with r:st.plotly_chart(px.bar(by_product,x="product",y="conversions",title="Digital conversions by product"),use_container_width=True)
    st.dataframe(by_product,use_container_width=True,hide_index=True)
    st.caption("Print is excluded from click/impression KPIs because these digital metrics are not defined for print placements.")
elif page == "Advertiser Intelligence":
    st.subheader("Advertiser Intelligence")
    grouped=filtered.groupby(["advertiser_id","advertiser_name","industry"],as_index=False).agg(booked_revenue=("booked_revenue","sum"),campaigns=("campaign_id","count"),products_used=("product","nunique"))
    max_revenue=grouped["booked_revenue"].max()
    max_count=grouped["campaigns"].max()
    grouped["opportunity_score"]=(50*grouped["booked_revenue"]/max_revenue+30*grouped["campaigns"]/max_count+20*(1-grouped["products_used"]/4)).round(1)
    grouped=grouped.sort_values("opportunity_score",ascending=False)
    l,r=st.columns(2)
    with l:st.plotly_chart(px.bar(grouped.nlargest(12,"booked_revenue"),x="booked_revenue",y="advertiser_name",orientation="h",title="Top advertisers by booked revenue"),use_container_width=True)
    with r:st.plotly_chart(px.scatter(grouped,x="campaigns",y="booked_revenue",size="opportunity_score",color="industry",hover_name="advertiser_name",title="Advertiser portfolio overview"),use_container_width=True)
    st.subheader("Cross-sell opportunity ranking")
    st.dataframe(grouped,use_container_width=True,hide_index=True)
    st.caption("Opportunity score is an illustrative ranking heuristic, not a validated predictive model. Scores change with the selected filters.")
else:
    st.subheader("Campaign Data Explorer")
    search=st.text_input("Search campaign or advertiser")
    shown=filtered
    if search:
        mask=filtered["campaign_id"].astype(str).str.contains(search,case=False,regex=False)|filtered["advertiser_name"].astype(str).str.contains(search,case=False,regex=False)
        shown=filtered[mask]
    st.dataframe(shown,use_container_width=True,hide_index=True)
    st.download_button("Download filtered campaign data (CSV)",data=shown.to_csv(index=False).encode("utf-8"),file_name="filtered_ad_campaigns.csv",mime="text/csv")
st.divider()
st.caption("Data: deterministic synthetic advertising campaigns. Booked revenue is not recognized revenue. Built with Streamlit, Pandas and Plotly.")
