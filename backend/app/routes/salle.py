from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.salle import Salle
from app.schemas.salle import SalleCreate, SalleOut, SalleUpdate

router = APIRouter(
    prefix="/salles",
    tags=["Salles"],
)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]


@router.post(
    "",
    response_model=SalleOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_salle(
    data: SalleCreate,
    session: SessionDep,
) -> Salle:
    salle = Salle(
        nom=data.nom,
        capacite=data.capacite,
        description=data.description,
    )

    session.add(salle)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une salle avec ce nom existe déjà.",
        )

    await session.refresh(salle)

    return salle


@router.get(
    "",
    response_model=list[SalleOut],
)
async def get_salles(
    session: SessionDep,
) -> list[Salle]:
    result = await session.execute(select(Salle).order_by(Salle.nom))

    return list(result.scalars().all())


@router.get(
    "/{salle_id}",
    response_model=SalleOut,
)
async def get_salle(
    salle_id: int,
    session: SessionDep,
) -> Salle:
    salle = await session.get(Salle, salle_id)

    if salle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salle introuvable.",
        )

    return salle


@router.patch(
    "/{salle_id}",
    response_model=SalleOut,
)
async def update_salle(
    salle_id: int,
    data: SalleUpdate,
    session: SessionDep,
) -> Salle:
    salle = await session.get(Salle, salle_id)

    if salle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salle introuvable.",
        )

    values = data.model_dump(
        exclude_unset=True,
    )

    for key, value in values.items():
        setattr(salle, key, value)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une salle avec ce nom existe déjà.",
        )

    await session.refresh(salle)

    return salle


@router.delete(
    "/{salle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_salle(
    salle_id: int,
    session: SessionDep,
) -> Response:
    salle = await session.get(Salle, salle_id)

    if salle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salle introuvable.",
        )

    await session.delete(salle)
    await session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
