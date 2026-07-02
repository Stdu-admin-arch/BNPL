from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="BNPL Regulatory API")
df = pd.read_csv('data/synthetic_transactions.csv')

@app.get("/audit/{txn_id}")
def get_transaction(txn_id: str):
    record = df[df['transaction_id'] == txn_id]
    return record.to_dict(orient="records")

@app.get("/compliance-summary")
def get_summary():
    return {"total": len(df), "non_compliant": len(df[df['is_compliant'] == 0])}