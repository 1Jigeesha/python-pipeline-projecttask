from fastapi import FastAPI, HTTPException, Query
from database import init_db, SessionLocal
from services.ingestion import fetch_all_customers, upsert_customers
from models.customer import Customer

app = FastAPI(on_startup=[init_db])


@app.post("/api/ingest")
def ingest():
    customers = fetch_all_customers()
    processed = upsert_customers(customers)
    return {"status": "success", "records_processed": processed}


@app.get("/api/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    db = SessionLocal()
    try:
        query = db.query(Customer).offset((page - 1) * limit).limit(limit)
        items = query.all()
        total = db.query(Customer).count()

        data = []
        for item in items:
            row = item.__dict__.copy()
            row.pop("_sa_instance_state", None)
            data.append(row)

        return {"data": data, "total": total, "page": page, "limit": limit}

    finally:
        db.close()


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()
    try:
        c = db.query(Customer).filter_by(customer_id=customer_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Customer not found")

        data = c.__dict__.copy()
        data.pop("_sa_instance_state", None)
        return {"data": data}

    finally:
        db.close()
