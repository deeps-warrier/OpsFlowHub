from database import revenue_collection, op_collection, ip_collection
from revenue_logic import normalize_revenue_row
from ip_logic import ip_counts


def is_ip_bill(bill_no):

    bill_no = str(bill_no or "").upper()

    if bill_no.startswith("IP"):
        return True

    if bill_no.endswith("IP"):
        return True

    if "/IP" in bill_no:
        return True

    return False


def executive_kpis():

    op = op_collection.count_documents({})

    ip_data = ip_counts()
    ip = ip_data["IP"]

    print("OP COUNT:", op)
    print("IP COUNT:", ip)

    op_revenue = 0
    ip_revenue = 0

    # ======================
    # SPLIT OP / IP REVENUE
    # ======================
    for r in revenue_collection.find():

        bill_no = r.get("Bill_No")

        req, raw, amt = normalize_revenue_row(r)

        # exclude canteen
        if "canteen" in raw:
            continue

        if is_ip_bill(bill_no):
            ip_revenue += amt
        else:
            op_revenue += amt


    # ======================
    # KPI CALCULATIONS
    # ======================

    avg_op = op_revenue / op if op else 0
    avg_ip = ip_revenue / ip if ip else 0

    op_ip_conversion = (ip / op * 100) if op else 0

    from datetime import datetime

    days = datetime.now().day

    daily_ip = ip / days if days else 0

    total_bed_days = 0

    for r in ip_collection.find():

        admit = r.get("Admission Date")
        discharge = r.get("Discharge Date")

        ward = str(r.get("Ward") or "").lower()

        if not admit or not discharge:
            continue

        try:
            admit_dt = admit if isinstance(admit, datetime) else datetime.fromisoformat(str(admit))
            dis_dt = discharge if isinstance(discharge, datetime) else datetime.fromisoformat(str(discharge))
        except:
            continue

        stay = (dis_dt - admit_dt).days

        # EXCLUDE SAME DAY CASES
        if stay <= 0:
            continue

        # EXCLUDE NON-IP WARDS
        if "dialysis" in ward:
            continue

        if "observation" in ward:
            continue

        if "labour" in ward:
            continue

        total_bed_days += stay

    import calendar
    from datetime import datetime

    today = datetime.now()
    days = calendar.monthrange(today.year, today.month)[1]

    daily_ip = ip / days if days else 0

    bed_proxy = (daily_ip / 130) * 100

    total_bed_days = 0

    for r in ip_collection.find():

        admit = r.get("Admission Date")
        discharge = r.get("Discharge Date")

        if not admit or not discharge:
            continue

        try:
            admit_dt = admit if isinstance(admit, datetime) else datetime.fromisoformat(str(admit))
            dis_dt = discharge if isinstance(discharge, datetime) else datetime.fromisoformat(str(discharge))
        except:
            continue

        stay = (dis_dt - admit_dt).days

        if stay <= 0:
            continue

        total_bed_days += stay

    los = total_bed_days / ip if ip else 0

    rev_per_bed_day = ip_revenue / total_bed_days if total_bed_days else 0

    return {

        "revenue_per_op": round(avg_op, 2),
        "revenue_per_ip": round(avg_ip, 2),

        "op_ip_conversion": round(op_ip_conversion, 2),
        "bed_proxy": round(bed_proxy, 2),

        "op_revenue": round(op_revenue, 2),
        "ip_revenue": round(ip_revenue, 2),

        "avg_los": round(los,2),
        "revenue_per_bed_day": round(rev_per_bed_day,2)

        
    }

    