import pytest

@pytest.mark.anyio
async def test_change_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
            "is_admin": False,
            "time_zone": "Asia/Almaty"
        }
    )

    folder_response = await client.post(
        "/api/folders",
        json={
            "name": "Old Folder",
            "user_id": 1
        }
    )

    folder_id = folder_response.json()["folder_id"]

    response = await client.put(
        f"/api/folders/{folder_id}",
        json={
            "folder_id": folder_id,
            "user_id": 1,
            "new_folder_name": "New Folder"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["new_folder_name"] == "New Folder"

@pytest.mark.anyio
async def test_change_folder_not_found(client):
    response = await client.put(
        "/api/folders/999",
        json={
            "folder_id": 999,
            "user_id": 1,
            "new_folder_name": "New Folder"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_change_folder_forbidden(client):
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
            "user_name": "another_user",
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

    response = await client.put(
        f"/api/folders/{folder_id}",
        json={
            "folder_id": folder_id,
            "user_id": 2,
            "new_folder_name": "Hack Folder"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "У вас нет прав на изменение этой папки!"

@pytest.mark.anyio
async def test_delete_folder_success(client):
    await client.post(
        "/api/user/1",
        json={
            "user_name": "owner",
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

    response = await client.request(
        "DELETE",
        f"/api/folders/{folder_id}",
        json={
            "folder_id": folder_id,
            "user_id": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

@pytest.mark.anyio
async def test_delete_folder_not_found(client):
    response = await client.request(
        "DELETE",
        "/api/folders/999",
        json={
            "folder_id": 999,
            "user_id": 1
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Папка не найдена!"

@pytest.mark.anyio
async def test_delete_folder_forbidden(client):
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
            "user_name": "another_user",
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

    response = await client.request(
        "DELETE",
        f"/api/folders/{folder_id}",
        json={
            "folder_id": folder_id,
            "user_id": 2
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "У вас нет прав на изменение этой папки!"