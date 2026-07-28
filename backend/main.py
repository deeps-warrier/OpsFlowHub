from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

# ===== DATABASE =====
from database import (
    db,
    users_collection,
    revenue_collection,
    upload_registry,
    op_collection,
    ip_collection
)

# ===== AUTH =====
from models import hash_password, verify_password

# ===== UPLOADS =====
from upload import upload_revenue_excel
from op_upload import upload_op_excel
from ip_upload import upload_ip_excel

# ===== LOGIC MODULES =====
from revenue_logic import revenue_summary
from dept_logic import department_revenue
from doctor_logic import doctor_revenue, doctor_revenue_trends
from op_logic import op_counts
from op_dept_logic import op_by_department
from op_doctor_logic import op_by_doctor
from age_logic import age_trends
from ip_logic import ip_counts
from date_kpi_logic import revenue_kpis
from daily_aggregate import build_daily_revenue
from daily_op import build_daily_op
from daily_ip import build_daily_ip
from executive_logic import executive_kpis
from executive_ip_logic import executive_ip_cards
from monthly_aggregate import build_monthly
from revenue_logic import fb_revenue


# ✅ ADDITIONAL REVENUE CARDS
from revenue_logic import (
    normalize_revenue_row,   # ← ADD THIS
    health_package_revenue,
    lab_revenue as lab_revenue_logic,
    radiology_revenue,
    govt_insurance_revenue,
    private_insurance_revenue,
    international_revenue,
    department_top10_revenue,
    monthly_growth_metrics,
    LAB_ALLOWED_CATEGORIES
)

# =========================
app = FastAPI(title="OpsFlowHub Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELS
# =========================
class User(BaseModel):
    username: str
    password: str

# =========================
# BASIC
# =========================
@app.get("/")
def root():
    return {"status": "OpsFlowHub backend running"}

# =========================
# AUTH
# =========================
@app.post("/register")
def register(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })
    return {"message": "User created"}

@app.post("/login")
def login(user: User):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

# =========================
# UPLOADS
# =========================
@app.post("/upload/revenue")
async def upload_revenue(file: UploadFile = File(...)):
    return await upload_revenue_excel(file)

@app.post("/upload/op")
async def upload_op(file: UploadFile = File(...)):
    return await upload_op_excel(file)

@app.post("/upload/ip")
async def upload_ip(file: UploadFile = File(...)):
    return await upload_ip_excel(file)

@app.get("/uploads")
def list_uploads():
    return [{
        "id": str(u["_id"]),
        "filename": u["filename"],
        "file_type": u["file_type"],
        "uploaded_at": u["uploaded_at"]
    } for u in upload_registry.find()]

@app.delete("/uploads/{upload_id}")
def revoke_upload(upload_id: str):
    upload = upload_registry.find_one({"_id": ObjectId(upload_id)})
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    if upload["file_type"] == "revenue":
        revenue_collection.delete_many({})

    upload_registry.delete_one({"_id": ObjectId(upload_id)})
    return {"message": "Upload revoked"}

# =========================
# REVENUE
# =========================
@app.get("/revenue/summary")
def revenue_summary_api():
    return revenue_summary()

@app.get("/revenue/kpis")
def revenue_kpis_api():
    return revenue_kpis()

@app.get("/revenue/by-department")
def revenue_dept():
    return department_revenue()

@app.get("/revenue/by-doctor")
def revenue_doctor():
    return doctor_revenue()

@app.get("/revenue/doctor-trends")
def revenue_doctor_trends():
    return doctor_revenue_trends()

@app.post("/revenue/build-daily")
def build_daily_revenue_api():
    return build_daily_revenue()

@app.get("/revenue/daily")
def daily_revenue():
    return list(db["daily_revenue"].find({}, {"_id": 0}).sort("date", 1))

# ✅ NEW CARDS
@app.get("/revenue/health-package")
def health_package():
    return {"total": health_package_revenue()}

@app.get("/revenue/lab")
def lab():
    total = 0
    breakdown = {}

    for r in revenue_collection.find():

        request_type = str(r.get("Request_type") or "").strip().lower()
        category = str(r.get("Category") or "").strip()

        _, _, amt = normalize_revenue_row(r)

        # Full Lab Investigations
        if request_type == "lab investigations":
            breakdown.setdefault("Lab Investigations", 0)
            breakdown["Lab Investigations"] += amt
            total += amt
            continue

        # Routine Investigations filtered
        if request_type == "routine investigations":
            cat_lower = category.lower()

            if cat_lower in LAB_ALLOWED_CATEGORIES or "urine" in cat_lower:

                # Rename special case
                if "urine tests and preservat" in cat_lower:
                    category = "Urine Test"

                breakdown.setdefault(category, 0)
                breakdown[category] += amt
                total += amt

    return {
        "total": round(total, 2),
        "breakdown": {k: round(v, 2) for k, v in breakdown.items()}
    }


@app.get("/revenue/radiology")
def radiology():
    return radiology_revenue()

@app.get("/revenue/govt-insurance")
def govt():
    return govt_insurance_revenue()

@app.get("/revenue/private-insurance")
def private():
    return private_insurance_revenue()

@app.get("/revenue/international")
def international():
    return {"total": international_revenue()}

@app.get("/revenue/top10-departments")
def top_departments():
    return department_top10_revenue()

@app.get("/revenue/monthly-growth")
def monthly_growth():
    return monthly_growth_metrics()

# =========================
# OP
# =========================
@app.get("/op/counts")
def op_counts_api():
    return op_counts()

@app.get("/op/by-department")
def op_dept():
    return op_by_department()

@app.get("/op/by-doctor")
def op_doc():
    return op_by_doctor()

@app.get("/op/age-trends")
def op_age():
    return age_trends()

@app.post("/op/rebuild")
def rebuild_op():
    return build_daily_op()

@app.get("/op/daily")
def daily_op():
    return list(db["daily_op"].find({}, {"_id": 0}).sort("date", 1))

# =========================
# IP
# =========================
@app.get("/ip/counts")
def ip_counts_api():
    return ip_counts()

@app.post("/ip/rebuild")
def rebuild_ip():
    return build_daily_ip()

@app.get("/ip/daily")
def daily_ip():
    return list(db["daily_ip"].find({}, {"_id": 0}).sort("date", 1))

# =========================
# EXECUTIVE
# =========================
@app.get("/executive/metrics")
def executive_metrics():
    return executive_kpis()

@app.get("/executive/ip-cards")
def ip_cards():
    return executive_ip_cards()

# =========================
# MONTHLY
# =========================
@app.post("/monthly/rebuild")
def rebuild_monthly_api():
    return build_monthly()

@app.get("/monthly/revenue")
def monthly_revenue():
    return list(db["monthly_revenue"].find({}, {"_id": 0}).sort("month", 1))

@app.get("/monthly/op")
def monthly_op():
    return list(db["monthly_op"].find({}, {"_id": 0}).sort("month", 1))

@app.get("/monthly/ip")
def monthly_ip():
    return list(db["monthly_ip"].find({}, {"_id": 0}).sort("month", 1))

@app.get("/revenue/fb")
def fnb():
    return {"total": fb_revenue()}

@app.get("/revenue/pharmacy")
def pharmacy_revenue():

    total = 0
    breakdown = {
        "OP": 0,
        "IP": 0
    }

    for r in revenue_collection.find():

        request_type = str(r.get("Request_type") or "").strip().lower()

        # include medicine sale only
        if "medicine" not in request_type:
            continue

        if "return" in request_type:
            continue

        try:
            amount = float(r.get("Request_Total_Amount") or 0)
        except:
            amount = 0

        bill_no = str(r.get("Bill_No") or "")

        if bill_no.endswith("/IP"):
            breakdown["IP"] += amount
        else:
            breakdown["OP"] += amount

        total += amount

    return {
        "total": round(total, 2),
        "breakdown": {
            "OP": round(breakdown["OP"], 2),
            "IP": round(breakdown["IP"], 2)
        }
    }
@app.get("/revenue/physiotherapy")
def physiotherapy_revenue():

    total = 0
    breakdown = {
        "Consultation": 0,
        "Procedure": 0
    }

    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "").strip()

        if doctor.lower() != "physiotherapist":
            continue

        request_type = str(r.get("Request_type") or "").strip().lower()

        if request_type == "consultation":
            try:
                amt = float(r.get("Request_Total_Amount") or 0)
                disc = float(r.get("Discount") or 0)
                amount = amt - disc
            except:
                amount = 0

            breakdown["Consultation"] += amount

        else:
            try:
                amount = float(r.get("Service Amount After Discount") or 0)
            except:
                amount = 0

            breakdown["Procedure"] += amount

        total += amount

    return {
        "total": round(total, 2),
        "breakdown": {
            "Consultation": round(breakdown["Consultation"], 2),
            "Procedure": round(breakdown["Procedure"], 2)
        }
    }
@app.get("/revenue/homecare")
def homecare_revenue():

    total = 0

    for r in revenue_collection.find():

        doctor = str(r.get("Doctor") or "").strip()

        if doctor.lower() != "home care doctors":
            continue

        try:
            amount = float(r.get("Service Amount After Discount") or 0)
        except:
            amount = 0

        total += amount

    return {
        "total": round(total, 2)
    }

from pydantic import BaseModel
from datetime import datetime

class DeptAnalysisRequest(BaseModel):
    from_date: str
    to_date: str
    departments: list[str] = []
    doctors: list[str] = []



from department_analysis_logic import department_analysis
from fastapi import Query

@app.get("/advanced/department-analysis")
def get_department_analysis(
    start: str,
    end: str,
    departments: list[str] = Query(default=None),
    doctors: list[str] = Query(default=None)
):
    return department_analysis(start, end, departments, doctors)

from department_doctor_matrix_logic import department_doctor_matrix

from fastapi import Query

@app.get("/analytics/doctor-department-matrix")
def doctor_department_matrix_api(
    start: str = None,
    end: str = None,
    department: str = None,
    doctor: str = None
):
    return department_doctor_matrix(start, end, department, doctor)

    
from department_totals_logic import department_totals


@app.get("/analytics/department-totals")
def get_department_totals(
    start: str = None,
    end: str = None,
    department: str = None,
    doctor: str = None
):
    return department_totals(start, end, department, doctor)


@app.get("/analytics/filter-options")
def filter_options():

    depts = set()
    docs = set()

    for r in revenue_collection.find({}, {"Department":1, "Doctor":1}):

        dept = r.get("Department")
        doc = r.get("Doctor")

        if isinstance(dept, str) and dept.strip():
            depts.add(dept.strip())

        if isinstance(doc, str) and doc.strip():
            docs.add(doc.strip())

    return {
        "departments": sorted(list(depts)),
        "doctors": sorted(list(docs))
    }

from dashboard_kpis import dashboard_kpis

@app.get("/analytics/dashboard-kpis")
def get_dashboard_kpis(start: str=None, end: str=None):

    return dashboard_kpis(start, end)

from executive_metrics import executive_metrics

@app.get("/executive/metrics")
def get_exec_metrics():
    return executive_metrics()

from revenue_logic import revenue_run_rate

@app.get("/revenue/run-rate")
def run_rate():
    return revenue_run_rate()


from doctor_logic import doctor_productivity

@app.get("/doctor/productivity")
def doctor_productivity_api():
    return doctor_productivity()

from revenue_logic import op_revenue_mix


@app.get("/revenue/op-mix")
def get_op_mix():
    return op_revenue_mix()

from doctor_conversion_logic import doctor_conversion

@app.get("/doctor/conversion")
def doctor_conversion_api():
    return doctor_conversion()