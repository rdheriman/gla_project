from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    salle_id: Mapped[int] = mapped_column(
        ForeignKey("salles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    reservataire: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    debut: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    fin: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    motif: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
