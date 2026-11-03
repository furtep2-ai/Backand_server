import pytest
from app.database_tools.jwt_token import create_access_token

@pytest.mark.asyncio
async def test_add_user_success(client):
    response = await client.post(
        "api/user/12345",
        json={
            "user_name": "new_user11",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["user_id"] == 12345


@pytest.mark.asyncio
async def test_add_user_already_exists(client):
    await client.post(
        "api/user/77777",
        json={
            "user_name": "admin_user",
            "is_admin": True,
            "time_zone": "Europe/Moscow"
        }
    )

    response = await client.post(
        "api/user/77777",
        json={
            "user_name": "admin_user",
            "is_admin": True,
            "time_zone": "Europe/Moscow"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "exists"
    assert data["message"] == "Пользователь уже зарегистрирован!"

@pytest.mark.asyncio
async def test_add_user_validation_error(client):
    """Міндетті өрістер түсіп қалғанда немесе қате тип жіберілгенде validation error (422) шығуын тексеру"""
    response = await client.post(
        "/api/user/99999",
        json={
            "is_admin": False
        }
    )

    assert response.status_code == 422

@pytest.mark.anyio
async def test_get_my_profile(client):

    await client.post(
        "/api/user/555",
        json={
            "user_name": "get_test",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(
        data={"sub": "555"}
    )

    response = await client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["user_id"] == 555
    assert data["user_name"] == "get_test"
    assert data["time_zone"] == "Asia/Almaty"


@pytest.mark.anyio
async def test_change_timezone(client):

    await client.post(
        "/api/user/888",
        json={
            "user_name": "tz_test",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(
        data={"sub": "888"}
    )

    response = await client.put(
        "/api/users/timezone",
        json={
            "new_time_zone": "Europe/Paris"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["user_id"] == 888
    assert data["time_zone"] == "Europe/Paris"


@pytest.mark.anyio
async def test_delete_user(client):

    await client.post(
        "/api/user/999",
        json={
            "user_name": "del_test",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(
        data={"sub": "999"}
    )

    response = await client.delete(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"