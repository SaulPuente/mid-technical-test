import datetime as dt
import uuid

from pydantic import BaseModel


class _BaseLoan(BaseModel):
    amount: float
    customer_id: uuid.UUID


class Loan(_BaseLoan):
    loan_id: uuid.UUID
    created: dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CreateLoan(_BaseLoan):
    pass
