import csv,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(filename):
 with (ROOT/"data"/filename).open(newline="") as f:return list(csv.DictReader(f))
def analyze():
 campaigns=load("campaigns.csv"); advertisers={a["advertiser_id"]:a for a in load("advertisers.csv")}
 targets={x["month"]:float(x["target_revenue"]) for x in load("sales_targets.csv")}
 monthly=collections.defaultdict(float);products=collections.defaultdict(float);accounts=collections.defaultdict(list)
 for c in campaigns:
  amount=float(c["booked_revenue"]);monthly[c["start_date"][:7]]+=amount;products[c["product"]]+=amount;accounts[c["advertiser_id"]].append(c)
 digital=[c for c in campaigns if c["product"]!="Print"]
 impressions=sum(int(c["impressions"]) for c in digital);clicks=sum(int(c["clicks"]) for c in digital)
 kpis={"booked_revenue":round(sum(products.values()),2),"campaign_count":len(campaigns),"advertisers":len(accounts),"digital_ctr_pct":round(100*clicks/impressions,2) if impressions else 0}
 performance=[{"month":m,"booked_revenue":round(monthly[m],2),"target":target,"attainment_pct":round(100*monthly[m]/target,1) if target else None} for m,target in sorted(targets.items())]
 max_spend=max(sum(float(c["booked_revenue"]) for c in rows) for rows in accounts.values())
 max_count=max(map(len,accounts.values()))
 opportunities=[]
 for aid,rows in accounts.items():
  spend=sum(float(c["booked_revenue"]) for c in rows);coverage=len({c["product"] for c in rows})
  score=round(50*spend/max_spend+30*len(rows)/max_count+20*(1-coverage/4),1)
  opportunities.append({"advertiser":advertisers[aid]["advertiser_name"],"industry":advertisers[aid]["industry"],"booked_revenue":round(spend,2),"campaigns":len(rows),"products_used":coverage,"opportunity_score":score})
 opportunities.sort(key=lambda x:x["opportunity_score"],reverse=True)
 reports=ROOT/"reports";reports.mkdir(exist_ok=True)
 for filename,rows in [("monthly_performance.csv",performance),("opportunity_scores.csv",opportunities)]:
  with (reports/filename).open("w",newline="") as f:
   w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 payload={"kpis":kpis,"monthly":performance,"products":[{"name":k,"revenue":round(v,2)} for k,v in products.items()],"opportunities":opportunities[:10]}
 (reports/"summary.json").write_text(json.dumps(payload,indent=2))
 template=(ROOT/"dashboard/template.html").read_text()
 (ROOT/"dashboard/index.html").write_text(template.replace("__DATA__",json.dumps(payload).replace("<","\\u003c")))
 return payload
if __name__=="__main__":
 print(json.dumps(analyze()["kpis"],indent=2))
