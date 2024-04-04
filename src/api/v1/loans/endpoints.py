import datetime as dt
import sys
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, status

import api.v1.costumers.services as _services_customers
import api.v1.loans.services as _services
import api.v1.pays.services as _services_pays
from api.v1.loans.schemas import CreateLoan, Loan
from api.v1.pays.schemas import CreatePay
from core.utils.responses import EnvelopeResponse

sys.path.append("....")
from db.session import get_session  # noqa: E402

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/Create", status_code=status.HTTP_200_OK, summary="Create Loan.", response_model=EnvelopeResponse)
async def create(loan: CreateLoan):
    if loan.amount <= 0:
        return EnvelopeResponse(errors="Enter a valid amount.", body=None)
    db = next(get_session())
    customer = await _services_customers.get_customer(customer_id=loan.customer_id, db=db)
    if customer is None:
        db.close()
        return EnvelopeResponse(errors="Customer does not exist.", body=None)
    loan.amount = loan.amount + loan.amount * 0.15 + loan.amount * 0.15 * 0.16
    result = await _services.create_loan(loan=loan, db=db)
    today = datetime.now(dt.UTC)
    pay_amount = loan.amount / 60
    for i in range(1, 61):
        pay = CreatePay(amount=pay_amount, loan_id=result.id_, paid=0, pay_date=today + timedelta(days=i))
        await _services_pays.create_pay(pay=pay, db=db)

    db.close()
    return EnvelopeResponse(errors=None, body=result)


@router.get("/List", status_code=status.HTTP_200_OK, summary="Loans list.", response_model=EnvelopeResponse)
async def get_loans() -> EnvelopeResponse:
    db = next(get_session())
    result = await _services.get_all_loans(db)
    db.close()
    return EnvelopeResponse(errors=None, body={"loans": result})


@router.get(
    "/Retrieve/{loan_id}", status_code=status.HTTP_200_OK, summary="Retrieve loan.", response_model=EnvelopeResponse
)
async def get_loan(loan_id: uuid.UUID):
    db = next(get_session())
    loan = await _services.get_loan(loan_id=loan_id, db=db)
    if loan is None:
        db.close()
        return EnvelopeResponse(errors="Loan does not exist.", body=None)
    db.close()
    return EnvelopeResponse(errors=None, body=Loan.model_validate(loan))


@router.delete("/{loan_id}", status_code=status.HTTP_200_OK, summary="Delete loan.", response_model=EnvelopeResponse)
async def delete_contact(loan_id: uuid.UUID):
    db = next(get_session())
    loan = await _services.get_loan(loan_id=loan_id, db=db)
    if loan is None:
        db.close()
        return EnvelopeResponse(errors="Loan does not exist.", body=None)
    await _services.delete_loan(loan=loan, db=db)
    db.close()
    return EnvelopeResponse(errors=None, body="successfully deleted the loan")


@router.put("/{loan_id}", status_code=status.HTTP_200_OK, summary="Update loan.", response_model=EnvelopeResponse)
async def update_loan(loan_id: uuid.UUID, loan_data: CreateLoan):
    if loan_data.amount <= 0:
        return EnvelopeResponse(errors="Enter a valid amount.", body=None)
    db = next(get_session())
    customer = await _services_customers.get_customer(customer_id=loan_data.customer_id, db=db)
    if customer is None:
        db.close()
        return EnvelopeResponse(errors="Customer does not exist.", body=None)
    loan = await _services.get_loan(loan_id=loan_id, db=db)
    if loan is None:
        db.close()
        return EnvelopeResponse(errors="Loan does not exist.", body=None)
    result = await _services.update_loan(loan_data=loan_data, loan=loan, db=db)
    db.close()
    return EnvelopeResponse(errors=None, body=Loan.model_validate(result))
