import re
import sys
import uuid

from fastapi import APIRouter, status

import api.v1.costumers.services as _services
from api.v1.costumers.schemas import CreateCustomer, Customer
from core.utils.responses import EnvelopeResponse

sys.path.append("....")
from db.session import get_session  # noqa: E402

router = APIRouter(prefix="/customers", tags=["Customers"])


def check_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return re.fullmatch(regex, email)


@router.post("/Create", status_code=status.HTTP_200_OK, summary="Create customer.", response_model=EnvelopeResponse)
async def create(customer: CreateCustomer) -> EnvelopeResponse:
    if not check_email(customer.email):
        return EnvelopeResponse(errors="Enter a valid email.", body=None)
    db = next(get_session())
    result = await _services.create_customer(customer=customer, db=db)
    db.close()
    return EnvelopeResponse(errors=None, body=result)


@router.get("/List", status_code=status.HTTP_200_OK, summary="Customers list.", response_model=EnvelopeResponse)
async def get_customers() -> EnvelopeResponse:
    db = next(get_session())
    result = await _services.get_all_customers(db)
    db.close()
    return EnvelopeResponse(errors=None, body={"customers": result})


@router.get(
    "/Retrieve/{customer_id}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve customer.",
    response_model=EnvelopeResponse,
)
async def get_customer(customer_id: uuid.UUID):
    db = next(get_session())
    customer = await _services.get_customer(customer_id=customer_id, db=db)
    if customer is None:
        db.close()
        return EnvelopeResponse(errors="Customer does not exist.", body=None)
    db.close()
    return EnvelopeResponse(errors=None, body=Customer.model_validate(customer))


@router.delete(
    "/{customer_id}", status_code=status.HTTP_200_OK, summary="Delete customer.", response_model=EnvelopeResponse
)
async def delete_contact(customer_id: uuid.UUID):
    db = next(get_session())
    customer = await _services.get_customer(customer_id=customer_id, db=db)
    if customer is None:
        db.close()
        return EnvelopeResponse(errors="Customer does not exist.", body=None)
    await _services.delete_customer(customer, db=db)
    db.close()
    return EnvelopeResponse(errors=None, body="successfully deleted the customer")


@router.put(
    "/{customer_id}", status_code=status.HTTP_200_OK, summary="Update customer.", response_model=EnvelopeResponse
)
async def update_customer(customer_id: uuid.UUID, customer_data: CreateCustomer):
    if not check_email(customer_data.email):
        return EnvelopeResponse(errors="Enter a valid email.", body=None)
    db = next(get_session())
    customer = await _services.get_customer(customer_id=customer_id, db=db)
    if customer is None:
        db.close()
        return EnvelopeResponse(errors="Customer does not exist.", body=None)

    result = await _services.update_customer(customer_data=customer_data, customer=customer, db=db)
    db.close()

    return EnvelopeResponse(errors=None, body=Customer.model_validate(result))
