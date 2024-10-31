# Mission model
from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import relationship
from app.models import Base

class Mission(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True, autoincrement=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Integer)
    attacking_aircraft = Column(Integer)
    bombing_aircraft = Column(Integer)
    aircraft_returned = Column(Integer)
    aircraft_failed = Column(Integer)
    aircraft_damaged = Column(Integer)
    aircraft_lost = Column(Integer)
    targets = relationship('Target', back_populates='mission')
