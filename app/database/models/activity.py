from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.database.models.company import company_activity

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Назание деятельности")
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    
    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")
    companies = relationship(
        "Company", 
        secondary=company_activity,
        back_populates="activities",
        lazy="selectin"
    )