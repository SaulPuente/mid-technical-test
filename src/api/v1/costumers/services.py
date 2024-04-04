import sys
import uuid
from typing import TYPE_CHECKING

from api.v1.costumers.schemas import CreateCustomer, Customer

sys.path.append("....")
import db.models as _models  # noqa: E402

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def create_customer(customer: CreateCustomer, db: "Session") -> Customer:
    customer = _models.Customer(**customer.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return Customer.model_validate(customer)


async def get_all_customers(db: "Session", limit, offset) -> list[Customer]:
    customers = db.query(_models.Customer).limit(limit).offset(offset)
    return list(map(Customer.model_validate, customers))


async def get_customer(customer_id: uuid.UUID, db: "Session"):
    return db.query(_models.Customer).filter(_models.Customer.id_ == customer_id).first()


async def delete_customer(customer: _models.Customer, db: "Session"):
    db.delete(customer)
    db.commit()


async def update_customer(customer_data: CreateCustomer, customer: _models.Customer, db: "Session") -> Customer:
    customer.full_name = customer_data.full_name
    customer.email = customer_data.email

    db.commit()
    db.refresh(customer)

    return Customer.model_validate(customer)
