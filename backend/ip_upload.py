import pandas as pd
import hashlib
from fastapi import UploadFile, HTTPException
from datetime import datetime
from database import ip_collection, upload_registry

def file_hash(df):
    text = df.to_csv(index=False)
    return hashlib.sha256(text.encode()).hexdigest()

async def upload_ip_excel(file: UploadFile):

    df = pd.read_excel(file.file, engine="openpyxl")

    required = [
        "Sl.No","Patient Name","MRN","Doctor","Department","Floor","Ward",
        "PtientRoomType","Room ID","Admission Date","AdmissionTime",
        "Discharge Date","Discharge Time","IPDays","IP Ref No"
    ]

    for c in required:
        if c not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column {c}")

    hash_val = file_hash(df)

    if upload_registry.find_one({"file_hash": hash_val}):
        raise HTTPException(status_code=400, detail="Duplicate IP file")

    # Convert time columns to string (MongoDB safe)
    for col in ["AdmissionTime", "Discharge Time"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    records = df.to_dict("records")
    ip_collection.insert_many(records)

    upload_registry.insert_one({
        "file_hash": hash_val,
        "file_type": "ip",
        "filename": file.filename,
        "uploaded_at": datetime.now()
    })

    return {"message": "IP uploaded", "rows": len(records)}
