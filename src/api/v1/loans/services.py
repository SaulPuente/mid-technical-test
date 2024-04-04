import sys
import uuid
from typing import TYPE_CHECKING

from api.v1.loans.schemas import CreateLoan, Loan

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

sys.path.append("....")
import db.models as _models  # noqa: E402


async def create_loan(loan: CreateLoan, db: "Session") -> Loan:
    loan = _models.Loan(**loan.model_dump())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return Loan.model_validate(loan)


async def get_all_loans(db: "Session") -> list[Loan]:
    loans = db.query(_models.Loan).all()
    return list(map(Loan.model_validate, loans))


async def get_loan(loan_id: uuid.UUID, db: "Session"):
    return db.query(_models.Loan).filter(_models.Loan.id_ == loan_id).first()


async def delete_loan(loan: _models.Loan, db: "Session"):
    db.delete(loan)
    db.commit()


async def update_loan(loan_data: CreateLoan, loan: _models.Loan, db: "Session") -> Loan:
    loan.amount = loan_data.amount
    loan.customer_id = loan_data.customer_id

    db.commit()
    db.refresh(loan)

    return Loan.model_validate(loan)
