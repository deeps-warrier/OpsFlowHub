from collections import defaultdict
from database import revenue_collection, op_collection, ip_collection
from revenue_logic import normalize_revenue_row
from datetime import datetime


def clean(x):
    return str(x or "").strip().lower()


def parse_date(d):
    if not d:
        return None
    try:
        if isinstance(d, datetime):
            return d
        return datetime.strptime(str(d)[:10], "%Y-%m-%d")
    except:
        return None


def department_doctor_matrix(start=None, end=None, department=None, doctor=None):

    doctors = defaultdict(lambda: {
        "department": "",
        "doctor": "",
        "revenue": 0,
        "pharmacy": 0,
        "lab": 0,
        "radiology": 0,
        "op": 0,
        "ip": 0
    })

    dept_revenue = defaultdict(float)
    dept_op = defaultdict(int)

    start_date = parse_date(start)
    end_date = parse_date(end)

    # =========================
    # REVENUE DATA
    # =========================
    for r in revenue_collection.find():

        bill_date = parse_date(r.get("BillDate") or r.get("Date"))

        if start_date and end_date and bill_date:
            if bill_date < start_date or bill_date > end_date:
                continue

        dept = clean(r.get("Department"))
        doc = clean(r.get("Doctor"))

        if not dept or dept in ["nan","none"]:
            continue

        if not doc or doc in ["nan","none"]:
            continue

        if department and dept != department.lower():
            continue

        if doctor and doctor.lower() not in doc:
            continue

        key = f"{dept}|{doc}"

        doctors[key]["department"] = dept.title()
        doctors[key]["doctor"] = doc.title()

        req, raw, amt = normalize_revenue_row(r)

        doctors[key]["revenue"] += amt
        dept_revenue[dept] += amt

        raw = raw.lower()

        if "medicine" in raw:
            doctors[key]["pharmacy"] += amt

        if "lab" in raw or "investigation" in raw:
            doctors[key]["lab"] += amt

        if any(x in raw for x in ["ct","mri","x ray","ultrasound"]):
            doctors[key]["radiology"] += amt


    # =========================
    # IP DATA
    # =========================
    for r in ip_collection.find():

        ip_date = parse_date(r.get("Date") or r.get("AdmissionDate"))

        if start_date and end_date and ip_date:
            if ip_date < start_date or ip_date > end_date:
                continue

        dept = clean(r.get("Department"))
        doc = clean(r.get("Doctor"))

        if not dept or dept in ["nan","none"]:
            continue

        if not doc or doc in ["nan","none"]:
            continue

        if department and dept != department.lower():
            continue

        if doctor and doctor.lower() not in doc:
            continue

        key = f"{dept}|{doc}"

        doctors[key]["department"] = dept.title()
        doctors[key]["doctor"] = doc.title()

        doctors[key]["ip"] += 1


    # =========================
    # OP DATA
    # =========================
    for r in op_collection.find():

        op_date = parse_date(r.get("Date") or r.get("VisitDate"))

        if start_date and end_date and op_date:
            if op_date < start_date or op_date > end_date:
                continue

        dept = clean(r.get("Department") or r.get("Dept"))

        if not dept or dept in ["nan","none"]:
            continue

        if department and dept != department.lower():
            continue

        dept_op[dept] += 1


    # =========================
    # DISTRIBUTE OP TO DOCTORS
    # =========================
    for key, d in doctors.items():

        dept = clean(d["department"])

        if dept_revenue[dept] == 0:
            continue

        share = d["revenue"] / dept_revenue[dept]
        d["op"] = round(dept_op[dept] * share)


    result = list(doctors.values())

    result = sorted(result, key=lambda x: x["revenue"], reverse=True)

    return result