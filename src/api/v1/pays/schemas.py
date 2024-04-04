import datetime as dt
import uuid

from pydantic import BaseModel


class _BasePay(BaseModel):
    amount: float
    loan_id: uuid.UUID
    paid: int
    pay_date: dt.datetime


class Pay(_BasePay):
    id_: uuid.UUID
    created: dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CreatePay(_BasePay):
    pass
