from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, Float

class Base(DeclarativeBase):
    pass

class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feature1: Mapped[float] = mapped_column(Float, nullable=False)
    feature2: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)