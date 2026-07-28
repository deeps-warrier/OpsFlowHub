from collections import defaultdict
from database import op_collection


def op_by_doctor():
    """
    OP count grouped by Doctor Name
    """

    result = defaultdict(int)

    for r in op_collection.find():
        doctor = str(r.get("Doctor Name") or "Unknown").strip()

        if not doctor or doctor.lower() in ["nan", "none"]:
            continue

        result[doctor] += 1

    # Top 15
    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:15]

    return dict(sorted_result)
