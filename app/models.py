from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String(10), index=True)  # YYYY-MM-DD
    workout_type: Mapped[str] = mapped_column(String(50), index=True)
    duration_min: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String(300), nullable=True)