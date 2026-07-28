import pandas as pd
from database import revenue_collection, db
from revenue_logic import normalize_revenue_row

daily_collection = db["daily_revenue"]

def build_daily_revenue():

    daily_collection.delete_many({})
    print("Old daily data cleared")

    temp = {}
    total_rows = revenue_collection.count_documents({})
    print("Total revenue rows:", total_rows)

    for r in revenue_collection.find():

        d = r.get("BillDate")

        if not d:
            continue

        try:
            day = pd.to_datetime(d).strftime("%Y-%m-%d")
        except Exception as e:
            print("Date error:", d)
            continue

        try:
            _, _, amt = normalize_revenue_row(r)
        except Exception as e:
            print("Amount error:", e)
            continue

        temp.setdefault(day, 0)
        temp[day] += amt

    docs = [{"date": k, "total": v} for k, v in temp.items()]

    print("Days generated:", len(docs))

    if docs:
        daily_collection.insert_many(docs)

    return {"days": len(docs)}
