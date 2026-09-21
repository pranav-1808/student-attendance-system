from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column , relationship
from db.base import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    attendances: Mapped[list["Attendance"]] = relationship(
        back_populates = "student"
    )