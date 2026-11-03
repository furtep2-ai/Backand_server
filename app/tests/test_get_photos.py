import pytest
from app.database_tools.jwt_token import create_access_token


@pytest.mark.anyio  # немесе @pytest.mark.asyncio
async def test_get_photo_not_found(client):
    """Жоқ фотоны сұрағанда 404 қатесі шығуын тексеру"""
    await client.post(
        "/api/user/1",
        json={
            "user_name": "test_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    response = await client.get(
        "/api/photos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"


@pytest.mark.anyio
async def test_delete_photo_not_found(client):
    """Жоқ фотоны өшірмек болғанда 404 қатесі шығуын тексеру"""
    await client.post(
        "/api/user/1",
        json={
            "user_name": "test_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )
    token = await create_access_token(data={"sub": "1"})

    response = await client.delete(
        "/api/photos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"

from unittest.mock import patch

@pytest.mark.anyio
@patch("cloudinary.uploader.upload")
async def test_photo_success_flow(mock_cloudinary_upload, client):
    """Фотоны қосу, алу және өшіру толық циклін тексеру"""
    mock_cloudinary_upload.return_value = {
        "secure_url": "https://res.cloudinary.com/demo/image/upload/test.jpg"
    }

    await client.post(
        "/api/user/2",
        json={
            "user_name": "folder_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    token = await create_access_token(data={"sub": "2"})

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Test Folder for Photos"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert folder_response.status_code == 200
    folder_data = folder_response.json()
    folder_id = folder_data["folder_id"]  

    # Фото қосу (JSON орнына data пен files арқылы)
    post_response = await client.post(
        "/api/photos",
        data={
            "folder_id": folder_id
        },
        files={
            "file": ("test.jpg", b"fake-image-bytes", "image/jpeg")
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert post_response.status_code == 200
    post_data = post_response.json()
    assert post_data["message"] == "Фото успешно добавлено в Cloudinary!"
    photo_id = post_data["photo_id"]

    get_response = await client.get(
        f"/api/photos/{photo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["status"] == "success"

    delete_response = await client.delete(
        f"/api/photos/{photo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "success"

    check_response = await client.get(
        f"/api/photos/{photo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert check_response.status_code == 404