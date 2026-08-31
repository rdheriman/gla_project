from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Salle(Base):
    __tablename__ = "salles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nom: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    capacite: Mapped[int] = mapped_column(
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
