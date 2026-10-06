from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True)

    students: Mapped[list["Student"]] = relationship(
        secondary="class_students", back_populates="classes"
    )


class ClassStudents(Base):
    __tablename__ = "class_students"

    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
