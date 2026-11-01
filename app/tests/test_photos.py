import pytest
from app.database_tools.database import Photo

@pytest.mark.asyncio
async def test_get_photo_not_found(client):
    """Жоқ фотоны сұрағанда 404 қатесі шығуын тексеру"""
    response = await client.get("/api/photos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"


@pytest.mark.asyncio
async def test_delete_photo_not_found(client):
    """Жоқ фотоны өшірмек болғанда 404 қатесі шығуын тексеру"""
    response = await client.delete("/api/photos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"

@pytest.mark.anyio
async def test_photo_success_flow(client):
    """Фотоны қосу, алу және өшіру толық циклін тексеру"""

    await client.post(
        "/api/user/2",
        json={
            "user_name": "folder_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    
    # 1. Алдымен қажетті папканы құрып аламыз (POST /api/folders)
    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Test Folder for Photos",
            "user_id": 2
        }
    )
    print(folder_response.status_code)
    print(folder_response.json())
    
    assert folder_response.status_code == 200
    folder_data = folder_response.json()
    folder_id = folder_data["folder_id"]  # База генерациялаған нақты ID-ді аламыз

    # 2. Сол алынған folder_id арқылы фото қосамыз (POST /api/photos)
    post_response = await client.post(
        "/api/photos",
        json={
            "file_url": "AgACAgIAAxkBA_real_photo_id",
            "folder_id": folder_id
        }
    )
    assert post_response.status_code == 200
    post_data = post_response.json()
    assert post_data["message"] == "Фото успешно добавлено!"
    photo_id = post_data["photo_id"]

    # 3. Фотоны ID арқылы алып тексереміз (GET /api/photos/{photo_id})
    get_response = await client.get(f"/api/photos/{photo_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["status"] == "success"
    assert get_data["file_id"] == "AgACAgIAAxkBA_real_photo_id"

    # 4. Фотоны өшіреміз (DELETE /api/photos/{photo_id})
    delete_response = await client.delete(f"/api/photos/{photo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "success"

    # 5. Өшірілгеннен кейін қайта сұрағанда 404 шығуын тексеру
    check_response = await client.get(f"/api/photos/{photo_id}")
   
    assert check_response.status_code == 404