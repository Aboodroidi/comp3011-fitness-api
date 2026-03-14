from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    workouts: Mapped[list["WorkoutLog"]] = relationship(
        "WorkoutLog",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[str] = mapped_column(String(10), index=True)  # YYYY-MM-DD
    workout_type: Mapped[str] = mapped_column(String(50), index=True)
    duration_min: Mapped[int] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="workouts")

    exercises: Mapped[list["WorkoutExercise"]] = relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout_logs.id", ondelete="CASCADE"),
        index=True,
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"),
        index=True,
    )
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    weight_kg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    workout: Mapped["WorkoutLog"] = relationship(
        "WorkoutLog",
        back_populates="exercises",
    )
    exercise = relationship("Exercise")

    @property
    def exercise_name(self) -> Optional[str]:
        return getattr(self.exercise, "name", None)

    @property
    def body_part(self) -> Optional[str]:
        return getattr(self.exercise, "body_part", None)

    @property
    def equipment(self) -> Optional[str]:
        return getattr(self.exercise, "equipment", None)