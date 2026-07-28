from database import revenue_collection, op_collection, ip_collection
from datetime import datetime


def parse_date(d):
    if not d:
        return None
    try:
        if isinstance(d, datetime):
            return d
        return datetime.strptime(str(d)[:10], "%Y-%m-%d")
    except:
        return None


def dashboard_kpis(start=None, end=None):

    start_date = parse_date(start)
    end_date = parse_date(end)

    total_revenue = 0
    total_op = 0
    total_ip = 0

    # Revenue
    for r in revenue_collection.find():

        d = parse_date(r.get("BillDate") or r.get("Date"))

        if start_date and end_date and d:
            if d < start_date or d > end_date:
                continue

        total_revenue += float(r.get("Amount") or 0)

    # OP count
    for r in op_collection.find():

        d = parse_date(r.get("Date") or r.get("VisitDate"))

        if start_date and end_date and d:
            if d < start_date or d > end_date:
                continue

        total_op += 1

    # IP count
    for r in ip_collection.find():

        d = parse_date(r.get("Date") or r.get("AdmissionDate"))

        if start_date and end_date and d:
            if d < start_date or d > end_date:
                continue

        total_ip += 1

    avg_op = total_revenue / total_op if total_op else 0
    avg_ip = total_revenue / total_ip if total_ip else 0

    return {
        "total_revenue": total_revenue,
        "total_op": total_op,
        "total_ip": total_ip,
        "avg_op_revenue": avg_op,
        "avg_ip_revenue": avg_ip
    }