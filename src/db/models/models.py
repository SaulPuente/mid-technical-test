from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from core.utils.datetime import LocalTime
from db.models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    full_name = Column(String(length=200), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)

    def __str__(self) -> str:
        return f"Customer(id='{self.id_}', full_name='{self.full_name}', email='{self.email}')"


class Loan(BaseModel):
    __tablename__ = "loans"

    amount = Column(Numeric(19, 2), nullable=False)
    customer_id = Column(ForeignKey(Customer.id_, deferrable=True, initially="DEFERRED"), nullable=False, index=True)

    customer = relationship(Customer, primaryjoin="Loan.customer_id == Customer.id_")

    def __str__(self) -> str:
        return f"Loan(id='{self.id_}', customer_id='{self.customer_id}')"


class Pay(BaseModel):
    __tablename__ = "pays"

    amount = Column(Numeric(19, 2), nullable=False)
    loan_id = Column(ForeignKey(Loan.id_, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    paid = Column(Integer, nullable=False)
    pay_date = Column(DateTime(timezone=True), default=LocalTime.now)

    loan = relationship(Loan, primaryjoin="Pay.loan_id == Loan.id_")

    def __str__(self) -> str:
        return f"Pay(id='{self.id_}', loan_id='{self.loan_id}')"
