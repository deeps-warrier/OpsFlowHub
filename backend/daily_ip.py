import pandas as pd
from database import ip_collection, db

daily_ip = db["daily_ip"]

def build_daily_ip():

    daily_ip.delete_many({})

    temp = {}

    for r in ip_collection.find():

        d = r.get("Admission Date")

        try:
            day = pd.to_datetime(d).strftime("%Y-%m-%d")
        except:
            continue

        temp.setdefault(day, 0)
        temp[day] += 1

    docs = [{"date": k, "count": v} for k, v in temp.items()]

    if docs:
        daily_ip.insert_many(docs)

    return {"days": len(docs)}
