from fastapi import APIRouter, status
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from core.utils.responses import EnvelopeResponse
import uuid

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import api.v1.costumers.schemas as _schemas

import sys
sys.path.append("....")
import db.models as _models
import db.session as _session

router = APIRouter(prefix="/customers", tags=["Customers"])

# @router.post("/Create", tags=["Customers"])
# async def create_customer(customer: _schemas.Customer):
#     print('iejfkj mdkmswi 0o')
#     print(customer.model_dump())
#     db = next(_session.get_session())
#     print(db.add)
#     return [{"username": "Rick"}, {"username": "Morty"}]

# @router.get("", tags=["Customers"])
# async def read_users():
#     print('hhhhhhha---------------')
#     return [{"username": "Rick"}, {"username": "Morty"}]

db = next(_session.get_session())

@router.post("/Create", response_model=_schemas.Customer)
async def create(
    customer: _schemas.CreateCustomer):
    return await create_customer(customer=customer)


async def create_customer(
    customer: _schemas.CreateCustomer) -> _schemas.Customer:
    customer = _models.Customer(**customer.model_dump())
    db = next(_session.get_session())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    # db.close()
    return _schemas.Customer.model_validate(customer)


@router.get("/List", status_code=status.HTTP_200_OK, summary="Customers List", response_model=EnvelopeResponse)
async def get_customers() -> EnvelopeResponse:
    result = await get_all_customers()
    return EnvelopeResponse(errors=None, body=result)

async def get_all_customers() -> List[_schemas.Customer]:
    # db = next(_session.get_session())
    customers = db.query(_models.Customer).all()
    # db.close()
    return list(map(_schemas.Customer.model_validate, customers))



@router.get("/Retrieve/{customer_id}", response_model=_schemas.Customer)
async def get_customer(customer_id: uuid.UUID):
    customer = await _get_customer(customer_id=customer_id)
    if customer is None:
        raise _fastapi.HTTPException(status_code=404, detail="Customer does not exist")

    return customer

async def _get_customer(customer_id: uuid.UUID):
    # db = next(_session.get_session())
    customer = db.query(_models.Customer).filter(_models.Customer.id == customer_id).first()
    # db.close()
    return customer


@router.delete("/{customer_id}")
async def delete_contact(customer_id: uuid.UUID):
    customer = await _get_customer(customer_id=customer_id)
    if customer is None:
        raise _fastapi.HTTPException(status_code=404, detail="Customer does not exist")

    await delete_customer(customer)

    return "successfully deleted the Customer"

async def delete_customer(customer: _models.Customer):
    # db = next(_session.get_session())
    db.delete(customer)
    db.commit()


@router.put("/{customer_id}", response_model=_schemas.Customer)
async def update_customer(
    customer_id: uuid.UUID,
    customer_data: _schemas.CreateCustomer,
):
    customer = await _get_customer(customer_id=customer_id)
    if customer is None:
        raise _fastapi.HTTPException(status_code=404, detail="Customer does not exist")
    
    return await _update_customer(
        customer_data=customer_data, customer=customer
    )

async def _update_customer(
    customer_data: _schemas.CreateCustomer, customer: _models.Customer
) -> _schemas.Customer:
    customer.full_name = customer_data.full_name
    if customer_data.email:
        customer.email = customer_data.email 

    # db = next(_session.get_session())

    db.commit()
    db.refresh(customer)

    return _schemas.Customer.model_validate(customer)