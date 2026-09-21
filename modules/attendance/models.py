from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "timetable_id",
            "date",
            name="unique_student_timetable_date"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    timetable_id: Mapped[int] = mapped_column(
        ForeignKey("timetable.id")
    )

    date: Mapped[date] = mapped_column(
        Date
    )

    status: Mapped[bool] = mapped_column(
        Boolean
    )

    student: Mapped["Student"] = relationship(
        back_populates="attendances"
    )

    timetable: Mapped["Timetable"] = relationship(
        back_populates="attendances"
    )