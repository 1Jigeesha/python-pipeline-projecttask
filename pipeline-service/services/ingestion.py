import requests
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from models.customer import Customer
from database import SessionLocal

FLASK_URL = "http://mock-server:5000/api/customers"


def fetch_all_customers(page_size: int = 10):
    page = 1
    all_customers = []

    while True:
        resp = requests.get(FLASK_URL, params={"page": page, "limit": page_size}, timeout=15)
        resp.raise_for_status()

        payload = resp.json()
        data = payload.get("data", [])

        if not data:
            break

        all_customers.extend(data)

        if len(data) < page_size:
            break

        page += 1

    return all_customers


def upsert_customers(customers):
    db = SessionLocal()
    total = 0

    try:
        for c in customers:
            key = str(c.get("customer_id"))
            existing = db.query(Customer).filter_by(customer_id=key).first()

            if existing is None:
                existing = Customer(customer_id=key)
                db.add(existing)

            existing.first_name = c.get("first_name")
            existing.last_name = c.get("last_name")
            existing.email = c.get("email")
            existing.phone = c.get("phone")
            existing.address = c.get("address")

            dob = c.get("date_of_birth")
            existing.date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None

            existing.account_balance = Decimal(str(c.get("account_balance", 0)))

            created_at = c.get("created_at")
            existing.created_at = datetime.fromisoformat(created_at) if created_at else None

            total += 1

        db.commit()
        return total

    except SQLAlchemyError:
        db.rollback()
        raise

    finally:
        db.close()
