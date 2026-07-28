import pandas as pd
from database import db

daily_rev = db["daily_revenue"]
daily_op = db["daily_op"]
daily_ip = db["daily_ip"]

monthly_rev = db["monthly_revenue"]
monthly_op = db["monthly_op"]
monthly_ip = db["monthly_ip"]


def build_monthly():

    monthly_rev.delete_many({})
    monthly_op.delete_many({})
    monthly_ip.delete_many({})

    rev_temp = {}
    op_temp = {}
    ip_temp = {}

    # Revenue
    for r in daily_rev.find():
        m = r["date"][:7]   # YYYY-MM
        rev_temp.setdefault(m, 0)
        rev_temp[m] += r["total"]

    # OP
    for o in daily_op.find():
        m = o["date"][:7]
        op_temp.setdefault(m, 0)
        op_temp[m] += o["count"]

    # IP
    for i in daily_ip.find():
        m = i["date"][:7]
        ip_temp.setdefault(m, 0)
        ip_temp[m] += i["count"]

    if rev_temp:
        monthly_rev.insert_many([{"month":k,"total":v} for k,v in rev_temp.items()])

    if op_temp:
        monthly_op.insert_many([{"month":k,"count":v} for k,v in op_temp.items()])

    if ip_temp:
        monthly_ip.insert_many([{"month":k,"count":v} for k,v in ip_temp.items()])

    return {
        "revenue_months": len(rev_temp),
        "op_months": len(op_temp),
        "ip_months": len(ip_temp)
    }
