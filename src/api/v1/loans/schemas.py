from pydantic import BaseModel
import datetime as dt
import uuid

class _BaseLoan(BaseModel):
    amount: float
    customer_id: uuid.UUID


class Loan(_BaseLoan):
    id: uuid.UUID
    created: dt.datetime

    class Config:
        orm_mode = True
        from_attributes=True


class CreateLoan(_BaseLoan):
    pass