from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, unique=True, comment="Адрес здания")
    latitude = Column(Float, nullable=False, comment="Широта")
    longitude = Column(Float, nullable=False, comment="Долгота")
    
    companies = relationship("Company", back_populates="building")