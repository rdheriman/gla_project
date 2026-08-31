async def create_salle(client):
    response = await client.post(
        "/salles",
        json={
            "nom": "A101",
            "capacite": 30,
        },
    )

    return response.json()["id"]


async def test_create_reservation(client):
    salle_id = await create_salle(client)

    response = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Alice",
            "debut": "2026-09-01T10:00:00+03:00",
            "fin": "2026-09-01T12:00:00+03:00",
            "motif": "Réunion",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["salle_id"] == salle_id
    assert data["reservataire"] == "Alice"


async def test_reservation_unknown_salle(client):
    response = await client.post(
        "/reservations",
        json={
            "salle_id": 999999,
            "reservataire": "Alice",
            "debut": "2026-09-01T10:00:00+03:00",
            "fin": "2026-09-01T12:00:00+03:00",
        },
    )

    assert response.status_code == 404


async def test_reservation_invalid_dates(client):
    salle_id = await create_salle(client)

    response = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Alice",
            "debut": "2026-09-01T12:00:00+03:00",
            "fin": "2026-09-01T10:00:00+03:00",
        },
    )

    assert response.status_code == 422


async def test_reservation_conflict(client):
    salle_id = await create_salle(client)

    first = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Alice",
            "debut": "2026-09-01T10:00:00+03:00",
            "fin": "2026-09-01T12:00:00+03:00",
        },
    )

    assert first.status_code == 201

    second = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Bob",
            "debut": "2026-09-01T11:00:00+03:00",
            "fin": "2026-09-01T13:00:00+03:00",
        },
    )

    assert second.status_code == 409


async def test_adjacent_reservations_are_allowed(
    client,
):
    salle_id = await create_salle(client)

    first = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Alice",
            "debut": "2026-09-01T10:00:00+03:00",
            "fin": "2026-09-01T12:00:00+03:00",
        },
    )

    assert first.status_code == 201

    second = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Bob",
            "debut": "2026-09-01T12:00:00+03:00",
            "fin": "2026-09-01T14:00:00+03:00",
        },
    )

    assert second.status_code == 201


import pytest


@pytest.mark.parametrize(
    "debut,fin,status_code",
    [
        (
            "2026-09-01T08:00:00+03:00",
            "2026-09-01T09:00:00+03:00",
            201,
        ),
        (
            "2026-09-01T09:00:00+03:00",
            "2026-09-01T10:00:00+03:00",
            201,
        ),
        (
            "2026-09-01T09:00:00+03:00",
            "2026-09-01T11:00:00+03:00",
            409,
        ),
        (
            "2026-09-01T10:30:00+03:00",
            "2026-09-01T11:30:00+03:00",
            409,
        ),
        (
            "2026-09-01T11:00:00+03:00",
            "2026-09-01T13:00:00+03:00",
            409,
        ),
        (
            "2026-09-01T09:00:00+03:00",
            "2026-09-01T13:00:00+03:00",
            409,
        ),
        (
            "2026-09-01T12:00:00+03:00",
            "2026-09-01T14:00:00+03:00",
            201,
        ),
    ],
)
async def test_reservation_overlap_cases(
    client,
    debut,
    fin,
    status_code,
):
    salle_id = await create_salle(client)

    await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Alice",
            "debut": "2026-09-01T10:00:00+03:00",
            "fin": "2026-09-01T12:00:00+03:00",
        },
    )

    response = await client.post(
        "/reservations",
        json={
            "salle_id": salle_id,
            "reservataire": "Bob",
            "debut": debut,
            "fin": fin,
        },
    )

    assert response.status_code == status_code
