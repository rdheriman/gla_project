from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.reservation import Reservation
from app.models.salle import Salle
from app.schemas.reservation import ReservationCreate, ReservationOut


router = APIRouter(
    prefix="/reservations",
    tags=["Réservations"],
)


SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]


@router.post(
    "",
    response_model=ReservationOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
    data: ReservationCreate,
    session: SessionDep,
) -> Reservation:
    salle = await session.get(
        Salle,
        data.salle_id,
    )

    if salle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salle introuvable.",
        )

    conflict_query = select(Reservation).where(
        Reservation.salle_id == data.salle_id,
        Reservation.debut < data.fin,
        Reservation.fin > data.debut,
    )

    result = await session.execute(conflict_query)

    conflict = result.scalar_one_or_none()

    if conflict is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La salle est déjà réservée sur ce créneau.",
        )

    reservation = Reservation(
        salle_id=data.salle_id,
        reservataire=data.reservataire,
        debut=data.debut,
        fin=data.fin,
        motif=data.motif,
    )

    session.add(reservation)

    await session.commit()
    await session.refresh(reservation)

    return reservation


@router.get(
    "",
    response_model=list[ReservationOut],
)
async def get_reservations(
    session: SessionDep,
) -> list[Reservation]:
    result = await session.execute(select(Reservation).order_by(Reservation.debut))

    return list(result.scalars().all())


@router.get(
    "/{reservation_id}",
    response_model=ReservationOut,
)
async def get_reservation(
    reservation_id: int,
    session: SessionDep,
) -> Reservation:
    reservation = await session.get(
        Reservation,
        reservation_id,
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Réservation introuvable.",
        )

    return reservation


@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reservation(
    reservation_id: int,
    session: SessionDep,
) -> Response:
    reservation = await session.get(
        Reservation,
        reservation_id,
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Réservation introuvable.",
        )

    await session.delete(reservation)
    await session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
