from database import ip_collection
from datetime import datetime

def clean(v):
    return str(v).lower().strip()

def same_day(a, d):
    try:
        return a.date() == d.date()
    except:
        return False

def ip_counts():

    result = {
        "IP": 0,
        "Observation": 0,
        "Labour Room Observation": 0,
        "Dialysis": 0,
        "ED_to_IP": 0
    }

    for r in ip_collection.find():

        admit = r.get("Admission Date")
        discharge = r.get("Discharge Date")

        ward = clean(r.get("Ward", ""))
        prev_doc = clean(r.get("PreviousDoctorName", ""))

        if not admit or not discharge:
            continue

        try:
            admit_dt = admit if isinstance(admit, datetime) else datetime.fromisoformat(str(admit))
            dis_dt = discharge if isinstance(discharge, datetime) else datetime.fromisoformat(str(discharge))
        except:
            continue

        is_same_day = same_day(admit_dt, dis_dt)

        # ---------------- Dialysis ----------------
        if "dialysis" in ward:
            result["Dialysis"] += 1
            continue

        # ---------------- Observation ----------------
        if is_same_day and "observation" in ward:
            result["Observation"] += 1
            continue

        # ---------------- Labour Room Observation ----------------
        if is_same_day and "labour" in ward:
            result["Labour Room Observation"] += 1
            continue

        # ---------------- TRUE IP ----------------
        if not is_same_day:

            result["IP"] += 1

            # ED → IP
            if "emergency physician" in prev_doc:
                result["ED_to_IP"] += 1

    return result
