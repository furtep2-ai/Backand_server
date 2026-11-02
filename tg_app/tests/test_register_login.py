import pytest

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

@pytest.mark.asyncio
async def test_get_user_success_and_not_found(client):
    """Қолданушы деректерін алу (GET) және жоқ болса 404 қайтару"""
    await client.post(
        "/api/user/555",
        json={
            "user_name": "get_test",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    response = await client.get("/api/user/555")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["user_name"] == "get_test"

    response_404 = await client.get("/api/user/999999")
    assert response_404.status_code == 404


@pytest.mark.asyncio
async def test_change_timezone(client):
    """Часовой поясты өзгерту (PUT)"""
    await client.post(
        "/api/user/888",
        json={
            "user_name": "tz_test",
            "is_admin": False,
            "new_time_zone": "Asia/Almaty"
        }
    )
    
    response = await client.put(
        "/api/user/888/timezone",
        json={"new_time_zone": "Europe/Paris"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["time_zone"] == "Europe/Paris"

    response_404 = await client.put(
        "/api/user/999999/timezone",
        json={"new_time_zone": "Europe/Paris"}
    )
    assert response_404.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(client):
    """Қолданушыны өшіру (DELETE)"""
    await client.post(
        "/api/user/999",
        json={
            "user_name": "del_test",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    response = await client.delete("/api/user/999")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["user_id"] == 999

    response_404 = await client.delete("/api/user/999")
    assert response_404.status_code == 404