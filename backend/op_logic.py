from database import op_collection

def classify_visit(v):
    t = str(v).lower()

    if "non registered" in t:
        return None
    if "health" in t:
        return "Health Package"
    if "follow" in t:
        return "Followup"
    if "revisit" in t or "renew" in t:
        return "Renewal"
    if "new" in t:
        return "New"

    return "Other"

def op_counts():
    result = {
        "New": 0,
        "Renewal": 0,
        "Followup": 0,
        "Health Package": 0,
        "Other": 0,
        "TOTAL": 0
    }

    for r in op_collection.find():
        bucket = classify_visit(r.get("Visit Type", ""))
        if not bucket:
            continue

        result[bucket] += 1
        result["TOTAL"] += 1

    return result
