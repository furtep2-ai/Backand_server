import pytest

@pytest.mark.anyio
async def test_get_photo_success(client):
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
            "name": "Photo Folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/test.jpg",
            "folder_id": folder_id
        }
    )

    photo_id = photo_response.json()["photo_id"]

    response = await client.get(f"/api/photos/{photo_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["photo_id"] == photo_id
    assert data["folder_id"] == folder_id

@pytest.mark.anyio
async def test_get_photo_not_found(client):
    response = await client.get("/api/photos/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"

@pytest.mark.anyio
async def test_delete_photo_success(client):
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
            "name": "Delete Folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/test.jpg",
            "folder_id": folder_id
        }
    )

    photo_id = photo_response.json()["photo_id"]

    response = await client.delete(
        f"/api/photos/{photo_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["photo_id"] == photo_id

@pytest.mark.anyio
async def test_delete_photo_then_get_404(client):
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
            "name": "Delete Folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    photo_response = await client.post(
        "/api/photos",
        json={
            "file_url": "https://cloudinary.com/test.jpg",
            "folder_id": folder_id
        }
    )

    photo_id = photo_response.json()["photo_id"]

    await client.delete(
        f"/api/photos/{photo_id}"
    )

    response = await client.get(
        f"/api/photos/{photo_id}"
    )

    assert response.status_code == 404

@pytest.mark.anyio
async def test_delete_photo_not_found(client):
    response = await client.delete(
        "/api/photos/99999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Фото не найдено!"