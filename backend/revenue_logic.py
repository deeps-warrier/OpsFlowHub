from database import revenue_collection
from collections import defaultdict
from datetime import datetime

PRIMARY_TYPES = [
    "consultation",
    "medicine",
    "canteen sale",
    "medicinereturn"
]

MEDICINE_ALIASES = ["medicine sale"]

LAB_ALIASES = [
    "routine investigation",
    "routine investigations",
    "lab investigations",
    "lab investigation"
]

def clean(text):
    return str(text).strip().lower()

def normalize_revenue_row(r):
    raw = clean(r.get("Request_type", ""))

    if raw in LAB_ALIASES:
        req = "Lab Investigation"
    elif raw in MEDICINE_ALIASES:
        req = "Medicine"
    else:
        req = raw.title()

    if raw in PRIMARY_TYPES or raw in MEDICINE_ALIASES:
        amt = float(r.get("Request_Total_Amount") or 0)
    else:
        amt = float(r.get("Service Amount After Discount") or 0)

    return req, raw, amt


# =========================
# EXISTING SUMMARY (UNCHANGED)
# =========================
def revenue_summary():
    summary = {}
    medicine_sale = 0
    medicine_return = 0

    for r in revenue_collection.find():
        req, raw, amt = normalize_revenue_row(r)

        if raw == "medicine":
            medicine_sale += amt
            continue

        if raw == "medicinereturn":
            medicine_return += amt
            continue

        summary.setdefault(req, 0)
        summary[req] += amt

    summary["Medicine"] = medicine_sale + medicine_return
    return {k: round(v, 2) for k, v in summary.items()}


# =========================
# HEALTH PACKAGE
# =========================
def health_package_revenue():
    total = 0
    for r in revenue_collection.find():
        doctor = str(r.get("Doctor") or "").strip().lower()
        if doctor == "health package":
            _, _, amt = normalize_revenue_row(r)
            total += amt
    return round(total, 2)


# =========================
# LAB REVENUE
# =========================
LAB_ALLOWED_CATEGORIES = [
    "blood test","culture","histopathology ( biopsy)",
    "microbiology","serology","stool","semen",
    "blood bank","hematology","skin test (dermatology)",
    "i u i","staining","body fluid","throat swab"
]

def lab_revenue():
    total = 0
    breakdown = defaultdict(float)

    for r in revenue_collection.find():
        request_type = str(r.get("Request_type") or "").lower()
        category = str(r.get("Category") or "").lower()
        _, _, amt = normalize_revenue_row(r)

        if request_type == "lab investigations":
            total += amt
            breakdown["Lab Investigations"] += amt
            continue

        if request_type == "routine investigations":
            if category in LAB_ALLOWED_CATEGORIES or "urine" in category:
                total += amt
                breakdown[category.title()] += amt

    return {
        "total": round(total, 2),
        "breakdown": {k: round(v, 2) for k, v in breakdown.items()}
    }

# =========================
# OP REVENUE MIX
# =========================

def op_revenue_mix():

    consultation = 0
    pharmacy = 0
    lab = 0
    radiology = 0

    for r in revenue_collection.find():

        bill_no = str(r.get("Bill_No") or "").upper()

        # Skip IP bills
        if bill_no.startswith("IP") or bill_no.endswith("IP") or "/IP" in bill_no:
            continue

        req, raw, amt = normalize_revenue_row(r)

        # Skip canteen revenue
        if "canteen" in raw:
            continue

        # Consultation
        if raw == "consultation":
            consultation += amt

        # Pharmacy
        elif "medicine" in raw:
            pharmacy += amt

        # Lab
        elif "lab" in raw or "investigation" in raw:
            lab += amt

        # Radiology
        elif any(x in raw for x in ["ct", "mri", "x ray", "ultrasound", "bmd"]):
            radiology += amt


    total = consultation + pharmacy + lab + radiology

    return {
        "Consultation": round(consultation, 2),
        "Pharmacy": round(pharmacy, 2),
        "Lab": round(lab, 2),
        "Radiology": round(radiology, 2),
        "Total": round(total, 2)
    }
# =========================
# RADIOLOGY
# =========================
RADIOLOGY_TYPES = [
    "ct division",
    "mri",
    "mammography",
    "ultrasound",
    "x ray",
    "bmd"
]

EXCLUDE_CATEGORIES = ["echo", "ecg"]   # <-- NEW

def radiology_revenue():

    total = 0
    breakdown = defaultdict(float)

    for r in revenue_collection.find():

        category_raw = str(r.get("Category") or "").strip().lower()

        # 🚫 EXCLUDE ECHO & ECG (from Category column)
        if any(ex in category_raw for ex in EXCLUDE_CATEGORIES):
            continue

        _, _, amt = normalize_revenue_row(r)

        for rt in RADIOLOGY_TYPES:
            if rt in category_raw:

                # Proper display names
                if rt == "ultrasound":
                    name = "USG"
                elif rt == "ct division":
                    name = "CT"
                elif rt == "x ray":
                    name = "X RAY"
                else:
                    name = rt.upper()

                breakdown[name] += amt
                total += amt
                break   # important: avoid double matching

    return {
        "total": round(total, 2),
        "breakdown": {
            k: round(v, 2)
            for k, v in breakdown.items()
        }
    }


# =========================
# GOVT INSURANCE
# =========================
def govt_insurance_revenue():
    breakdown = {"CGHS":0,"ECHS":0,"ESI":0}

    for r in revenue_collection.find():
        mode = str(r.get("BillPaymentMode") or "").lower()
        _, _, amt = normalize_revenue_row(r)

        if "cghs" in mode:
            breakdown["CGHS"] += amt
        elif "echs" in mode:
            breakdown["ECHS"] += amt
        elif "esic thrissur" in mode:
            breakdown["ESI"] += amt

    total = sum(breakdown.values())

    return {
        "total": round(total,2),
        "breakdown": {k: round(v,2) for k,v in breakdown.items()}
    }


# =========================
# PRIVATE INSURANCE
# =========================
def private_insurance_revenue():
    breakdown = {}

    for r in revenue_collection.find():
        mode = str(r.get("BillPaymentMode") or "").strip()
        mode_lower = mode.lower()

        _, _, amt = normalize_revenue_row(r)

        if "insurance" in mode_lower:
            breakdown.setdefault(mode, 0)
            breakdown[mode] += amt

    total = sum(breakdown.values())

    return {
        "total": round(total, 2),
        "breakdown": {k: round(v, 2) for k, v in breakdown.items()}
    }




# =========================
# INTERNATIONAL
# =========================
def international_revenue():
    total = 0
    for r in revenue_collection.find():
        mode = str(r.get("BillPaymentMode") or "").lower()
        _, _, amt = normalize_revenue_row(r)
        if "epcg" in mode:
            total += amt
    return round(total,2)


# =========================
# TOP 10 DEPARTMENTS
# =========================
def department_top10_revenue():
    result = defaultdict(float)

    for r in revenue_collection.find():
        dept = str(r.get("Department") or "Unknown").strip()
        _, raw, amt = normalize_revenue_row(r)

        if "canteen" in raw:
            continue

        result[dept] += amt

    sorted_depts = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]
    return {k: round(v,2) for k,v in sorted_depts}


# =========================
# MONTHLY GROWTH (INCLUDE CANTEEN)
# =========================
def monthly_growth_metrics():
    now = datetime.now()

    current_month = now.month
    current_year = now.year

    prev_month = 12 if current_month == 1 else current_month - 1
    prev_year = current_year - 1 if current_month == 1 else current_year

    same_month_last_year = current_year - 1

    current_total = prev_total = last_year_total = 0

    for r in revenue_collection.find():
        bill_date = r.get("BillDate")
        if not bill_date:
            continue

        try:
            date_obj = bill_date if isinstance(bill_date, datetime) else datetime.strptime(str(bill_date), "%Y-%m-%d")
        except:
            continue

        _, _, amt = normalize_revenue_row(r)

        if date_obj.month == current_month and date_obj.year == current_year:
            current_total += amt

        if date_obj.month == prev_month and date_obj.year == prev_year:
            prev_total += amt

        if date_obj.month == current_month and date_obj.year == same_month_last_year:
            last_year_total += amt

    mom = ((current_total - prev_total) / prev_total * 100) if prev_total else 0
    yoy = ((current_total - last_year_total) / last_year_total * 100) if last_year_total else 0

    return {
        "current_month": round(current_total,2),
        "previous_month": round(prev_total,2),
        "same_month_last_year": round(last_year_total,2),
        "mom_growth_percent": round(mom,2),
        "yoy_growth_percent": round(yoy,2)
    }

# =========================
# Canteen Revenue
# =========================

def fb_revenue():
    total = 0

    for r in revenue_collection.find():
        _, raw, amt = normalize_revenue_row(r)

        if "canteen" in raw:
            total += amt

    return round(total, 2)

import calendar
from datetime import datetime
from database import revenue_collection
from revenue_logic import normalize_revenue_row

def revenue_run_rate():

    from datetime import datetime
    import calendar

    latest_date = None

    # find latest bill date in dataset
    for r in revenue_collection.find():

        bill_date = r.get("BillDate") or r.get("Date")

        if not bill_date:
            continue

        try:
            if isinstance(bill_date, datetime):
                d = bill_date
            else:
                d = datetime.strptime(str(bill_date)[:10], "%Y-%m-%d")
        except:
            continue

        if not latest_date or d > latest_date:
            latest_date = d


    if not latest_date:
        return {
            "revenue_so_far":0,
            "daily_average":0,
            "month_end_forecast":0
        }


    current_month = latest_date.month
    current_year = latest_date.year
    today = latest_date.day

    days_in_month = calendar.monthrange(current_year,current_month)[1]


    revenue_so_far = 0

    for r in revenue_collection.find():

        bill_date = r.get("BillDate") or r.get("Date")

        if not bill_date:
            continue

        try:
            if isinstance(bill_date, datetime):
                date_obj = bill_date
            else:
                date_obj = datetime.strptime(str(bill_date)[:10], "%Y-%m-%d")
        except:
            continue

        if date_obj.month != current_month or date_obj.year != current_year:
            continue

        _, raw, amt = normalize_revenue_row(r)

        if "canteen" in raw:
            continue

        revenue_so_far += amt


    daily_avg = revenue_so_far / today if today else 0
    forecast = daily_avg * days_in_month


    return {
        "revenue_so_far": round(revenue_so_far,2),
        "daily_average": round(daily_avg,2),
        "month_end_forecast": round(forecast,2)
    }

   