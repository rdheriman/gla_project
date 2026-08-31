from pydantic import BaseModel, ConfigDict, Field


class SalleCreate(BaseModel):
    nom: str = Field(
        min_length=1,
        max_length=100,
    )

    capacite: int = Field(
        gt=0,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )


class SalleUpdate(BaseModel):
    nom: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    capacite: int | None = Field(
        default=None,
        gt=0,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )


class SalleOut(BaseModel):
    id: int
    nom: str
    capacite: int
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )
