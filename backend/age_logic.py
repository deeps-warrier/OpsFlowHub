from database import op_collection

def age_bucket(age):

    try:
        age = int(age)
    except:
        return None

    if age <= 10: return "0-10"
    if age <= 20: return "11-20"
    if age <= 30: return "21-30"
    if age <= 40: return "31-40"
    if age <= 50: return "41-50"
    if age <= 60: return "51-60"
    if age <= 70: return "61-70"
    return "70+"


def age_trends():

    result = {
        "0-10":0,"11-20":0,"21-30":0,"31-40":0,
        "41-50":0,"51-60":0,"61-70":0,"70+":0
    }

    for r in op_collection.find():

        b = age_bucket(r.get("Age"))

        if b:
            result[b] += 1

    return result
