from database import revenue_collection
from revenue_logic import normalize_revenue_row

def department_revenue():

    result = {}

    for r in revenue_collection.find():

        dept = str(r.get("Department", "Unknown")).strip()

        req, amt = normalize_revenue_row(r)

        result.setdefault(dept, 0)
        result[dept] += amt

    return result
