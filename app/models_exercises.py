from sqlalchemy import Column, Integer, String, Text, Float
from .db import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    body_part = Column(String(100), nullable=True, index=True)
    equipment = Column(String(100), nullable=True, index=True)
    difficulty = Column(String(50), nullable=True, index=True)
    exercise_type = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    rating_desc = Column(Text, nullable=True)