from database import revenue_collection, op_collection
from collections import defaultdict


def doctor_conversion():

    op_counts = defaultdict(int)
    lab_counts = defaultdict(int)
    radio_counts = defaultdict(int)
    pharm_counts = defaultdict(int)
    revenue = defaultdict(float)

    # OP visits
    for r in op_collection.find():
        doctor = str(r.get("Doctor") or "").strip()
        if doctor:
            op_counts[doctor] += 1


    # Revenue data
    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "").strip()
        req = str(r.get("Request_type") or "").lower()

        try:
            amt = float(
                r.get("Service Amount After Discount")
                or r.get("Request_Total_Amount")
                or 0
            )
        except:
            amt = 0

        revenue[doctor] += amt

        # LAB
        if req in ["lab investigations","routine investigations"]:
            lab_counts[doctor] += 1

        # RADIOLOGY
        if any(x in req for x in ["ct","mri","ultrasound","x ray"]):
            radio_counts[doctor] += 1

        # PHARMACY
        if "medicine" in req:
            pharm_counts[doctor] += 1


    results = []

    for doctor, op in op_counts.items():

        if op == 0:
            continue

        lab = lab_counts.get(doctor,0)
        rad = radio_counts.get(doctor,0)
        pharm = pharm_counts.get(doctor,0)

        rev = revenue.get(doctor,0)

        results.append({

            "doctor":doctor,
            "op":op,
            "lab_percent":round(lab/op*100,2),
            "radiology_percent":round(rad/op*100,2),
            "pharmacy_percent":round(pharm/op*100,2),
            "revenue_per_patient":round(rev/op,2)

        })


    results.sort(key=lambda x:x["op"],reverse=True)

    return results[:15]