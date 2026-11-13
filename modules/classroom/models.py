from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

class_students = Table(
    "class_students",
    Base.metadata,
    Column("class_id", ForeignKey("classes.id"), primary_key=True),
    Column("student_id", ForeignKey("students.id"), primary_key=True),
)


class Class(Base):
    """Represents a classroom and its associated students."""

    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    students: Mapped[list["Student"]] = relationship(
        secondary=class_students,
        back_populates="classes",
    )
