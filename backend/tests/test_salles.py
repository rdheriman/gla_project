async def test_create_salle(client):
    response = await client.post(
        "/salles",
        json={
            "nom": "A101",
            "capacite": 30,
            "description": "Salle de cours",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["nom"] == "A101"
    assert data["capacite"] == 30


async def test_get_salles(client):
    await client.post(
        "/salles",
        json={
            "nom": "A101",
            "capacite": 30,
        },
    )

    await client.post(
        "/salles",
        json={
            "nom": "B202",
            "capacite": 20,
        },
    )

    response = await client.get("/salles")

    assert response.status_code == 200

    salles = response.json()

    assert len(salles) == 2


async def test_create_salle_with_invalid_capacity(
    client,
):
    response = await client.post(
        "/salles",
        json={
            "nom": "A101",
            "capacite": -5,
        },
    )

    assert response.status_code == 422


async def test_duplicate_salle_name(client):
    salle = {
        "nom": "A101",
        "capacite": 30,
    }

    first_response = await client.post(
        "/salles",
        json=salle,
    )

    second_response = await client.post(
        "/salles",
        json=salle,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


async def test_get_unknown_salle(client):
    response = await client.get("/salles/999999")

    assert response.status_code == 404


async def test_delete_salle(client):
    create_response = await client.post(
        "/salles",
        json={
            "nom": "A101",
            "capacite": 30,
        },
    )

    salle_id = create_response.json()["id"]

    response = await client.delete(f"/salles/{salle_id}")

    assert response.status_code == 204

    get_response = await client.get(f"/salles/{salle_id}")

    assert get_response.status_code == 404
