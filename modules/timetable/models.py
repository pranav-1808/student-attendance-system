from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Timetable(Base):
    __tablename__ = "timetable"

    id: Mapped[int] = mapped_column(primary_key=True)

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id")
    )

    subject: Mapped[str] = mapped_column(
        String(100)
    )

    day: Mapped[str] = mapped_column(
        String(20)
    )

    period: Mapped[int] = mapped_column()
    
    teacher: Mapped["Teacher"] = relationship(
        back_populates="timetables"
    )

    attendances: Mapped[list["Attendance"]] = relationship(
    back_populates="timetable",
    cascade="all, delete-orphan"
)