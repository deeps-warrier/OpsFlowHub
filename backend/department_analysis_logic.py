from datetime import datetime
from collections import defaultdict
from database import op_collection, ip_collection, revenue_collection
from revenue_logic import normalize_revenue_row
from op_logic import classify_visit
from ip_logic import same_day


# =========================
# NORMALIZER
# =========================
def norm(x):
    return (
        str(x or "")
        .strip()
        .lower()
        .replace(".", "")
        .replace(",", "")
        .replace("  ", " ")
    )


# =========================
# DATE FILTER
# =========================
def in_range(date_val, start, end):
    try:
        d = date_val if isinstance(date_val, datetime) else datetime.fromisoformat(str(date_val))
        return start <= d.date() <= end
    except:
        return False


# =========================
# MAIN FUNCTION
# =========================
def department_analysis(start_date, end_date, departments=None, doctors=None):

    start = datetime.fromisoformat(start_date).date()
    end = datetime.fromisoformat(end_date).date()

    # normalize filters once
    departments = [norm(d) for d in departments] if departments else None
    doctors = [norm(d) for d in doctors] if doctors else None


    dept_summary = defaultdict(lambda: {
        "label": "",
        "OP": 0,
        "IP": 0,
        "Medicine": 0,
        "Lab": 0,
        "Radiology": defaultdict(float)
    })

    doctor_summary = defaultdict(lambda: {
        "label": "",
        "OP": 0,
        "IP": 0,
        "Medicine": 0,
        "Lab": 0,
        "Radiology": defaultdict(float)
    })


    # ================= OP =================
    for r in op_collection.find():

        if not in_range(r.get("Visit Date"), start, end):
            continue

        dept_raw = r.get("Department")
        doc_raw = r.get("Doctor Name")

        dept = norm(dept_raw)
        doc = norm(doc_raw)

        if departments and dept not in departments:
            continue
        if doctors and doc not in doctors:
            continue

        if not classify_visit(r.get("Visit Type","")):
            continue

        dept_summary[dept]["label"] = dept_raw
        doctor_summary[doc]["label"] = doc_raw

        dept_summary[dept]["OP"] += 1
        doctor_summary[doc]["OP"] += 1


    # ================= IP =================
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

        if not (start <= admit_dt.date() <= end):
            continue

        dept_raw = r.get("Department")
        doc_raw = r.get("Doctor")

        dept = norm(dept_raw)
        doc = norm(doc_raw)

        if departments and dept not in departments:
            continue
        if doctors and doc not in doctors:
            continue

        if not same_day(admit_dt, dis_dt):

            dept_summary[dept]["label"] = dept_raw
            doctor_summary[doc]["label"] = doc_raw

            dept_summary[dept]["IP"] += 1
            doctor_summary[doc]["IP"] += 1


    # ================= REVENUE =================
    for r in revenue_collection.find():

        if not in_range(r.get("BillDate"), start, end):
            continue

        dept_raw = r.get("Department")
        doc_raw = r.get("Doctor")

        dept = norm(dept_raw)
        doc = norm(doc_raw)

        if not dept:
            continue

        if departments and dept not in departments:
            continue
        if doctors and doc not in doctors:
            continue

        dept_summary[dept]["label"] = dept_raw
        doctor_summary[doc]["label"] = doc_raw

        req, raw, amt = normalize_revenue_row(r)
        category = str(r.get("Category") or "").lower()


        # MEDICINE
        if "medicine" in raw:
            dept_summary[dept]["Medicine"] += amt
            doctor_summary[doc]["Medicine"] += amt
            continue


        # LAB
        if raw in (
            "lab investigations",
            "lab investigation",
            "routine investigations",
            "routine investigation"
        ):
            dept_summary[dept]["Lab"] += amt
            doctor_summary[doc]["Lab"] += amt
            continue


        # RADIOLOGY
        if any(x in category for x in (
            "ct division","mri","mammography",
            "ultrasound","x ray","bmd"
        )):

            if "echo" in category or "ecg" in category:
                continue

            if "ct division" in category:
                name = "CT"
            elif "ultrasound" in category:
                name = "USG"
            elif "x ray" in category:
                name = "X RAY"
            else:
                name = category.upper()

            dept_summary[dept]["Radiology"][name] += amt
            doctor_summary[doc]["Radiology"][name] += amt


    # ================= CLEAN OUTPUT =================
    def clean(data):
        out = {}
        for k,v in data.items():
            out[v["label"] or k] = {
                "OP": v["OP"],
                "IP": v["IP"],
                "Medicine": round(v["Medicine"],2),
                "Lab": round(v["Lab"],2),
                "Radiology": {rk: round(rv,2) for rk,rv in v["Radiology"].items()}
            }
        return out


    return {
        "department_summary": clean(dept_summary),
        "doctor_summary": clean(doctor_summary)
    }