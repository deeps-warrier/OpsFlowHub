from database import ip_collection

def executive_ip_cards():
    result = {
        "OP": 0,
        "IP": 0,
        "Observation": 0,
        "Labour Room Observation": 0,
        "ED_to_IP": 0,
        "Dialysis": 0
    }

    for r in ip_collection.find():
        admit = r.get("Admission Date")
        discharge = r.get("Discharge Date")
        ward = str(r.get("Ward") or "").lower()
        prev_doc = str(r.get("PreviousDoctorName") or "").lower()

        if admit:
            result["OP"] += 1

        # Dialysis
        if "dialysis" in ward:
            result["Dialysis"] += 1
            continue

        # Observation same-day
        if admit and discharge and admit == discharge:
            if "labour" in ward:
                result["Labour Room Observation"] += 1
            else:
                result["Observation"] += 1
            continue

        # IP proper
        if admit and discharge and admit != discharge:
            result["IP"] += 1

            if "emergency physician" in prev_doc:
                result["ED_to_IP"] += 1

    return result
