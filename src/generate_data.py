"""Deterministic synthetic advertising portfolio data."""
import csv,random
from pathlib import Path
random.seed(24)
root=Path(__file__).resolve().parents[1]/"data"
root.mkdir(exist_ok=True)
def write(name,fields,rows):
 with (root/name).open("w",newline="") as f:
  w=csv.writer(f);w.writerow(fields);w.writerows(rows)
products=["Print","Display","Newsletter","Sponsored Content"]
write("advertisers.csv",["advertiser_id","advertiser_name","industry"],[(f"A{i:03d}",f"Advertiser {i}",random.choice(["Manufacturing","Technology","Automotive","Industrial"])) for i in range(1,51)])
write("sales_targets.csv",["month","target_revenue"],[(f"2025-{m:02d}",200000) for m in range(1,13)])
rows=[]
for i in range(1,501):
 product=random.choice(products);impressions=random.randint(5000,250000) if product!="Print" else 0
 clicks=int(impressions*random.uniform(.003,.035));conversions=int(clicks*random.uniform(.01,.12))
 rows.append((f"C{i:04d}",f"A{random.randint(1,50):03d}",f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}",product,random.randint(1000,12000),impressions,clicks,conversions))
write("campaigns.csv",["campaign_id","advertiser_id","start_date","product","booked_revenue","impressions","clicks","conversions"],rows)
print("Generated",len(rows),"synthetic campaigns")
