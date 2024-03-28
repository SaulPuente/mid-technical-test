from fastapi import APIRouter, status
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from core.utils.responses import EnvelopeResponse
import uuid

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import api.v1.loans.schemas as _schemas

import sys
sys.path.append("....")
import db.models as _models
import db.session as _session

router = APIRouter(prefix="/loans", tags=["Loans"])

db = next(_session.get_session())

@router.post("/Create", response_model=_schemas.Loan)
async def create(
    loan: _schemas.CreateLoan):
    return await create_loan(loan=loan)


async def create_loan(
    loan: _schemas.CreateLoan) -> _schemas.Loan:
    loan = _models.Loan(**loan.model_dump())
    db = next(_session.get_session())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    # db.close()
    return _schemas.Loan.model_validate(loan)
