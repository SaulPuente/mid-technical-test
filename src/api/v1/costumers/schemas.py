from pydantic import BaseModel
import datetime as dt
import uuid

class _BaseCustomer(BaseModel):
    full_name: str
    email: str


class Customer(_BaseCustomer):
    id: uuid.UUID
    created: dt.datetime

    class Config:
        orm_mode = True
        from_attributes=True


class CreateCustomer(_BaseCustomer):
    pass