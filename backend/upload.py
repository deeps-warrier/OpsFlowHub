import pandas as pd
import hashlib
from fastapi import UploadFile, HTTPException
from database import revenue_collection, upload_registry
from datetime import datetime

def file_hash(df):
    text = df.to_csv(index=False)
    return hashlib.sha256(text.encode()).hexdigest()

async def upload_revenue_excel(file: UploadFile):

    df = pd.read_excel(file.file, engine="openpyxl")

    required_cols = [
        "BillDate","Bill_No","Request_Total_Amount","Request_type",
        "Service Amount After Discount","Doctor","Department"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column {col}")

    # convert numerics
    df["Request_Total_Amount"] = pd.to_numeric(df["Request_Total_Amount"], errors="coerce").fillna(0)
    df["Service Amount After Discount"] = pd.to_numeric(df["Service Amount After Discount"], errors="coerce").fillna(0)

    # compute FinalRevenue
    def calc(row):
        rt = str(row["Request_type"]).lower()
        if rt in ["consultation","canteen sale","medicine"]:
            return row["Request_Total_Amount"]
        else:
            return row["Service Amount After Discount"]

    df["FinalRevenue"] = df.apply(calc, axis=1)

    # duplicate check
    hash_val = file_hash(df)
    if upload_registry.find_one({"file_hash": hash_val}):
        raise HTTPException(status_code=400, detail="Duplicate file detected")

    # wipe old revenue
    revenue_collection.delete_many({})

    # insert raw
    revenue_collection.insert_many(df.to_dict("records"))

    # ---------- department aggregation ----------
    dept_totals = df.groupby("Department")["FinalRevenue"].sum().reset_index()

    from database import db
    dept_col = db["daily_department"]
    dept_col.delete_many({})
    dept_col.insert_many(dept_totals.to_dict("records"))

    # ---------- daily aggregation ----------
    df["BillDate"] = pd.to_datetime(df["BillDate"])
    daily = df.groupby(df["BillDate"].dt.date)["FinalRevenue"].sum().reset_index()

    daily_col = db["daily_revenue"]
    daily_col.delete_many({})
    daily_col.insert_many([
        {"date":str(r["BillDate"]),"total":float(r["FinalRevenue"])}
        for _,r in daily.iterrows()
    ])

    upload_registry.insert_one({
        "file_hash": hash_val,
        "file_type": "revenue",
        "uploaded_at": datetime.now(),
        "filename": file.filename
    })

    return {"message":"Revenue uploaded successfully","rows":len(df)}

