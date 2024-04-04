import sys
import uuid
from typing import TYPE_CHECKING

from api.v1.pays.schemas import CreatePay, Pay

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

sys.path.append("....")
import db.models as _models  # noqa: E402


async def create_pay(pay: CreatePay, db: "Session") -> Pay:
    pay = _models.Pay(**pay.model_dump())
    db.add(pay)
    db.commit()
    db.refresh(pay)
    return Pay.model_validate(pay)


async def get_all_pays(db: "Session") -> list[Pay]:
    pays = db.query(_models.Pay).all()
    return list(map(Pay.model_validate, pays))


async def get_pay(pay_id: uuid.UUID, db: "Session"):
    return db.query(_models.Pay).filter(_models.Pay.id_ == pay_id).first()


async def delete_loan(pay: _models.Pay, db: "Session"):
    db.delete(pay)
    db.commit()


async def update_loan(pay_data: CreatePay, pay: _models.Pay, db: "Session") -> Pay:
    pay.amount = pay_data.amount
    pay.loan_id = pay_data.loan_id

    db.commit()
    db.refresh(pay)

    return Pay.model_validate(pay)
