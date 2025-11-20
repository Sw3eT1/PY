from sqlalchemy import Column, Integer, Float
from database import Base

class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True)
    feature1 = Column(Float, nullable=False)
    feature2 = Column(Float, nullable=False)
    category = Column(Integer, nullable=False)
