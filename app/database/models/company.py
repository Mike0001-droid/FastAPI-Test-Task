from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base


company_activity = Table(
    'company_activity',
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Название компании")
    building_id = Column(Integer, ForeignKey("buildings.id"))
    
    building = relationship("Building", back_populates="companies", lazy="selectin")
    activities = relationship("Activity", secondary=company_activity, back_populates="companies", lazy="selectin")
    phones = relationship("CompanyPhone", back_populates="company",  lazy="selectin")


class CompanyPhone(Base):
    __tablename__ = "company_phones"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    phone_number = Column(String, nullable=False, comment="Номер телефона")
    
    company = relationship("Company", back_populates="phones")