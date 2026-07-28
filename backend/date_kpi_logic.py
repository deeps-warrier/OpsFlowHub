from datetime import date
from database import db
import pandas as pd

daily = db["daily_revenue"]

def sum_between(start, end):

    total = 0

    for r in daily.find():
        d = pd.to_datetime(r["date"]).date()
        if start <= d <= end:
            total += r["total"]

    return total


def revenue_kpis():

    today = date.today()

    mtd = today.replace(day=1)
    cytd = today.replace(month=1, day=1)

    if today.month >= 4:
        fytd = date(today.year,4,1)
    else:
        fytd = date(today.year-1,4,1)

    ly = today.year - 1

    last_mtd_s = date(ly, today.month, 1)
    last_mtd_e = date(ly, today.month, today.day)

    last_cytd_s = date(ly,1,1)
    last_cytd_e = date(ly,today.month,today.day)

    if today.month >= 4:
        last_fytd_s = date(ly,4,1)
        last_fytd_e = date(ly+1,today.month,today.day)
    else:
        last_fytd_s = date(ly-1,4,1)
        last_fytd_e = date(ly,today.month,today.day)

    return {
        "mtd": sum_between(mtd,today),
        "cytd": sum_between(cytd,today),
        "fytd": sum_between(fytd,today),
        "last_mtd": sum_between(last_mtd_s,last_mtd_e),
        "last_cytd": sum_between(last_cytd_s,last_cytd_e),
        "last_fytd": sum_between(last_fytd_s,last_fytd_e)
    }

