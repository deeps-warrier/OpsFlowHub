from collections import defaultdict
from database import revenue_collection, op_collection, ip_collection
from revenue_logic import normalize_revenue_row
from datetime import datetime


def clean(x):
    return str(x or "").strip().lower()


def department_totals(start=None, end=None, department=None, doctor=None):

    data = defaultdict(lambda: {
        "department": "",
        "revenue": 0,
        "pharmacy": 0,
        "lab": 0,
        "radiology": 0,
        "op": 0,
        "ip": 0
    })

    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None


    # REVENUE
    for r in revenue_collection.find():

        dept = clean(r.get("Department"))
        doc = clean(r.get("Doctor"))

        if department and dept != clean(department):
            continue

        if doctor and doc != clean(doctor):
            continue

        bill_date = r.get("BillDate")

        if start_dt and end_dt and bill_date:
            try:
                d = bill_date if isinstance(bill_date, datetime) else datetime.strptime(str(bill_date), "%Y-%m-%d")
                if d < start_dt or d > end_dt:
                    continue
            except:
                pass

        if not dept:
            continue

        data[dept]["department"] = dept.title()

        req, raw, amt = normalize_revenue_row(r)

        data[dept]["revenue"] += amt

        raw = raw.lower()

        if "medicine" in raw:
            data[dept]["pharmacy"] += amt

        if "lab" in raw or "investigation" in raw:
            data[dept]["lab"] += amt

        if any(x in raw for x in ["ct", "mri", "x ray", "ultrasound"]):
            data[dept]["radiology"] += amt


    # OP
    for r in op_collection.find():

        dept = clean(r.get("Department"))
        doc = clean(r.get("Doctor"))

        if department and dept != clean(department):
            continue

        if doctor and doc != clean(doctor):
            continue

        if not dept:
            continue

        data[dept]["department"] = dept.title()
        data[dept]["op"] += 1


    # IP
    for r in ip_collection.find():

        dept = clean(r.get("Department"))
        doc = clean(r.get("Doctor"))

        if not dept or dept in ["nan","none"]:
            continue

        if department and dept != clean(department):
            continue

        if doctor and doc != clean(doctor):
            continue

        if not dept:
            continue

        data[dept]["department"] = dept.title()
        data[dept]["ip"] += 1


    result = list(data.values())

    result = sorted(result, key=lambda x: x["revenue"], reverse=True)

    return result