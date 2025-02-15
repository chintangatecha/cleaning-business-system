from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class GSTType(enum.Enum):
    NDIS = "NDIS"
    AGED_CARE = "AGED_CARE"
    RESIDENTIAL = "RESIDENTIAL"
    CORPORATE = "CORPORATE"

class PaymentMode(enum.Enum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    NDIS_PORTAL = "NDIS_PORTAL"
    CARD_PAYMENT = "CARD_PAYMENT"

class EmploymentType(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    CONTRACTOR = "CONTRACTOR"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact = Column(String)
    address = Column(String)
    frequency = Column(String)  # Weekly, Fortnightly, Monthly, 3-Monthly
    preferences = Column(String)
    gst_type = Column(Enum(GSTType))
    payment_mode = Column(Enum(PaymentMode))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    jobs = relationship("Job", back_populates="client")

class Cleaner(Base):
    __tablename__ = "cleaners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost_rate = Column(Float)
    employment_type = Column(Enum(EmploymentType))
    availability = Column(String)  # JSON string of available days/hours
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    jobs = relationship("Job", back_populates="cleaner")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    cleaner_id = Column(Integer, ForeignKey("cleaners.id"))
    date = Column(DateTime)
    time = Column(String)
    status = Column(String)  # Scheduled, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="jobs")
    cleaner = relationship("Cleaner", back_populates="jobs")
    roster = relationship("Roster", back_populates="job", uselist=False)
    invoice = relationship("Invoice", back_populates="job", uselist=False)

class Roster(Base):
    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("Job", back_populates="roster")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    amount = Column(Float)
    gst = Column(Float)
    status = Column(String)  # Pending, Paid, Overdue
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("Job", back_populates="invoice")
    payment = relationship("Payment", back_populates="invoice", uselist=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    mode = Column(Enum(PaymentMode))
    amount = Column(Float)
    payment_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="payment")
