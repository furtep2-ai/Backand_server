import pytest

@pytest.mark.anyio
async def test_create_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "folder_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    response = await client.post(
        "/api/folders",
        json={
            "name": "My Folder",
            "user_id": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Папка успешно создана!"
    assert isinstance(data["folder_id"], int)

@pytest.mark.anyio
async def test_add_photo_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Photos",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/test.jpg",
            "folder_id": folder_id
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Фото успешно добавлено!"
    assert isinstance(data["photo_id"], int)

@pytest.mark.anyio
async def test_add_photo_folder_not_found(client):
    response = await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/test.jpg",
            "folder_id": 99999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка табылмады!"
