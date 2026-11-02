import pytest

@pytest.mark.anyio
async def test_get_user_folders_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "test_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    await client.post(
        "/api/folders",
        json={
            "name": "Folder 1",
            "user_id": 1
        }
    )

    await client.post(
        "/api/folders",
        json={
            "name": "Folder 2",
            "user_id": 1
        }
    )

    response = await client.get("/api/user/1/folders")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["user_id"] == 1

@pytest.mark.anyio
async def test_get_user_folders_empty(client):
    await client.post(
        "/api/user/10",
        json={
            "user_name": "empty_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    response = await client.get("/api/user/10/folders")

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.anyio
async def test_get_folder_photos_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_user",
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

    await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/photo1.jpg",
            "folder_id": folder_id
        }
    )

    response = await client.get(
        f"/api/folders/{folder_id}/photos"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["url"] == "https://cloudinary.com/photo1.jpg"

@pytest.mark.anyio
async def test_get_folder_photos_empty(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "photo_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Empty folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.get(
        f"/api/folders/{folder_id}/photos"
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.anyio
async def test_get_folder_not_found(client):
    response = await client.get(
        "/api/folder/99999?user_id=1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_get_folder_forbidden(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    await client.post(
        "/api/user/2",
        json={
            "user_name": "other_user",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Private Folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.get(
        f"/api/folder/{folder_id}?user_id=2"
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "У вас нет прав на просмотр этой папки!"