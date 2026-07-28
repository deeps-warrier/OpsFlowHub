from database import revenue_collection, op_collection, ip_collection
from revenue_logic import normalize_revenue_row


def is_ip_bill(bill_no):

    bill_no = str(bill_no or "").upper()

    if bill_no.startswith("IP"):
        return True

    if bill_no.endswith("IP"):
        return True

    if "/IP" in bill_no:
        return True

    return False


def executive_metrics():

    op_revenue = 0
    ip_revenue = 0

    # =========================
    # SPLIT OP vs IP REVENUE
    # =========================
    for r in revenue_collection.find():

        bill_no = r.get("Bill_No")

        req, raw, amt = normalize_revenue_row(r)

        # exclude canteen
        if "canteen" in raw:
            continue

        if is_ip_bill(bill_no):
            ip_revenue += amt
        else:
            op_revenue += amt


    # =========================
    # OP COUNT
    # =========================
    total_op = op_collection.count_documents({})

    # =========================
    # IP COUNT
    # =========================
    total_ip = ip_collection.count_documents({})


    # =========================
    # KPI CALCULATIONS
    # =========================
    avg_op = op_revenue / total_op if total_op else 0
    avg_ip = ip_revenue / total_ip if total_ip else 0


    return {
        "revenue_per_op": round(avg_op,2),
        "revenue_per_ip": round(avg_ip,2),

        "op_revenue": round(op_revenue,2),
        "ip_revenue": round(ip_revenue,2),

        "total_op": total_op,
        "total_ip": total_ip
    }