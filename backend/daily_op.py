import pandas as pd
from database import op_collection, db

daily_op = db["daily_op"]

def build_daily_op():

    daily_op.delete_many({})

    temp = {}

    for r in op_collection.find():

        d = r.get("Visit Date")

        if not d:
            continue

        try:
            day = pd.to_datetime(d).strftime("%Y-%m-%d")
        except:
            continue

        temp.setdefault(day, 0)
        temp[day] += 1

    docs = [{"date": k, "count": v} for k, v in sorted(temp.items())]

    if docs:
        daily_op.insert_many(docs)

    return {"days": len(docs)}
