from collections import defaultdict
from database import revenue_collection
from revenue_logic import normalize_revenue_row


def doctor_revenue(start_date=None, end_date=None):

    result = defaultdict(float)

    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "").strip()
        dept = str(r.get("Department") or "").strip() or "--"

        if not doctor or doctor.lower() in ["nan", "none", "unknown"]:
            continue

        req, raw, amt = normalize_revenue_row(r)

        if "canteen" in raw:
            continue

        key = f"{doctor} | {dept}"
        result[key] += amt

    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:15]

    return {k: round(v, 2) for k, v in sorted_result}


def doctor_revenue_trends():
    return doctor_revenue()

def doctor_revenue():

    result = defaultdict(float)

    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "Unknown").strip()

        _, raw, amt = normalize_revenue_row(r)

        if "canteen" in raw:
            continue

        result[doctor] += amt


    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])


def doctor_revenue_trends():
    return {}

from collections import defaultdict
from database import revenue_collection
from revenue_logic import normalize_revenue_row


def doctor_productivity():

    doctor_revenue = defaultdict(float)
    doctor_op = defaultdict(int)

    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "").strip()

        if not doctor:
            continue

        req, raw, amt = normalize_revenue_row(r)

        # ignore canteen
        if "canteen" in raw:
            continue

        doctor_revenue[doctor] += amt

        if raw == "consultation":
            doctor_op[doctor] += 1


    result = []

    for doctor in doctor_revenue:

        op_count = doctor_op.get(doctor, 0)

        # 🔴 Ignore doctors with very small OP count
        if op_count < 30:
            continue

        productivity = doctor_revenue[doctor] / op_count

        result.append({
            "doctor": doctor,
            "revenue_per_op": round(productivity, 2),
            "op_count": op_count
        })

    result = sorted(result, key=lambda x: x["revenue_per_op"], reverse=True)

    return result[:10]