import datetime as dt
import uuid

from pydantic import BaseModel


class _BaseCustomer(BaseModel):
    full_name: str
    email: str


class Customer(_BaseCustomer):
    customer_id: uuid.UUID
    created: dt.datetime

    class Config:
        orm_mode = True
        from_attributes = True


class CreateCustomer(_BaseCustomer):
    pass
