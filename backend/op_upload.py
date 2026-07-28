import pandas as pd
import hashlib
from fastapi import UploadFile, HTTPException
from datetime import datetime
from database import op_collection, upload_registry

def file_hash(df):
    text = df.to_csv(index=False)
    return hashlib.sha256(text.encode()).hexdigest()

async def upload_op_excel(file: UploadFile):

    df = pd.read_excel(file.file, engine="openpyxl")

    required = [
        "Sl No","Visit Date","Department","Doctor Name","OP Number",
        "Registration No","Patient Name","Age","Mobile No",
        "Visit Type","Registration Type","Bill No","Bill Amt","Status"
    ]

    for c in required:
        if c not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column {c}")

    hash_val = file_hash(df)

    if upload_registry.find_one({"file_hash": hash_val}):
        raise HTTPException(status_code=400, detail="Duplicate OP file")

    records = df.to_dict("records")
    op_collection.insert_many(records)

    upload_registry.insert_one({
        "file_hash": hash_val,
        "file_type": "op",
        "filename": file.filename,
        "uploaded_at": datetime.now()
    })

    return {"message": "OP uploaded", "rows": len(records)}
