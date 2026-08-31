from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ReservationCreate(BaseModel):
    salle_id: int = Field(gt=0)

    reservataire: str = Field(
        min_length=1,
        max_length=100,
    )

    debut: datetime

    fin: datetime

    motif: str | None = Field(
        default=None,
        max_length=255,
    )

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.fin <= self.debut:
            raise ValueError("La date de fin doit être postérieure à la date de début.")

        return self


class ReservationOut(BaseModel):
    id: int
    salle_id: int
    reservataire: str
    debut: datetime
    fin: datetime
    motif: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
