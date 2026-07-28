from database import op_collection

def op_by_department():

    result = {}

    for r in op_collection.find():

        dept = str(r.get("Department","Unknown")).strip()

        result.setdefault(dept, 0)
        result[dept] += 1

    return result
